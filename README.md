# py_guard

So The plan is to implement multiThread system

* Thread One - Listen to microphone stuff(for the N db) -> write to Queue1... and keep listening 
* Thread Two - Checking Queue1 for an event -> turn on camera take N pictures put them to Queue2 
* Thread Three - Checking Queue2 for pictures receive them and pack in gzip put it in Queue3
* Thread Four - Checking Queue3 for gzip, send to an email

## Required Libraries:
* pyaudio
* OpenCv (instructions: http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/)
