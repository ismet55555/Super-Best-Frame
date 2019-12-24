# Picture-Frame
Simple picture frame slideshow for linux setups

### Setting Up Picture-Frame (Remote Deployment)
1. ssh into remote linux device:
    - Linux: `ssh <username/login>@<IP address>`
    - Windows: `TODO`
    - MAC: `TODO`
3. Navigate into user download directory: 
    - `$ cd ~/Documents`
3. [If needed] Install git:
    - `$ sudo apt install git-all`
4. [If needed] Configure git:
    - `$ git config --global user.name "<Your Name"`
    - `$ git config --global user.email "<your_email@example.com>"`
4. Clone git repo form github:
    - `$ git clone <copied ssh clone link>`
4. Set system environmental variable so images apear on remote desktop:
    - `$ export DISPLAY=:0`
5. Change directory into cloned directory:
    - `$ cd Picture-Frame`
6. Create python virtual environment: 
    - `$ python3 -m venv env`
7. Activate the virtual environment: 
    - `$ . env/bin/activate`
8. Install OpenCV system dependencies:
    - `(env) $ sudo apt install libatlas3-base libwebp6 libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4`
8. Install all dependencies:
    - `(env) $ pip install -r requirements.txt`
9. Run the program using python
    - `(env) $ python3 picture-frame.py`


### Adding Images
All images must be stored in the "Images" directory of this project.
Note that subdirectories in the "Images" directory will not be considered.
