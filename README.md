# Pokemon Macro - Automated Shiny/Gradient Hunter

An automated OCR-powered macro for Alpha Modded that helps you hunt for Shiny, Gradient, and Reskin Pokemon by automatically soft resetting eggs.

## Overview

This program automates the process of:
1. Rejoining the game
2. Executing a sequence of clicks to navigate through the UI
3. Monitoring the chat window for specific keywords (your username + Shiny/Gradient/Reskin Pokemon names)
4. Automatically stopping when a match is found and saving the game

The macro uses OCR (Optical Character Recognition) to read text from the chat window and pixel color detection to wait for specific UI elements to appear.

## Features

- **OCR-powered detection**: Automatically reads chat messages to detect when you've obtained a Shiny, Gradient, or Reskin Pokemon
- **Automated clicking**: Executes a sequence of clicks to rejoin and navigate the game
- **Pixel color detection**: Waits for specific UI elements to appear before proceeding
- **Configurable matching modes**: Hunt for specific types (Shiny, Gradient, Reskin) or any combination
- **Cross-platform support**: Works on both macOS and Windows
- **YAML configuration**: Easy to customize via `configs.yaml` file
- **Logging**: Automatically logs detected chat messages to `history.log`

## Requirements

- Python 3.10 or higher
- macOS or Windows
- Tesseract OCR installed on your system
- Roblox game window visible and accessible
- Accessibility permissions granted (for automation on macOS)
- Windows users: `pywinauto` package (optional, for better window handling)

### Installing Tesseract OCR

**On macOS:**
```bash
brew install tesseract
```

**On Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## Installation

1. Clone or download this repository

2. Create a virtual environment (recommended):

```bash
python3 -m venv ENV
source ENV/bin/activate  # On Windows: ENV\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional) Install as a package:

```bash
pip install -e .
```

## Configuration

**You MUST configure the program before use**

All configuration is done in `configs.yaml` at the root of the project. The default values are examples and will likely not work for your setup.

### Configuration File Structure

The `configs.yaml` file contains the following sections:

```yaml
# Your username (display name)
Username: "YourUsername"

# Pokemon wishlist
Wishlist:
  Reskins:
    - "Whiteout"
    - "Phantom"
    - "Glitch"
  Gradients:
    - "Gaia"
    - "Chronos"
    - "Nereus"
    # ... more gradients

# UI element positions
Positions:
  EggManPosition: [675, 739]
  EventButton: [1418, 965]
  DialogueYES: [1170, 405]
  QuickRejoinSprite: [1475, 850]
  QuickRejoinButton: [1000, 580]
  MenuButton: [43, 451]
  SaveButton: [70, 735]

# Chat window region for OCR
ChatWindow:
  LeftCorner: [13, 136]
  RightCorner: [440, 354]

# Matching mode flags
IsReskin: false
IsShiny: false
IsGradient: false
IsAny: false
IsGood: false
```

### 1. Username Configuration

Set your Roblox username:

```yaml
Username: "YourUsername"
```

### 2. Wishlist Configuration

Configure which Pokemon variants you want to hunt for:

```yaml
Wishlist:
  Reskins:
    - "Whiteout"
    - "Phantom"
    - "Glitch"
  Gradients:
    - "Gaia"
    - "Chronos"
    - "Nereus"
    # Add more as needed
```

**What to change**: Add or remove Pokemon names from the Reskins and Gradients lists based on what you're hunting for.

### 3. Positions Configuration

All UI element positions need to be configured for your screen resolution:

```yaml
Positions:
  EggManPosition: [675, 739]        # Position of the Egg NPC
  EventButton: [1418, 965]          # Event button position
  DialogueYES: [1170, 405]          # "YES" button in dialogue
  QuickRejoinSprite: [1475, 850]    # Quick rejoin sprite position
  QuickRejoinButton: [1000, 580]    # Quick rejoin confirmation button
  MenuButton: [43, 451]              # Menu button (must be on white text)
  SaveButton: [70, 735]              # Save button position
```

**What to change**: 
- Update all `[x, y]` coordinates to match your screen resolution and game UI
- Use a tool like `MouseInfo` (included with PyAutoGUI) or screenshot tools to find coordinates
- **Important**: `EggManPosition` may need to be updated frequently as it can change
- `MenuButton` must be positioned on white text for pixel detection to work

### 4. Chat Window Configuration

Define the region where the chat window appears:

```yaml
ChatWindow:
  LeftCorner: [13, 136]    # Top-left corner of chat window
  RightCorner: [440, 354]  # Bottom-right corner of chat window
```

**What to change**: Adjust these coordinates to match your chat window position and size. The macro will capture the region between these two corners for OCR.

### 5. Matching Mode Configuration

Control what the macro should detect:

```yaml
IsReskin: false    # Only match Reskins from wishlist
IsShiny: false     # Only match Shiny Pokemon
IsGradient: false  # Only match Gradients from wishlist
IsAny: false       # Match any Reskin or Gradient from wishlist
IsGood: false      # Match "good" combinations (Reskin+Gradient or Shiny+Gradient)
```

**Matching modes explained**:
- `IsAny: true`: Matches any Pokemon in your Reskins or Gradients wishlist
- `IsReskin: true`: Only matches Reskins from your wishlist
- `IsShiny: true`: Only matches Shiny Pokemon
- `IsGradient: true`: Only matches Gradients from your wishlist
- `IsGood: true`: Matches "good" combinations (Reskin+Gradient or Shiny+Gradient)
- **Note**: Only one flag should be `true` at a time

**Example configurations**:

Hunt for any Shiny:
```yaml
IsShiny: true
IsAny: false
IsReskin: false
IsGradient: false
IsGood: false
```

Hunt for any Reskin or Gradient from wishlist:
```yaml
IsAny: true
IsShiny: false
IsReskin: false
IsGradient: false
IsGood: false
```

Hunt for "good" combinations:
```yaml
IsGood: true
IsAny: false
IsShiny: false
IsReskin: false
IsGradient: false
```

## Usage

1. **Grant Accessibility Permissions** (macOS):
   - Go to System Settings → Privacy & Security → Accessibility
   - Add Terminal (or your Python IDE) to the allowed apps

2. **Position your game window**:
   - Make sure Roblox is visible and the chat window is in the configured region
   - The game should be ready to be rejoined

3. **Run the macro**:

```bash
python -m src.auto_resetter.main
```

Or if installed as a package:

```bash
pokemon-macro
```

4. **Stop the macro**:
   - Move your mouse to the top-left corner of the screen (PyAutoGUI failsafe)
   - Or press Ctrl+C in the terminal

## How It Works

1. **Initialization**: The macro waits for the initial delay (3 seconds by default), then starts the loop

2. **Click Sequence**: Executes the configured click sequence to:
   - Click on the main screen
   - Wait for the Pokemon loading screen (yellow text detection)
   - Select the save slot (green card detection)
   - Navigate to the Egg NPC
   - Click through dialogue (including right-click on Egg NPC)
   - Focus on the chat window

3. **OCR Detection**: 
   - Captures the chat window region
   - Uses OCR to extract text
   - Processes text:
     - Removes "Chronos Event 2025 is out" phrases
     - Trims text from username to "attempts" keyword

4. **Keyword Matching**: 
   - Checks if your username appears in the text
   - Logs to `history.log` if username is detected
   - Matches against configured wishlist and matching mode

5. **Match Found**: 
   - Clicks dialogue YES button 3 times (to clear additional dialogue)
   - Opens menu
   - Saves the game
   - Clicks YES to confirm save
   - Stops the macro

6. **No Match**: 
   - Clicks quick rejoin sprite
   - Clicks quick rejoin confirmation button
   - Waits for delay between iterations
   - Repeats the process

## Logging

When the macro detects your username in the chat, it automatically logs the detected text to `history.log` in the project root. This helps you track what the OCR is detecting and debug any issues.

## Troubleshooting

### OCR not detecting text
- Ensure the chat window region is correctly configured in `configs.yaml`
- Make sure the chat window is visible and not obscured
- Check that Tesseract OCR is properly installed
- Try adjusting the `ChatWindow` coordinates to capture more of the chat
- Check `history.log` to see what text is being detected

### Clicks not working
- Verify all positions in `configs.yaml` are correct for your screen resolution
- Check that Accessibility permissions are granted (macOS)
- Ensure the game window is in the foreground
- On Windows, ensure `pywinauto` is installed if you want better window handling

### Pixel color detection timing out
- The click sequence includes pixel color detection for UI elements
- If timeouts occur, the game UI may have changed colors
- Check the terminal for timeout messages showing which pixel/color failed

### Macro stops unexpectedly
- Check the terminal for error messages
- Verify all coordinates in `configs.yaml` are within your screen bounds
- Ensure the game hasn't changed its UI layout
- Check `history.log` to see if OCR is working correctly

### Wrong Pokemon detected
- Verify your matching mode flags in `configs.yaml`
- Check that your wishlist contains the correct Pokemon names
- Ensure your username is correctly set
- Review `history.log` to see what text OCR is detecting

## Safety Features

- **Failsafe**: Move mouse to top-left corner to stop the macro immediately
- **Timeout protection**: Pixel color detection has timeouts to prevent infinite waiting
- **Error handling**: OCR errors are caught and handled gracefully
- **Logging**: All username detections are logged for debugging

## Project Structure

```
Pokemon-Macro/
├── configs.yaml              # Main configuration file
├── history.log               # OCR detection log
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Package configuration
├── src/
│   └── auto_resetter/
│       ├── main.py           # Entry point
│       ├── macro_runner.py   # Main macro logic
│       ├── macro_config.py   # Configuration loading
│       ├── click_executor.py # Click sequence execution
│       ├── platform_clicker.py # Platform-specific clicking
│       ├── img_funcs.py      # OCR and image processing
│       └── pixel_utils.py    # Pixel color detection
└── README.md
```

## Notes

- This macro supports both macOS and Windows
- Screen coordinates are absolute and depend on your screen resolution
- The macro assumes a specific game UI layout - you may need to adjust if the game updates
- Always test the macro in a safe environment before using it for extended periods
- The `EggManPosition` may need frequent updates as it can change

## License

MIT License

## Author

Manta
