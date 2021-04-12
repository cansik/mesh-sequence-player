from MeshSequencePlayer.MeshSequencePlayer import MeshSequencePlayer
import argparse


def main():
    player = MeshSequencePlayer(fps=args.fps, loop=not args.no_loop)
    player.rotation_x = args.rotation

    print("loading meshes...")
    player.load(args.input)

    print("playing...")
    player.open(width=args.width, height=args.height, visible=not args.hidden)
    player.play()
    player.close()


if __name__ == "__main__":
    a = argparse.ArgumentParser(
        description="Play mesh sequences directly in python.")
    a.add_argument("input", help="Path to the mesh files (directory).")
    a.add_argument("--format", default="*.obj", type=str,
                   help="File format (default *.obj).")
    a.add_argument("--fps", default=24, type=int, help="Framerate for playback.")
    a.add_argument("--no-loop", action='store_true', help="Do not loop the sequence.")
    a.add_argument("--width", default=1920, type=int, help="Player width (default 1920).")
    a.add_argument("--height", default=1080, type=int, help="Player height (default 1080).")
    a.add_argument("--rotation", default=0.0, type=float, help="Horizontal axis rotation.")
    a.add_argument("--hidden", action='store_true', help="Hide preview window.")
    args = a.parse_args()

    main()
