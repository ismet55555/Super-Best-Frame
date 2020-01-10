<h1 align="center">Picture-Frame :eyes:</h1>

This is a picture frame slideshow for running on linux systems that is connected to a display/monitor. These linux systems may include Raspian, Ubuntu, Mint, or even WSL (Windows Subsystem for Linux).
The slideshow is displayed on a connected display device / monitor in either horizontal (landscape) or vertical (portrait) orientation.
TODO: Explain the remote control blah blah


### Very Basically ...
1. You run this on a computer that is connected to a monitor or display.
2. You will then be able to control the shown images on the monitor using a website that you can access with a computer, phone, or tablet.
3. You can access this website as long as you are on your local or home network.

## :eyeglasses: Overview



## Demo
`picture-frame` is able to create a beautiful mointor/display slideshows

<p align="center">
  <img width="700" align="center" src="https://user-images.githubusercontent.com/9840435/60266022-72a82400-98e7-11e9-9958-f9004c2f97e1.gif" alt="demo"/>
</p>




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

TODO: TEST ON WSL!!



## :rocket: Installing and Setup
TODO: Need `sudo apt install -y openssh-server` ... maybe seperate .md for ssh setup for different devices?
1. *[If on remote computer]* Enter remote linux device using `ssh`:
    - Linux: `ssh <username/login>@<IP address of picture frame computer>`
    - Windows: `TODO`
    - MAC: `TODO`
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
    - `$ ./start.sh`

**NOTE**: *Check out the [`start.sh`](start.sh) script to see what exactly it executes.*


## :boom: Usage
TODO - maybe some gifs


### Image Formats You Can Use
- `.png`, `.jpg`, `.jpeg`, `.bmp`, `.dib`, `.jpe`, `.jp2`, `.pgm`, `.tiff`, `.tif`, `.ppm`



### Adding Images
All images that are displayed in the picture frame must be stored in the `Images` directory of this project.
Note that subdirectories in the "Images" directory will not be considered.

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
