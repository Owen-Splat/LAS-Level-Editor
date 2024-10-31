import os, sys, yaml

if getattr(sys, "frozen", False):
    RUNNING_FROM_SOURCE = False
    root_path = os.path.dirname(sys.executable)
else:
    RUNNING_FROM_SOURCE = True
    root_path = os.path.dirname(sys.argv[0])

data_folder = 'LevelEditorCore/Data' if RUNNING_FROM_SOURCE else 'lib/LevelEditorCore/Data'
DATA_PATH = os.path.join(root_path, data_folder)
with open(os.path.join(DATA_PATH, 'actors.yml'), 'r') as f:
    actor_list = yaml.safe_load(f)
with open(os.path.join(DATA_PATH, 'actor_parameters.yml'), 'r') as f:
    ACTOR_PARAMETERS = yaml.safe_load(f)

ACTORS = {}
for i, actor in enumerate(actor_list):
    ACTORS[actor['name']] = hex(i)
ACTOR_IDS = list(ACTORS.values())
ACTOR_NAMES = list(ACTORS.keys())
REQUIRED_ACTORS = [0x185] # MapStatic

icons_folder = 'LevelEditorUi/Icons' if RUNNING_FROM_SOURCE else 'lib/LevelEditorUi/Icons'
ACTOR_ICONS_PATH = os.path.join(root_path, icons_folder, 'Actors')
ACTOR_ICONS = [f.split('.')[0] for f in os.listdir(ACTOR_ICONS_PATH) if f.endswith('.png')]
TILE_ICONS_PATH = os.path.join(root_path, icons_folder, 'Tiles')
