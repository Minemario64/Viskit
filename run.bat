@echo off
python ipLog.py
python -u mescPy/splitConsole.py run-frontend.bat run-backend.bat
call oneup.bat