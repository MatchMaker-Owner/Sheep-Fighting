# 🐑 Sheep Wrestling

A turn-based strategy game for one player, written in pure Python with the built-in `turtle` module. You and a computer opponent each send sheep onto a 10-slot field. When opposing sheep meet, the side with more combined power shoves the other back. Push a sheep all the way into the enemy pen to win, and don't let the enemy reach yours.

![Gameplay screenshot](docs/screenshots/gameplay.png)

## Why this project exists

This was built as a Python practice project to get comfortable with the core language without reaching for external libraries: lists, dictionaries, nested loops, mouse-click events and simple game-state logic. The whole game is deliberately written as a single top-level script with **no functions** (hence the window title, *"Buttons (No def)"*), which makes the control flow easy to read from top to bottom.

## Built with

| Item | Details |
|---|---|
| Language | Python 3.8 or newer |
| Graphics / input | [`turtle`](https://docs.python.org/3/library/turtle.html) (standard library, uses Tkinter under the hood) |
| Other modules | `time` (standard library) |
| External packages | **None**: nothing to `pip install` |

## Screenshots

> Replace these with your own captures (see [Adding screenshots](#adding-screenshots)).

| Start of the game | Mid-battle collision | Win / lose message |
|---|---|---|
| ![Start](docs/screenshots/start.png) | ![Collision](docs/screenshots/collision.png) | ![Result](docs/screenshots/result.png) |

## Getting started

### 1. Prerequisites

You need Python 3.8+ with Tkinter. Tkinter ships with the official Python installers for Windows and macOS. On some Linux distributions it is a separate package:

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (Homebrew Python only)
brew install python-tk
```

Check that everything is in place:

```bash
python --version        # should print 3.8 or higher
python -m tkinter       # should open a small test window
```

### 2. Get the code

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

Or just download `sheep_wrestling.py` and open a terminal in the same folder.

### 3. Run it

```bash
# Windows
python sheep_wrestling.py

# macOS / Linux
python3 sheep_wrestling.py
```

A 1200×420 window opens. **Keep the terminal visible**: the rules are printed there when the game starts, and every turn's events (deployments, collisions, pushes) are logged there.

There are no environment variables, config files, or build steps.

## How to play

The board is a green field with a row of ten brown slots numbered 1 to 10. Your pen (where your sheep spawn) is the small box on the **left**; the enemy's pen is the box on the **right**.

- **White dots** are your sheep. They walk **right**.
- **Black dots** are the enemy's sheep. They walk **left**.
- A **bigger dot means a stronger sheep.**

### Controls

Click the buttons below the field with the mouse. Every click ends one turn.

| Button | Action |
|---|---|
| **1** | Deploy Sheep 1 |
| **2** | Deploy Sheep 2 |
| **3** | Deploy Sheep 3 |
| **Skip** | Deploy nothing this turn |
| **Exit** | Quit the game |

> Close the game with **Exit**. Closing the window with the ✕ button can print a harmless traceback in the terminal.

### Sheep stats

| Sheep | Power | Your cooldown | Enemy cooldown |
|---|---|---|---|
| Sheep 1 (small) | 1 | 3 turns | 3 turns |
| Sheep 2 (medium) | 3 | 5 turns | 9 turns |
| Sheep 3 (large) | 5 | 7 turns | 15 turns |

After a sheep is deployed it goes on cooldown and can't be deployed again until the cooldown reaches 0. If you click a sheep that is still cooling down, the deployment fails and the turn is wasted, so check the `CD PS` line in the terminal, which shows the current cooldowns before each turn. All sheep start ready.

### Winning and losing

- **You win** when one of your sheep reaches the enemy's pen on the right.
- **You lose** when an enemy sheep reaches slot 1, the first slot next to your pen.

### What happens in a turn

1. Wait for you to click a button.
2. Every cooldown ticks down by 1.
3. Your chosen sheep (if available) spawns in your pen.
4. All your sheep step one slot right, and all enemy sheep step one slot left, if the slot ahead of them is empty.
5. **Collision check.** If a white sheep sits directly next to a black sheep, the game looks at the whole connected group of sheep around that point (bounded by empty slots) and adds up the power on each side:
   - More power on your side: the whole group shifts one slot **right**.
   - More power on the enemy side: the whole group shifts one slot **left**.
   - Equal power: nothing moves.
6. The enemy deploys a sheep into its pen if it's empty. It cycles through Sheep 1, 2, 3 in order and picks the first one that is off cooldown.
7. The board is redrawn and the win/lose conditions are checked.

Strategy tip: a lone Sheep 3 beats a lone Sheep 1, but a column of several small sheep stacked behind the front line can add up to more power than a single big one.

## How the code is organised

Everything lives in one file, `sheep_wrestling.py`, in this order:

1. **Setup**: creates the turtle screen and two "pens": `SD` (static drawer, for the field, pens and buttons) and `ED` (entity drawer, for sheep).
2. **Game data**: a nested dictionary `data` holds each side's sheep (`Number`, `Power`, `CD`). The `Field` list has 12 entries: index `0` is your pen, indices `1`–`10` are the visible battlefield slots, and index `11` is the enemy pen. Positive numbers are your sheep, negative numbers are the enemy's (`1`/`-1` for Sheep 1, and so on).
3. **UI**: the five button rectangles are stored as tuples of coordinates; a single `onscreenclick` handler records where you clicked, and the main loop checks whether that point is inside a button.
4. **Main loop**: one iteration per turn, following the steps listed above, with a redraw at the end and a 1.5 s pause between turns.

```
index:   0       1  2  3  4  5  6  7  8  9  10       11
       [ your ] [          battlefield          ] [ enemy ]
       [  pen ] [ slots 1 ........................ 10 ] [  pen  ]
          ->  your sheep move right      enemy sheep move left  <-
```

## Project structure

```
.
├── sheep_wrestling.py      # the entire game
├── README.md
└── docs/
    └── screenshots/        # images used in this README
```

## Adding screenshots

1. Run the game and play a few turns.
2. Capture the window (Windows: `Win + Shift + S`; macOS: `Cmd + Shift + 4`; Linux: your screenshot tool).
3. Save the images as `start.png`, `collision.png`, `result.png` and `gameplay.png` in `docs/screenshots/`.
4. Commit them so they render on GitHub.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named '_tkinter'` or `tkinter` | Install Tkinter for your platform (see [Prerequisites](#1-prerequisites)). |
| Window is cut off | The window is 1200×420; use a display that's at least 1200 px wide. |
| Clicks seem to do nothing | Click inside the grey buttons, and make sure the game window (not the terminal) is focused. |
| Traceback after closing the window | Use the **Exit** button next time. |

## Known limitations and ideas

- The enemy follows a fixed deployment cycle rather than reacting to the board.
- Win and lose conditions are asymmetric: you must reach the enemy pen, while the enemy only needs to reach slot 1.
- The program is intentionally one flat script. A natural next step would be to refactor it into functions or classes, and add a restart option, sound or score tracking.

## License

Add a license of your choice (for example MIT) as a `LICENSE` file, and mention it here.
