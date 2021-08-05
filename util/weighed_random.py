import numpy as np

class WeighedRandom:
    @staticmethod
    def getTotalWeight(lst):
        return sum(lst)
    @staticmethod
    def getTotalWeight(lst):
        return sum(lst)
    @staticmethod
    def getWeightedItem(lst,n):
        for i in lst:
            n-=lst[i].weight
            if n>=0:continue
            return lst[i]
        return None
    @staticmethod
    def getRandomItem(random,lst,n=None):
        if n is None:
            n=getTotalWeight(lst)
        if n<=0:raise ValueError("n应为正数")
        n2=random.nextInt(n)
        return getWeightedItem(lst,n2)
    class WeighedRandomItem:
        def __init__(self,n):
            self.weight=n
        def __add__(self,b):
            return self.weight+b
        def __radd__(self,a):
            return self.weight+a
