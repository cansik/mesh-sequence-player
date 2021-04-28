import time

import numpy as np
import open3d as o3d
from cv2 import VideoWriter_fourcc, VideoWriter
from tqdm import tqdm

from mesh_sequence_player.FPSCounter import FPSCounter
from mesh_sequence_player.utils import get_files_in_path


class MeshSequencePlayer:
    def __init__(self, fps: int = 24, loop: bool = True):
        self.fps = fps
        self.loop = loop
        self.meshes = []
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.background_color = [255, 255, 255]

        self.debug = False

        self.render = False
        self.output_path = "render.mp4"
        self.render_index = 0

        self.vis = o3d.visualization.Visualizer()

        self._is_playing: bool = False
        self._index: int = 0
        self._last_update_ts = 0

        self._writer: VideoWriter = None
        self._progress_bar: tqdm = None

        self._fps_counter = FPSCounter()

    def add(self, mesh_path: str):
        self.meshes.append(o3d.io.read_triangle_mesh(mesh_path))

    def load(self, mesh_folder: str, mesh_format: str = "*.obj"):
        files = sorted(get_files_in_path(mesh_folder, extensions=[mesh_format]))

        with tqdm(total=len(files), desc="loading meshes") as pbar:
            for mesh_path in files:
                self.add(mesh_path)
                pbar.update()

    def open(self, window_name: str = 'Mesh Sequence Player',
             width: int = 1080, height: int = 1080,
             visible: bool = True):
        self.vis.create_window(window_name=window_name,
                               width=width,
                               height=height,
                               visible=visible)

        if len(self.meshes) == 0:
            print("No meshes to show!")
            return

        if self.render:
            fourcc = VideoWriter_fourcc(*'mp4v')
            self._writer = VideoWriter(self.output_path, fourcc, self.fps, (width, height))
            self._progress_bar = tqdm(total=len(self.meshes), desc="rendering")

            # make rendering as fast as possible
            self.fps = 10000.0

        # set background color
        opt = self.vis.get_render_option()
        opt.background_color = np.asarray(self.background_color)

        # add first mesh
        self.vis.add_geometry(self.meshes[self._index], reset_bounding_box=True)

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
            if len(self.meshes) == 0:
                continue

            # render
            if self.render:
                color = self.vis.capture_screen_float_buffer(False)
                color = np.asarray(color)
                color = np.uint8(color * 255.0)
                self._writer.write(color)

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
        if not self.loop and self._index == len(self.meshes) - 1:
            if self.render:
                self._writer.release()
                self._progress_bar.close()

            self._is_playing = False

        self.vis.remove_geometry(self.meshes[self._index], reset_bounding_box=False)
        self._index = (self._index + 1) % len(self.meshes)
        self.vis.add_geometry(self.meshes[self._index], reset_bounding_box=False)

    @staticmethod
    def _millis() -> int:
        return round(time.time() * 1000)
