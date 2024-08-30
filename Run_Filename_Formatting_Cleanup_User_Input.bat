@echo off
setlocal

REM Use PowerShell to open a folder selection dialog
for /f "tokens=*" %%i in ('powershell -command "Add-Type -AssemblyName System.Windows.Forms; $fbd = New-Object System.Windows.Forms.FolderBrowserDialog; $fbd.ShowDialog() | Out-Null; $fbd.SelectedPath"') do set folder_path=%%i

REM Run the Python script with the selected folder path
pythonw "A:\OneDrive\Documents\Python_Scripts_Running_in_Windows\Filename_Formating_Cleanup\Filename_Formatting_Cleanup.py" "%folder_path%"

endlocal
