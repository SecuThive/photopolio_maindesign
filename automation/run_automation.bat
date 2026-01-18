@echo off
REM Automated Design Upload Script for Windows

REM Change to automation directory
cd /d "%~dp0"

REM Activate virtual environment (if using)
REM call venv\Scripts\activate

REM Run the Python script with random category
set categories=Landing Page Dashboard E-commerce Portfolio Blog
for /f "tokens=%random% delims= " %%a in ("%categories%") do set category=%%a

echo Running automated design upload for category: %category%
python upload_design.py --category "%category%"

REM Log the execution
echo [%date% %time%] Design upload completed for %category% >> automation.log
