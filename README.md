# Mesh Sequence Player
A simple mesh sequence player based on [open3d](https://github.com/intel-isl/Open3D).

![person](readme/person_square.gif)

It just loads all the mesh files and plays them back. The tool is intended for preview and visualisation purposes only. Currently there is no support for multi-processing in open3d, so mesh loading takes some time.

### Installation
To install the necessary packages, use the requirements file:

```
pip install -r requirements.txt
```

### Usage
To display a sequence of mesh files just run the following command:

```
python mesh-sequence-player.py mesh-folder --format *.obj
```

#### Rendering
It is also possible to render the individual frames into a png sequence. Currently only one mesh view will be rendered and not the stable FPS. If an `output` path is provided, the `no-loop` option is automatically set to `True`.

```
python mesh-sequence-player.py mesh-folder --output frames
```

#### Help

```
usage: mesh-sequence-player.py [-h] [--format FORMAT] [--fps FPS] [--no-loop]
                               [--width WIDTH] [--height HEIGHT]
                               [--rotation ROTATION] [--hidden]
                               input

Play mesh sequences directly in python.

positional arguments:
  input                Path to the mesh files (directory).

optional arguments:
  -h, --help           show this help message and exit
  --format FORMAT      File format (default *.obj).
  --fps FPS            Framerate for playback.
  --no-loop            Do not loop the sequence.
  --width WIDTH        Player width (default 1920).
  --height HEIGHT      Player height (default 1080).
  --rotation ROTATION  Horizontal axis rotation.
  --hidden             Hide preview window.
```

### About
MIT License - Copyright (c) 2021 Florian Bruggisser
