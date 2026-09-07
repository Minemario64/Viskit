@echo off
call "C:\Program Files\Microsoft OneDrive\OneDrive.exe" /shutdown
cd api
call python -u main.py