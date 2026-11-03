@echo off
setlocal
cd /d %~dp0..
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
if not exist .env copy .env.example .env
echo Setup complete. Configure .env, then run scripts\run_smerka.bat
