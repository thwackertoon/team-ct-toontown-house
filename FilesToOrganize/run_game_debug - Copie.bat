@echo off
rem Easier to launch client...
rem -Sheriff

echo Launching localhost client...
echo ===============================
ppython main.py -svaddr localhost -le
echo ===============================
echo Client ended...
pause