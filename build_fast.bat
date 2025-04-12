@echo off
echo === Fast Build for Canva File Namer ===
echo.

REM Clean dist directory
if exist "dist\Canva File Namer.exe" (
    echo Removing old executable...
    del /F /Q "dist\Canva File Namer.exe" 2>nul
)

REM Make sure dist directory exists
if not exist "dist" mkdir dist

echo Building with PyInstaller (optimized mode)...
python -m PyInstaller ^
    --clean ^
    --windowed ^
    --onefile ^
    --name "Canva File Namer" ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module PIL ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module pytest ^
    --exclude-module flask ^
    --exclude-module django ^
    --exclude-module _tkinter.test ^
    file_namer.py

echo.
if exist "dist\Canva File Namer.exe" (
    echo Build successful! Executable created at:
    echo %CD%\dist\Canva File Namer.exe
    echo.
    echo You can now double-click the executable to run the application.
) else (
    echo Build failed. Please check the error messages above.
)