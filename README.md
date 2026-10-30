# ab

An image-recognition bot for Asphalt that plays races automatically. It runs on Windows only.

## Requirements

- Windows 10 or 11
- Python 3.11
- The game installed

## Setup

```cmd
git clone https://github.com/ayaanjaved07/ab.git
cd ab
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Before you run

- Set the Windows display scale to **100%** (Settings > System > Display > Scale).
- Set the game language to **English**.
- Open the game in **windowed mode**, and don't be in a race.
- Turn off any overlays that cover parts of the screen (Discord, GeForce, Xbox Game Bar and similar).
- In `settings.ini`, uncomment `window_title` and set it to the exact title of the game window, for example:

  ```ini
  window_title = Asphalt - v50.0.6a - D3D12
  ```

## Running

The bot looks for its own console window by the title `<current folder>\bot.exe`. When you run from source, set that title first. Use **Command Prompt** (cmd), not PowerShell:

```cmd
cd path\to\ab
.venv\Scripts\activate
title %cd%\bot.exe
python bot.py
```

The bot moves its console to the bottom of the screen and the game window to the top left (1280x720), then starts playing.

- Press **Ctrl + Shift + Q** to stop the bot at any time.
- If the game window isn't found, open the game and press Enter in the console to try again.

## Settings

All options are in `settings.ini`, and each one has a comment above it. The main ones:

| Setting | Meaning |
|---|---|
| `number` | How many times the hunt runs |
| `car` | Which car to use (`pur`, `nino`) |
| `watch_ad` | Watch ads for bonus coins |
| `ticket_refill` / `token_refill` / `ad_ticket_refill` | How tickets get refilled when they run out |
| `play_infinitely` / `play_infinitely_sleep` | When tickets run out, sleep for this many minutes and then continue |
| `route`, `route_config`, `route_set` | Which route signs to take, in priority order |
| `car_switch_sleep` | Seconds to wait for a car to load after switching |
| `sleep` | Base delay between actions. Raise it if your PC is slow |

## Files

- `bot.py`: the bot
- `settings.ini`: the configuration
- `images/`: the screen templates the bot matches against. Don't rename or move them.
