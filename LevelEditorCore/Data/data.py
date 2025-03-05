from pathlib import Path
import sys, yaml

if getattr(sys, "frozen", False):
    RUNNING_FROM_SOURCE = False
    root_path = Path(sys.executable).parent
else:
    RUNNING_FROM_SOURCE = True
    root_path = Path(sys.argv[0]).parent

SETTINGS_PATH = (root_path / 'settings.txt')
try:
    with open(SETTINGS_PATH, 'r') as f:
        SETTINGS = yaml.safe_load(f)
    if SETTINGS == None:
        raise FileNotFoundError
    if 'romfs_path' not in SETTINGS or 'output_path' not in SETTINGS:
        raise FileNotFoundError
except (FileNotFoundError, yaml.constructor.ConstructorError):
    SETTINGS = {
        'romfs_path': '',
        'output_path': ''
    }

data_folder = 'LevelEditorCore/Data' if RUNNING_FROM_SOURCE else 'lib/LevelEditorCore/Data'
DATA_PATH = root_path / data_folder
with open(DATA_PATH / 'actors.yml', 'r') as f:
    actor_list = yaml.safe_load(f)
with open(DATA_PATH / 'actor_parameters.yml', 'r') as f:
    ACTOR_PARAMETERS = yaml.safe_load(f)

ACTORS = {}
for i, actor in enumerate(actor_list):
    ACTORS[actor['name']] = hex(i)
ACTOR_IDS = list(ACTORS.values())
ACTOR_NAMES = list(ACTORS.keys())
REQUIRED_ACTORS = [0x185] # MapStatic

icons_folder = 'LevelEditorUi/Icons' if RUNNING_FROM_SOURCE else 'lib/LevelEditorUi/Icons'
ACTOR_ICONS_PATH = root_path / icons_folder / 'Actors'
icon_files = [f for f in ACTOR_ICONS_PATH.iterdir() if f.is_file()]
ACTOR_ICONS = []
for f in icon_files:
    ACTOR_ICONS.append(f.name.split('.')[0])
# ACTOR_ICONS = [f.split('.')[0] for f.name in icon_files if f.endswith('.png')]
TILE_ICONS_PATH = root_path / icons_folder / 'Tiles'

resource_folder = 'LevelEditorUi/Resources' if RUNNING_FROM_SOURCE else 'lib/LevelEditorUi/Resources'
RESOURCE_PATH = root_path / resource_folder
with open(RESOURCE_PATH / 'light_theme.txt', 'r') as f:
    LIGHT_STYLE = f.read()
