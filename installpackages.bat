@echo off
set activatevenv="%~dp0ability-tracker\Scripts\activate.bat"
set pip="%~dp0ability-tracker\Scripts\python.exe -m pip"
echo %activatevenv% && pip install ahk && pip install pynput && pip install pyautogui && pip install pillow && pip install numpy
