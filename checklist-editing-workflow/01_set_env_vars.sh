#!/usr/bin/env bash
# Script to set environment variables for FAIR4AI form automation in WSL/Linux
# This will add variables to ~/.bashrc for persistence across sessions
# Run this script with: source ./01_set_env_vars.sh

echo "Setting environment variables for current session..."

# Set environment variables
export FORM_ID="1gz570yBe2zDJFI__iIhLkWjK69Yy7KIkmVYiWYTQMLw"
export CREDS_PATH="/mnt/c/Users/esokol/OneDrive - Battelle Ecology/Documents/MY_KEYES/fair4ai-f47a43a6a4df.json"

echo "âœ“ FORM_ID set to: $FORM_ID"
echo "âœ“ CREDS_PATH set to: $CREDS_PATH"

# Add to ~/.bashrc for persistence if not already present
if ! grep -q "# FAIR4AI environment variables" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# FAIR4AI environment variables" >> ~/.bashrc
    echo "export FORM_ID=\"1gz570yBe2zDJFI__iIhLkWjK69Yy7KIkmVYiWYTQMLw\"" >> ~/.bashrc
    echo "export CREDS_PATH=\"/mnt/c/Users/esokol/OneDrive - Battelle Ecology/Documents/MY_KEYES/fair4ai-f47a43a6a4df.json\"" >> ~/.bashrc
    echo ""
    echo "âœ“ Environment variables added to ~/.bashrc for persistence"
    echo "  These will be available in all future bash sessions"
else
    echo ""
    echo "âš  Environment variables already exist in ~/.bashrc"
    echo "  If you need to update them, edit ~/.bashrc manually"
fi

echo ""
echo "Environment variables set successfully!"
echo "Note: Run this script with 'source ./01_set_env_vars.sh' to apply to current session"
