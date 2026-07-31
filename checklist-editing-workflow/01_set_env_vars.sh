#!/usr/bin/env bash
# Script to set environment variables for FAIR4AI form automation in WSL/Linux
# This will add variables to ~/.bashrc for persistence across sessions
# Run this script with: source ./01_set_env_vars.sh

echo "Setting environment variables for current session..."

# Set environment variables (edit these or export them before sourcing this file)
export FORM_ID="${FORM_ID:-YOUR_FORM_ID_HERE}"
export CREDS_PATH="${CREDS_PATH:-/path/to/your/credentials.json}"

echo "✓ FORM_ID set to: $FORM_ID"
echo "✓ CREDS_PATH set to: $CREDS_PATH"

# NOTE: This script intentionally does not modify ~/.bashrc.
# If you want these values to persist across sessions, add the exports to your shell profile manually (e.g., ~/.bashrc, ~/.zshrc).
# Example:
#   export FORM_ID="..."
#   export CREDS_PATH="..."

echo ""
echo "Environment variables set successfully!"
echo "Note: Run this script with 'source ./01_set_env_vars.sh' to apply to current session"
