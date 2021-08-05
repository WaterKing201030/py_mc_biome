import math
import numpy as np

from util.java.javarandom import Random
import util.mth as mth
from core.vec import ChunkPos
from world.worldgen import WorldgenRandom
from core.noise import PerlinNoise,PerlinSimplexNoise,SimplexNoise

class ChunkGenerator:
    def __init__(self,biomeSource,seed=np.int64(0),runtimeBiomeSource=None):
        if runtimeBiomeSource is None:runtimeBiomeSource=biomeSource
        self.biomeSource=biomeSource
        self.runtimeBiomeSource=runtimeBiomeSource
        self.strongholdSeed=seed
    @property
    def seaLevel(self):
        return 63
    @property
    def genDepth(self):
        return 256

class NoiseBasedChunkGenerator(ChunkGenerator):
    BIOME_WEIGHTS=[10/mth.sqrt(i**2+j**2+0.2) for j in range(-2,3) for i in range(-2,3)]
    def __init__(self,biomeSource,seed,supplier):
        super().__init__(biomeSource,supplier().structureSettings,seed,biomeSource)
        self.seed=seed
        noiseGeneratorSettings=supplier()
        self.settings=supplier
        noiseSettings=noiseGeneratorSettings.noiseSettings
        self.height=noiseSettings.height                                            # 256
        self.chunkHeight=noiseSettings.noiseSizeVertical*4                          # 8
        self.chunkWidth=noiseSettings.noiseSizeHorizontal*4                         # 4
        self.chunkCountX=16//self.chunkWidth                                        # 4
        self.chunkCountY=noiseSettings.height//self.chunkHeight                     # 32
        self.chunkCountZ=16//self.chunkWidth                                        # 4
        self.random=WorldgenRandom(seed)
        self.minLimitPerlinNoise=PerlinNoise(self.random,list(range(-15,1)))
        self.maxLimitPerlinNoise=PerlinNoise(self.random,list(range(-15,1)))
        self.mainPerlinNoise=PerlinNoise(self.random,list(range(-7,1)))
        if noiseSettings.useSimplexSurface:                                         # True
            self.surfaceNoise=PerlinSimplexNoise(self.random,list(range(-3,1)))
        else:
            self.surfaceNoise=PerlinNoise(self.random,list(range(-3,1)))
        self.random.consumeCount(2620)
        self.depthNoise=PerlinNoise(self.random,list(range(-15,1)))
        if noiseSettings.islandNoiseOverride:                                       # False
            worldgenRandom=WorldgenRandom(seed)
            worldgenRandom.consumeCount(17292)
            self.islandNoise=SimplexNoise(worldgenRandom)
        else:
            self.islandNoise=None
    @property
    def seaLevel(self):                                                             # 63
        return self.settings().seaLevel
    @property
    def genDepth(self):
        return self.height
    def getRandomDensity(self,vec2):
            d=self.depthNoise.getValue(np.insert(vec2*200,1,10.0),1.0,0.0,True)
            d2=-d*0.3 if d<0 else d
            d3=d2*24.575625-2.0
            if d3<0:
                return d3*0.009486607142857142
    def sampleAndClampNoise(self,vec3i,xzs,ys,xzf,yf):
        d5=0.0
        d6=0.0
        d7=0.0
        d8=1.0
        for i in range(16):
            wx=PerlinNoise.wrap(vec3i[0]*xzs*d8)
            wy=PerlinNoise.wrap(vec3i[1]*ys*d8)
            wz=PerlinNoise.wrap(vec3i[2]*xzs*d8)
            w=np.array([wx,wy,wz])
            d12=ys*d8
            improvedNoise3=self.minLimitPerlinNoise.getOctaveNoise(i)
            if improvedNoise3 is not None:
                d5=d5+improvedNoise3.noise(w,d12,vec3i[1]*d12)/d8
            improvedNoise=self.maxLimitPerlinNoise.getOctaveNoise(i)
            if improvedNoise is not None:
                d6=d6+improvedNoise.noise(w,d12,vec3i[1]*d12)/d8
            if i<8:
                improvedNoise2=self.mainPerlinNoise.getOctaveNoise(i)
                if improvedNoise2 is not None:
                    wx2=PerlinNoise.wrap(vec3i[0]*xzf*d8)
                    wy2=PerlinNoise.wrap(vec3i[1]*yf*d8)
                    wz2=PerlinNoise.wrap(vec3i[2]*xzf*d8)
                    w2=np.array([wx2,wy2,wz2])
                    d7=d7+improvedNoise2.noise(w2,yf*d8,vec3i[1]*yf*d8)/d8
            d8/=2
        return mth.clampedLerp(d5/512,d6/512,(d7/10+1)/2)
    def fillNoiseColumn(self,arrd,vec2i):
        noiseSettings=self.settings().noiseSettings
        if self.islandNoise is not None:
            pass
        else:
            f=0.0
            f2=0.0
            f3=0.0
            n3=2
            y=self.seaLevel
            vec3i=np.insert(vec2i,1,y)
            biomeDepthO=self.biomeSource.getNoiseBiome(vec3i).depth
            for dx in range(-2,3):
                for dz in range(-2,3):
                    biome=self.biomeSource.getNoiseBiome(vec3i+[dx,0,dz])
                    biomeDepth=biome.depth
                    biomeScale=biome.scale
                    if noiseSettings.isAmplified and biomeDepth>0:
                        f5=1+biomeDepth*2
                        f6=1+biomeScale*2
                    else:
                        f5=biomeDepth
                        f6=biomeScale
                    f9=0.5 if biomeDepth>biomeDepthO else 1.0
                    f10=f9*self.BIOME_WEIGHTS[dx+2+(dz+2)*5]/(f5+2)
                    f+=f6*f10
                    f2+=f5*f10
                    f3+=f10
            f11=f2/f3
            f12=f/f3
            d3=f11*0.5-0.125
            d2=f12*0.9+0.1
            d4=d3*0.265625
            d=96/d2
        d5=684.412*noiseSettings.noiseSamplingSettings.xzScale
        d6=684.412*noiseSettings.noiseSamplingSettings.yScale
        d7=d5/noiseSettings.noiseSamplingSettings.xzFactor
        d8=d5/noiseSettings.noiseSamplingSettings.yFactor
        d3=noiseSettings.topSlideSettings.target
        d2=noiseSettings.topSlidSettings.size
        d9=noiseSettings.topSlideSettings.offset
        d10=noiseSettings.bottomSlideSettings.target
        d11=noiseSettings.bottomSlideSettings.size
        d12=noiseSettings.bottomSlideSettings.offset
        d13=self.getRandomDensity(vec2i) if noiseSettings.getRandomDensityOffset else 0.0
        d14=noiseSettings.densityFactor
        d15=noiseSettings.densityOffset
        for i in range(self.chunkCountY+1):
            d17=self.sampleAndClampNoise(np.insert(vec2i,1,0),d5,d6,d7,d8)
            d18=1.0-i*2.0/self.chunkCountY
            d19=d18*d14+d15
            d20=(d19+d4)*d
            if d20>0:
                d17+=d20*4
            else:
                d17+=d20
            if d2>0:
                d16=(self.chunkCountY-i-d9)/d2
                d17=mth.clampedLerp(d3,d17,d16)
            if d11>0:
                d16=(i-d12)/d11
                d17=mth.clampedLerp(d10,d17,d16)
            arrd[i]=d17
    def makeAndFillNoiseColum(self,vec2):
        arrd=[0.0]*(self.chunkCountY+1)
        self.fillNoiseColumn(arrd,vec2)
        return arrd