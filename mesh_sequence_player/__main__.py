import os

from mesh_sequence_player.MeshSequencePlayer import MeshSequencePlayer
import argparse


def main():
    player = MeshSequencePlayer(fps=args.fps, loop=not args.no_loop)
    player.rotation_x = args.rotation
    dir_name = os.path.split(args.input)[-1]

    if args.output is not None:
        # force mp4 filename for renderer
        if not args.output.endswith(".mp4"):
            args.output += ".mp4"

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        player.render = True
        player.output_path = os.path.abspath(args.output)

    print("loading meshes...")
    player.load(args.input)

    print("playing...")
    player.open(window_name="Mesh Sequence Player - %s" % dir_name,
                width=args.width, height=args.height, visible=not args.hidden)
    player.play()
    player.close()


if __name__ == "__main__":
    a = argparse.ArgumentParser(
        prog="mesh_sequence_player",
        description="Play mesh sequences directly in python.")
    a.add_argument("input", default=".", help="Path to the mesh files (directory).")
    a.add_argument("--format", default="*.obj", type=str, help="File format (default *.obj).")
    a.add_argument("--fps", default=24, type=int, help="Framerate for playback.")
    a.add_argument("--no-loop", action='store_true', help="Do not loop the sequence.")
    a.add_argument("--width", default=512, type=int, help="Player width (default 512).")
    a.add_argument("--height", default=512, type=int, help="Player height (default 512).")
    a.add_argument("--hidden", action='store_true', help="Hide preview window.")
    a.add_argument("--rotation", default=0.0, type=float, help="Horizontal axis rotation.")
    a.add_argument("--output", default=None, type=str,
                   help="Output path to mp4 file. Sets no-loop to True.")
    args = a.parse_args()

    if args.output is not None:
        args.no_loop = True
        args.output = os.path.abspath(args.output)

    main()
