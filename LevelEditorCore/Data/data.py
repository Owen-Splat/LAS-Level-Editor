from PySide6.QtGui import QIcon
import os, sys, yaml

if getattr(sys, "frozen", False):
    RUNNING_FROM_SOURCE = False
    root_path = os.path.dirname(sys.executable)
else:
    RUNNING_FROM_SOURCE = True
    root_path = os.path.dirname(sys.argv[0])

SETTINGS_PATH = os.path.join(root_path, 'settings.txt')
try:
    with open(SETTINGS_PATH, 'r') as f:
        SETTINGS = yaml.safe_load(f)
    if SETTINGS == None:
        raise FileNotFoundError
    if 'romfs_path' not in SETTINGS or 'output_path' not in SETTINGS:
        raise FileNotFoundError
except FileNotFoundError:
    SETTINGS = {
        'romfs_path': '',
        'output_path': ''
    }

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

icons_folder = 'LevelEditorUI/Icons' if RUNNING_FROM_SOURCE else 'lib/LevelEditorUI/Icons'
ACTOR_ICONS_PATH = os.path.join(root_path, icons_folder, 'Actors')
ACTOR_ICONS = [f.split('.')[0] for f in os.listdir(ACTOR_ICONS_PATH) if f.endswith('.png')]
TILE_ICONS_PATH = os.path.join(root_path, icons_folder, 'Tiles')

# resource_folder = 'LevelEditorUi/Resources' if RUNNING_FROM_SOURCE else 'lib/LevelEditorUi/Resources'
# RESOURCE_PATH = os.path.join(root_path, resource_folder)
# with open(os.path.join(RESOURCE_PATH, 'Stylesheets/light_theme.txt'), 'r') as f:
#     LIGHT_STYLE = f.read()
# with open(os.path.join(RESOURCE_PATH, 'Stylesheets/sidebar.txt'), 'r') as f:
#     SIDEBAR_THEME = f.read()
# with open(os.path.join(RESOURCE_PATH, 'Stylesheets/main_view.txt'), 'r') as f:
#     MAIN_THEME = f.read()

# WINDOW ICONS
ICONS_PATH = 'LevelEditorUI/Window/Icons' if RUNNING_FROM_SOURCE else 'lib/LevelEditorUI/Window/Icons'

MAIN_ICON = ICONS_PATH + '/icon.png'

MENU_ICON = ICONS_PATH + '/cil-menu.png'
HOME_ICON = ICONS_PATH + '/cil-home.png'
LOCATION_ICON = ICONS_PATH + '/cil-location-pin.png'
PROPERTIES_ICON = ICONS_PATH + '/cil-settings.png'
ROOM_ICON = ICONS_PATH + '/cil-rectangle.png'
DATASHEET_ICON = ICONS_PATH + '/cil-notes.png'
EVENTS_ICON = ICONS_PATH + '/cil-task.png'
CODE_ICON = ICONS_PATH + '/cil-code.png'

RESTORE_ICON = ICONS_PATH + '/cil-window-restore.png'
MAXIMIZE_ICON = ICONS_PATH + '/cil-window-maximize.png'
MINIMIZE_ICON = ICONS_PATH + '/cil-window-minimize.png'
CLOSE_ICON = ICONS_PATH + '/cil-x.png'
SIZE_ICON = ICONS_PATH + '/cil-size-grip.png'
