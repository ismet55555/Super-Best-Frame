# Picture-Frame
This is a picture frame slideshow for running on linux systems that is connected to a display/monitor. These linux systems may include Raspian, Ubuntu, Mint, or even WSL (Windows Subsystem for Linux).
The slideshow is displayed on a connected display device / monitor in either horizontal (landscape) or vertical (portrait) orientation.
TODO: Explain the remote control blah blah

## Basic Description
You will run this on a computer that is connected to a monitor or display.
You will then be able to control the images on the display using a web browser an through your local or home network.

---
## Compatibility

### Minimum System Requirements
The following are the minimum system requirments where this application will work smooth and as intendent.
- __CPU__: 1.2 GHz
- __Cores__: 4
- __RAM__: 1GB
- __Disk Storage__: 400 MB + Images


### Verified Platforms
This program has been tested on a limited number of different systems, this is what I know so far:

|           Works Fine           |    Will Not Work    |
|:------------------------------:|:-------------------:|
| Raspberry Pi 3b+ *(Raspbian)*  | Raspberry Pi Zero W |
| Raspberry Pi 4 *(Raspbian)*    |                     |
| Atomic Pi *(Lubuntu 18.04)*    |                     |
| Ubuntu 16.04 and up            |                     |

TODO: TEST ON WSL!!

---

## Installing and Setting Up Picture-Frame
1. *[If on remote computer]* Enter remote linux device using `ssh`:
    - Linux: `ssh <username/login>@<IP address of picture frame computer>`
    - Windows: `TODO`
    - MAC: `TODO`
2. Navigate into user documents directory: 
    - `$ cd ~/Documents`
3. *[If needed]* Install git:
    - `$ sudo apt install git-all`
4. *[If needed]* Configure git:
    - `$ git config --global user.name "<Your Name"`
    - `$ git config --global user.email "<your_email@example.com>"`
5. Clone git repo form github:
    - `$ git clone <copied ssh clone link>`
6. Install OpenCV system dependencies:
    - `(env) $ sudo apt install libatlas3-base libwebp6 libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4`
    - `(env) $ sudo apt install python3-opencv`
7. Change directory into cloned directory:
    - `$ cd Picture-Frame`
8. Run the start script
    - `$ ./start.sh`

**NOTE**: The `start.sh` script executes the following:
1. Creates a virtual environment (`$ python3 -m venv env`)
2. Activates the virtual environment (`$ source env/bin/activate`)
3. Installs python package dependencies (`(env) $ pip install -r requirements.txt`)
4. Runs the python script (`(env) $ python3 picture-frame.py`)
---

## Supported Image Formats
- `.png`, `.jpg`, `.jpeg`, `.bmp`, `.dib`, `.jpe`, `.jp2`, `.pgm`, `.tiff`, `.tif`, `.ppm`

---

## Adding Images to the `Images` Directory
All images that are displayed in the picture frame must be stored in the "Images" directory of this project.
Note that subdirectories in the "Images" directory will not be considered.

### Via Physical Flash/USB Drive
- TODO

### Remotely Via `scp` Command
- TODO

### Remotely Via `ftp` Command
- TODO


