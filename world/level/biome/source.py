import numpy as np

from core.vec import BlockPos
from world.level.biome.util import BiomeManager
from world.level.biome.new.layers import Layers

class BiomeSource(BiomeManager.NoiseBiomeSource):
    def __init__(self,lst):
        if lst and isinstance(lst[0],function):
            lst=[i() for i in lst]
        self.possibleBiomes=lst
    def findBiomeHorizontal(self,vec3,r,predicate,random,step=1,isNearest=False):
        quart=vec3>>2
        quartr=r>>2
        blockPos=None
        count=0
        start=0 if isNearest else quartr
        for i in range(0,quartr+1,step):
            for dz in range(-i,i+1,step):
                isEdgeZ=abs(dz)==i
                for dx in range(-i,i+1,step):
                    if isNearest and not abs(dx)==i and not isEdgeZ:
                        continue
                    q=np.array(quart+np.array([dx,0,dz],dtype=np.int32))
                    if not predicate(self.getNoiseBiome(q)):
                        continue
                    if blockPos is None or random.nextInt(count+1)==0:
                        blockPos=BlockPos(q<<2)
                        blockPos[1]=vec3[1]
                        if isNearest:
                            return blockPos
                    count+=1
        return blockPos
    def getBiomesWithin(self,vec3,r):
        qs=vec3-r>>2
        qe=vec3+r>>2
        ql=qe-qs+1
        biomes=set()
        for dz in range(ql[2]):
            for dx in range(ql[0]):
                for dy in range(ql[1]):
                    qpos=qs+np.array([dx,dy,dz])
                    biomes.add(self.getNoiseBiome(qpos))
        return biomes

class OverworldBiomeSource(BiomeSource):
    POSSIBLE_BIOMES=[]
    def __init__(self,seed,legacyBiomeInitLayer,largeBiomes,biomes):
        super().__init__(self.POSSIBLE_BIOMES)
        self.seed=seed
        self.legacyBiomeInitLayer=legacyBiomeInitLayer
        self.largeBiomes=largeBiomes
        self.biomes=biomes
        self.noiseBiomeLayer=Layers.getDefaultLayer(seed,legacyBiomeInitLayer,6 if largeBiomes else 4,4)
    def withSeed(self,seed):
        return type(self)(seed,self.legacyBiomeInitLayer,self.largeBiomes,self.biomes)
    def getNoiseBiome(self,vec3i):
        return self.noiseBiomeLayer.get(self.biomes,vec3i[(0,2),])