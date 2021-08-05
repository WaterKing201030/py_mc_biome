import numpy as np
import time

class Random:
    def __init__(self,seed=np.int64(round(time.time()*1000))):
        self.setSeed(seed)
    
    def setSeed(self,seed:np.int64)->None:
        seed=np.int64(seed)
        self.seed=(seed^0x5DEECE66D)&((1<<48)-1)
    
    def next(self,bits:np.int32)->np.int32:
        self.seed=(self.seed*0x5DEECE66D+0xB)&((1<<48)-1)
        n=(self.seed>>(48-bits))&((1<<32)-1)
        if n>>31:
            return np.int32(n&((1<<31)-1))-(1<<31)
        else:
            return np.int32(n)
    
    def nextInt(self,n=np.int32(32))->np.int32:
        if n<=0:
            raise ValueError("n必须要是正数")
        if ((n&-n)==n):
            return np.int32(n*np.int64(self.next(31))>>31&(1<<31)-1)
        while True:
            bits=self.next(31)
            val=bits%n
            if bits-val+(n-1)>=0:
                break
        return val
    
    def nextLong(self)->np.int64:
        return (np.int64(self.next(32))<<32)+self.next(32)
    
    def nextDouble(self):
        return ((np.int64(self.next(26))<<27)+self.next(27))/np.float64(1<<53)

def getRandom(arr,random):
    return arr[random.nextInt(len(arr))]