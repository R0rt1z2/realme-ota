@echo off

setlocal
chcp 65001 2>nul >nul

:: Location should be where the main.py file is located
:: This will be automatically updated via Install script
cd "C:\Program Files\Python*\Scripts\realme_ota\realme_ota" 2>nul >nul

if exist main.py (
    python main.py %*
) else (
    powershell write-host -fore Red realme-ota not found!
)

pause
