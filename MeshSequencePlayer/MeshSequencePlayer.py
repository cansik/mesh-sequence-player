import time

import open3d as o3d

from MeshSequencePlayer.utils import get_files_in_path


class MeshSequencePlayer:
    def __init__(self, fps: int = 24, loop: bool = True):
        self.fps = fps
        self.loop = loop
        self.meshes = []

        self.vis = o3d.visualization.Visualizer()

        self._is_playing: bool = False
        self._index: int = 0
        self._last_update_ts = 0

    def add(self, mesh_path: str):
        self.meshes.append(o3d.io.read_triangle_mesh(mesh_path))

    def load(self, mesh_folder: str, mesh_format: str = "*.obj"):
        files = sorted(get_files_in_path(mesh_folder, extensions=[mesh_format]))
        [self.add(mesh_path) for mesh_path in files]

    def open(self, window_name: str = 'Mesh Sequence Player',
             width: int = 1080, height: int = 1080,
             visible: bool = True):
        self.vis.create_window(window_name=window_name,
                               width=width,
                               height=height,
                               visible=visible)

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
        while self._is_playing:
            self.vis.poll_events()
            self.vis.update_renderer()

            current = self._millis()
            if (current - self._last_update_ts) > (1000.0 / self.fps):
                self._next_frame()
                self._last_update_ts = current

    def _next_frame(self):
        if not self.loop and self._index == len(self.meshes) - 1:
            self._is_playing = False

        self.vis.remove_geometry(self.meshes[self._index])
        self._index = (self._index + 1) % len(self.meshes)
        self.vis.add_geometry(self.meshes[self._index])

    @staticmethod
    def _millis() -> int:
        return round(time.time() * 1000)
