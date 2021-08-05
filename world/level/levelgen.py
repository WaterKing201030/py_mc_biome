class NoiseSamplingSettings:
    def __init__(self,xzs,ys,xzf,yf):
        self.xzScale=xzs
        self.yScale=ys
        self.xzFactor=xzf
        self.yFactor=yf

class NoiseSlideSettings:
    def __init__(self,t,s,o):
        self.target=t
        self.size=s
        self.offset=o

class NoiseSettings:
    def __init__(self,h,noiseSamplingSettings,topSlideSettings,bottomSlideSettings,noiseSizeHorizontal,noiseSizeVertical,densityFactor,densityOffset,useSimplexSurfaceNoise,randomDensityOffset,islandNoiseOverride,isAmplified):
        self.height=h
        self.noiseSamplingSettings=noiseSamplingSettings
        self.topSlideSettings=topSlideSettings
        self.bottomSlideSettings=bottomSlideSettings
        self.noiseSizeHorizontal=noiseSizeHorizontal
        self.noiseSizeVertical=noiseSizeVertical
        self.densityFactor=densityFactor
        self.densityOffset=densityOffset
        self.useSimplexSurfaceNoise=useSimplexSurfaceNoise
        self.randomDensityOffset=randomDensityOffset
        self.islandNoiseOverride=islandNoiseOverride
        self.isAmplified=isAmplified

class NoiseGeneratorSettings:
    def __init__(self,noiseSettings,bedrockRoofPosition,bedrockFloorPosition,seaLevel):
        self.structureSettings=structureSettings
        self.noiseSettings=noiseSettings
        self.bedrockRoofPosition=bedrockRoofPosition
        self.bedrockFloorPosition=bedrockFloorPosition
        self.seaLevel=seaLevel
    @classmethod
    def overworld(cls,isAmplified):
        d=0.9999999814507745
        return cls(
            NoiseSettings(
                256,
                NoiseSamplingSettings(d,d,80,160),
                NoiseSlideSettings(-10,3,0),
                NoiseSlideSettings(-30,0,0),
                1,2,
                1.0,-0.46875,
                True,True,False,isAmplified
            ),
            -10,0,63
        )
setattr(NoiseGeneratorSettings,'OVER_WORLD',NoiseGeneratorSettings.overworld(False))