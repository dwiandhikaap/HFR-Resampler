import math
import numpy as np
from enum import IntEnum

class Mode(IntEnum):
    EQUAL           = 0
    GAUSS           = 1
    GAUSS_SYM       = 2
    PYRAMID         = 3
    PYRAMID_SYM     = 4
    QUARTER_CIRCLE  = 5
    SEMI_CIRCLE     = 6

def equal(n):
    return [1/n]*n

def gauss(n):
    r = range(n,0,-1)
    val = [math.exp(-(1.5*x/n)**2) for x in r]
    val = val/np.sum(val)
    return val

def gauss_sym(n):
    n = n/2
    r = range(int(n),-math.ceil(n),-1)
    val = ([math.exp(-(1.5*x/(n))**2) for x in r])
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

def quarter_circle(n):
    r = reversed(range(n))
    val = [math.sqrt(1-(x/(n))**2) for x in r]
    val = val/np.sum(val)
    return val

def semi_circle(n):
    #val = [1-((x-((n-1)/2))/(n-1))**2 for x in range(n)]
    val = [math.sqrt(1-((n-2*x-1)/(2*(n-1)))**2) for x in range(n)]
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
            Mode.QUARTER_CIRCLE : quarter_circle(count),
            Mode.SEMI_CIRCLE    : semi_circle(count)
        }[mode]

def modeName(mode):
    return {
            Mode.EQUAL          : "[1] Equal",
            Mode.GAUSS          : "[2] Gaussian Asymmetric",
            Mode.GAUSS_SYM      : "[3] Gaussian Symmetric",
            Mode.PYRAMID        : "[4] Pyramid Asymmetric",
            Mode.PYRAMID_SYM    : "[5] Pyramid Symmetric",
            Mode.QUARTER_CIRCLE : "[6] Quarter-Circle",
            Mode.SEMI_CIRCLE    : "[7] Semi-Circle"
        }[mode]
