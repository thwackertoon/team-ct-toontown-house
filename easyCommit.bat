@echo off
set INPUT=
set /P INPUT=Commit message: %=%

echo Adding...
git add *
echo Committing..
git commit -m "%INPUT%"
echo Pushing...
git push origin master

pause