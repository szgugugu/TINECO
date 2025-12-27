@echo off
echo Building System Monitor with new packaging approach...

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

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "release" rmdir /s /q release

REM Build launcher only
echo Building launcher with PyInstaller...
pyinstaller --onefile --windowed %ICON_OPTION% --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=requests --hidden-import=webbrowser --name=SystemMonitorLauncher backend_launcher.py

if %ERRORLEVEL% NEQ 0 (
    echo Launcher build failed!
    pause
    exit /b 1
)

REM Create release directory structure
echo Creating release directory...
mkdir release
mkdir release\backend

REM Copy backend files
echo Copying backend files...
xcopy /E /I /Y backend release\backend

REM Copy launcher exe
echo Copying launcher exe...
copy /Y dist\SystemMonitorLauncher.exe release\

REM Create README
echo Creating README...
echo System Monitor Launcher > release\README.txt
echo. >> release\README.txt
echo Usage: >> release\README.txt
echo 1. Run SystemMonitorLauncher.exe >> release\README.txt
echo 2. The launcher will start the backend server automatically >> release\README.txt
echo 3. Access the system monitor at http://localhost:8000 >> release\README.txt
echo. >> release\README.txt
echo Directory Structure: >> release\README.txt
echo release\ >> release\README.txt
echo   - SystemMonitorLauncher.exe >> release\README.txt
echo   - backend\ [backend files] >> release\README.txt

echo.
echo Build complete!
echo Release directory: release\
echo.
echo Directory structure:
echo release\
echo   - SystemMonitorLauncher.exe
echo   - backend\
echo     - [backend files]
echo   - README.txt
echo.
echo You can now distribute the entire 'release' folder to users.
pause