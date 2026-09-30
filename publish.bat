@echo off
REM Double-click to publish the dashboard: runs every check, shows what changed, then asks before it
REM commits and pushes to GitHub (Streamlit Cloud redeploys from main). Nothing is pushed unless
REM every check passes and you answer y.   Checks only:  publish.bat --dry-run
cd /d "%~dp0"
"C:\ProgramData\anaconda3\python.exe" publish.py %*
pause
