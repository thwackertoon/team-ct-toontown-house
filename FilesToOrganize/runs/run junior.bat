@echo off
cls
:input
set INPUT=
set /P INPUT=Type input: %=%
D:/Panda3D-1.8.0/Python/ppython.exe main.py %INPUT%
goto input