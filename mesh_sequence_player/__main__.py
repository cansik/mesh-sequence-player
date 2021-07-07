import argparse
import os

from mesh_sequence_player.MeshSequencePlayer import MeshSequencePlayer


def parse_arguments():
    a = argparse.ArgumentParser(
        prog="mesh-sequence-player",
        description="Play mesh sequences directly in python.")
    a.add_argument("input", default=".", help="Path to the mesh files (directory).")
    a.add_argument("--format", default="*.obj", type=str, help="File format (default *.obj).")
    a.add_argument("--fps", default=24, type=int, help="Framerate for playback.")
    a.add_argument("--no-loop", action='store_true', help="Do not loop the sequence.")
    a.add_argument("--size", default=[512, 512], type=int, nargs=2, metavar=('width', 'height'),
                   help="Size of the window.")
    a.add_argument("--background", default=[255, 255, 255], type=int, nargs=3, metavar=('r', 'g', 'b'),
                   help="Background color (0-255).")
    a.add_argument("--hidden", action='store_true', help="Hide preview window.")
    a.add_argument("--rotate", default=0.0, type=float, help="Horizontal axis rotation.")
    a.add_argument("--output", default=None, type=str, help="Output path to mp4 file. Sets no-loop to True.")
    a.add_argument("--load-safe", action='store_true', help="Load meshes the safe way and with texture (but slower).")
    a.add_argument("--lazy", action='store_true', help="Load meshes one at a time (render large sequences).")
    a.add_argument("-p", "--pointcloud", action='store_true', help="Load pointclouds (*.ply) instead of meshes.")
    a.add_argument("--debug", action='store_true', help="Show debug information.")

    args = a.parse_args()

    if args.output is not None:
        args.no_loop = True
        args.output = os.path.abspath(args.output)

    # set pointcloud specific settings
    if args.pointcloud:
        if args.format == "*.obj":
            args.format = "*.ply"

    return args


def main():
    args = parse_arguments()

    player = MeshSequencePlayer(fps=args.fps, loop=not args.no_loop)
    player.rotation_x = args.rotate
    player.background_color = args.background
    player.debug = args.debug
    player.load_safe = args.load_safe
    player.lazy_loading = args.lazy

    dir_name = os.path.split(args.input)[-1]

    if args.output is not None:
        # force mp4 filename for renderer
        if not args.output.endswith(".mp4"):
            args.output += ".mp4"

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        player.render = True
        player.output_path = os.path.abspath(args.output)

    if args.pointcloud:
        player.load_pointclouds(args.input, args.format)
    else:
        player.load_meshes(args.input, args.format)

    width, height = args.size

    player.open(window_name="Mesh Sequence Player - %s" % dir_name,
                width=width, height=height, visible=not args.hidden)

    player.play()
    player.close()


if __name__ == "__main__":
    main()
