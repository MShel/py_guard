# py_guard

So The plan is to implement multiThread system

* Thread One - Listen to microphone stuff(for the N db) -> write to Queue, and keep listening 
* Thread Two - Checking Queue for an _microphone_sentinel -> turn on camera take N pictures put them to archive -> and write _camera_sentinel 
* Thread Three - Checking Queue for _camera_sentinel  pack all pictures in zip put _archiver_sentinel and archive name into queue
* Thread Four - Checking queue for _archiver_sentinel get the archive name connect to remote smptp and send it

## Required Libraries:
* pyaudio
* OpenCv (instructions: http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/)

## Required Things:
* linux(tested on ubuntu)
* microphone
* camera
* credentials to any remote smptp server(gmail?)
* email address


