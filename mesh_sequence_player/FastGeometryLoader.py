import multiprocessing
from functools import partial
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

import open3d as o3d
import numpy as np
from tqdm import tqdm


class _MeshTransmissionFormat:
    def __init__(self, mesh: o3d.geometry.TriangleMesh):
        self.adjacency_list = mesh.adjacency_list

        self.textures = [np.asarray(tex) for tex in mesh.textures if not tex.is_empty()]

        self.triangle_material_ids = np.array(mesh.triangle_material_ids)
        self.triangle_normals = np.array(mesh.triangle_normals)
        self.triangle_uvs = np.array(mesh.triangle_uvs)
        self.triangles = np.array(mesh.triangles)

        self.vertex_colors = np.array(mesh.vertex_colors)
        self.vertex_normals = np.array(mesh.vertex_normals)
        self.vertices = np.array(mesh.vertices)

    def create_mesh(self) -> o3d.geometry.TriangleMesh:
        mesh = o3d.geometry.TriangleMesh()

        mesh.adjacency_list = self.adjacency_list

        mesh.textures = [o3d.geometry.Image(tex) for tex in self.textures]

        mesh.triangle_material_ids = o3d.utility.IntVector(self.triangle_material_ids)
        mesh.triangle_normals = o3d.utility.Vector3dVector(self.triangle_normals)
        mesh.triangle_uvs = o3d.utility.Vector2dVector(self.triangle_uvs)
        mesh.triangles = o3d.utility.Vector3iVector(self.triangles)

        mesh.vertex_colors = o3d.utility.Vector3dVector(self.vertex_colors)
        mesh.vertex_normals = o3d.utility.Vector3dVector(self.vertex_normals)

        mesh.vertices = o3d.utility.Vector3dVector(self.vertices)
        return mesh


class _PointCloudTransmissionFormat:
    def __init__(self, pointcloud: o3d.geometry.PointCloud):
        self.points = np.array(pointcloud.points)
        self.colors = np.array(pointcloud.colors)
        self.normals = np.array(pointcloud.normals)

    def create_pointcloud(self) -> o3d.geometry.PointCloud:
        pointcloud = o3d.geometry.PointCloud()
        pointcloud.points = o3d.utility.Vector3dVector(self.points)
        pointcloud.colors = o3d.utility.Vector3dVector(self.colors)
        pointcloud.normals = o3d.utility.Vector3dVector(self.normals)
        return pointcloud


def _load_mesh_data(file: str, post_processing: bool = False) -> _MeshTransmissionFormat:
    mesh: o3d.geometry.TriangleMesh = o3d.io.read_triangle_mesh(file, enable_post_processing=post_processing)
    # mesh.compute_vertex_normals()
    # mesh.compute_triangle_normals()
    # mesh.compute_adjacency_list()
    return _MeshTransmissionFormat(mesh)


def load_geometries(files: [str]) -> [o3d.geometry.TriangleMesh]:
    meshes = []
    with tqdm(desc="mesh loading", total=len(files)) as prog:
        for file in files:
            meshes.append(_load_mesh_data(file))
            prog.update()
    return [mesh.create_mesh() for mesh in meshes]


def load_meshes_fast(files: [str], post_processing: bool = False) -> [o3d.geometry.TriangleMesh]:
    meshes = []
    with Pool(processes=min(multiprocessing.cpu_count(), len(files))) as pool:
        method = partial(_load_mesh_data, post_processing=post_processing)
        for result in tqdm(pool.imap(method, files), total=len(files), desc="mesh loading"):
            meshes.append(result)
    return [mesh.create_mesh() for mesh in meshes]


def load_meshes_safe(files: [str], post_processing: bool = False) -> [o3d.geometry.TriangleMesh]:
    meshes = []
    with ThreadPool(processes=min(multiprocessing.cpu_count(), len(files))) as pool:
        method = partial(o3d.io.read_triangle_mesh, enable_post_processing=post_processing)
        for mesh in tqdm(pool.imap(method, files), total=len(files), desc="mesh loading"):
            meshes.append(mesh)
    return meshes


def load_pointclouds_safe(files: [str]) -> [o3d.geometry.PointCloud]:
    clouds = []
    with tqdm(desc="pointcloud loading", total=len(files)) as prog:
        for file in files:
            clouds.append(o3d.io.read_point_cloud(file))
            prog.update()
    return clouds


def _load_pointcloud_data(file: str) -> _PointCloudTransmissionFormat:
    pointcloud = o3d.io.read_point_cloud(file)
    return _PointCloudTransmissionFormat(pointcloud)


def load_pointclouds_fast(files: [str]) -> [o3d.geometry.PointCloud]:
    clouds = []
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        for result in tqdm(pool.imap(_load_pointcloud_data, files), total=len(files), desc="pointcloud loading"):
            clouds.append(result)
    return [cloud.create_pointcloud() for cloud in clouds]
