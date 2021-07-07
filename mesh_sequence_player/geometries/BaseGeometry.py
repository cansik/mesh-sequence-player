from abc import ABC, abstractmethod

from open3d.cpu.pybind.geometry import Geometry3D


class BaseGeometry(ABC):
    @abstractmethod
    def get(self) -> Geometry3D:
        pass