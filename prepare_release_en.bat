@echo off
echo Preparing release directory...

REM Create release directory
if not exist "release" mkdir release
if not exist "release\backend" mkdir release\backend

REM Copy backend directory contents to release directory
echo [INFO] Copying backend directory contents...
xcopy /E /I /Y backend release\backend

REM Copy packaged exe file to release directory
echo [INFO] Copying packaged exe file...
copy /Y dist\SystemMonitorLauncher.exe release\

REM Copy README file if it exists
if exist "README.txt" (
    echo [INFO] Copying README file...
    copy /Y README.txt release\
)

REM Create a simple README if it doesn't exist
if not exist "release\README.txt" (
    echo [INFO] Creating README file...
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
)

echo [INFO] Release directory prepared!
echo [INFO] Release directory location: release\
echo.
echo [INFO] Directory structure:
echo release\
echo   - SystemMonitorLauncher.exe
echo   - backend\
echo     - [backend files]
echo   - README.txt
pause