# Asteroids

A classic Asteroids arcade game built with Python and Pygame. Shoot down asteroids, survive as long as possible, and beat your high score.

## Features

- Sprite-based player ship with smooth rotation and movement
- Purple engine trail when thrusting forward
- Asteroids that split into smaller pieces when shot
- Elastic physics-based asteroid collisions
- 3 lives per game
- Persistent high score saved between sessions
- Game event and state logging to JSONL files

## Controls

| Key     | Action          |
| ------- | --------------- |
| `W`     | Thrust forward  |
| `S`     | Thrust backward |
| `A`     | Rotate left     |
| `D`     | Rotate right    |
| `Space` | Shoot           |

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
# Clone the repo
git clone <repo-url>
cd asteroids

# Run the game (uv handles dependencies automatically)
uv run main.py
```

Dependencies are managed via `pyproject.toml`. The only runtime dependency is `pygame==2.6.1`.

## Project Structure

```
asteroids/
├── main.py           # Game loop, collision logic, scoring
├── player.py         # Player ship: movement, shooting, trail, lives
├── asteroid.py       # Asteroid sprite with split behavior
├── asteroidfield.py  # Spawns asteroids from screen edges
├── shot.py           # Bullet projectile
├── circleshape.py    # Base class for circle-based sprites
├── constants.py      # Tunable game parameters
├── logger.py         # JSONL event/state logging
├── item.py           # Collectible item base
└── assets/           # Ship and asteroid sprites
```
