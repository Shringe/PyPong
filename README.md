# About
This was my first Python project that I made. I learned the basics beforehand following [py4e](https://www.py4e.com/). The main project code is inside of `PyPongALPHA.py`. I also wrapped this project in a Nix flake for future reproduceability, though suprsingly, the latest versions of python and pygame still work for this project, even years after the project's creation.

# Features
PyPong has scoring, assets, easter eggs, UI, a settings menu, and a configurable physics system.

## Assets
The game includes audio, music, sound effects, animations, and 2D assets.
Most of the 2D assets were made by me using [GIMP](https://www.gimp.org/). The button animation was made frame-by-frame by me in GIMP. The music, sounds, font, and background were free assets I found online.

## Easter Eggs
<details>
  <summary>Pong Animation</summary>
    Hover over the "Classic 2P" button in the gamemode selection screen for a few seconds to get a cool animation.
</details>
<details>
  <summary>Exit Message</summary>
    Look in stdout after quiting the game. Most of the tme you will get a nice exit message, but there is a small chance you will get a unique and funny exit message instead. There are a small handful of possible messages, if you get lucky. If you want to view all of them, it might be faster to look for the strings inside of the source code instead of launching and quiting the game a bunch.
</details>

# Download and Installation
```sh
git clone https://github.com/Shringe/PyPong.git
cd PyPong
```

## Running
Make sure to be in the CWD while running the program so that it can find necessary assets.

### Running with Nix
Using the [Nix package manager](https://github.com/NixOS/nix) is the recommended method, since it is fully reproduceable.
```sh
nix run
```

### Running with a virtual environment
Make sure to install python3 beforehand.
```sh
python3 -m venv venv
source ./venv/bin/activate
pip install pygame
python3 "PyPongALPHA.py"
```

# Screenshots
![screenshot](images/Title_Screen.png)
![screenshot](images/Settings_Menu.png)
![screenshot](images/Game_Mode_Select.png)
![screenshot](images/Gameplay.png)
