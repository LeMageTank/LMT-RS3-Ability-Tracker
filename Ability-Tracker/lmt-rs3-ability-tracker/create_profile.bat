@echo off
set activatevenv="%~dp0ability-tracker\Scripts\activate.bat"
set startscript="%~dp0ability-tracker\Scripts\profile_creator.py"
%activatevenv% && %startscript% && pause