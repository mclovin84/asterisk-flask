# Auto-push script for GitHub
param(
    [string]$CommitMessage = "Auto-update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
)

Write-Host "🔄 Auto-pushing changes to GitHub..." -ForegroundColor Green

# Add all changes
git add .

# Commit with timestamp
git commit -m $CommitMessage

# Push to GitHub
git push origin main

Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
Write-Host "📝 Commit message: $CommitMessage" -ForegroundColor Yellow 