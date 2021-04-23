import argparse
import os.path
import time

import open3d as o3d

from mesh_sequence_player.utils import get_files_in_path


class Watch:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        print("%s: %.4fs" % (self.name, self.end - self.start))


def load(mesh_path, index: int = 0):
    x = index % 24 * 0.8
    y = int(index / 24) * -1.8

    with Watch("read"):
        mesh = o3d.io.read_triangle_mesh(mesh_path)
    mesh.translate((x, y, 0))
    with Watch("add"):
        vis.add_geometry(mesh, reset_bounding_box=True)
    print("loading %s" % mesh_path)


if __name__ == '__main__':
    a = argparse.ArgumentParser(description="Play mesh sequences directly in python.")
    a.add_argument("input", default=".", help="Path to the mesh files (directory).")
    args = a.parse_args()

    files = list(sorted(get_files_in_path(args.input, extensions=["*.obj"])))
    files = [os.path.abspath(p) for p in files][:5]  # [:168]

    vis = o3d.visualization.Visualizer()

    vis.create_window(window_name="test",
                      width=512 * 3,
                      height=512 * 3,
                      visible=True)

    [load(p, i) for i, p in enumerate(files)]

    vis.reset_view_point(True)

    # events
    while True:
        if not vis.poll_events():
            break

        vis.update_renderer()
        time.sleep(0.03)
