@echo off
for %%a in (C:\Users\vidabas\Desktop\Cloud\Notes\ffmpeg\rishabhvibhor.mp4) do ffmpeg -y -i %%a -r 3 -s 2560x1440 -f image2 "C:\Users\vidabas\Desktop\Cloud\Notes\ffmpeg\SMPS_%%04d.jpg" 
REM here -r 3 means a rate of 3 frames 
echo conversion complete
pause


