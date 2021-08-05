import numpy as np
import math

def sqrt(f):
    return math.sqrt(f)

def floor(f):
    n=np.int32(f)
    return n-1 if f<n else n
vfloor=np.vectorize(floor)

def lflooor(d):
    l=np.int64(d)
    return l-1 if d<l else l
vlfloor=np.vectorize(lflooor)

def ceil(f):
    n=np.int32(f)
    return n+1 if f<n else n

def clamp(x,m,M):
    if x<m:
        return m
    elif x>M:
        return M
    return x

def smoothstep(d):
    return d*d*d*(d*(d*6.0-15.0)+10.0)
vsmoothstep=np.vectorize(smoothstep)

def lerp(k,s,e):
    return s+k*(e-s)

def lerp2(k1,k2,ss,se,es,ee):
    return lerp(k2,lerp(k1,ss,se),lerp(k1,es,ee))

def lerp3(k1,k2,k3,sss,sse,ses,see,ess,ese,ees,eee):
    return lerp(k3,lerp2(k1,k2,sss,sse,ses,see),lerp2(k1,k2,ess,ese,ees,eee))

def clampedLerp(d,d2,d3):
    if d3<0:return d
    if d3>1:return d2
    return lerp(d3,d,d2)

def smallestEncompassingPowerOfTwo(n):
    n2=n-1
    n2|=n2>>1
    n2|=n2>>2
    n2|=n2>>4
    n2|=n2>>8
    n2|=n2>>16
    return n2+1

def isPowerOfTwo(n):
    return n!=0 and (n&n-1)==0

def ceillog2(n):
    if not isPowerOfTwo(n):n=smallestEncompassingPowerOfTwo(n)
    return math.ceil(math.log2(n)) # ?

def floorlog2(n):
    return ceillog2(n)-(0 if isPowerOfTwo(n) else 1)

def hsvToRgb(h,s,v):
    hi=np.int32(h*6)/6
    f=hi*6-h
    p=v*(1-s)
    q=v*(1-f*s)
    t=v*(1-(1-f)*s)
    if hi==0:
        x=v
        y=t
        z=p
    elif hi==1:
        x=q
        y=v
        z=p
    elif hi==2:
        x=p
        y=v
        z=t
    elif hi==3:
        x=p
        y=q
        z=v
    elif hi==4:
        x=t
        y=p
        z=v
    elif hi==5:
        x=v
        y=p
        z=q
    else:
        raise RuntimeError("hsv转化为rgb时出错")
    r=clamp(np.int32(x*255),np.int32(0),np.int32(255))
    g=clamp(np.int32(y*255),np.int32(0),np.int32(255))
    b=clamp(np.int32(z*255),np.int32(0),np.int32(255))
    return r<<16|g<<8|b