@echo off

:create_profile
echo Create profile >> logs.txt
set activatevenv="%~dp0ability-tracker\Scripts\activate.bat"
set startscript="%~dp0ability-tracker\Scripts\profile_creator.py"
%activatevenv% && %startscript% >> logs.txt

