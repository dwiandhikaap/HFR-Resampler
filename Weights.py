import math
import numpy as np
from enum import IntEnum

class Mode(IntEnum):
    EQUAL           = 0
    GAUSS           = 1
    GAUSS_SYM       = 2
    PYRAMID         = 3
    PYRAMID_SYM     = 4
    SIVEROO_1       = 5
    SIVEROO_2       = 6

#This function will return an list of value, like below:
# [0,1,2,3,...,n] -> [a,...,b]
def scaleRange(n,a,b):
    return [(x*(b-a)/(n-1))+a for x in range(0,n)]

def equal(n):
    return [1/n]*n

def gauss(n):
    r = range(n,0,-1)
    val = [math.exp(-(2.0*x/n)**2) for x in r]
    val = val/np.sum(val)
    return val

def gauss_sym(n):
    n = n/2
    r = range(int(n),-math.ceil(n),-1)
    val = ([math.exp(-(2.0*x/(n))**2) for x in r])
    val = val/np.sum(val)
    return val

def pyramid(n):
    r = range(1,n+1)
    val = [x/n for x in r]
    val = val/np.sum(val)
    return val

def pyramid_sym(n):
    r = range(0,n)
    val = [(n/2)-abs(x-(n-1)/2) for x in r]
    val = val/np.sum(val)
    return val

def siveroo1(n):
    r = scaleRange(n,-3,0.1)
    val = [math.floor(3*math.exp(-(x/1.9)**2))/3+0.1 for x in r]
    val = val/np.sum(val)
    return val

#divide equally and weight individual part equally
#lets say, 1,3,2
def divide(n,w):
    #weight array/list
    #w = [1,3,2]

    #rescale n
    r = scaleRange(n,0,len(w)-0.1)

    val = []
    idx = [math.floor(x) for x in r]
    for x in range(0,n):
        index = int(idx[x])
        val.append(w[index])
    val = val/np.sum(val)
    return val

def null(n):
    return [0]*n

def weight(mode,count):
    if count == 1:
        return [1.0]
    else:
        return {
            Mode.EQUAL          : equal(count),
            Mode.GAUSS          : gauss(count),
            Mode.GAUSS_SYM      : gauss_sym(count),
            Mode.PYRAMID        : pyramid(count),
            Mode.PYRAMID_SYM    : pyramid_sym(count),
            Mode.SIVEROO_1      : siveroo1(count),
            Mode.SIVEROO_2      : divide(count,[1,3,3,2,2])
        }[mode]

def modeName(mode):
    return {
            Mode.EQUAL          : "[1] Equal",
            Mode.GAUSS          : "[2] Gaussian Asymmetric",
            Mode.GAUSS_SYM      : "[3] Gaussian Symmetric",
            Mode.PYRAMID        : "[4] Pyramid Asymmetric",
            Mode.PYRAMID_SYM    : "[5] Pyramid Symmetric",
            Mode.SIVEROO_1      : "[6] Siveroo's Preset I",
            Mode.SIVEROO_2      : "[7] Siveroo's Preset II"
        }[mode]
