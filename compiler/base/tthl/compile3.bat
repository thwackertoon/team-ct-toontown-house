@echo off
cd ..\..
python tthc.py --noprcdata --nomkdata %1
cd base\tthl
echo Compile
call compile
echo Copy
copy ToontownHouse_dev.exe ..\TTH_dev.exe
cd..
TTH_dev -u nacib -51
cd tthl