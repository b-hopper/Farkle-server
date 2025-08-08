:: Place these .bat files in your repo root (same level as the /backend folder)
:: All scripts are safe to run from anywhere; they cd to the repo root first.

:: ==============================
:: setup_and_run_server.bat
:: - Creates venv if missing
:: - Installs dev requirements (falls back to prod reqs)
:: - Starts the FastAPI server with auto-reload
:: ==============================
@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"

:: Create venv if it doesn't exist
if not exist .venv (
    echo [setup] Creating virtual environment...
    py -3 -m venv .venv
)

:: Activate venv
call .venv\Scripts\activate.bat

:: Upgrade pip (quiet)
python -m pip install --upgrade pip >nul 2>&1

:: Install requirements (prefer dev requirements if present)
if exist backend\requirements-dev.txt (
    echo [setup] Installing dev requirements...
    pip install -r backend\requirements-dev.txt
) else (
    echo [setup] Installing requirements...
    pip install -r backend\requirements.txt
)

:: Default DATABASE_URL if not set
if "%DATABASE_URL%"=="" (
    set "DATABASE_URL=sqlite:///./farkle.db"
)

:: Run the server
echo [run] Starting FastAPI on http://127.0.0.1:8000 ...
uvicorn backend.main:app --reload

popd
endlocal

:: ==============================
:: run_server.bat
:: - Assumes venv and deps already installed
:: - Starts the FastAPI server with auto-reload
:: ==============================
@echo off
setlocal
pushd "%~dp0"
call .venv\Scripts\activate.bat
if "%DATABASE_URL%"=="" set "DATABASE_URL=sqlite:///./farkle.db"
echo [run] Starting FastAPI on http://127.0.0.1:8000 ...
uvicorn backend.main:app --reload
popd
endlocal

:: ==============================
:: run_tests_pytest.bat
:: - Runs pytest test suite
:: ==============================
@echo off
setlocal
pushd "%~dp0"
call .venv\Scripts\activate.bat
pytest backend/tests
popd
endlocal

:: ==============================
:: run_tests_unittest.bat
:: - Runs unittest discovery
:: ==============================
@echo off
setlocal
pushd "%~dp0"
call .venv\Scripts\activate.bat
python -m unittest discover backend/tests
popd
endlocal

:: ==============================
:: seed_dev_data.bat
:: - Seeds the local database with sample data
:: ==============================
@echo off
setlocal
pushd "%~dp0"
call .venv\Scripts\activate.bat
python -m backend.scripts.seed_dev_data
popd
endlocal
