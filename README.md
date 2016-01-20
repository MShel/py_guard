# py_guard

So some planning is to implement mltithread system:

* Thread One - Listen to microphone stuff(for the N db) -> write to Queue1... and keep listening 
* Thread Two - Checking Queue1 for an event -> turn on camera take N pictures put them to Queue2 
* Thread Three - Checking Queue2 for pictures receive them and pack in gzip put it in Queue3
* Thread Four - Checking Queue3 for gzip, send to an email
