# Flappy Bird

A Flappy Bird clone built with Pygame, featuring multiple bird skins, animations, sound effects, and a high score system.

## About

A pygame study project completed on March 10, 2025, focused on sprite animation, collision detection, game state management (menu, playing, game over), and asset handling.

## Features

- 3 playable bird skins (blue, yellow, red)
- Sound effects and background music
- High score tracking
- Menu, get ready, and game over screens

## Screenshots

| Menu | Gameplay | Game Over |
|------|----------|-----------|
| ![Menu](screenshots/menu.png) | ![Gameplay](screenshots/gameplay.png) | ![Game Over](screenshots/game-over.png) |

## How to run

```bash
# Clone the repository
git clone https://github.com/caioax/flappy-bird.git
cd flappy-bird

# Install pygame (Arch Linux)
sudo pacman -S python-pygame

# Create and activate virtual environment
python3 -m venv venv --system-site-packages
source venv/bin/activate

# Run
python3 main.py
```

## Technologies

- Python 3
- [Pygame](https://www.pygame.org/)
