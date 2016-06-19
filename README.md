# py_guard

python3 based little system which listens to microphone
registers taps takes pictures, archives and sends to defined 
email addr. Build only in educational purposes.

to run:

* Make sure you have all the stuff from Required Things:
* adjust setting in config/config.ini
* run python3 pyguard.py

https://trello.com/b/gxxXDyA4/python-protector

### For working coroutines based  system plz checkout v 0.0.2
### For working multithreaded system plz checkout v 0.0.1

## Required Libraries:
* pyaudio: apt-get install python3-pyaudio
* OpenCv: (instructions: http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/)

## Required Things:
* linux(tested on ubuntu)
* microphone
* camera
* credentials to any remote smtp server(gmail?)
* email address


