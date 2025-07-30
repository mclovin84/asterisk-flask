@echo off
echo 🚀 Quick Deploy - Asterisk + Flask
echo.

REM Check if SSH key exists
if not exist "newSSH" (
    echo ❌ SSH key 'newSSH' not found!
    echo Please make sure your SSH key is in the current directory
    pause
    exit /b 1
)

REM Make deploy script executable and run it
echo 📁 Deploying to droplet...
bash deploy.sh 147.182.184.153

echo.
echo ✅ Deployment complete!
echo 📞 Test by calling +1 480 786 8280
echo 🌐 Web app: http://147.182.184.153:5000
echo.
pause 