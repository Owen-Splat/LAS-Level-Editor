from LevelEditorCore.Data.data import ACTOR_NAMES, ACTOR_IDS
import LevelEditorCore.Tools.conversions as convert
import LevelEditorCore.Tools.FixedHash.leb as leb
from LevelEditorCore.Tools.FixedHash.fixed_hash import Vector3


class ActorObj:
    def __init__(self, actor: leb.Actor) -> None:
        self.visible = True
        self.id = actor.key
        self.type = actor.type
        self.name = ACTOR_NAMES[ACTOR_IDS.index(hex(actor.type))]
        self.position: Vector3 = actor.position
        self.rotation: Vector3 = actor.rotation
        self.scale: Vector3 = actor.scale
        self.parameters = [convert.removeTrailingZeros(str(param)) for param in actor.parameters]
        self.flags = [self.Flag(f[0], f[1]) for f in actor.switches]
        self.links = self.Links(actor.relationships)


    class Flag:
        flag_types = {
            0: "Local", # local flags per level
            1: "Global", # global flags stored in the save
            2: "Hardcoded", # static True or False
            3: "Panel", # local flags specific to Panel levels, little research has gone into this
            4: "Unused" # always 0
        }

        def __init__(self, usage, index) -> None:
            self.usage = self.flag_types[usage]
            self.index = index


    class Links:
        def __init__(self, relationships: leb.Relationship) -> None:
            self.actors = [r[1] for r in relationships.section_1] # actors (by ID) that this actor references
            self.points = [r[2] for r in relationships.section_2] # points (Vector3) that this actor references
            # section 3 is a list of other actors that reference this actor, but we don't care about storing that
            # we can determine that when repacking the data


class RoomObj:
    def __init__(self, rm_data: bytes) -> None:
        rm_data: leb.Room = leb.Room(rm_data)
        self.info = rm_data.grid.info
        self.actors = []
        for actor in rm_data.actors:
            self.actors.append(ActorObj(actor))
        for actor in self.actors:
            actor: ActorObj = actor
            for i, index in enumerate(actor.links.actors): # reference key/ID instead of actor index
                actor.links.actors[i] = rm_data.actors[index].key
            for point in actor.links.points: # reference actual positions instead of point index
                point = Vector3(point.x, point.y, point.z)
