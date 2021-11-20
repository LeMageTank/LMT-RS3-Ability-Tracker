@echo off
set activatevenv="%~dp0ability-tracker\Scripts\activate.bat"
set pythonpath="%~dp0ability-tracker\Scripts\python.exe"
set mainscript="%~dp0ability-tracker\tracker\main.py"
%activatevenv% && %pythonpath% %mainscript% & exit

