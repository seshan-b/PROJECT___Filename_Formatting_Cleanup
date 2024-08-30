# Filename Formatting

## Make your file name look like Book Titles


To run this:
- You need Python installed.
- No need to run it from the command line you can run a .bat file that ask you which folder you want to modify
- You also have a .bat file where you can edit link directly. 



```bash
@echo off
REM Change directory to the location of your Python script
cd /d "Your file path"

REM Run the Python script in the background using pythonw
pythonw Filename_Formatting_Cleanup.py "Your file path"

REM To kill the created python tasks
REM taskkill /f /im pythonw.exe
```

Still having problems shoot me a message. 