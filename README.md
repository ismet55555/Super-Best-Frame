<h1 align="center">Picture-Frame :bowtie:</h1>

This is a picture frame slideshow for running on linux systems that is connected to a display/monitor. These linux systems may include Raspian, Ubuntu, Mint, or even WSL (Windows Subsystem for Linux).
The image slideshow is displayed on a connected display, monitor, or projector in either horizontal (landscape) or vertical (portrait) orientation.

You can then control the picture frame slideshow's behavior using a simple browser based web interface of the local network at port `5555`. That is, you can access this web interface with `http://<IP Address of Picture Frame Host>:55555`

### Very Basically ...
1. You run this on a computer that is connected to a monitor, display, or projector.
2. You will then be able to control the shown images on the monitor using a website that you can access with a computer, phone, or tablet.
3. You can access this website as long as you are on your local or home network.

## :eyeglasses: Overview

* [Compatibility](#thumbsup-compatibility)
    * [Minimum System Requirements](#minimum-system-requirements)
    * [Verified Platforms](#verified-platforms)
* [Installing and Setup](#rocket-installing-and-setup)
* [Usage](#boom-usage)
    * [Image Formats You Can Use](#image-formats-you-can-use)
    * [Adding Images](#adding-images)
        * [Via Physical Flash/USB Drive](#via-physical-flashusb-drive)
        * [Remotely Via scp Command](#remotely-via-scp-command)
        * [Remotely Via ftp Command](#remotely-via-ftp-command)
* [Author](#bust_in_silhouette-author)
* [Licence](#licence)


## :thumbsup: Compatibility

### Minimum System Requirements
The following are the minimum system requirments where this application will work smooth and as intendent.
- __CPU__: 1.2 GHz
- __CPUs/Cores__: 4
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

I have not tried it out on `Microsoft WSL (Windows Subsystem for Linux)`, but may work on it as well.



## :rocket: Installing and Setup
1. *[If on remote computer]* Enter remote linux device using `ssh`:
    - MAC/Linux Terminal, Windows Powershell: `ssh <username/login>@<IP address of picture frame computer>`
    - May need to enable SSH on remote linux host computer: `sudo apt install -y openssh-server`
2. Navigate into user documents directory: 
    - `$ cd ~/Documents`
3. Install git:
    - `$ sudo apt -y install git-all`
4. Configure git:
    - `$ git config --global user.name "Your Name Here"`
    - `$ git config --global user.email "your.email@here.com"`
5. Clone this public git repo form github:
    - `$ git clone git@github.com:ismet55555/Picture-Frame.git`
6. Change directory into cloned directory:
    - `$ cd Picture-Frame`
7. Install OpenCV system dependencies:
    - `$ sudo apt -y install python3-opencv`
8. Run the start script
    - `$ ./start`

**NOTE**: *Check out the [`start`](start) script to see what exactly it executes.*


## :boom: Usage
TODO - Maybe some gifs


### Image Formats You Can Use
- `.png`, `.jpg`, `.jpeg`, `.bmp`, `.dib`, `.jpe`, `.jp2`, `.pgm`, `.tiff`, `.tif`, `.ppm`



### Adding Images
All images that are displayed in the picture frame must be stored in the `Images` directory of this project.
Note that subdirectories in the "Images" directory will not be considered.

#### Using The Web Interface
- TODO

#### Via Physical Flash/USB Drive
- TODO

#### Remotely Via `scp` Command
- TODO

#### Remotely Via `ftp` Command
- TODO


## :bust_in_silhouette: Author
**Ismet Handžić** - Github: [@ismet55555](https://github.com/ismet55555)



## Licence
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
