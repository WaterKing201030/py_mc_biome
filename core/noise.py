import copy,math
import numpy as np
from util.java.javarandom import Random
from world.worldgen import WorldgenRandom
import util.mth as mth

class SimplexNoise:#单形噪声
    GRADIENT=np.array([[1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0],[1,0,1],[-1,0,1],[1,0,-1],[-1,0,-1],[0,1,1],[0,-1,1],[0,1,-1],[0,-1,-1],[1,1,0],[0,-1,1],[-1,1,0],[0,-1,-1]])
    SQRT_3=np.float64(math.sqrt(3.0))
    F2=0.5*(SQRT_3-1.0)#意为2维情况下的转化常数
    G2=(3-SQRT_3)/6.0
    F3=np.float64(0.3333333333333333)
    G3=np.float64(0.16666666666666666)
    p=np.zeros((512),dtype=np.int32)
    def __init__(self,random):
        r=random
        self.xo=r.nextDouble()*256.0
        self.yo=r.nextDouble()*256.0
        self.zo=r.nextDouble()*256.0
        for i in range(256):
            self.p[i]=np.int32(i)
        for i in range(256):
            n=r.nextInt(256-i)
            self.p[i],self.p[n+i]=self.p[n+i],self.p[n]
    def getp(self,n):
        return self.p[n&0xFF]
    @staticmethod
    def dot(vec30,vec31):
        return np.dot(vec30,vec31)
    @staticmethod
    def getCornerNoise3D(ii,vec3,d2):
        tmp=d2-np.dot(vec3,vec3)
        if tmp<0.0:
            res=0.0
        else:
            tmp*=tmp
            res=tmp*tmp*SimplexNoise.dot(SimplexNoise.GRADIENT[ii],vec3)
        return res
    def getValue(self,p):#太丑了！！！
        s=p.size
        if s==2:
            f=SimplexNoise.F2
            g=SimplexNoise.G2
            d=0.5
            fac=70.0
        elif s==3:
            f=SimplexNoise.F3
            g=SimplexNoise.G3
            d=0.6
            fac=32.0
        else:
            raise ValueError("不支持输入向量对应维数的单形噪声")
        ff=p.sum()*f
        tmp=mth.vfloor(p+ff)
        gg=np.float64(tmp.sum())*g
        q=tmp.astype(np.float64)-gg
        o=p-q
        e=np.zeros((s+1,3),dtype=np.int32)
        if s==2:
            order=o.argsort()[::-1]
        elif s==3:
            order=(-o).argsort()
        for i in range(s):
            e[i+1:,order[i]]=1
        l=(np.pad(o,(0,3-s))-e).astype(np.float64)
        for i in range(s+1):
            l[i,:s]+=i*g
        ii=tmp&0xFF
        h=np.zeros((s+1),dtype=np.int32)
        for i in range(s+1):
            t=0
            for j in range(s-1,-1):
                t=self.getp(ii[j]+e[i,j]+t)
            h[i]=t%12
        r=np.zeros((s+1),dtype=np.float64)
        for i in range(s+1):
            r[i]=type(self).getCornerNoise3D(h[i],l[i],d)
        return fac*r.sum()

class ImprovedNoise:
    def __init__(self,random):
        r=random
        self.xo=r.nextDouble()*256.0
        self.yo=r.nextDouble()*256.0
        self.zo=r.nextDouble()*256.0
        self.p=np.zeros((256),dtype=np.int8)
        for i in range(256):
            self.p[i]=np.int8(i)
        for i in range(256):
            n=r.nextInt(256-i)
            self.p[i],self.p[n+i]=self.p[n+i],self.p[i]
        # 洗牌算法
    def noise(self,vec3,d4,d5):
        vec31=vec3+np.array([self.xo,self.yo,self.zo])
        vec32=mth.vfloor(vec31)
        vec33=vec31-vec32
        vec34=mth.smoothstep(vec33)
        if d4!=0.0:
            d6=np.float64(mth.floor(min(d5,vec33[1])/d4)*d4)
        else:
            d6=np.float64(0.0)
        vec33[1]-=d6
        #print(vec32,vec33,vec34)
        return self.sampleAndLerp(vec32,vec33,vec34)
    @staticmethod
    def gradDot(ii,vec3):
        iii=ii&0xF
        return SimplexNoise.dot(SimplexNoise.GRADIENT[iii],vec3)
    def getp(self,ii):
        return self.p[ii&0xFF]&0xFF
    def sampleAndLerp(self,vec30,vec31,vec32):
        l=[0]*8
        for i in range(8):
            v=vec31.copy()
            t=0
            n=i
            for j in range(3):
                m=n&1
                t=self.getp(vec30[j]+m+t)
                v[j]-=m
                n>>=1
            l[i]=ImprovedNoise.gradDot(t,v)
        kx,ky,kz=vec32
        sss,sse,ses,see,ess,ese,ees,eee=l
        return mth.lerp3(kx,ky,kz,sss,sse,ses,see,ess,ese,ees,eee)

class SurfaceNoise:
    pass

class PerlinNoise(SurfaceNoise):
    def __init__(self,worldRandom,pair):
        if type(pair)==list:
            a=list(set(pair))
            a.sort()
            pair=self.makeAmplitudes(a)
        first=pair[0]
        self.amplitudes=pair[1].copy()
        improvedNoise=ImprovedNoise(worldRandom)
        s=self.amplitudes.size
        self.noiseLevels=[None]*s
        n3=-first
        d=self.amplitudes[n3]
        if n3>=0 and n3<s and d!=0.0:
            self.noiseLevels[n3]=improvedNoise
        for i in range(n3-1,-1,-1):
            if i<s:
                if self.amplitudes[i]!=0:
                    self.noiseLevels[i]=ImprovedNoise(worldRandom)
                    continue
                worldRandom.consumeCount(262)
                continue
            worldRandom.consumeCount(262)
        if n3<s-1:
            noiseSeed=np.int64(improvedNoise.noise(np.array([0.0,0.0,0.0],dtype=np.float64),0,0)*np.float64(9.223372036854776e18))
            worldRandom2=WorldgenRandom(noiseSeed)
            for i in range(n3+1,s):
                if i>=0:
                    if self.amplitudes[i]!=0:
                        self.noiseLevels[i]=ImprovedNoise(worldRandom2)
                        continue
                    worldRandom2.consumeCount(262)
                    continue
                worldRandom2.consumeCount(262)
        self.lowestFreqInputFactor=np.float64(pow(2.0,-n3))
        self.lowestFreqValueFactor=np.float64(pow(2.0,s-1))/np.float((2.0,s)-1)
    def getValue(self,vec3,k1=0,k2=0,bl=False):
        d6=0
        d7=self.lowestFreqInputFactor
        d8=self.lowestFreqValueFactor
        for i in range(len(self.noiseLevels)):
            improvedNoise=self.noiseLevels[i]
            if improvedNoise!=None:
                a=wrap(vec3*d7)
                if bl:
                    a[1]=-improvedNoise.yo
                d6+=self.amplitudes[i]*improvedNoise.noise(a,k1*d7,k2*d7)*d8
            d7*=2
            d8/=2
        return d6
    @staticmethod
    def wrap(d):
        if isinstance(d,np.ndarray):
            res=np.zeros((d.size),dtype=np.float64)
            for i in range(d.size):
                res[i]=PerlinNoise.wrap(d[i])
            return res
        else:
            return d-np.float64(mth.lfloor(d/3.3554432e7+0.5))*3.3554432e7
    def makeAmplitudes(self,sortedarr):
        if sortedarr.size<=0:
            raise ValueError("需要一些叠加！")
        first=sortedarr[0]
        last=sortedarr[-1]
        l=last-first+1
        if l<1:
            raise ValueError("叠加的数量需要大于等于1")
        res=np.zeros((l),dtype=np.float64)
        for n in sortedarr:
            res[n-first]=1.0
        return (first,res)
    def getOctaveNoise(self,n):
        return self.noiseLevels[len(self.noiseLevels)-1-n]
    def getSurfaceNoiseValue(self,vec2,k1,k2):
        return self.getValue(np.append(vec2,0),k1,k2,False)

class PerlinSimplexNoise(SurfaceNoise):
    def __init__(self,wr,lst):
        a=list(set(lst))
        a.sort()
        if not a:
            raise ValueError("Need Some ovtaves!")
        first=a[0]
        last=a[-1]
        l=last-first+1
        if l<1:
            raise ValueError("Total number of octaves need to be >=1")
        sn=SimplexNoise(wr)
        tmp=last
        self.noiseLevels=[None]*l
        if tmp>=0 and tmp<l and 0 in a:
            self.noiseLevels[tmp]=sn
        for i in range(tmp+1,l):
            if i>=0 and tmp-i in a:
                self.noiseLevels[i]=SimplexNoise(wr)
                continue
            wr.consumeCount(262)
        if(last>0):
            l=np.int64(sn.getValue(np.array([sn.xo,sn.yo,sn.zo]))*9.223372036854776E18)
            wr2=WorldgenRandom(l)
            for i in range(tmp-1,-1,-1):
                if i<l and tmp-i in a:
                    self.noiseLevels[i]=SimplexNoise(wr2)
                    continue
                wr2.consumeCount(262)
        self.highestFreqInputFactor=pow(2.0,last)
        self.highestFreqValueFactor=1.0/(pow(2.0,l)-1.0)
    def getValue(self,vec2,bl):
        v=0
        hfiq=self.highestFreqInputFactor
        hfvq=self.highestFreqValueFactor
        for sn in self.noiseLevels:
            if sn!=None:
                if bl:
                    a=np.array([sn.xo,sn.yo])
                else:
                    a=np.array([0.0,0.0])
                v+=sn.getValue(vec2*hfiq+a)*hfvq
            hfiq/=2
            hfvq*=2
        return v
    def getSurfaceNoiseValue(self,vec2,d3,d4):
        return self.getValue(vec2,True)*0.55