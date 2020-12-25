# RecordingSystem_py
Principles used: Parallelism, Synchronization, Communication-UDP

I created a recording system that will listen and receive packages from two channels simultaneously, using UDP.
Channel 1 is for transmitting data packages, and channel 2 is for transmitting header packages.(each header package is associated with several data packages)
The system should receive the packages, and keep them in a file in a logical way: each header package with its data packages.

The file "main.py" creates the listener threads, and the file "test.py" creates the sender threads. 
One should run "main.py" first, and then "test.py".
The system creates and writes into the file "output.txt".

For comparison, I wrote the same project in C++ as well. Feel free to take a look.
