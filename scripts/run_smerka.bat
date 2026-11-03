@echo off
setlocal
cd /d %~dp0..
start "SMERKA Service" cmd /k "call .venv\Scripts\activate.bat && python -m smerka_service"
cd desktop
cargo run
