@echo off
set activatevenv="%~dp0app\Scripts\activate.bat"
set startscript="%~dp0app\Scripts\profile_creator.py"
%activatevenv% && %startscript% && pause