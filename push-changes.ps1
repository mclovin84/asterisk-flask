# Quick push script
param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

Write-Host "🚀 Pushing changes: $Message" -ForegroundColor Cyan

git add .
git commit -m $Message
git push origin main

Write-Host "✅ Pushed successfully!" -ForegroundColor Green 