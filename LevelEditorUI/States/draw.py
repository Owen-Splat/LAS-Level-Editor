from PySide6 import QtCore, QtWidgets, QtGui
from LevelEditorCore.Data.data import *
from LevelEditorUI.custom_widgets import *
import LevelEditorCore.Tools.FixedHash.leb as leb
import numpy as np


class DrawState:
    def __init__(self, parent, toggle_hide=False, hide_empty_sprites=True) -> None:
        self.window = parent
        self.drawRoom(toggle_hide, hide_empty_sprites)


    def drawRoom(self, toggle_hide=False, hide_empty_sprites=True) -> None:
        """Updates actor info and draws basic sprites to represent the room and its actors"""

        # delete old actor sprites
        for act in self.window.actor_sprites:
            act.deleteLater()
        self.window.actor_sprites = []

        # draw out the room based on tile data
        if self.window.room_data.grid.info.room_type == '3D':
            self.draw3DRoomLayout()
        else:
            self.draw2DRoomLayout()

        # redraw actor list
        self.window.actor_keys.clear()
        self.window.ui.listWidget.clear()
        for act in self.window.room_data.actors:
            self.window.actor_keys.append(act.key)
            self.window.ui.listWidget.addItem(ACTOR_NAMES[ACTOR_IDS.index(hex(act.type))])
        if self.window.current_actor >= 0:
            self.window.ui.listWidget.setCurrentRow(self.window.next_actor)
        else:
            self.window.ui.listWidget.setCurrentRow(0)

        # display the info of the currently selected actor
        self.displayActorInfo()

        # now draw the actor sprites
        current_sprite = None
        enemy_sprites = []
        for i, act in enumerate(self.window.room_data.actors):
            if i == self.window.current_actor:
                sprite = SelectedLabel(self.window.ui.roomFrame)
            else:
                sprite = ActorLabel(self.window.ui.roomFrame)
                sprite.actor_index = i

            # define the sprite name and create a pixmap out of it
            name = self.window.ui.listWidget.item(i).text()
            if name in ACTOR_ICONS:
                pix = QtGui.QPixmap(ACTOR_ICONS_PATH / f"{name}.png")
            else:
                pix = QtGui.QPixmap(ACTOR_ICONS_PATH / "NoSprite.png")
                # if "hide objects without sprites" was just toggled, set the visible variable
                if toggle_hide:
                    act.visible = not hide_empty_sprites

            # create refs of enemy sprites to raise above other sprites
            if name.startswith('Enemy'):
                enemy_sprites.append(sprite)

            # rotate sprite, will need to create a mapping of actors and default rotations
            # trans = QtGui.QTransform()
            # trans.rotate(act.rotY * -1)
            # pix = pix.transformed(trans)

            # define geometry
            spr_width = round(self.window.tile_pixel_size * act.scale.x)
            spr_height = round(self.window.tile_pixel_size * act.scale.z)
            unit_pixel_ratio = self.window.tile_pixel_size / self.window.tile_unit_size
            posX = round(((act.position.x - self.window.topleft[0]) * unit_pixel_ratio) - (spr_width / 2))
            if self.window.room_data.grid.info.room_type == '3D':
                posY = round(((act.position.z - self.window.topleft[1]) * unit_pixel_ratio) - (spr_height / 2))
            else:
                spr_height = round(self.window.tile_pixel_size * act.scale.y)
                posY = round((12 - act.position.y) * unit_pixel_ratio)
            sprite.setGeometry(posX, posY, spr_width, spr_height)

            # we scale the pixmap instead of letting the QLabel do it, this way the pixel art is not blurred and stays crisp
            pix = pix.scaled(sprite.width(), sprite.height(), 
                QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, QtCore.Qt.TransformationMode.FastTransformation)
            sprite.setPixmap(pix)

            # add sprite to a reference list so we can delete it before a redraw
            self.window.actor_sprites.append(sprite)

            # create reference to the sprite of the currently selected actor
            if i == self.window.current_actor:
                current_sprite = sprite

            # only show the sprite if it's not hidden
            if act.visible:
                sprite.show()

        # raise enemy sprites
        for spr in enemy_sprites:
            spr.raise_()

        # raise the currently selected actor above everything else
        if current_sprite != None:
            current_sprite.raise_()

        self.window.toggleShowButton()


    def draw3DRoomLayout(self) -> None:
        """Draws out the sprites to represent a 3D room from a top-down view"""

        grid = self.getRoomGridData()
        for i, tile in enumerate(grid.tilesdata):
            v_tile: QtWidgets.QLabel = self.window.tiles[i]
            v_tile.setPixmap(QtGui.QPixmap(TILE_ICONS_PATH / f"{self.getTileSprite(tile)}.png"))
            v_tile.setScaledContents(True)


    def draw2DRoomLayout(self) -> None:
        """Draws out the sprites to represent a 2D room from a front-facing view"""

        # we do not care about the z-axis technically being 2 tiles long, so we only look at half the tile data
        # tile_data = self.window.room_data.grid.tilesdata
        # tile_data = tile_data[:int(len(tile_data) / 2)]
        grid = self.getRoomGridData()
        for i, tile in enumerate(grid.tilesdata):
            spr = self.getTileSprite(tile)
            pos = int(i + 80 - (10 * (tile.elevation // 1.5))) - 10
            if spr == "Wall" and str(pos)[-1] in ("0", "9"): # walls need to go up all the way
                pos = int(str(pos)[-1])
            while pos < 80:
                v_tile: QtWidgets.QLabel = self.window.tiles[pos]
                v_tile.setPixmap(QtGui.QPixmap(TILE_ICONS_PATH / f"{spr}.png"))
                v_tile.setScaledContents(True)
                pos += 10


    def getRoomGridData(self) -> leb.Grid:
        """Reads the map model from the MapStatic actor and returns that room's grid data"""

        ms = None
        for act in self.window.room_data.actors:
            if act.type == 0x185: # MapStatic
                ms = act
                break

        if ms == None:
            raise TypeError('MapStatic actor was not found!')

        rm = str(ms.parameters[0], 'utf-8') # get room name
        with open(self.window.rom_path / "region_common/level" / rm.split('_')[0] / f"{rm}.leb", 'rb') as f:
            rm_data = leb.Room(f.read())
        return rm_data.grid


    def getTileSprite(self, tile) -> str:
        """Determines the sprite by reading the tile's data, and returns the pixmap"""

        contains_collision: bool = tile.flags1['containscollision']
        deep_water: bool = tile.flags1['deepwaterlava']
        is_water: bool = tile.flags3['iswaterlava']
        can_dig: bool = tile.flags3['isdigspot']
        tile_sprite = 'Walkable' #"#e5cc8f"

        # Some tiles contain collision for actors. By checking can_dig & is_water, we can elim most
        if contains_collision and (not can_dig or not is_water):
            tile_sprite = 'Wall' #"#775c2e"
        else:
            if deep_water:
                tile_sprite = 'Water' #"#6b7d63"
                if not is_water:
                    tile_sprite = 'Hole' #"black"
            elif is_water:
                tile_sprite = 'ShallowWater' #"#8a9b75"

        return tile_sprite


    def displayActorInfo(self) -> None:
        window = self.window

        if not window.deleted:
            window.saveActor(window.current_actor)
        else:
            window.deleted = False

        window.current_actor = window.ui.listWidget.currentRow() if window.room_data.actors else -1

        if window.current_actor != -1:
            try:
                act = window.room_data.actors[window.current_actor]
            except IndexError:
                return
            else:
                full_name = ACTOR_NAMES[ACTOR_IDS.index(hex(act.type))]
                window.ui.ID_lineEdit.setText(str(act.key))
                window.ui.dataType.setCurrentIndex(
                    window.ui.dataType.findText(full_name, QtCore.Qt.MatchExactly))
                window.ui.dataPos_X.setText(convert.removeTrailingZeros(f'{act.position.x:.4f}'))
                window.ui.dataPos_Y.setText(convert.removeTrailingZeros(f'{act.position.y:.4f}'))
                window.ui.dataPos_Z.setText(convert.removeTrailingZeros(f'{act.position.z:.4f}'))
                window.ui.dataRot_X.setText(convert.removeTrailingZeros(f'{act.rotation.x:.4f}'))
                window.ui.dataRot_Y.setText(convert.removeTrailingZeros(f'{act.rotation.y:.4f}'))
                window.ui.dataRot_Z.setText(convert.removeTrailingZeros(f'{act.rotation.z:.4f}'))
                window.ui.dataScale_X.setText(convert.removeTrailingZeros(f'{act.scale.x:.4f}'))
                window.ui.dataScale_Y.setText(convert.removeTrailingZeros(f'{act.scale.y:.4f}'))
                window.ui.dataScale_Z.setText(convert.removeTrailingZeros(f'{act.scale.z:.4f}'))

                for i in range(8):
                    if isinstance(act.parameters[i], bytes):
                        param = str(act.parameters[i], 'utf-8')
                    elif isinstance(act.parameters[i], np.float32):
                        param = convert.removeTrailingZeros(f'{act.parameters[i]:.4f}')
                    else:
                        param = str(act.parameters[i])
                    window.ui.tableWidget.item(i, 0).setText('???')
                    window.ui.tableWidget.item(i, 1).setText(param)
                    if full_name in ACTOR_PARAMETERS:
                        if i+1 <= len(ACTOR_PARAMETERS[full_name]):
                            param_info = str(ACTOR_PARAMETERS[full_name][i])
                            window.ui.tableWidget.item(i, 0).setText(param_info)

                window.ui.dataSwitches_0.setText(str(act.switches[0][1]))
                window.ui.comboBox.setCurrentIndex(act.switches[0][0])
                window.ui.dataSwitches_1.setText(str(act.switches[1][1]))
                window.ui.comboBox_2.setCurrentIndex(act.switches[1][0])
                window.ui.dataSwitches_2.setText(str(act.switches[2][1]))
                window.ui.comboBox_3.setCurrentIndex(act.switches[2][0])
                window.ui.dataSwitches_3.setText(str(act.switches[3][1]))
                window.ui.comboBox_4.setCurrentIndex(act.switches[3][0])

                # relationships
                # window.ui.comboBox_5.setCurrentIndex(act.relationships.is_enemy)
                # window.ui.comboBox_6.setCurrentIndex(act.relationships.check_kills)
                # window.ui.comboBox_7.setCurrentIndex(act.relationships.is_chamber_enemy)
                # window.displayEntryInfo()

        for field in window.ui.centralwidget.findChildren(QtWidgets.QLineEdit): # forces QLineEdit to display from leftmost character
            field.home(False)


    # def displayEntryInfo(self) -> None:
    #     act = self.room_data.actors[self.current_actor]
    #     relationship_info = {}

    #     relationship_info['Controlled_Actors'] = []
    #     for entry in act.relationships.section_1:
    #         params = []
    #         for param in entry[0]:
    #             params.append(str(param))
    #         relationship_info['Controlled_Actors'].append({
    #             self.room_data.actors[entry[1]].key: {
    #                 'Parameters': params
    #             }
    #         })
        
    #     relationship_info['Needed_Positions'] = []
    #     for entry in act.relationships.section_2:
    #         params = []
    #         for param in entry[0]:
    #             params.append(str(param))
    #         relationship_info['Needed_Positions'].append({
    #             'Rail_Index': entry[1],
    #             'Point_Index': entry[2],
    #             'Parameters': params
    #         })
        
    #     relationship_info['Actors_That_Use_Me'] = []
    #     for entry in act.relationships.section_3:
    #         relationship_info['Actors_That_Use_Me'].append(self.room_data.actors[entry].key)
        
    #     # self.ui.textEdit.setText(yaml.dump(relationship_info, Dumper=MyDumper, sort_keys=False, default_flow_style=False, indent=4))
