import numpy as np

def floorMod(x,y):
    xx=np.int64(x)
    yy=np.int64(y)
    return xx%yy
    """ if x>y:
        return xx%yy
    else:
        if xx^yy>0:return (yy-xx)*(1 if yy>0 else -1)
        return xx%yy """