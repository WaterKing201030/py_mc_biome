import numpy as np

from core.vec import Vec3i

class BoundingBox:
    def __init__(self,vec3i0,vec3i1):
        self.start=Vec3i([min(vec3i0[i],vec3i1[i]) for i in range(3)])
        self.end=Vec3i([max(vec3i0[i],vec3i1[i]) for i in range(3)])