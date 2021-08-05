from util.java.javarandom import Random
import numpy as np
import time

class WorldgenRandom(Random):
    count=0
    def __init__(self,seed=np.int64(round(time.time()*1000))):
        super().__init__(seed)
    def next(self,bits):
        self.count+=1
        return super().next(bits)
    def consumeCount(self,n):
        for i in range(n):
            self.next(1)
    def setBaseChunkSeed(self,vec2):
        cx=vec2[0]
        cz=vec2[1]
        bcs=np.int64(cx)*341873128712+np.int64(cz)*132897987541
        self.setSeed(bcs)
        return bcs
    def setDecorationSeed(self,seed,vec2):
        bx=vec2[0]
        bz=vec2[1]
        self.setSeed(seed)
        seed2=self.nextLong()|1
        seed3=self.nextLong()|1
        ds=np.int64(bx)*seed2+np.int64(bz)*seed3^seed
        self.setSeed(ds)
        return ds
    def setFeatureSeed(self,seed,vec2):
        x=vec2[0]
        z=vec2[1]
        fs=seed+np.int64(x)+np.int64(10000*z)
        self.setSeed(fs)
        return fs
    def setLargeFeatureSeed(self,seed,vec2):
        cx=vec2[0]
        cz=vec2[1]
        self.setSeed(seed)
        seed2=self.nextLong()
        seed3=self.nextLong()
        lfs=np.int64(cx)*seed2^np.int64(cz)*seed3^seed
        self.setSeed(lfs)
        return lfs
    def setLargeFeatureWithSalt(self,seed,vec2,salt):
        x=vec2[0]
        z=vec2[1]
        lfws=np.int64(x)*341873128712+np.int64(z)*132897987541+seed+np.int64(salt)
        self.setSeed(lfws)
        return lfws
    @staticmethod
    def seedSlimeChunk(vec2,seed,salt):
        cx=vec2[0]
        cz=vec2[1]
        return Random(seed+np.int64(cx*cx*4987142)+np.int64(cx*5947611)+np.int64(cz*cz)*4392871+np.int64(cz*389711)^salt)