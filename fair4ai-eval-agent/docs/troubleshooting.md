# Troubleshooting

This file addresses common issues one may encounter while using this package.

## Installation Issues

**Error: "ModuleNotFoundError: No module named 'openai'"**
- Solution: Install dependencies
  ```bash
  pip install -r requirements_agent.txt
  # or
  pip install openai pandas requests beautifulsoup4
  ```

**Error: "No module named 'tkinter'" (Linux)**
- Solution: Install tkinter
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  # Fedora
  sudo dnf install python3-tkinter
  ```

## API Key Issues

**Error: "OPENAI_API_KEY environment variable not set"**
- Solution: Set your API key
  ```powershell
  $env:OPENAI_API_KEY="sk-your-key-here"
  ```
- Make sure to set it in the same terminal session before running

**Error: "Incorrect API key provided"**
- Solution: Verify your API key is correct
- Check for extra spaces or quotes
- Get a new key from the provider's console

**Error: "You exceeded your current quota"**
- Solution: Add credits to your account or check billing settings
- OpenAI: https://platform.openai.com/account/billing
- Anthropic: https://console.anthropic.com/settings/billing

## URL Extraction Issues

**Error: "No metadata found at URL"**
- Solution: 
  - Verify URL is accessible in browser
  - Check if page has structured metadata (View Page Source → search for "json-ld")
  - Try downloading metadata files manually and use `--metadata` instead
  - Some sites block automated scraping

**Error: "Invalid URL format"**
- Solution: URL must start with `http://` or `https://`

## File Issues

**Error: "No metadata files found"**
- Solution: 
  - Check files are in correct directory
  - Use absolute paths or wildcards: `--metadata c:/path/to/*.json`
  - Verify files are valid JSON format

**Error: "Permission denied" when creating folder**
- Solution:
  - Choose directory with write permissions
  - Run as administrator (if needed)
  - Check available disk space

## Processing Issues

**Error: "JSON parse error" from LLM**
- Solution: Rare formatting issue - try running again
- The LLM sometimes returns invalid JSON; retry usually succeeds

**Error: "Rate limit exceeded"**
- Solution:
  - Wait a moment and retry
  - Reduce concurrent requests
  - Upgrade API tier if frequent

**Partial results after error**
- The agent saves progress - check output files for partial results
- Review log for specific question that failed
- Can manually fix or re-run failed sections

# GUI Issues

**GUI doesn't open**
- Solution: Run from command line to see error messages
  ```bash
  python fair4ai_agent_ui.py
  ```
- Check tkinter is installed (see Installation Issues above)

**"Browse" button doesn't work**
- Solution: Ensure you have file dialog support
- Try using command-line interface instead
