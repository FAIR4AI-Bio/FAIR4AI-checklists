# Template script to set permanent environment variables for FAIR4AI form automation
# 
# INSTRUCTIONS:
# 1. Copy this file to set_env_vars.ps1
# 2. Replace the placeholder values below with your actual values
# 3. Run the script with: .\set_env_vars.ps1
#
# These variables will persist across all PowerShell sessions

Write-Host "Setting permanent environment variables..." -ForegroundColor Cyan

# Set FORM_ID - Replace with your Google Form ID
# Find this in your form URL: https://docs.google.com/forms/d/YOUR_FORM_ID/edit
[System.Environment]::SetEnvironmentVariable('FORM_ID', 'YOUR_FORM_ID_HERE', 'User')
Write-Host "✓ FORM_ID set" -ForegroundColor Green

# Set CREDS_PATH - Replace with the full path to your service account JSON key file
# Example: C:\Users\YourName\Documents\your-service-account-key.json
[System.Environment]::SetEnvironmentVariable('CREDS_PATH', 'YOUR_CREDENTIALS_PATH_HERE', 'User')
Write-Host "✓ CREDS_PATH set" -ForegroundColor Green

Write-Host "`nEnvironment variables have been set permanently." -ForegroundColor Green
Write-Host "Please restart your terminal or open a new PowerShell window for changes to take effect." -ForegroundColor Yellow

# Display current values in this session
$env:FORM_ID = 'YOUR_FORM_ID_HERE'
$env:CREDS_PATH = 'YOUR_CREDENTIALS_PATH_HERE'

Write-Host "`nCurrent session values:" -ForegroundColor Cyan
Write-Host "FORM_ID: $env:FORM_ID"
Write-Host "CREDS_PATH: $env:CREDS_PATH"
