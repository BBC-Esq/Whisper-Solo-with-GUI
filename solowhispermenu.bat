@echo off
for /f "tokens=* delims=" %%a in ('where solowhispermenu.py') do set "script_path=%%a"
if not defined script_path (
    echo solomenu2.py not found in the system path. Please check the system path configuration.
    exit /b 1
)
python "%script_path%" "large-v2" "%~1" "vtt"
