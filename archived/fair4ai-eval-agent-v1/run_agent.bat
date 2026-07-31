@echo off
REM Batch script to run FAIR4AI agent on Windows

echo ======================================================================
echo FAIR4AI Evaluation Agent
echo ======================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if API key is set
if "%OPENAI_API_KEY%"=="" if "%ANTHROPIC_API_KEY%"=="" (
    echo ERROR: No API key found!
    echo Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable
    echo.
    echo Example:
    echo   set OPENAI_API_KEY=your-key-here
    echo.
    pause
    exit /b 1
)

REM Run the agent with metadata files
echo Running evaluation...
echo.

python fair4ai_agent.py --metadata metadata_downloads\*.json --output evaluation_results

echo.
echo ======================================================================
echo Done! Check evaluation_results.json and evaluation_results.csv
echo ======================================================================
pause
