#!/usr/bin/env bash
# Template script to set environment variables for FAIR4AI form automation in WSL/Linux
#
# INSTRUCTIONS:
# 1. Copy this file to 01_set_env_vars.sh
# 2. Replace the placeholder values below with your actual values
# 3. Run the script with: source ./01_set_env_vars.sh
#
# This will add variables to ~/.bashrc for persistence across sessions

echo "Setting environment variables for current session..."

# Set environment variables
# Replace with your Google Form ID from: https://docs.google.com/forms/d/YOUR_FORM_ID/edit
export FORM_ID="YOUR_FORM_ID_HERE"

# Replace with the path to your service account JSON key file
# For WSL, Windows paths are accessible via /mnt/c/... 
# Example: /mnt/c/Users/YourName/Documents/your-service-account-key.json
export CREDS_PATH="YOUR_CREDENTIALS_PATH_HERE"

echo "✓ FORM_ID set to: $FORM_ID"
echo "✓ CREDS_PATH set to: $CREDS_PATH"

# Add to ~/.bashrc for persistence if not already present
if ! grep -q "# FAIR4AI environment variables" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# FAIR4AI environment variables" >> ~/.bashrc
    echo "export FORM_ID=\"YOUR_FORM_ID_HERE\"" >> ~/.bashrc
    echo "export CREDS_PATH=\"YOUR_CREDENTIALS_PATH_HERE\"" >> ~/.bashrc
    echo ""
    echo "✓ Environment variables added to ~/.bashrc for persistence"
    echo "  These will be available in all future bash sessions"
    echo ""
    echo "⚠ IMPORTANT: Edit ~/.bashrc and replace the placeholder values!"
else
    echo ""
    echo "⚠ Environment variables already exist in ~/.bashrc"
    echo "  If you need to update them, edit ~/.bashrc manually"
fi

echo ""
echo "Environment variables set successfully!"
echo "Note: Run this script with 'source ./01_set_env_vars.sh' to apply to current session"
