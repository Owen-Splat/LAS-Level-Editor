import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], 
                    "excludes": ["tkinter", "unittest", "sqlite3", "numpy", "matplotlib", "zstandard"],
                    "zip_include_packages": ["encodings", "PySide6"],
                    "include_files": [],
                    "optimize": 2}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# build_icon = "Resources/icon.ico"
# if sys.platform == "darwin": # mac
#     build_icon = "Resources/icon.icns"

setup(
    name = "Links Awakening Switch Level Editor",
    version = "0.3",
    description = "A level editor for The Legend of Zelda: Link's Awakening remake!",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base, target_name="LAS Level Editor")] #, icon=build_icon)]
)