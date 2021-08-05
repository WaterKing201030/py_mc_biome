from core.noise import PerlinSimplexNoise
from world.worldgen import WorldgenRandom

class Biome:
    TEMPERATURE_NOISE=PerlinSimplexNoise(WorldgenRandom(1234),(0,))
    FROZEN_TEMPERATURE_NOISE=PerlinSimplexNoise(WorldgenRandom(3456),(-2,-1,0))
    BIOME_INFO_NOISE=PerlinSimplexNoise(WorldgenRandom(2345),(0,))
    def __init__(self,dep,sca):
        self.depth=dep
        self.scale=sca
class BiomeBuilder:
    depth=None
    scale=None
    def setDepth(self,dep):
        self.depth=dep
        return self
    def setScale(self,sca):
        self.scale=sca
        return self
    def build(self):
        if (
            self.depth is None or
            self.scale is None
        ):raise ValueError("Missing parameters for biome:\n"+str(self))
        return Biome(self.depth,self.scale)
    def __str__(self):
        return (
            """
BiomeBuilder:
  depth=%f
  scale=%f
            """%(
                self.depth,
                self.scale
            )
        )

class VanillaBiomes:
    @staticmethod
    def giantTreeTaiga(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def birchForestBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def baseJungleBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def jungleBiome(dep=0.1,sca=0.2):
        return VanillaBiomes.baseJungleBiome(dep,sca)
    @staticmethod
    def jungleEdgeBiome():
        return VanillaBiomes.baseJungleBiome(0.1,0.2)
    @staticmethod
    def modifiedJungleEdgeBiome():
        return VanillaBiomes.baseJungleBiome(0.2,0.4)
    @staticmethod
    def modifiedJungleBiome():
        return VanillaBiomes.baseJungleBiome(0.2,0.4)
    @staticmethod
    def jungleHillsBiome():
        return VanillaBiomes.jungleBiome(0.45,0.3)
    @staticmethod
    def bambooJungleBiome(dep=0.1,sca=0.2):
        return VanillaBiomes.baseJungleBiome(dep,sca)
    @staticmethod
    def bambooJungleHillsBiome():
        return VanillaBiomes.bambooJungleBiome(0.45,0.3)
    @staticmethod
    def mountainBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def desertBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def plainsBiome(bl):
        return (
            BiomeBuilder()
                .setDepth(0.125)
                .setScale(0.05)
                .build()
        )
    @staticmethod
    def baseEndBiome():
        return (
            BiomeBuilder()
                .setDepth(0.1)
                .setScale(0.2)
                .build()
        )
    @staticmethod
    def endBarrensBiome():
        return VanillaBiomes.baseEndBiome()
    @staticmethod
    def theEndBiome():
        return VanillaBiomes.baseEndBiome()
    @staticmethod
    def endMidlandsBiome():
        return VanillaBiomes.baseEndBiome()
    @staticmethod
    def endHighlandsBiome():
        return VanillaBiomes.baseEndBiome()
    @staticmethod
    def smallEndIslandsBiome():
        return VanillaBiomes.baseEndBiome()
    @staticmethod
    def mushroomFieldsBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def baseSavannaBiome(dep,sca):
        return BiomeBuilder().setDepth(dep).setScale(sca).build()
    @staticmethod
    def savannaBiome(dep,sca):
        return VanillaBiomes.baseSavannaBiome(dep,sca)
    @staticmethod
    def savannaPlateauBiome():
        return VanillaBiomes.baseSavannaBiome(1.5,0.025)
    @staticmethod
    def baseBadlandsBiome(dep,sca):
        return BiomeBuilder().setDepth(dep).setScale(sca).build()
    @staticmethod
    def badlandsBiome(dep,sca):
        return VanillaBiomes.baseBadlandsBiome(dep,sca)
    @staticmethod
    def woodedBadlandsPlateauBiome(dep,sca):
        return VanillaBiomes.baseBadlandsBiome(dep,sca)
    @staticmethod
    def erodedBadlandsBiome():
        return VanillaBiomes.baseBadlandsBiome(0.1,0.2)
    @staticmethod
    def baseOceanBiome(isDeep):
        return (BiomeBuilder()
                    .setDepth(-1.8 if isDeep else -1.0)
                    .setScale(0.1)
                    .build()
        )
    @staticmethod
    def coldOceanBiome(isDeep):
        return VanillaBiomes.baseOceanBiome(isDeep)
    @staticmethod
    def oceanBiome(isDeep):
        return VanillaBiomes.baseOceanBiome(isDeep)
    @staticmethod
    def lukeWarmOceanBiome(isDeep):
        return VanillaBiomes.baseOceanBiome(isDeep)
    @staticmethod
    def warmOceanBiome():
        return VanillaBiomes.baseOceanBiome(False)
    @staticmethod
    def deepWarmOceanBiome():
        return VanillaBiomes.baseOceanBiome(True)
    @staticmethod
    def frozenOceanBiome(isDeep):
        return (
            BiomeBuilder()
                .setDepth(-1.8 if isDeep else -1.0)
                .setScale(0.1)
                .build()
        )
    @staticmethod
    def baseForestBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def forestBiome(dep,sca):
        return VanillaBiomes.baseForestBiome(dep,sca)
    @staticmethod
    def flowerForestBiome():
        return VanillaBiomes.baseForestBiome(0.1,0.4)
    @staticmethod
    def taigaBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def darkForestBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def swampBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def tundraBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def riverBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def beachBiome(dep,sca):
        return (
            BiomeBuilder()
                .setDepth(dep)
                .setScale(sca)
                .build()
        )
    @staticmethod
    def theVoidBiome():
        return (
            BiomeBuilder()
                .setDepth(0.1)
                .setScale(0.2)
                .build()
        )
    @staticmethod
    def netherWastesBiome():
        return (
            BiomeBuilder()
                .setDepth(0.1)
                .setScale(0.2)
                .build()
        )
    @staticmethod
    def soulSandValleyBiome():
        return (
            BiomeBuilder()
                .setDepth(0.1)
                .setScale(0.2)
                .build()
        )
    @staticmethod
    def basaltDeltasBiome():
        return (
            BiomeBuilder()
                .setDepth(0.1)
                .setScale(0.2)
                .build()
        )
    @staticmethod
    def crimsonForestBiome():
        return (
            BiomeBuilder()
                .setDepth(0.1)
                .setScale(0.2)
                .build()
        )
    @staticmethod
    def warpedForestBiome():
        return (
            BiomeBuilder()
                .setDepth(0.1)
                .setScale(0.2)
                .build()
        )

BIOMES={
    0:VanillaBiomes.oceanBiome(False),
    1:VanillaBiomes.plainsBiome(False),
    2:VanillaBiomes.desertBiome(0.125,0.05),
    3:VanillaBiomes.mountainBiome(1.0,0.5),
    4:VanillaBiomes.forestBiome(0.1,0.2),
    5:VanillaBiomes.taigaBiome(0.2, 0.2),
    6:VanillaBiomes.swampBiome(-0.2, 0.1),
    7:VanillaBiomes.riverBiome(-0.5, 0.0),
    8:VanillaBiomes.netherWastesBiome(),
    9:VanillaBiomes.theEndBiome(),
    10:VanillaBiomes.frozenOceanBiome(False),
    11:VanillaBiomes.riverBiome(-0.5, 0.0),
    12:VanillaBiomes.tundraBiome(0.125, 0.05),
    13:VanillaBiomes.tundraBiome(0.45, 0.3),
    14:VanillaBiomes.mushroomFieldsBiome(0.2, 0.3),
    15:VanillaBiomes.mushroomFieldsBiome(0.0, 0.025),
    16:VanillaBiomes.beachBiome(0.0, 0.025),
    17:VanillaBiomes.desertBiome(0.45, 0.3),
    18:VanillaBiomes.forestBiome(0.45, 0.3),
    19:VanillaBiomes.taigaBiome(0.45, 0.3),
    20:VanillaBiomes.mountainBiome(0.8, 0.3),
    21:VanillaBiomes.jungleBiome(),
    22:VanillaBiomes.jungleHillsBiome(),
    23:VanillaBiomes.jungleEdgeBiome(),
    24:VanillaBiomes.oceanBiome(True),
    25:VanillaBiomes.beachBiome(0.1, 0.8),
    26:VanillaBiomes.beachBiome(0.0, 0.025),
    27:VanillaBiomes.birchForestBiome(0.1, 0.2),
    28:VanillaBiomes.birchForestBiome(0.45, 0.3),
    29:VanillaBiomes.darkForestBiome(0.1, 0.2),
    30:VanillaBiomes.taigaBiome(0.2, 0.2),
    31:VanillaBiomes.taigaBiome(0.45, 0.3),
    32:VanillaBiomes.giantTreeTaiga(0.2, 0.2),
    33:VanillaBiomes.giantTreeTaiga(0.45, 0.3),
    34:VanillaBiomes.mountainBiome(1.0, 0.5),
    35:VanillaBiomes.savannaBiome(0.125, 0.05),
    36:VanillaBiomes.savannaPlateauBiome(),
    37:VanillaBiomes.badlandsBiome(0.1, 0.2),
    38:VanillaBiomes.woodedBadlandsPlateauBiome(1.5, 0.025),
    39:VanillaBiomes.badlandsBiome(1.5, 0.025),
    40:VanillaBiomes.smallEndIslandsBiome(),
    41:VanillaBiomes.endMidlandsBiome(),
    42:VanillaBiomes.endHighlandsBiome(),
    43:VanillaBiomes.endBarrensBiome(),
    44:VanillaBiomes.warmOceanBiome(),
    45:VanillaBiomes.lukeWarmOceanBiome(False),
    46:VanillaBiomes.coldOceanBiome(False),
    47:VanillaBiomes.deepWarmOceanBiome(),
    48:VanillaBiomes.lukeWarmOceanBiome(True),
    49:VanillaBiomes.coldOceanBiome(True),
    50:VanillaBiomes.frozenOceanBiome(True),
    127:VanillaBiomes.theVoidBiome(),
    129:VanillaBiomes.plainsBiome(True),
    130:VanillaBiomes.desertBiome(0.225, 0.25),
    131:VanillaBiomes.mountainBiome(1.0, 0.5),
    132:VanillaBiomes.flowerForestBiome(),
    133:VanillaBiomes.taigaBiome(0.3, 0.4),
    134:VanillaBiomes.swampBiome(-0.1, 0.3),
    140:VanillaBiomes.tundraBiome(0.425, 0.45000002),
    149:VanillaBiomes.modifiedJungleBiome(),
    151:VanillaBiomes.modifiedJungleEdgeBiome(),
    155:VanillaBiomes.birchForestBiome(0.2, 0.4),
    156:VanillaBiomes.birchForestBiome(0.55, 0.5),
    157:VanillaBiomes.darkForestBiome(0.2, 0.4),
    158:VanillaBiomes.taigaBiome(0.3, 0.4),
    160:VanillaBiomes.giantTreeTaiga(0.2, 0.2),
    161:VanillaBiomes.giantTreeTaiga(0.2, 0.2),
    162:VanillaBiomes.mountainBiome(1.0, 0.5),
    163:VanillaBiomes.savannaBiome(0.3625, 1.225),
    164:VanillaBiomes.savannaBiome(1.05, 1.2125001),
    165:VanillaBiomes.erodedBadlandsBiome(),
    166:VanillaBiomes.woodedBadlandsPlateauBiome(0.45, 0.3),
    167:VanillaBiomes.badlandsBiome(0.45, 0.3),
    168:VanillaBiomes.bambooJungleBiome(),
    169:VanillaBiomes.bambooJungleHillsBiome(),
    170:VanillaBiomes.soulSandValleyBiome(),
    171:VanillaBiomes.crimsonForestBiome(),
    172:VanillaBiomes.warpedForestBiome(),
    173:VanillaBiomes.basaltDeltasBiome(),
}