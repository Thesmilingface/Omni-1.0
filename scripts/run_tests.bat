@echo off
setlocal
cd /d %~dp0..
call .venv\Scripts\activate.bat
python -m pytest
if errorlevel 1 exit /b 1
cd desktop
cargo test
