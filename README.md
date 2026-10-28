# City Defenders TD
Fantasy medieval-themed tower defense game made entirely in Pygame-Ce.

https://github.com/user-attachments/assets/c554c462-f5d6-4dd8-a799-03a6dd1d51c3

# Features
- 7 individual towers, with 2 upgrades each, to fight enemies with
- 7 maps to move around (drag right click), place towers, and fight enemies on
- 9 enemies with varying stats to fight
- Progression of maps and towers (tower shop)
- ~82 custom pixel art sprites drawn by me
- Fully custom GUI system made from scratch in pure Pygame

# Installation
# Build From Scratch
**Minimum Python Version: `v3.8`**

1. Clone the GitHub repository onto your system
2. Open a shell inside the folder of the cloned repository
3. Copy and run the following commands:
- On Linux:
```sh
python -m venv .venv && \
source .venv/bin/activate && \
python -m pip install -r requirements.txt && \
python -m pip install pyinstaller && \
pyinstaller --onefile --windowed \
  --add-data "src/assets:assets" \
  --add-data "src/maps:maps" \
  --icon="src/assets/other/game_icon.ico" \
  --exclude-module numpy \
  --exclude-module pandas \
  --exclude-module scipy \
  --exclude-module matplotlib \
  --name="CityDefendersTD" \
  run.py
```
- On Windows (Powershell):
```powershell
python -m venv .venv && ^
.venv\Scripts\activate && ^
python -m pip install -r requirements.txt && ^
python -m pip install pyinstaller && ^
pyinstaller --onefile --windowed ^
  --add-data "src/assets;assets" ^
  --add-data "src/maps;maps" ^
  --icon="src/assets/other/game_icon.ico" ^
  --exclude-module numpy ^
  --exclude-module pandas ^
  --exclude-module scipy ^
  --exclude-module matplotlib ^
  --name="CityDefendersTD" ^
  run.py
```

# Credits
- [Oleaguid font](https://opengameart.org/content/oleaguid-font) by [arynoc](https://opengameart.org/users/arynoc)
  - Modification: *Removed short quiet segments at the beginning and end removed*
- [Heroic Demise (Updated Version)](https://opengameart.org/content/heroic-demise-updated-version) by [Matthew Pablo](https://opengameart.org/users/matthew-pablo)
  - Modification: *Removed short quiet segments at the beginning and end removed*
- [Soliloquy](https://opengameart.org/content/soliloquy) by [Matthew Pablo](https://opengameart.org/users/matthew-pablo)
  - Modification: *Compressed, removed short quiet segments at the beginning and end*
- [The Fall of Arcana (New Era Version)](https://opengameart.org/content/the-fall-of-arcana-new-era-version) by [Matthew Pablo](https://opengameart.org/users/matthew-pablo)
  - Modification: *Removed short quiet segments at the beginning and end removed*
- [Classical/Medieval Song](https://opengameart.org/content/classicalmedieval-song) by [professorlamp](https://opengameart.org/users/professorlamp) ([website](https://jrtheories.webs.com))
  - Modification: *Removed short quiet segments at the beginning and end removed*
- [Can't Stop Winning](https://opengameart.org/content/cant-stop-winning-rpg-orchestral-essentials-battle-victory-music) by [Jonathan Shaw](https://opengameart.org/users/inspectorj) ([website](https://www.jshaw.co.uk/))
  - Modification: *Removed short quiet segments at the beginning and end removed*
- [The Fallen](https://opengameart.org/content/the-fallen-rpg-orchestral-essentials-defeated-music) by [Jonathan Shaw](https://opengameart.org/users/inspectorj) ([website](https://www.jshaw.co.uk/))
  - Modification: *Removed short quiet segments at the beginning and end removed*
- [The Bard's Tale](https://opengameart.org/content/medieval-the-bards-tale) by [RandomMind](https://opengameart.org/users/randommind)
  - Modification: *Removed short quiet segments at the beginning and end removed*
