@echo off
For /f %%a in (C:\Users\vidabas\Desktop\Cloud\Notes\batchfile\schoolname.txt) do (set schoolname=%%a)
echo %schoolname%
pause