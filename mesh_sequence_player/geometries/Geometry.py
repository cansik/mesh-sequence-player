import open3d as o3d
from mesh_sequence_player.geometries.BaseGeometry import BaseGeometry


class Geometry(BaseGeometry):
    def __init__(self, geometry):
        self.geometry = geometry

    def get(self) -> o3d.geometry.Geometry3D:
        return self.geometry
