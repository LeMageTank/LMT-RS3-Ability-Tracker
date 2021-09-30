@echo off
set activatevenv="%~dp0ability-tracker\Scripts\activate.bat"
set startscript="%~dp0ability-tracker\tracker\main.py"
%activatevenv% && %startscript% 

