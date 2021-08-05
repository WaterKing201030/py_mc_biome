import numpy as np
import util.mth as mth
from util.lcg import lcgnext
from util.java.javamath import floorMod

class BiomeZoomer:pass

class FuzzyOffsetBiomeZoomer(BiomeZoomer):
    def getBiome(self,seed,blockPos,noiseBiomeSource):
        off=blockPos-2
        offQuart=off>>2
        offRate=np.float64(off&3)/4
        arrd=[self.getFiddledDistance(seed,offQuart+list(map(bool,[i&4,i&2,i&1])),offRate-list(map(bool,[i&4,i&2,i&1]))) for i in range(8)]
        d7=min(arrd)
        n7=arrd.index(d7)
        #return n7
        return noiseBiomeSource.getNoiseBiome(offQuart+list(map(bool,[n7&4,n7&2,n7&1])))
    def getFiddledDistance(self,seed,vec3i,vec3d):
        l2=seed
        for i in vec3i:
            l2=lcgnext(l2,i)
        for i in vec3i:
            l2=lcgnext(l2,i)
        d4=self.getFiddle(l2)
        l2=lcgnext(l2,seed)
        d5=self.getFiddle(l2)
        l2=lcgnext(l2,seed)
        d6=self.getFiddle(l2)
        return sum((vec3d+[d4,d5,d6])**2)
    def getFiddle(self,l):
        d=np.float64(floorMod(l>>24,1024)/1024)
        return (d-0.5)*0.9

class BiomeManager:
    class NoiseBiomeSource:pass
    def __init__(self,noiseBiomeSource,seed,biomeZoomer):
        self.noiseBiomeSource=noiseBiomeSource
        self.biomeZoomSeed=seed
        self.zoomer=biomeZoomer
    def withDifferentSource(self,biomeSource):
        type(self)(biomeSource,self.biomeZoomSeed,self.zoomer)
    def getBiome(self,blockPos):
        return self.zoomer.getBiome(self.biomeZoomSeed,blockPos,self.noiseBiomeSource)
    def getNoiseBiomeAtQuart(self,vec3i):
        return self.noiseBiomeSource.getNoiseBiome(vec3i)
    def getNoiseBiomeAtPosition(self,vec3):
        self.getNoiseBiomeAtQuart(mth.vfloor(vec3)>>2)