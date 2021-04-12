from MeshSequencePlayer.MeshSequencePlayer import MeshSequencePlayer
import argparse


def main():
    player = MeshSequencePlayer(fps=args.fps, loop=not args.no_loop)

    print("loading meshes...")
    player.load(args.input)

    print("playing...")
    player.open()
    player.play()
    player.close()


if __name__ == "__main__":
    a = argparse.ArgumentParser(
        description="Play mesh sequences directly in python.")
    a.add_argument("input", help="Path to the mesh files (directory).")
    a.add_argument("--format", default="*.obj", type=str,
                   help="File format (Default *.obj).")
    a.add_argument("--fps", default=24, type=int,
                   help="Framerate for playback.")
    a.add_argument("--no-loop", action='store_true', help="Do not loop the sequence.")
    args = a.parse_args()

    main()
