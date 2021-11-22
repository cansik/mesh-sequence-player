import os.path
import time
from functools import partial
from typing import Optional

import numpy as np
import open3d as o3d
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from tqdm import tqdm

from mesh_sequence_player.FPSCounter import FPSCounter
from mesh_sequence_player.FastGeometryLoader import load_meshes_fast, load_meshes_safe, load_pointclouds_safe, \
    load_pointclouds_fast
from mesh_sequence_player.geometries.BaseGeometry import BaseGeometry
from mesh_sequence_player.geometries.Geometry import Geometry
from mesh_sequence_player.geometries.LazyGeometry import LazyGeometry
from mesh_sequence_player.utils import get_files_in_path


class MeshSequencePlayer:
    def __init__(self, fps: int = 24, loop: bool = True):
        self.fps = fps
        self.loop = loop
        self.geometries: [BaseGeometry] = []
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.background_color = [255, 255, 255]

        self.debug = False
        self.load_safe = False
        self.lazy_loading = False
        self.post_process_mesh = False

        self.render = False
        self.output_path = "render.mp4"
        self.render_index = 0

        self.vis = o3d.visualization.Visualizer()

        self._is_playing: bool = False
        self._index: int = 0
        self._last_update_ts = 0
        self._current_geometry = None

        self.bitrate = "1.5M"
        self._frames = []
        self._progress_bar: Optional[tqdm] = None
        self._render_fps = fps

        self._fps_counter = FPSCounter()

    def load_meshes(self, mesh_folder: str, mesh_format: str = "*.obj"):
        files = sorted(get_files_in_path(mesh_folder, extensions=[mesh_format]))

        if self.lazy_loading:
            method = partial(o3d.io.read_triangle_mesh, enable_post_processing=self.post_process_mesh)
            self.geometries = [LazyGeometry(os.path.abspath(file), method) for file in files]
            return

        if self.load_safe:
            meshes = load_meshes_safe(files, post_processing=self.post_process_mesh)
        else:
            meshes = load_meshes_fast(files, post_processing=self.post_process_mesh)

        self.geometries = [Geometry(mesh) for mesh in meshes]

    def load_pointclouds(self, pcl_folder: str, pcl_format: str = "*.ply"):
        files = sorted(get_files_in_path(pcl_folder, extensions=[pcl_format]))

        if self.lazy_loading:
            self.geometries = [LazyGeometry(os.path.abspath(file), o3d.io.read_point_cloud) for file in files]
            return

        if self.load_safe:
            pcds = load_pointclouds_safe(files)
        else:
            pcds = load_pointclouds_fast(files)

        self.geometries = [Geometry(pcd) for pcd in pcds]

    def open(self, window_name: str = 'Mesh Sequence Player',
             width: int = 1080, height: int = 1080,
             visible: bool = True):
        self.vis.create_window(window_name=window_name,
                               width=width,
                               height=height,
                               visible=visible)

        if len(self.geometries) == 0:
            print("No meshes to show!")
            return

        if self.render:
            self._frames = []
            self._progress_bar = tqdm(total=len(self.geometries), desc="rendering")

            # make rendering as fast as possible
            self.fps = 10000.0

        # set background color
        opt = self.vis.get_render_option()
        opt.background_color = np.asarray(self.background_color)

        # add first mesh
        self._current_geometry = self.geometries[self._index].get()
        self.vis.add_geometry(self._current_geometry, reset_bounding_box=True)

    def close(self):
        self._is_playing = False
        self.vis.destroy_window()

    def play(self):
        self._is_playing = True
        self._play_loop()

    def pause(self):
        self._is_playing = False

    def jump(self, index: int):
        self._index = index

    def _play_loop(self):
        self._fps_counter.reset()

        while self._is_playing:
            # rotation
            ctr = self.vis.get_view_control()
            ctr.rotate(self.rotation_x, self.rotation_y)

            # events
            if not self.vis.poll_events():
                break

            self.vis.update_renderer()

            # skip if no meshes available
            if len(self.geometries) == 0:
                continue

            # render
            if self.render:
                color = self.vis.capture_screen_float_buffer(False)
                color = np.asarray(color)
                color = np.uint8(color * 255.0)
                # im_rgb = cvtColor(color, COLOR_BGR2RGB)
                self._frames.append(color)

                self.render_index += 1
                self._progress_bar.update()

            # frame playing
            current = self._millis()
            if (current - self._last_update_ts) > (1000.0 / self.fps):
                self._next_frame()
                self._last_update_ts = current

            # keep track of fps
            self._fps_counter.update()

            if self.debug:
                tqdm.write("FPS: %0.2f" % self._fps_counter.fps)

    def _next_frame(self):
        if not self.loop and self._index == len(self.geometries) - 1:
            if self.render:
                tqdm.write("\nsaving rendering...")
                clip = ImageSequenceClip(self._frames, fps=self._render_fps)
                clip.write_videofile(self.output_path, bitrate=self.bitrate, logger=None)
                clip.close()
                self._progress_bar.close()

            self._is_playing = False

        self.vis.remove_geometry(self._current_geometry, reset_bounding_box=False)
        self._index = (self._index + 1) % len(self.geometries)
        self._current_geometry = self.geometries[self._index].get()
        self.vis.add_geometry(self._current_geometry, reset_bounding_box=False)

    @staticmethod
    def _millis() -> int:
        return round(time.time() * 1000)
