# ArUco Tester

This script can be used to test out [ArUco marker](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html) detection on video or image files as well as live webcam or RTSP feeds. It supports switching marker sizes and max-IDs on-the-fly. Requires Python v3.10 or greater.

<p align="center">
  <img src=".readme_assets/demo_anim.gif">
</p>

You can generate ArUco markers for testing using several [online](https://chev.me/arucogen/) [generator](https://aruco-gen.netlify.app/) [tools](https://fodi.github.io/arucosheetgen/).

## Usage

There are helper scripts available which handle the initial setup & running the tester script. These can be run as follows:

```bash
# Linux & MacOS
./run.sh

# Windows (cmd)
winrun.bat
```

When running the script, you'll be asked for the input video source, which can take one of several forms:

- an rtsp url (e.g. `rtsp://username:password@123.45.67.89:554/stream`)
- a path to a video file (e.g. `/path/to/video.mp4`)
- a path to an image (e.g. `/path/to/picture.jpg`)
- or an integer can be given, which will select a webcam if available (0 selects the 'first' webcam, 1, 2, 3 etc. can be used to read from other webcams if more than one is present)

You can optionally provide the video source when running the script by using the `-i` flag, there is also a `-s` flag which controls the default display size.

## Manual Usage

If you'd rather not use the helper script, it's possible to manually install the dependencies and run the tester script directly.

### Install

Before the tester script can be run, you first need to create a virtual environment and install some dependencies. This can be done as follows:

```bash
# Linux & MacOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Windows (cmd)
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Running the tester script

To run the script, make sure the virtual environment is activated (the one created in the [Install](https://github.com/pacefactory/aruco_tester?tab=readme-ov-file#install) section), and then run:

```bash
python aruco_tester.py
```

This script takes the same `-i` and `-s` flags as the helper script (or `--help` to see more info about the supported flags).

