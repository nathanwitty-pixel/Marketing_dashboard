@echo off
REM Double-click to launch the Denri Marketing Dashboard locally.
cd /d "%~dp0"
"C:\ProgramData\anaconda3\python.exe" -m streamlit run streamlit_app.py
pause
