@echo off
echo Tracker >> logs.txt
set activatevenv="%~dp0ability-tracker\Scripts\activate.bat"
set startscript="%~dp0ability-tracker\Scripts\main.py"
%activatevenv% && %startscript% 

