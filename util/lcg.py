import numpy as np

def lcgnext(l,l2):
    l*=np.int64(l)*np.int64(6364136223846793005)+np.int64(1442695040888963407)
    l+=l2
    return l