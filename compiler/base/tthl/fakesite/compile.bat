@echo off
gcc -shared -IC:\Panda3D-1.8.0\python\include -LC:\Panda3D-1.8.0\python\include -LC:\Panda3D-1.8.0\python\libs -o site.pyd main.c -lpython27
pause