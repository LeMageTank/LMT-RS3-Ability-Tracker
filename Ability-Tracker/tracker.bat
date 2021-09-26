@echo off
set activatevenv="%~dp0app\Scripts\activate.bat"
set startscript="%~dp0app\Scripts\main.py"
%activatevenv% && %startscript%