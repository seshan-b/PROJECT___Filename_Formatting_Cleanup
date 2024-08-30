@echo off
REM Change directory to the location of your Python script
cd /d "A:\OneDrive\Documents\Python_Scripts_Running_in_Windows\Filename_Formating_Cleanup"

REM Run the Python script in the background using pythonw
pythonw Filename_Formatting_Cleanup.py "A:\OneDrive\Downloads"

REM To kill the created python tasks
REM taskkill /f /im pythonw.exe
