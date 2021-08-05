import numpy as np
import util.java.javamath as jmath
from util.lcg import lcgnext
from core.noise import ImprovedNoise
from util.java.javarandom import Random
from world.level.biome.new.area import LazyArea

class Context:
    def nextRandom(self,v):pass
    def getBiomeNoise(self):pass

class BigContext(Context):
    def random(self,*lst):
        a=np.array(lst)
        if a.size==2:
            if self.nextRandom(2)==0:
                return a[0]
            else:
                return a[1]
        elif a.size==4:
            n=self.nextRandom(4)
            if n==0:
                return a[0]
            elif n==1:
                return a[1]
            elif n==2:
                return a[2]
            else:
                return a[3]
        else:
            raise ValueError("不合法输入长度")

class LazyAreaContext(BigContext):pass
class LazyAreaContext(BigContext):
    def __init__(self,seed,salt):
        self.seed=LazyAreaContext.mixSeed(seed,salt)
        self.biomeNoise=ImprovedNoise(Random(seed))
        self.cache=dict()
    def createResult(self,f):
        return LazyArea(self.cache,f)
    def initRandom(self,vec2):
        x=np.int64(vec2[0])
        z=np.int64(vec2[1])
        l3=self.seed
        l3=lcgnext(l3,x)
        l3=lcgnext(l3,z)
        l3=lcgnext(l3,x)
        l3=lcgnext(l3,z)
        self.rval=l3
    def nextRandom(self, v):
        n2=jmath.floorMod(self.rval>>24,np.int64(v))
        self.rval=lcgnext(self.rval,self.seed)
        return n2
    def mixSeed(seed,salt):
        l3=salt
        l3=lcgnext(l3,salt)
        l3=lcgnext(l3,salt)
        l3=lcgnext(l3,salt)
        l4=seed
        l4=lcgnext(l4,l3)
        l4=lcgnext(l4,l3)
        l4=lcgnext(l4,l3)
        return l4
    def getBiomeNoise(self):
        return self.biomeNoise