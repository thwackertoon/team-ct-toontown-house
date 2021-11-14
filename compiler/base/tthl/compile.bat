@echo off
python blah.py
ld -r -b binary -o binary.o ToontownHouse.py.enc
python blah.py 2
ld -r -b binary -o size.o osize
gcc -Wall -mwindows -IC:\Panda3D-1.8.0\python\include -LC:\Panda3D-1.8.0\python\include -LC:\Panda3D-1.8.0\python\libs -o ToontownHouse.exe main.c binary.o size.o -lpython27

gcc -IC:\Panda3D-1.8.0\python\include -LC:\Panda3D-1.8.0\python\include -LC:\Panda3D-1.8.0\python\libs -o ToontownHouse_dev.exe main.c binary.o size.o -lpython27  