@echo off
echo Building backend launcher (launcher only)...

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found, please run setup_venv.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if icon file exists
set ICON_OPTION=
if exist "icon.ico" (
    set ICON_OPTION=--icon=icon.ico
)

REM Use PyInstaller to package only the launcher, not including backend directory
echo Packaging launcher with PyInstaller...
pyinstaller --onefile --windowed %ICON_OPTION% --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=requests --hidden-import=webbrowser --name=SystemMonitorLauncher backend_launcher.py

if %ERRORLEVEL% NEQ 0 (
    echo Packaging failed!
    pause
    exit /b 1
)

echo Packaging complete!
echo Executable location: dist\SystemMonitorLauncher.exe
echo.
echo Note: Please ensure the backend folder is in the same directory as the exe file
pause