@echo off
cls
:input
set INPUT=
set PPYTHON=
set /P INPUT=Type input: %=%
set /p PPYTHON=Where is your ppython: %=%
%PPYTHON% main.py %INPUT%
