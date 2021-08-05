""" from world.level.biome.new.layers import Layers
import numpy as np
from world.level.biome.biomes import BIOMES """

import numpy as np
from util.java.javarandom import Random
from core.noise import SimplexNoise,ImprovedNoise

from world.level.biome.source import OverworldBiomeSource
from world.level.biome.util import FuzzyOffsetBiomeZoomer
from core.vec import BlockPos

np.set_printoptions(threshold=np.inf,linewidth=np.inf)

seed=np.int64(-235687325506561462)
noiseBiomeSource=OverworldBiomeSource(seed,False,False,[])
biomeZoomer=FuzzyOffsetBiomeZoomer()
arr=np.zeros((6,6),dtype=np.int32)
target=np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [7,7,7,7,7,7,1,1,1,1,1,1,1,1,1,1],
    [7,7,7,7,7,7,7,1,1,1,1,1,1,1,1,1],
    [7,7,7,7,7,7,7,7,1,1,1,1,1,1,1,1],
    [7,7,7,7,7,7,7,7,7,1,1,7,1,1,1,1],
    [7,7,7,7,7,7,7,7,7,7,7,7,7,7,1,1],
    [7,7,7,7,7,7,7,7,7,7,7,7,7,7,1,7],
    [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,1,7,7,7,7,7,7,7,7,7,7],
    [7,7,1,1,1,1,1,1,7,7,7,7,7,7,7,7],
    [7,7,1,1,1,1,1,1,7,7,7,7,7,7,7,7],
    [7,7,1,1,1,1,1,1,7,7,7,7,7,7,7,7],
    [7,1,1,1,1,1,1,1,1,1,1,7,7,7,7,7]
],dtype=np.int32)
height=np.array([
    [63,63,63,63,63,63,62,62,62,62,62,62,62,61,61,60],
    [62,62,62,62,62,62,62,62,62,62,62,62,62,61,61,60],
    [61,61,61,61,61,61,62,62,62,62,62,62,62,62,61,60],
    [59,60,60,60,60,61,61,62,62,62,62,62,63,62,61,60],
    [57,57,58,58,58,60,61,61,62,62,62,63,63,62,61,60],
    [57,57,58,58,59,60,61,61,62,62,62,62,62,62,61,60],
    [57,57,58,58,59,60,60,61,62,62,62,62,62,61,61,60],
    [56,57,58,59,59,60,60,61,61,61,61,61,61,60,60,60],
    [56,57,58,59,60,60,60,60,61,60,60,60,60,60,60,60],
    [58,59,60,61,61,61,61,61,61,61,60,60,60,60,60,60],
    [60,60,61,62,62,62,62,61,61,61,61,61,61,61,61,61],
    [61,61,62,62,63,63,62,62,61,61,61,61,61,61,61,61],
    [61,62,62,63,64,63,63,62,61,61,61,61,61,62,62,62],
    [62,62,63,63,63,63,63,63,62,62,62,63,63,63,63,63],
    [62,62,63,63,63,63,63,63,63,63,63,63,63,63,63,64],
    [62,63,63,63,63,63,63,63,63,64,64,64,65,65,65,65]
]).transpose()+1
x=80 #-40330*16
z=80 #15241*16
arr=np.zeros((16,16),dtype=np.int32)
for i in range(16):
    for j in range(16):
        arr[i][j]=biomeZoomer.getBiome(seed,BlockPos([x+i,0,z+j]),noiseBiomeSource)
print(arr.transpose())
#print(biomeZoomer.getBiome(seed,BlockPos([92,0,95]),noiseBiomeSource))

arr=np.zeros((32,32),dtype=np.int32)
for i in range(32):
    for j in range(32):
        arr[i][j]=noiseBiomeSource.noiseBiomeLayer.get({},np.array([i,j]))
print(arr.transpose())