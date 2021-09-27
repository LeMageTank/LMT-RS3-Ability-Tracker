@echo off
>> logs.txt (
echo Installing packages
set activatevenv="%~dp0ability-tracker\Scripts\activate.bat"
echo %activatevenv% && pip install ahk && pip install pynput && pip install pyautogui && pip install pillow && pip install numpy
echo \Installing packages
)