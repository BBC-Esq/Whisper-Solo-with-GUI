@echo off

setlocal enabledelayedexpansion

set "model=%~1"
set "audio_file=%~2"
set "output_format=%~3"
set "task_flag=%~4"
set "source_language_flag=%~5"

echo Checking if Whisper is installed...
where "whisper.exe" >nul
if not errorlevel 1 (
    echo Whisper is installed.
) else (
    echo "Unable to run. Whisper might not be installed, in the system PATH, the user does not have sufficient permissions to access the file system, or another reason. Exiting..."
    pause >nul
    exit /b 1
)

set "log_error=false"

set /a "total_files=1"
set /a "processed_files=0"
set /a "skipped_files=0"

set "start_time=%time%"

if not "!task_flag!"=="" (
    set "task_flag=!task_flag!"
)

if not "!source_language_flag!"=="" (
    set "source_language_flag=!source_language_flag!"
)

set "whisper_command=whisper "!audio_file!" --model !model! --output_format !output_format! !task_flag! !source_language_flag!"

echo Running command: !whisper_command!
cmd /c "!whisper_command!" 2> nul

if errorlevel 1 (
    echo Error: Failed to process "!audio_file!" using the whisper command.
    set /a "skipped_files+=1"
    set "log_error=true"
) else (
    echo Successfully processed "!audio_file!".
)

if %log_error%==true (
    set "hour=%time:~0,2%"
    if "%hour:~0,1%"==" " set "hour=0%hour:~1,1%"
    set "log_file=log_%date:~10,4%%date:~4,2%%date:~7,2%_%hour%%time:~3,2%%time:~6,2%.txt"
    echo Script started: %date% %time% > "%log_file%"
    echo Total files: %total_files% >> "%log_file%"
    echo Skipped files: %skipped_files% >> "%log_file%"
    type "%log_file%" | findstr /C:"Error: Failed"
    echo There were errors during processing. Check the log file for details.
)

goto :eof
