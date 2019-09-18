echo off
set n=2
rem set /p n= Number? 
TASKKILL /F /IM wechat.exe > nul
for /L %%i in (1,1,%n%) do (
start "" "C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"
)
