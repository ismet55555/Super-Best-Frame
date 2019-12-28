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
6. Run the start script
    - `$ ./start.sh`

NOTE: The `start.sh` script:
    - Creates a virtual environment (`$ python3 -m venv env`)
    - Activates the virtual environment (`$ . env/bin/activate`)
    - Installs OpenCV system dependencies (`(env) $ sudo apt install <a few packages>`)
    - Installs python package dependencies (`(env) $ pip install -r requirements.txt`)
    - Runs the python script (``(env) $ python3 picture-frame.py`)


### Adding Images to the `Images` directory
All images must be stored in the "Images" directory of this project.
Note that subdirectories in the "Images" directory will not be considered.
