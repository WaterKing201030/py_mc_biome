import copy,time
from core.vec import ChunkPos

class Area:
    pass

class LazyArea(Area):
    def __init__(self,dct,f):
        self.cache=dct
        self.transformer=f
    def get(self,vec2):
        l=ChunkPos.asLong(vec2)
        if l in self.cache:
            return self.cache[l]
        else:
            biomeId=self.transformer(vec2)
            self.cache[l]=biomeId
            return biomeId