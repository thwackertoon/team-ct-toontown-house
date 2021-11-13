@echo off
cls
:input
set INPUT=
set /P INPUT=Type input: %=%
C:/Panda3D-1.8.0/python/ppython.exe main.py %INPUT%
goto input