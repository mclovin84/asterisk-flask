@echo off
echo 🚀 Pushing to GitHub...
git add .
git commit -m "Auto-update: %date% %time%"
git push origin main
echo ✅ Done! 