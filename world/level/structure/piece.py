import numpy as np

from core.vec import Plane,Axis,DirectionFrom2DDataValue,Vec3i,BlockPos
from world.level.structure.util import BoundingBox

class StructurePiece:
    def __init__(self,dct):
        if not isinstance(dct,dict):
            self.genDepth=dct
            return 
        else:
            self.genDepth=dct['GD']
        if "BB" in dct:
            arr=dct["BB"]
            self.boundingBox=BoundingBox(arr[:3],arr[3:])
        if 'O' not in dct or dct['O']==-1:
            a=None
        else:
            a=DirectionFrom2DDataValue(dct['O'])
        self.setOrientation(a)
    def setOrientation(self,direction):
        self.orientation=direction
        if direction is None:
            pass
        else:
            pass

class ScatteredFeaturePiece(StructurePiece):
    def __init__(self,random,pos,size):
        super().__init__(0)
        self.size=size
        self.setOrientation(Plane.HORIZONTAL.getRandomDirection(random))
        self.boundingBox= BoundingBox(pos,pos+size-1) if self.orientation.axis==Axis.Z else BoundingBox(pos,pos+size[::-1]-1)

class TemplateStructurePiece(StructurePiece):
    def __init__(self,dct):
        super().__init__(dct)
        if isinstance(dct,dict):
            self.templatePosition=BlockPos(dct["TP"])

class BuriedTreasurePieces:
    class BuriedTreasurePiece(StructurePiece):
        def __init__(self,blockPos):
            super().__init__(0)
            self.boundingBox=BoundingBox(blockPos,blockPos)

class DesertPyramidPiece(ScatteredFeaturePiece):
    def __init__(self,random,vec2):
        super().__init__(random,np.insert(vec2,1,64),Vec3i([21,15,21]))

class IglooPieces:
    class IglooPiece(TemplateStructurePiece):
        def __init__(self,rot,n):
           super().__init__(0)
           self.rotation=rot

class JunglePyramidPiece(ScatteredFeaturePiece):
    def __init__(self,rnd,dct):
        super().__init__(rnd,np.insert(dct,1,64),Vec3i([12,10,15]))

class MineShaftPieces:
    class MineShaftPiece(StructurePiece):
        pass
    class MineShaftStairs(MineShaftPiece):
        pass
    class MineShaftCrossing(MineShaftPiece):
        pass
    class MineShaftCorridor(MineShaftPiece):
        pass
    class MineShaftRoom(MineShaftPiece):
        pass

class OceanMonumentPieces:
    class OceanMonumentPiece(StructurePiece):
        pass

class OceanRuinPieces:
    class OceanRuinPiece(TemplateStructurePiece):
        pass