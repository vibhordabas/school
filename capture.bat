@echo off
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c_%%a_%%b)
REM For /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set schoolname=SMPS
echo %mydate%_%schoolname%
for %%a in (1) do (ffmpeg -y -t 5 -sample_rate 30 -f dshow -i video="Integrated Webcam" "C:\Users\vidabas\Desktop\Cloud\Notes\ffmpeg\%schoolname%_%mydate%.mp4")  
REM here -t 5 means record video from webcam for 5 seconds.-y overwrites.

for %%a in (C:\Users\vidabas\Desktop\Cloud\Notes\ffmpeg\%schoolname%_%mydate%.mp4) do ffmpeg -y -i %%a -r 2 -s 2560x1440 -f image2 "C:\Users\vidabas\Desktop\Cloud\Notes\ffmpeg\%schoolname%_%mydate%_%%04d.jpg" 
REM here -r 3 means a rate of 3 frames 

echo conversion complete
REM pause




