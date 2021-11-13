@echo off
cls
:input
set INPUT=
set /P INPUT=Type input: %=%
C:/Python27/ppython.exe main.py %INPUT%
goto input