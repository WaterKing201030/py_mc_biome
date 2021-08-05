from enum import Enum
import numpy as np
from util import mth
from util.java import javarandom,javaconst

class Position(np.ndarray):pass

class Vec2(np.ndarray):pass
class Vec2(np.ndarray):
    def __new__(cls,input_array):
        obj=np.asarray(input_array,dtype=np.float32).view(cls)
        return obj
    def __eq__(self,obj):
        if self is obj:return True
        if not isinstance(obj,Vec2):return False
        return self[0]==obj[0] and self[1]==obj[1]
    ZERO      =__new__(Vec2,[0.0,0.0])
    ONE       =__new__(Vec2,[1.0,1.0])
    UNIT_X    =__new__(Vec2,[1.0,0.0])
    NEG_UNIT_X=__new__(Vec2,[-1.0,0.0])
    UNIT_Y    =__new__(Vec2,[0.0,1.0])
    NEG_UNIT_Y=__new__(Vec2,[0.0,-1.0])
    MAX       =__new__(Vec2,[javaconst.FLOAT_MAX_VALUE,javaconst.FLOAT_MAX_VALUE])
    MIN       =__new__(Vec2,[javaconst.FLOAT_MIN_VALUE,javaconst.FLOAT_MIN_VALUE])
    @property
    def x(self):return self[0]
    @property
    def y(self):return self[1]

class Vec3i(np.ndarray):pass
class Vec3i(np.ndarray):
    def __new__(cls,input_array):
        obj=np.asarray(mth.vfloor(input_array),dtype=np.int32).view(cls)
        return obj
    def __eq__(self,obj):
        if self is obj:return True
        if not isinstance(obj,Vec3i):return False
        return self[0]==obj[0] and self[1]==obj[1] and self[2]==obj[2]
    def __hash__(self):
        return self.getX()+31*(self.getY()+31*self.getZ())
    @property
    def x(self):return self[0]
    @property
    def y(self):return self[1]
    @property
    def z(self):return self[2]
    def getX(self):
        return self[0]
    def getY(self):
        return self[1]
    def getZ(self):
        return self[2]
    def compare(self,vec3i):
        if self.getY()==vec3i.getY():
            if self.getZ()==vec3i.getZ():
                return self.getX()-vec3i.getX()
            return self.getZ()-vec3i.getZ()
        return self.getY()-vec3i.getY()
    def setX(self,x):
        self[0]=x
    def setY(self,y):
        self[1]=y
    def setZ(self,z):
        self[2]=z
    def above(self,n=1):
        self.relative(Direction.UP,n)
    def below(self,n=1):
        self.relative(Direction.DOWN,n)
    def relative(self,direct,dis):
        if dis==0:return self
        return self+direct.normal*dis
    def cross(self,vec3i):
        return np.cross(self,vec3i).view(Vec3i)
    def closerThan(self,vec3i,dis):
        return self.distSqr(vec3i,isinstance(vec3i,Vec3i))<dis*dis
    def distSqr(self,vec3,bl=True):
        d4=np.float64(0.5 if bl else 0.0)
        return sum((self.astype(np.float64)+vec3.astype(np.float64)-d4)**2)
    def distManhattan(self,vec3i):
        return sum(abs(vec3i-self))
    def get(self,ax):
        return ax.choose(self)

class AxisDirection(Enum):
    POSITIVE=( 1,"Towards positive")
    NEGATIVE=(-1,"Towards negative")
    def __init__(self,n,s):
        self.step=n
        self.dname=s
    def getStep(self):
        return self.step
    def __str__(self):
        return self.dname
    @property
    def opposite(self):
        return self.NEGATIVE if self==self.POSITIVE else self.POSITIVE

class Axis(Enum):
    X=("x",0)
    Y=("y",1)
    Z=("z",2)
    def __init__(self,s,i):
        self.dname=s
        self.choose=lambda a:a[i]
    def isVertical(self):
        return self==self.Y
    def isHorizontal(self):
        return self==self.X or self==self.Z
    def __str__(self):
        return self.dname
    def getPlane(self):
        if self.isHorizontal():return Plane.HORIZONTAL
        elif self.isVertical():return Plane.VERTICAL
        raise Exception("操作者可能不处于三维空间中")
    @classmethod
    def getRandom(cls,random):
        return javarandom.getRandom(list(cls),random)

class Direction(Enum):
    DOWN =(0,1,-1, "down",AxisDirection.NEGATIVE,Axis.Y,Vec3i([ 0,-1, 0]))
    UP   =(1,0,-1,   "up",AxisDirection.POSITIVE,Axis.Y,Vec3i([ 0, 1, 0]))
    NORTH=(2,3, 2,"north",AxisDirection.NEGATIVE,Axis.Z,Vec3i([ 0, 0,-1]))
    SOUTH=(3,2, 0,"south",AxisDirection.POSITIVE,Axis.Z,Vec3i([ 0, 0, 1]))
    WEST =(4,5, 1, "west",AxisDirection.NEGATIVE,Axis.X,Vec3i([-1, 0, 0]))
    EAST =(5,4, 3, "east",AxisDirection.POSITIVE,Axis.X,Vec3i([ 1, 0, 0]))
    def __init__(self,d3,od3,d2,s,ad,a,v):
        self.data3d=d3
        self.data2d=d2
        self.oppositeIndex=od3
        self.dname=s
        self.axis=a
        self.axisDirection=ad
        self.normal=v
DIRECTION_VALUES=list(Direction)
DIRECTION_BY_2D_DATA=[sorted([i for i in Direction if i.axis.isHorizontal()],key=lambda x:x.data2d)]
def DirectionFrom2DDataValue(n):
    return DIRECTION_BY_2D_DATA[abs(n%len(DIRECTION_BY_2D_DATA))]

class Plane(Enum):
    HORIZONTAL=([Direction.NORTH,Direction.EAST,Direction.SOUTH,Direction.WEST],[Axis.X,Axis.Z])
    VERTICAL  =([Direction.UP,Direction.DOWN],[Axis.Y])
    def __init__(self,direction,ax):
        self.faces=direction
        self.axis=ax
    def getRandomDirection(self,random):
        return javarandom.getRandom(self.faces,random)
    def getRandomAxis(self,random):
        return javarandom.getRandom(self.axis,random)

class Vec3(Position):pass
class Vec3(Position):
    def __new__(cls,input_array):
        obj=np.asarray(input_array,dtype=np.float64).view(cls)
        return obj
    ZERO=__new__(Vec3,[0.0,0.0,0.0])
    @property
    def x(self):return self[0]
    @property
    def y(self):return self[1]
    @property
    def z(self):return self[2]
    @classmethod
    def fromRGB24(cls,rgb):
        r=np.float64(rgb>>16&0xFF)/255.0
        g=np.float64(rgb>>8&0xFF)/255.0
        b=np.float64(rgb&0xFF)/255.0
        return cls([r,g,b])
    @classmethod
    def atCenterOf(cls,vec3i):
        return (vec3i+0.5).astype(np.float64).view(cls)
    @classmethod
    def atLowerCornerOf(cls,vec3i):
        return vec3i.astype(np.float64).view(cls)
    @classmethod
    def atBottomCenterOf(cls,vec3i):
        return (vec3i+np.array([0.5,0.0,0.5])).astype(np.float64).view(cls)
    @classmethod
    def upFromBottomCenterOf(cls,vec3i,d):
        return (vec3i+np.array([0.5,d,0.5])).astype(np.float64).view(cls)
    def vectorTo(self,vec3):
        return vec3-self
    def normalize(self):
        l=self.length
        if l<1.0e-4:return self.ZERO
        return self/l
    def dot(self,vec3):
        return np.dot(self,vec3)
    def cross(self,vec3):
        return np.cross(self,vec3).view(Vec3)
    def distanceToSqr(self,vec3):
        return sum((vec3-self)**2)
    def distanceTo(self,vec3):
        return mth.sqrt(self.distanceToSqr(vec3))
    def closerThan(self,position,d):
        return self.distanceToSqr(position)<d*d
    def scale(self,d):
        return self*d
    @property
    def reverse(self):
        return self.scale(-1.0)
    def lengthSqr(self):
        return sum(self**2)
    @property
    def length(self):
        return mth.sqrt(self.lengthSqr())
    def __eq__(self,obj):
        if self is obj:return True
        if not isinstance(obj,Vec3):return False
        return self[0]==obj[0] and self[1]==obj[1] and self[2]==obj[2]
    def __str__(self):
        return "(%f,%f,%f)"%tuple(self)

class PositionImpl(Position):
    def __new__(cls,input_array):
        obj=np.asarray(input_array,dtype=np.float64).view(cls)
        return obj
    @property
    def x(self):return self[0]
    @property
    def y(self):return self[1]
    @property
    def z(self):return self[2]

class BlockPos(Vec3i):pass
class BlockPos(Vec3i):
    def __new__(cls, input_array):
        return super().__new__(cls,input_array)
    PACKED_X_LENGTH=np.int32(1+mth.floorlog2(mth.smallestEncompassingPowerOfTwo(30000000)))
    PACKED_Z_LENGTH=PACKED_X_LENGTH
    PACKED_Y_LENGTH=64-PACKED_X_LENGTH-PACKED_Z_LENGTH
    PACKED_X_MASK=(np.int64(1)<<PACKED_X_LENGTH)-1
    PACKED_Y_MASK=(np.int64(1)<<PACKED_Y_LENGTH)-1
    PACKED_Z_MASK=(np.int64(1)<<PACKED_Z_LENGTH)-1
    Z_OFFSET=PACKED_Y_LENGTH
    X_OFFSET=PACKED_Y_LENGTH+PACKED_Z_LENGTH
    Y_OFFSET=0
    PACKED_LENGTH=np.array([PACKED_X_LENGTH,PACKED_Y_LENGTH,PACKED_Z_LENGTH],dtype=np.int32)
    PACKED_MASK=np.array([PACKED_X_MASK,PACKED_Y_MASK,PACKED_Z_MASK],dtype=np.int64)
    OFFSET=np.array([X_OFFSET,Y_OFFSET,Z_OFFSET],dtype=np.int32)
    @staticmethod
    def offsetLong(l,d):
        if isinstance(d,Direction):d=d.normal
        if d[0]==0 and d[1]==0 and d[2]==0:return l
        return BlockPos.asLong(BlockPos.of(l)+d)
    def offset(self,d):
        return BlockPos(self+d)
    @staticmethod
    def getLongX(l):
        return np.int32(l<<64-BlockPos.X_OFFSET-BlockPos.PACKED_X_LENGTH>>64-BlockPos.PACKED_X_LENGTH)
    @staticmethod
    def getLongY(l):
        return np.int32(l<<64-BlockPos.Y_OFFSET-BlockPos.PACKED_Y_LENGTH>>64-BlockPos.PACKED_Y_LENGTH)
    @staticmethod
    def getLongZ(l):
        return np.int32(l<<64-BlockPos.Z_OFFSET-BlockPos.PACKED_Z_LENGTH>>64-BlockPos.PACKED_Z_LENGTH)
    @classmethod
    def of(cls,l):
        return cls(l<<64-BlockPos.OFFSET-BlockPos.PACKED_LENGTH>>64-BlockPos.PACKED_LENGTH)
    def asLong(self):
        l=0
        l|=(self.x&self.PACKED_X_MASK)<<self.X_OFFSET
        l|=(self.y&self.PACKED_Y_MASK)<<self.Y_OFFSET
        l|=(self.z&self.PACKED_Z_MASK)<<self.Z_OFFSET
        return l
    @staticmethod
    def getFlastIndex(l):
        return l & 0xFFFFFFFFFFFFFFF0
    def relative(self,d,n=1):
        if isinstance(d,Direction):
            if n==0:return self
            return BlockPos(self+d.normal*n)
        elif isinstance(d,Axis):
            if n==0:return self
            x=n if d==Axis.X else 0
            y=n if d==Axis.Y else 0
            z=n if d==Axis.Z else 0
            return BlockPos(self+np.ndarray([x,y,z]))
    def above(self,n=1):
        return self.relative(Direction.UP,n)
    def below(self,n=1):
        return self.relative(Direction.DOWN,n)
    def north(self,n=1):
        return self.relative(Direction.NORTH,n)
    def south(self,n=1):
        return self.relative(Direction.SOUTH,n)
    def west(self,n=1):
        return self.relative(Direction.WEST,n)
    def east(self,n=1):
        return self.relative(Direction.EAST,n)
    @property
    def x(self):return self[0]
    @property
    def y(self):return self[1]
    @property
    def z(self):return self[2]

class ChunkPos(np.ndarray):pass
class ChunkPos(np.ndarray):
    def __new__(cls,input_array):
        if isinstance(input_array,np.int64) or isinstance(input_array,int):
            l=input_array
            input_array=np.array([l,l>>32],dtype=np.int32)
        if isinstance(input_array,BlockPos):
            input_array=input_array[(0,2),]>>4
        obj=np.asarray(input_array,dtype=np.int32).view(cls)
        return obj
    @property
    def x(self):return self[0]
    @property
    def z(self):return self[1]
    def toLong(self):
        ChunkPos.asLong(self)
    @staticmethod
    def asLong(vec2):
        return np.int64(vec2[0])&0xFFFFFFFF|(np.int64(vec2[1])&0xFFFFFFFF)<<32
    @staticmethod
    def getX(l):
        return np.int32(l&0xFFFFFFFF)
    @staticmethod
    def getZ(l):
        return np.int32(l>>32&0xFFFFFFFF)# 略有不同，理论无影响
    def __hash__(self):
        n=np.int32(1664525*self.x+1013904223)
        n2=np.int32(1664525*(self.z^0xDEADBEEF)+1013904223)
        return n^n2
    def __eq__(self,obj):
        if self is obj:return True
        if isinstance(obj,ChunkPos):return self.x==obj.x and self.z==obj.z
        return False
    @property
    def minBlockX(self):return self.x<<4
    @property
    def minBlockZ(self):return self.z<<4
    @property
    def maxBlockX(self):return (self.x<<4)+15
    @property
    def maxBlockZ(self):return (self.z<<4)+15
    @property
    def regionX(self):return self.x>>5
    @property
    def regionZ(self):return self.z>>5
    @property
    def regionLocalX(self):return self.x&0x1F
    @property
    def regionLocalZ(self):return self.z&0x1F
    def __str__(self):
        return "[%d,%d]"%tuple(self)

class SectionPos(Vec3i):pass
class SectionPos(Vec3i):
    def __new__(cls, input_array,y=None):
        if isinstance(input_array,np.int64) or isinstance(input_array,int):
            input_array=np.array([input_array<<0>>42,input_array<<44>>44,input_array<<22>>42],dtype=np.int32)
        if isinstance(input_array,BlockPos):
            input_array=input_array>>4
        if y is not None:
            input_array=np.array([input_array[0],y,input_array[2]])
        return super().__new__(cls,input_array)
    @staticmethod
    def getLongX(l):
        return np.int32(l<<0>>42)
    @staticmethod
    def getLongY(l):
        return np.int32(l<<44>>44)
    @staticmethod
    def getLongZ(l):
        return np.int32(l<<22>>42)
    @property
    def x(self):return self[0]
    @property
    def y(self):return self[1]
    @property
    def z(self):return self[2]
    @property
    def minBlockX(self):return self.x<<4
    @property
    def minBlockY(self):return self.y<<4
    @property
    def minBlockZ(self):return self.z<<4
    @property
    def maxBlockX(self):return (self.x<<4)+15
    @property
    def maxBlockY(self):return (self.y<<4)+15
    @property
    def maxBlockZ(self):return (self.z<<4)+15
    def asLong(self):
        l=np.int64(0)
        l|=(self[0]&0x3FFFFF)<<42
        l|=(self[1]&0xFFFFF)<<0
        l|=(self[2]&0x3FFFFF)<<20
        return l
    @classmethod
    def blockToSection(cls,blockPos):
        return cls(blockPos>>4)
    def sectionToBlock(self):
        return BlockPos(self<<4)
    @property
    def chunk(self):return ChunkPos(self[(0,2),])
    @property
    def origin(self):return BlockPos(self<<4)
    @property
    def center(self):return self.origin.offset(np.array([8,8,8]))