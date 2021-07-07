from open3d.cpu.pybind.geometry import Geometry3D

from mesh_sequence_player.geometries.BaseGeometry import BaseGeometry


class LazyGeometry(BaseGeometry):
    def __init__(self, file_path, loader):
        self.file_path = file_path
        self.loader = loader

    def get(self) -> Geometry3D:
        return self.loader(self.file_path)
