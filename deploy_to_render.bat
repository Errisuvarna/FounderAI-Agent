@echo off
REM Quick deployment script for Render

echo ============================================================
echo   FounderAI - Render Deployment Script
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

echo Step 1: Running deployment readiness check...
echo ------------------------------------------------------------
python check_deployment_ready.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Deployment readiness check failed!
    echo Please fix the issues above and try again.
    pause
    exit /b 1
)

echo.
echo Step 2: Checking Git status...
echo ------------------------------------------------------------
git status

echo.
echo Step 3: Ready to commit and push to GitHub
echo ------------------------------------------------------------
echo.
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Add Render deployment configuration

echo.
echo Committing with message: %COMMIT_MSG%
git add .
git commit -m "%COMMIT_MSG%"

echo.
echo Pushing to GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo   SUCCESS! Code pushed to GitHub
    echo ============================================================
    echo.
    echo Next steps:
    echo 1. Go to https://dashboard.render.com/
    echo 2. Click "New +" -^> "Blueprint"
    echo 3. Select your GitHub repository
    echo 4. Click "Apply"
    echo 5. Set environment variables ^(see QUICK_START.md^)
    echo.
    echo For detailed instructions, see DEPLOYMENT.md
    echo ============================================================
) else (
    echo.
    echo ERROR: Failed to push to GitHub
    echo Please check your Git configuration and try again.
)

echo.
pause
