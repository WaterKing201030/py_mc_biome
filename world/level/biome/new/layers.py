import numpy as np

from world.level.biome.new.context import LazyAreaContext
from world.level.biome.biomes import BIOMES

class Layer:
    def __init__(self,areaFactory):
        self.area=areaFactory()
    def get(self,dct,vec2):
        biomeId=self.area.get(vec2)
        if biomeId not in BIOMES:
            raise KeyError("Unknown biome id %d"%biomeId)
        #return BIOMES[biomeId]
        return biomeId

class Layers:
    class Category:
        NONE=0
        TAIGA=1
        EXTREME_HILLS=2
        JUNGLE=3
        MESA=4
        BADLANDS_PLATEAU=5
        PLAINS=6
        SAVANNA=7
        ICY=8
        BEACH=9
        FOREST=10
        OCEAN=11
        DESERT=12
        RIVER=13
        SWAMP=14
        MUSHROOM=15
    @staticmethod
    def isShallowOcean(n):
        return n in (44,45,0,46,10)
    @staticmethod
    def isOcean(n):
        return n in (44,45,0,46,10,47,48,24,49,50)
    @staticmethod
    def isSame(n,n2):
        if n==n2:return True
        return Layers.CATEGORIES[n]==Layers.CATEGORIES[n2]
    @staticmethod
    def zoom(salt,areaTransformer1,areaFactory,times,contextSupplier):
        areaFactory2=areaFactory
        for i in range(times):
            areaFactory2=areaTransformer1.run(contextSupplier(salt+i),areaFactory2)
        return areaFactory2
    @staticmethod
    def getDefaultLayer(seed,legacyBiomeInitLayer,biomeSize,riverSize):
        contextSupplier=lambda salt:LazyAreaContext(seed,salt)
        biomeAreaFactory=None
        tempAreaFactory=IslandLayer().run(contextSupplier(1))
        tempAreaFactory=ZoomLayerFuzzy().run(contextSupplier(2000),tempAreaFactory)
        tempAreaFactory=AddIslandLayer().run(contextSupplier(1),tempAreaFactory)
        tempAreaFactory=ZoomLayer().run(contextSupplier(2001),tempAreaFactory)
        tempAreaFactory=AddIslandLayer().run(contextSupplier(2),tempAreaFactory)
        tempAreaFactory=AddIslandLayer().run(contextSupplier(50),tempAreaFactory)
        tempAreaFactory=AddIslandLayer().run(contextSupplier(70),tempAreaFactory)
        tempAreaFactory=RemoveTooMuchOceanLayer().run(contextSupplier(2),tempAreaFactory)
        oceanAreaFactory=OceanLayer().run(contextSupplier(2))
        oceanAreaFactory=Layers.zoom(2001,ZoomLayer(),oceanAreaFactory,6,contextSupplier)
        tempAreaFactory=AddSnowLayer().run(contextSupplier(2),tempAreaFactory)
        tempAreaFactory=AddIslandLayer().run(contextSupplier(3),tempAreaFactory)
        tempAreaFactory=AddEdgeLayer.CoolWarm().run(contextSupplier(2),tempAreaFactory)
        tempAreaFactory=AddEdgeLayer.HeatIce().run(contextSupplier(2),tempAreaFactory)
        tempAreaFactory=AddEdgeLayer.IntroduceSpecial().run(contextSupplier(3),tempAreaFactory)
        tempAreaFactory=ZoomLayer().run(contextSupplier(2002),tempAreaFactory)
        tempAreaFactory=ZoomLayer().run(contextSupplier(2003),tempAreaFactory)
        tempAreaFactory=AddIslandLayer().run(contextSupplier(4),tempAreaFactory)
        tempAreaFactory=AddMushroomIslandLayer().run(contextSupplier(5),tempAreaFactory)
        tempAreaFactory=AddDeepOceanLayer().run(contextSupplier(4),tempAreaFactory)
        #tempAreaFactory=Layers.zoom(1000,ZoomLayer(),tempAreaFactory,0,contextSupplier)
        riverAreaFactory=tempAreaFactory
        #riverAreaFactory=Layers.zoom(1000,ZoomLayer(),riverAreaFactory,0,contextSupplier)
        riverAreaFactory=RiverInitLayer().run(contextSupplier(100),riverAreaFactory)
        biomeAreaFactory=tempAreaFactory
        biomeAreaFactory=BiomeInitLayer(legacyBiomeInitLayer).run(contextSupplier(200),biomeAreaFactory)
        biomeAreaFactory=RareBiomeLargeLayer().run(contextSupplier(1001),biomeAreaFactory)
        biomeAreaFactory=Layers.zoom(1000,ZoomLayer(),biomeAreaFactory,2,contextSupplier)
        biomeAreaFactory=BiomeEdgeLayer().run(contextSupplier(1000),biomeAreaFactory)
        hillsAreaFactory=riverAreaFactory
        hillsAreaFactory=Layers.zoom(1000,ZoomLayer(),hillsAreaFactory,2,contextSupplier)
        biomeAreaFactory=RegionHillsLayer().run(contextSupplier(1000),biomeAreaFactory,hillsAreaFactory)
        riverAreaFactory=Layers.zoom(1000,ZoomLayer(),riverAreaFactory,2,contextSupplier)
        riverAreaFactory=Layers.zoom(1000,ZoomLayer(),riverAreaFactory,riverSize,contextSupplier)
        riverAreaFactory=RiverLayer().run(contextSupplier(1),riverAreaFactory)
        riverAreaFactory=SmoothLayer().run(contextSupplier(1000),riverAreaFactory)
        biomeAreaFactory=RareBiomeLargeLayer().run(contextSupplier(1001),biomeAreaFactory)
        for i in range(biomeSize):
            biomeAreaFactory=ZoomLayer().run(contextSupplier(1000+i),biomeAreaFactory)
            if i==0:
                biomeAreaFactory=AddIslandLayer().run(contextSupplier(3),biomeAreaFactory)
            if i!=1 and biomeSize!=1:continue
            biomeAreaFactory=ShoreLayer().run(contextSupplier(1000),biomeAreaFactory)
        biomeAreaFactory=SmoothLayer().run(contextSupplier(1000),biomeAreaFactory)
        biomeAreaFactory=RiverMixerLayer().run(contextSupplier(100),biomeAreaFactory,riverAreaFactory)
        biomeAreaFactory=OceanMixerLayer().run(contextSupplier(100),biomeAreaFactory,oceanAreaFactory)
        return Layer(biomeAreaFactory)
setattr(Layers,'CATEGORIES',dict(
        {i:Layers.Category.BEACH for i in (16,26)}.items()|
        {i:Layers.Category.DESERT for i in (2,17,130)}.items()|
        {i:Layers.Category.EXTREME_HILLS for i in (131,162,20,3,34)}.items()|
        {i:Layers.Category.FOREST for i in (27,28,29,157,132,4,155,156,18)}.items()|
        {i:Layers.Category.ICY for i in (140,13,12)}.items()|
        {i:Layers.Category.JUNGLE for i in (168,169,21,23,22,149,151)}.items()|
        {i:Layers.Category.MESA for i in (37,165,167,166)}.items()|
        {i:Layers.Category.BADLANDS_PLATEAU for i in (39,38)}.items()|
        {i:Layers.Category.MUSHROOM for i in (14,15)}.items()|
        {i:Layers.Category.NONE for i in (25,)}.items()|
        {i:Layers.Category.OCEAN for i in (46,49,50,48,24,47,10,45,0,44)}.items()|
        {i:Layers.Category.PLAINS for i in (1,129)}.items()|
        {i:Layers.Category.RIVER for i in (11,7)}.items()|
        {i:Layers.Category.SAVANNA for i in (35,36,163,164)}.items()|
        {i:Layers.Category.SWAMP for i in (6,134)}.items()|
        {i:Layers.Category.TAIGA for i in (160,161,32,33,30,31,158,5,19,133)}.items()
    ))

class DimensionTransformer:pass

class AreaTransformer0:
    def run(self,bigContext):
        def f(vec2):
            bigContext.initRandom(vec2)
            return self.applyPixel(bigContext,vec2)
        return lambda:bigContext.createResult(f)

class AreaTransformer1(DimensionTransformer):
    def run(self,bigContext,areaFactory):
        area=areaFactory()
        def f(vec2):
            bigContext.initRandom(vec2)
            return self.applyPixel(bigContext,area,vec2)
        return lambda:bigContext.createResult(f)

class AreaTransformer2(DimensionTransformer):
    def run(self,bigContext,areaFactory,areaFactory2):
        def f(vec2):
            bigContext.initRandom(vec2)
            return self.applyPixel(bigContext,areaFactory(),areaFactory2(),vec2)
        return lambda:bigContext.createResult(f)

class DimensionOffset0Transformer(DimensionTransformer):
    def getParent(self,vec):
        return vec

class DimensionOffset1Transformer(DimensionTransformer):
    def getParent(self,vec):
        return vec-1

class C0Transformer(AreaTransformer1,DimensionOffset0Transformer):
    def applyPixel(self,bigContext,area,vec2):
        return self.apply(bigContext,area.get(self.getParent(vec2)))

class C1Transformer(AreaTransformer1,DimensionOffset1Transformer):
    def applyPixel(self,bigContext,area,vec2):
        return self.apply(bigContext,area.get(self.getParent(vec2+1)))

class BishopTransformer(AreaTransformer1,DimensionOffset1Transformer):
    def applyPixel(self,bigContext,area,vec2):
        return self.apply(bigContext,
            area.get(self.getParent(vec2+[0,2])),
            area.get(self.getParent(vec2+[2,2])),
            area.get(self.getParent(vec2+[2,0])),
            area.get(self.getParent(vec2)),
            area.get(self.getParent(vec2+[1,1]))
        )

class CastleTransformer(AreaTransformer1,DimensionOffset1Transformer):
    def applyPixel(self,bigContext,area,vec2):
        return self.apply(bigContext,
            area.get(self.getParent(vec2+[1,0])),
            area.get(self.getParent(vec2+[2,1])),
            area.get(self.getParent(vec2+[1,2])),
            area.get(self.getParent(vec2+[0,1])),
            area.get(self.getParent(vec2+[1,1]))
        )

class IslandLayer(AreaTransformer0):
    def applyPixel(self,context,vec2):
        if vec2[0]==0 and vec2[1]==0:return 1
        if context.nextRandom(10)==0:return 1
        return 0

class ZoomLayer(AreaTransformer1):
    def getParent(self,vec):
        return vec>>1
    def applyPixel(self,bigContext,area,vec2):
        biomeIdOrigin=area.get(self.getParent(vec2))
        bigContext.initRandom(vec2>>1<<1)
        v=vec2&1
        if v[0]==0 and v[1]==0:
            return biomeIdOrigin
        biomeIdSouth=area.get(self.getParent(vec2+[0,1]))
        newBiomeX=bigContext.random(biomeIdOrigin,biomeIdSouth)
        if v[0]==0 and v[1]==1:
            return newBiomeX
        biomeIdEast=area.get(self.getParent(vec2+[1,0]))
        newBiomeZ=bigContext.random(biomeIdOrigin,biomeIdEast)
        if v[0]==1 and v[1]==0:
            return newBiomeZ
        biomeIdDiagonal=area.get(self.getParent(vec2+[1,1]))
        return self.moreOrRandom(bigContext,biomeIdOrigin,biomeIdEast,biomeIdSouth,biomeIdDiagonal)
    def moreOrRandom(self,bigContext,biomeIdOrigin,biomeIdEast,biomeIdSouth,biomeIdDiagonal):
        if biomeIdEast==biomeIdSouth and biomeIdSouth==biomeIdDiagonal:
            return biomeIdEast
        if(
            biomeIdOrigin==biomeIdEast and biomeIdOrigin==biomeIdSouth or
            biomeIdOrigin==biomeIdEast and biomeIdOrigin==biomeIdDiagonal or
            biomeIdOrigin==biomeIdSouth and biomeIdOrigin==biomeIdDiagonal
        ):return biomeIdOrigin
        if(
            biomeIdOrigin==biomeIdEast and biomeIdSouth!=biomeIdDiagonal or 
            biomeIdOrigin==biomeIdSouth and biomeIdEast!=biomeIdDiagonal or
            biomeIdOrigin==biomeIdDiagonal and biomeIdEast!=biomeIdSouth
        ):return biomeIdOrigin
        if (
            biomeIdEast==biomeIdSouth and biomeIdOrigin!=biomeIdDiagonal or 
            biomeIdEast==biomeIdDiagonal and biomeIdOrigin!=biomeIdSouth
        ):return biomeIdEast
        if biomeIdSouth==biomeIdDiagonal and biomeIdOrigin!=biomeIdEast:
            return biomeIdSouth
        return bigContext.random(biomeIdOrigin,biomeIdEast,biomeIdSouth,biomeIdDiagonal)

class ZoomLayerFuzzy(ZoomLayer):
    def moreOrRandom(self, bigContext, biomeIdOrigin, biomeIdEast, biomeIdSouth, biomeIdDiagonal):
        return bigContext.random(biomeIdOrigin,biomeIdEast,biomeIdSouth,biomeIdDiagonal)

class AddIslandLayer(BishopTransformer):
    def apply(self,context,biomeIdSW,biomeIdSE,biomeIdNE,biomeIdNW,biomeIdO):
        if not (not Layers.isShallowOcean(biomeIdO) or (
            Layers.isShallowOcean(biomeIdNW) and 
            Layers.isShallowOcean(biomeIdNE) and 
            Layers.isShallowOcean(biomeIdSW) and 
            Layers.isShallowOcean(biomeIdSE)
        )):
            count=1
            tempId=1
            if not Layers.isShallowOcean(biomeIdNW):
                if context.nextRandom(count)==0:
                    count+=1
                    tempId=biomeIdNW
            if not Layers.isShallowOcean(biomeIdNE):
                if context.nextRandom(count)==0:
                    count+=1
                    tempId=biomeIdNE
            if not Layers.isShallowOcean(biomeIdSW):
                if context.nextRandom(count)==0:
                    count+=1
                    tempId=biomeIdSW
            if not Layers.isShallowOcean(biomeIdSE):
                if context.nextRandom(count)==0:
                    count+=1
                    tempId=biomeIdSE
            if context.nextRandom(3)==0:
                return tempId
            return 4 if tempId==4 else biomeIdO
        if not Layers.isShallowOcean(biomeIdO) and (
            Layers.isShallowOcean(biomeIdNW) or
            Layers.isShallowOcean(biomeIdSW) or
            Layers.isShallowOcean(biomeIdNE) or 
            Layers.isShallowOcean(biomeIdSE)
        ) and context.nextRandom(5)==0:
            if Layers.isShallowOcean(biomeIdNW):
                return 4 if biomeIdO==4 else biomeIdNW
            if Layers.isShallowOcean(biomeIdSW):
                return 4 if biomeIdO==4 else biomeIdSW
            if Layers.isShallowOcean(biomeIdNE):
                return 4 if biomeIdO==4 else biomeIdNE
            if Layers.isShallowOcean(biomeIdSE):
                return 4 if biomeIdO==4 else biomeIdSE
        return biomeIdO

class RemoveTooMuchOceanLayer(CastleTransformer):
    def apply(self,context,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO):
        if (
            Layers.isShallowOcean(biomeIdO) and
            Layers.isShallowOcean(biomeIdN) and 
            Layers.isShallowOcean(biomeIdE) and
            Layers.isShallowOcean(biomeIdS) and 
            Layers.isShallowOcean(biomeIdW) and
            context.nextRandom(2)==0
        ):
            return 1
        return biomeIdO

class OceanLayer(AreaTransformer0):
    def applyPixel(self,context,vec2):
        noise=context.biomeNoise
        val=noise.noise(np.append(vec2/8,0.0),0.0,0.0)
        if val>0.4:return 44
        if val>0.2:return 45
        if val<-0.4:return 10
        if val<-0.2:return 46
        return 0

class AddSnowLayer(C1Transformer):
    def apply(self,context,biomeId):
        if Layers.isShallowOcean(biomeId):
            return biomeId
        n2=context.nextRandom(6)
        if n2==0:return 4
        if n2==1:return 3
        return 1

class AddEdgeLayer:
    class IntroduceSpecial(C0Transformer):
        def apply(self,context,biomeId):
            if not Layers.isShallowOcean(biomeId) and context.nextRandom(13)==0:
                biomeId|=1+context.nextRandom(15)<<8&0xF00
            return biomeId
    class HeatIce(CastleTransformer):
        def apply(self,context,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO):
            if biomeIdO==4 and (
                biomeIdN==1 or biomeIdE==1 or biomeIdS==1 or biomeIdW==1 or
                biomeIdN==2 or biomeIdE==2 or biomeIdS==2 or biomeIdW==2
            ):
                return 3
            return biomeIdO
    class CoolWarm(CastleTransformer):
        def apply(self,context,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO):
            if biomeIdO==1 and (
                biomeIdN==3 or biomeIdE==3 or biomeIdS==3 or biomeIdW==3 or
                biomeIdN==4 or biomeIdE==4 or biomeIdS==3 or biomeIdW==4
            ):return 2
            return biomeIdO

class AddMushroomIslandLayer(BishopTransformer):
    def apply(self,context,biomeIdSW,biomeIdSE,biomeIdNE,biomeIdNW,biomeIdO):
        if (
            Layers.isShallowOcean(biomeIdO) and 
            Layers.isShallowOcean(biomeIdNW) and 
            Layers.isShallowOcean(biomeIdSW) and 
            Layers.isShallowOcean(biomeIdNE) and
            Layers.isShallowOcean(biomeIdNE) and
            context.nextRandom(100)==0
        ):
            return 14
        return biomeIdO

class AddDeepOceanLayer(CastleTransformer):
    def apply(self,context,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO):
        if Layers.isShallowOcean(biomeIdO):
            count=0
            if Layers.isShallowOcean(biomeIdN):count+=1
            if Layers.isShallowOcean(biomeIdE):count+=1
            if Layers.isShallowOcean(biomeIdS):count+=1
            if Layers.isShallowOcean(biomeIdW):count+=1
            if count>3:
                if biomeIdO==44:return 47
                if biomeIdO==45:return 48
                if biomeIdO==0:return 24
                if biomeIdO==46:return 49
                if biomeIdO==10:return 50
                return 24
        return biomeIdO

class RiverInitLayer(C0Transformer):
    def apply(self,context,biomeId):
        return biomeId if Layers.isShallowOcean(biomeId) else context.nextRandom(299999)+2

class BiomeInitLayer(C0Transformer):
    LEGACY_WARM_BIOMES=(2,4,3,6,1,5)
    WARM_BIOMES=(2,2,2,35,35,1)
    MEDIUM_BIOMES=(4,29,3,1,27,6)
    COLD_BIOMES=(4,3,5,1)
    ICE_BIOMES=(12,12,12,30)
    warmbiomes=WARM_BIOMES
    def __init__(self,legacyBiomeInitLayer):
        if legacyBiomeInitLayer:
            self.warmbiomes=self.LEGACY_WARM_BIOMES
    def apply(self,context,biomeId):
        data=(biomeId&0xF00)>>8
        biomeId&=0xFFFFF0FF
        if Layers.isOcean(biomeId) or biomeId==14:
            return biomeId
        if biomeId==1:
            if data>0:
                return 39 if context.nextRandom(3)==0 else 38
            return self.warmbiomes[context.nextRandom(len(self.warmbiomes))]
        elif biomeId==2:
            if data>0:
                return 21
            return self.MEDIUM_BIOMES[context.nextRandom(len(self.MEDIUM_BIOMES))]
        elif biomeId==3:
            if data>0:
                return 32
            return self.COLD_BIOMES[context.nextRandom(len(self.COLD_BIOMES))]
        elif biomeId==4:
            return self.ICE_BIOMES[context.nextRandom(len(self.ICE_BIOMES))]
        return 14

class RareBiomeLargeLayer(C1Transformer):
    def apply(self,context,biomeId):
        if context.nextRandom(10)==0 and biomeId==21:
            return 168
        return biomeId

class BiomeEdgeLayer(CastleTransformer):
    def checkEdge(self,arrn,biomeId):
        if not Layers.isSame(biomeId,3):return False
        arrn[0]=biomeId
        return True
    def checkEdgeStrict(self,arrn,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO,biomeId,biomeId2):
        if biomeIdO!=biomeId:return False
        if (
            Layers.isSame(biomeIdN,biomeId) and
            Layers.isSame(biomeIdE,biomeId) and
            Layers.isSame(biomeIdS,biomeId) and
            Layers.isSame(biomeIdW,biomeId)
        ):a=biomeIdO
        else:a=biomeId2
        arrn[0]=a
        return True
    def apply(self,context,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO):
        arrn=[0]
        if (
            self.checkEdge(arrn,biomeIdO) or 
            self.checkEdgeStrict(arrn,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO,38,37) or
            self.checkEdgeStrict(arrn,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO,39,37) or
            self.checkEdgeStrict(arrn,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO,32,5)
        ):return arrn[0]
        st={biomeIdN,biomeIdE,biomeIdS,biomeIdW}
        if biomeIdO==2 and 12 in st:return 34
        if biomeIdO==6:
            if 2 in st or 30 in st or 12 in st:return 1
            if 21 in st or 168 in st:return 23
        return biomeIdO

class RegionHillsLayer(AreaTransformer2,DimensionOffset1Transformer):
    MUTATIONS={
         1:129, 2:130, 3:131, 4:132, 5:133, 6:134,12:140,
        21:149,23:151,27:155,28:156,29:157,30:158,32:160,
        33:161,34:162,35:163,36:164,37:165,38:166,39:167
    }
    def applyPixel(self,context,area,area2,vec2):
        biomeId=area.get(self.getParent(vec2+1))
        biomeId2=area2.get(self.getParent(vec2+1))
        if biomeId>255:raise ValueError("old! %d"%biomeId)
        data=(biomeId2-2)%29
        if not Layers.isShallowOcean(biomeId) and biomeId>=2 and data==1:
            return self.MUTATIONS[biomeId] if biomeId in self.MUTATIONS else biomeId
        n=context.nextRandom(3)
        if n==0 or data==0:
            res=biomeId
            if biomeId==2:res=17
            elif biomeId==4:res=18
            elif biomeId==27:res=28
            elif biomeId==29:res=1
            elif biomeId==5:res=19
            elif biomeId==32:res=33
            elif biomeId==30:res=31
            elif biomeId==1:res=18 if context.nextRandom(3)==0 else 4
            elif biomeId==12:res=13
            elif biomeId==21:res=22
            elif biomeId==168:res=169
            elif biomeId==0:res=24
            elif biomeId==45:res=48
            elif biomeId==46:res=49
            elif biomeId==10:res=50
            elif biomeId==3:res=34
            elif biomeId==35:res=36
            elif Layers.isSame(biomeId,38):res=37
            elif biomeId in (24,48,49,50) and context.nextRandom(3)==0:
                res=1 if context.nextRandom(2)==0 else 4
            if data==0 and res!=biomeId:
                if res in self.MUTATIONS:
                    res=self.MUTATIONS[res]
                else:
                    res=biomeId
            if res!=biomeId:
                count=0
                if Layers.isSame(area.get(self.getParent(vec2+[1,0])),biomeId):count+=1
                if Layers.isSame(area.get(self.getParent(vec2+[2,1])),biomeId):count+=1
                if Layers.isSame(area.get(self.getParent(vec2+[0,1])),biomeId):count+=1
                if Layers.isSame(area.get(self.getParent(vec2+[1,2])),biomeId):count+=1
                if count>=3:return res
        return biomeId

class RiverLayer(CastleTransformer):
    riverFilter=lambda n:2+(n&1) if n>=2 else n
    def apply(self,context,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO):
        biomeId=RiverLayer.riverFilter(biomeIdO)
        if (
            biomeId==RiverLayer.riverFilter(biomeIdS) and
            biomeId==RiverLayer.riverFilter(biomeIdN) and
            biomeId==RiverLayer.riverFilter(biomeIdE) and
            biomeId==RiverLayer.riverFilter(biomeIdW)
        ):return -1
        return 7

class SmoothLayer(CastleTransformer):
    def apply(self,context,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO):
        neqs=biomeIdN==biomeIdS
        weqe=biomeIdW==biomeIdE
        if neqs==weqe:
            if weqe:
                return biomeIdW if context.nextRandom(2)==0 else biomeIdN
            return biomeIdO
        return biomeIdW if weqe else biomeIdN

class RareBiomeSpotLayer(C1Transformer):
    def apply(self,context,biomeId):
        if context.nextRandom(57)==0 and biomeId==1:
            return 129
        return biomeId

class ShoreLayer(CastleTransformer):
    SNOWY=(26,11,12,13,140,30,31,158,10)
    JUNGLES=(168,169,21,22,23,149,151)
    isJungleCompatible=lambda n:n in (168,169,21,22,23,149,151) or n==4 or n==5 or Layers.isOcean(n)
    def isMesa(self,n):
        return n in (37,38,39,165,166,167)
    def apply(self,context,biomeIdN,biomeIdE,biomeIdS,biomeIdW,biomeIdO):
        if biomeIdO==14:
            if Layers.isShallowOcean(biomeIdN) or Layers.isShallowOcean(biomeIdE) or Layers.isShallowOcean(biomeIdS) or Layers.isShallowOcean(biomeIdW):
                return 15
        elif biomeIdO in self.JUNGLES:
            if not (ShoreLayer.isJungleCompatible(biomeIdN) and ShoreLayer.isJungleCompatible(biomeIdE) and ShoreLayer.isJungleCompatible(biomeIdS) and ShoreLayer.isJungleCompatible(biomeIdW)):
                return 23
        elif biomeIdO in (3,34,20):
            if not Layers.isOcean(biomeIdO) and (
                Layers.isOcean(biomeIdN) or Layers.isOcean(biomeIdE) or Layers.isOcean(biomeIdS) or Layers.isOcean(biomeIdW)
            ):return 25
        elif biomeIdO in self.SNOWY:
            if not Layers.isOcean(biomeIdO) and (
                Layers.isOcean(biomeIdN) or Layers.isOcean(biomeIdE) or Layers.isOcean(biomeIdS) or Layers.isOcean(biomeIdW)
            ):return 26
        elif biomeIdO in (37,38):
            if not (
                Layers.isOcean(biomeIdN) or Layers.isOcean(biomeIdE) or Layers.isOcean(biomeIdS) or Layers.isOcean(biomeIdW) or
                self.isMesa(biomeIdN) and self.isMesa(biomeIdE) and self.isMesa(biomeIdS) and self.isMesa(biomeIdW)
            ):return 2
        elif not Layers.isOcean(biomeIdO) and biomeIdO not in (7,6) and (
            Layers.isOcean(biomeIdN) or Layers.isOcean(biomeIdE) or Layers.isOcean(biomeIdS) or Layers.isOcean(biomeIdW)
        ):return 16
        return biomeIdO

class RiverMixerLayer(AreaTransformer2,DimensionOffset0Transformer):
    def applyPixel(self,context,area,area2,vec2):
        biomeId=area.get(self.getParent(vec2))
        biomeId2=area2.get(self.getParent(vec2))
        if Layers.isOcean(biomeId):
            return biomeId
        if biomeId2==7:
            if biomeId==12:
                return 11
            if biomeId in (14,15):
                return 15
            return biomeId2&0xFF
        return biomeId

class OceanMixerLayer(AreaTransformer2,DimensionOffset0Transformer):
    def applyPixel(self,context,area,area2,vec2):
        biomeId=area.get(self.getParent(vec2))
        biomeId2=area2.get(self.getParent(vec2))
        if not Layers.isOcean(biomeId):
            return biomeId
        radius=8
        step=4
        for dx in range(-radius,radius+1,step):
            for dz in range(-radius,radius+1,step):
                biomeIdSur=area.get(self.getParent(vec2+[dx,dz]))
                if Layers.isOcean(biomeIdSur):continue
                if biomeId2==44:
                    return 45
                if biomeId2!=10:continue
                return 46
        if biomeId==24:
            if biomeId2==45:return 48
            if biomeId2==0:return 24
            if biomeId2==46:return 49
            if biomeId2==10:return 50
        return biomeId2