@echo off
echo Compile
call compile
echo Copy
copy ToontownHouse_dev.exe ..\TTH_dev.exe
cd..
TTH_dev %1
cd tthl