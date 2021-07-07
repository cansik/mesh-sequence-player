from open3d.cpu.pybind.geometry import Geometry3D

from mesh_sequence_player.geometries.BaseGeometry import BaseGeometry


class Geometry(BaseGeometry):
    def __init__(self, geometry):
        self.geometry = geometry

    def get(self) -> Geometry3D:
        return self.geometry
