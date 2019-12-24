#!/bin/bash

echo

# Check to see if in the right base directory
CURRENT_BASE_DIR=${PWD##*/}
if [ $CURRENT_BASE_DIR = "Picture-Frame" ]
then
    # Virtual enviromnment for flask application
    echo "[Picture-Frame] : Checking if virtual enviroment is setup ..."
    if [ -d ./env ]   # Check to see if virtual enviroment exists in current working directory
    then
        echo "[Picture-Frame] : Virtual environment already exists."
        echo "[Picture-Frame] : Activating virtual enviroment ..."
        . env/bin/activate                      # Activate virtual enviroment
    else
        echo "[Picture-Frame] : Creating a virtual environment for application ..."
        virtualenv -p python3 env               # Creating the virtual environment
        echo "[Picture-Frame] : Activating virtual enviroment ..."
        . env/bin/activate                      # Activate virtual enviroment
        echo "[Picture-Frame] : Installing all required python packages ..."
        pip3 install -U -r requirements.txt     # Install all required packages for virtual environment
    fi

    # Running the flask application
    echo "[Picture-Frame] : Starting application ..."
    echo
    python3 picture-frame.py
    echo
    echo "[Picture-Frame] : Application has stopped."
else
    # Current directory is not correct
    echo
    echo "[Picture-Frame] : CRITICAL! - Application was not able to start up!"
    echo "[Picture-Frame] : CRITICAL! - Shell script not executed within the correct directory."
    echo
fi
