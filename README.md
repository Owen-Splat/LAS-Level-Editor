# LAS-Room-Editor
A GUI editor for LEB files

**LEB** is a custom format used to store room data in Link's Awakening. This editor specifically targets the actor data. You can read more information [here](https://zeldamods.org/las/LEB)

**Actors** are in-game entities. Link, enemies and NPCs are all examples of actors.

In Link's Awakening, the concept of actors is fairly similar to that of classic 3D Zelda games such as Ocarina of Time. However, unlike past Zelda games, actors are internally implemented with an entity-component architecture.

Actors should not be confused with their models, even though model files are found under the actor/ directory in the RomFS.

You can see a complete list of all actors [here](https://zeldamods.org/las/Actors)

Join the [Discord](https://discord.com/invite/rfBSCUfzj8) to talk about modding or ask any questions you have!

## How to run:

Either just download the latest release or you can also run from source.
If you want to run from source, then you need to clone this repository and make sure you have Python 3.8+ installed

Open the folder in a command prompt and install dependencies by running:  
`py -3.8 -m pip install PySide6` (on Windows)  
`python3 -m pip install PySide6` (on Mac)  
`python3 -m pip install PySide6` (on Linux)

Then run the editor with:  
`py -3.8 main.py` (on Windows)  
`python3 main.py` (on Mac)  
`python3 main.py` (on Linux)  