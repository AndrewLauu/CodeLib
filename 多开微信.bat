echo off

set /p n= Number?
rem echo %n%
TASKKILL /F /IM wechat.exe
for /L %%i in (1,1,%n%) do (
start "" "C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"
)
pause
