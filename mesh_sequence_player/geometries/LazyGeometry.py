import open3d as o3d
from mesh_sequence_player.geometries.BaseGeometry import BaseGeometry


class LazyGeometry(BaseGeometry):
    def __init__(self, file_path, loader):
        self.file_path = file_path
        self.loader = loader

    def get(self) -> o3d.geometry.Geometry3D:
        return self.loader(self.file_path, enable_post_processing=True)
