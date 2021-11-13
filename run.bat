@echo off
cls
:input
set INPUT=
set /P INPUT=Type input: %=%
python.exe main.py %INPUT%
goto input