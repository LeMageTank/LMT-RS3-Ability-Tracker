@echo on
set activatevenv="%~dp0ability-tracker\Scripts\activate.bat"
%activatevenv% && pip install ahk && pip install pynput && pip install pyautogui && pip install pillow && pip install numpy