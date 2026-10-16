@echo off
setlocal
title ZIZIPHUS JUJUBA - Signal Intelligence Lab
cd /d "D:\Projects\ZIZIPHUS_JUJUBA"

if exist "C:\Python314\python.exe" (
    "C:\Python314\python.exe" run_app.py
) else (
    python run_app.py
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Could not start application.
    pause
)
