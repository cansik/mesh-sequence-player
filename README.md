# Mesh Sequence Player
A simple mesh sequence player based on [open3d](https://github.com/intel-isl/Open3D).

![person](readme/person_square.gif)

It just loads all the mesh files and plays them back. The tool is intended for preview and visualisation purposes only. Currently there is no support for multi-processing in open3d, so mesh loading takes some time.

### Installation
To install the necessary packages, use the requirements file:

```
pip install git+https://github.com/cansik/mesh-sequence-player.git@1.2.0
```

### Usage
To display a sequence of mesh files just run the following command:

```
python -m mesh_sequence_player folder_to_meshes
```

#### Rendering
It is also possible to render the individual frames into a mp4 file. Currently only one mesh view will be rendered. If an `output` path is provided, the `no-loop` option is automatically set to `True` and rendering will run with `1000.0 FPS` to render as fast as possible.

```
python -m mesh_sequence_player folder_to_meshes --output render.mp4
```

#### Help
Here is the full help file.

```
usage: mesh_sequence_player [-h] [--format FORMAT] [--fps FPS] [--no-loop]
                            [--width WIDTH] [--height HEIGHT] [--hidden]
                            [--rotation ROTATION] [--output OUTPUT]
                            input

Play mesh sequences directly in python.

positional arguments:
  input                Path to the mesh files (directory).

optional arguments:
  -h, --help           show this help message and exit
  --format FORMAT      File format (default *.obj).
  --fps FPS            Framerate for playback.
  --no-loop            Do not loop the sequence.
  --width WIDTH        Player width (default 512).
  --height HEIGHT      Player height (default 512).
  --hidden             Hide preview window.
  --rotation ROTATION  Horizontal axis rotation.
  --output OUTPUT      Output path to mp4 file. Sets no-loop to True.
```

### About
MIT License - Copyright (c) 2021 Florian Bruggisser
