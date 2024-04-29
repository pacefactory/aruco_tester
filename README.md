# ArUco Tester

This script can be used to test out [ArUco marker](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html) detection on video or image files as well as live webcam or RTSP feeds.

<p align="center">
  <img src=".readme_assets/demo_anim.gif">
</p>

You can generate ArUco markers for testing using several [online](https://chev.me/arucogen/) [generator](https://aruco-gen.netlify.app/) [tools](https://fodi.github.io/arucosheetgen/).

## Install

To run the script, you first need to create a virtual environment and install some dependencies. This can be done as follows:

```bash
# Linux & MacOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Windows
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```


## Running the script

To run the script, make sure the virtual environment is activated (the one created in the [Install](https://github.com/EricPacefactory/rtsp_demo_2024?tab=readme-ov-file#install) section), and then run:

```bash
python aruco_tester.py
```

Optionally there's a `-i` flag that can be used to specify the input video source and a `-s` flag which can be used to adjust the initial display sizing (the up/down arrow keys can be used to adjust the sizing while running).
Input sources can take the form of:
- an rtsp url (e.g. `rtsp://username:password@123.45.67.89:554/stream`)
- a path to a video file (e.g. `/path/to/video.mp4`)
- a path to an image (e.g. `/path/to/picture.jpg`)
- or an integer can be given, which will select a webcam if available (0 selects the 'first' webcam, 1, 2, 3 etc. can be used to read from other webcams if more than one is present)

If the `-i` flag is not provided, you'll be asked to enter the input source when running the script.

### Helper scripts

For convenience, there are helper scripts available which handle all of the setup (including creating/activating the virtual environment) and running the script. They can be used as follows:

```bash
# Linux & MacOS
./envrun.sh

# Windows (cmd)
winenvrun.bat
```

The `-i` and `-s` flags can also be passed to these scripts.


