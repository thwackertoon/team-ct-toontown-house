@echo off
rem This should now run both Blob and Server...
echo Launching Server...
start cmd.exe /k "blob.bat"
cd server
ppython server.py -lc
pause