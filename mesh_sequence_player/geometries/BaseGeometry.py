from abc import ABC, abstractmethod
import open3d as o3d


class BaseGeometry(ABC):
    @abstractmethod
    def get(self) -> o3d.geometry.Geometry3D:
        pass
