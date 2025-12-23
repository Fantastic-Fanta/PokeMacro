# Pokemon Macro - Automated Shiny/Gradient Hunter

An automated OCR-powered macro for Pokemon games on Roblox that helps you hunt for Shiny and Gradient Pokemon by automatically rejoining the game and monitoring chat notifications.

## Overview

This program automates the process of:
1. Rejoining the game
2. Macroing through UI
3. Monitoring the chat window for specific keywords (your username + Shiny/Gradient Pokemon name)
4. Automatically stopping when a match is found

The macro uses OCR (Optical Character Recognition) to read text from the chat window and pixel color detection to wait for specific UI elements to appear.

## Features

- **OCR-powered detection**: Automatically reads chat messages to detect when you've obtained a Shiny or Gradient Pokemon
- **Automated clicking**: Executes a sequence of clicks to rejoin and navigate the game
- **Pixel color detection**: Waits for specific UI elements to appear before proceeding
- **Configurable**: Easy to customize for your screen resolution and game setup

## Requirements

- Python 3.10 or higher
- macOS (the program uses macOS-specific libraries)
- Tesseract OCR installed on your system
- Roblox game window visible and accessible
- Accessibility permissions granted (for automation on macOS)

### Installing Tesseract OCR

On macOS, install Tesseract using Homebrew:

```bash
brew install tesseract
```

## Installation

1. Clone or download this repository

2. Create a virtual environment (recommended):

```bash
python3 -m venv ENV
source ENV/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

**You MUST configure the program before use**

All configuration is done in `src/auto_resetter/macro_config.py`. The default values are examples and will likely not work for your setup.

### 1. Screen Region Configuration

The `DEFAULT_REGION` defines the chat window area that will be monitored:

```python
DEFAULT_REGION = RegionConfig(
    x=10,        # X position of chat window (left edge)
    y=130,       # Y position of chat window (top edge)
    width=460,   # Width of chat window
    height=220,  # Height of chat window
)
```

**What to change**: Adjust these values to match your chat window position and size on your screen. You can use a tool like `MouseInfo` (included with PyAutoGUI) to find coordinates.

### 2. Click Sequence Configuration

The `DEFAULT_CLICK_SEQUENCE` defines the sequence of clicks to rejoin and navigate the game:

```python
DEFAULT_CLICK_SEQUENCE = [
    {
        "position": (745, 920),  # Click position
        "sleep": 1.5,            # Wait time after click
        "wait_for_pixel": {      # Optional: wait for pixel color
            "position": (387, 311),
            "color": (249, 239, 146),  # RGB color to wait for
            "timeout": 50.0,
        },
    },
    # ... more clicks
]
```

**What to change**:
- **All click positions**: Update `(x, y)` coordinates to match your screen resolution and game UI
- **Pixel color positions**: Update positions where the macro waits for UI elements
- **Pixel colors**: Update RGB values to match your game's UI colors
- **Sleep times**: Adjust delays if needed for your system speed

Key positions you'll need to update:
- Main loading screen click position
- Save slot selection position (green card)
- **Egg NPC position** (marked with `[MUST CHANGE]` comment)
- Dialogue "YES" button position
- Chat window focus position

### 3. Keywords Configuration

The `DEFAULT_KEYWORDS` defines what text to search for in the chat:

```python
DEFAULT_KEYWORDS = ("Manta", "Shiny", "Nereus")
```

**What to change**: 
- Replace `"Manta"` with your Roblox username
- Replace `"Nereus"` with the Gradient/Reskin name if you are hunting for them
- Keep `"Shiny"` if hunting for Shiny Pokemon

Example: If your username is `Player123` and you're hunting for just a Shiny:
```python
DEFAULT_KEYWORDS = ("Player123", "Shiny")
```

### 4. Timing Configuration

Adjust delays in `DEFAULT_MACRO_CONFIG`:

```python
DEFAULT_MACRO_CONFIG = MacroConfig(
    region=DEFAULT_REGION,
    click_sequence=DEFAULT_CLICK_SEQUENCE,
    keywords=DEFAULT_KEYWORDS,
    initial_delay_seconds=3.0,              # Delay before starting
    post_click_delay_seconds=1.0,           # Delay after click sequence
    between_iterations_delay_seconds=5.0,   # Delay between reset attempts
)
```

**What to change**: Adjust these values if the macro runs too fast or too slow for your system.

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

1. **Initialization**: The macro waits for the initial delay, then starts the loop
2. **Click Sequence**: Executes the configured click sequence to:
   - Click on the main screen
   - Wait for the Pokemon loading screen (yellow text)
   - Select the save slot (green card)
   - Navigate to the Egg NPC
   - Click through dialogue
   - Focus on the chat window
3. **OCR Detection**: Captures the chat window region and uses OCR to extract text
4. **Keyword Matching**: Checks if all configured keywords appear in the extracted text
5. **Match Found**: If keywords match, the macro performs actions to claim the Pokemon and stops
6. **No Match**: If no match, the macro clicks to rejoin the game and repeats the process

## Troubleshooting

### OCR not detecting text
- Ensure the chat window region is correctly configured
- Make sure the chat window is visible and not obscured
- Check that Tesseract OCR is properly installed
- Try adjusting the region size to capture more of the chat

### Clicks not working
- Verify all click positions are correct for your screen resolution
- Check that Accessibility permissions are granted
- Ensure the game window is in the foreground
- Adjust sleep times if clicks happen too fast

### Pixel color detection timing out
- Update pixel color RGB values to match your game's UI
- Check that pixel positions are correct
- Increase timeout values if your system is slow

### Macro stops unexpectedly
- Check the terminal for error messages
- Verify all coordinates are within your screen bounds
- Ensure the game hasn't changed its UI layout

## Safety Features

- **Failsafe**: Move mouse to top-left corner to stop the macro immediately
- **Timeout protection**: Pixel color detection has timeouts to prevent infinite waiting
- **Error handling**: OCR errors are caught and handled gracefully

## Notes

- This macro is designed for macOS. Windows/Linux users may need to modify pixel detection code
- Screen coordinates are absolute and depend on your screen resolution
- The macro assumes a specific game UI layout - you may need to adjust if the game updates
- Always test the macro in a safe environment before using it for extended periods

## License

MIT License

## Author

Manta

