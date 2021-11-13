@echo off
set LANGUAGE=en
set USER=
set /P USER=Username: %=%
if not exist "server/data/blobs/%USER%.blob" (
    echo Creating user: %USER%...
    echo. 2>"server/data/blobs/%USER%.blob"
)
if not exist "server/data/toons" (
    echo Creating 'toons' directory...
    mkdir "server/data/toons"
)
if not exist "logs" (
    mkdir "logs"
)
echo ===============================
echo Launching localhost client with debugging...
echo Language: %LANGUAGE%
echo User: %USER%
echo ===============================
ppython main.py -svaddr localhost -l %LANGUAGE% -d -u %USER%
echo Client ended...
pause