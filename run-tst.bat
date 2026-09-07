@echo off
call python ipLog.py 127.0.0.1
call python -u mescPy/splitConsole.py run-frontend-dev.bat run-backend.bat
start "" "C:\Program Files\Microsoft OneDrive\OneDrive.exe" /background
exit