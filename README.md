# Bear Country

A small top-down pixel-art demo built with Pygame. The player stays centered while world sprites scroll around, and the HUD shows world coordinates.

**Features**
- **Top-down demo:** Player-centered camera with world sprites.
- **Pixel-art scaling:** Controlled by the `SCALE` constant in [main.py](main.py).
- **Simple movement:** WASD / arrow keys, with diagonal normalization and tunable speed.

**Requirements**
- **Python 3.8+**
- **Dependencies:** See [requirements.txt](requirements.txt). Install with:

```bash
python3 -m pip install -r requirements.txt
```

**Run**

```bash
python3 main.py
```

**Controls**
- **Move:** `W`/`A`/`S`/`D` or arrow keys
- **Quit:** `Esc` or close the window

**Project Structure**
- **[main.py](main.py):** Entrypoint and main loop (window, rendering, world sprites, HUD).
- **[player.py](player.py):** `Player` class and sprite handling.
- **[requirements.txt](requirements.txt):** Project dependencies (currently `pygame`).
- **[sprites/](sprites/):** Image assets used by the demo. If a sprite is missing, `main.py` will use a magenta placeholder and print a warning.

**Configuration / Tuning**
- Edit `WIDTH`, `HEIGHT`, `SCALE`, and `PLAYER_SPEED` in [main.py](main.py) to change screen size, pixel scale, and player movement speed.

**Notes for contributors**
- Add sprite assets to the `sprites/` folder. Filenames referenced by the code include `sprite.15.png` in the current demo.
- Keep pixel-art sprites at integer multiples for clean scaling (the code uses integer `SCALE`).

**License**
- No license is specified. Add a LICENSE file if you want to make the project open-source.
