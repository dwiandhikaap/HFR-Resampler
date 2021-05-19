import math
import numpy as np
import json

from Exceptions import *

settingsJson = None
with open("settings.json") as settings:
    settingsJson = json.load(settings)["blend_settings"]

# This function will return an list of value, like below:
# [0,1,2,3,...,n] -> [a,...,b]
def scaleRange(n,a,b):
    return [(x*(b-a)/(n-1))+a for x in range(0,n)]
    
def equal(n):
    return [1/n]*n

def gauss(n, c, bound):
    r = scaleRange(n, bound[0], bound[1])
    val = [math.exp(-((x)**2)/(2*(c**2))) for x in r]
    val = val/np.sum(val)
    return val

def gauss_sym(n, c, bound):
    r = scaleRange(n, -np.amax(np.abs(bound)), np.amax(np.abs(bound)))
    val = [math.exp(-((x)**2)/(2*(c**2))) for x in r]
    val = val/np.sum(val)
    return val

def pyramid(n, reverse):
    val = []
    if reverse:
        val = [x for x in range(n,0,-1)]
    else:
        val = [x for x in range(1,n+1)]
    val = val/np.sum(val)
    return val

def pyramid_sym(n):
    r = range(0,n)
    val = [((n-1)/2-abs(x-((n-1)/2))+1) for x in r]
    val = val/np.sum(val)
    return val

def funcEval(func,nums):
        try:
            return eval(f"[({func}) for x in nums]")
        except NameError as e:
            raise InvalidCustomWeighting

def custom(n, func="", bound=(0,1)):
    r = scaleRange(n, bound[0], bound[1])
    val = funcEval(func, r)
    if np.amin(val) < 0: val -= np.amin(val)
    val = val/np.sum(val)
    return val

# This function will stretch the given array (weights) to a specific length (n)
# Example : n = 10, weights = [1,2]
# Result : val = [1,1,1,1,1,2,2,2,2,2], then normalize it to [0.0667, 0.0667, 0.0667, 0.0667, 0.0667, 0.1333, 0.1333, 0.1333, 0.1333, 0.1333]
def divide(n,weights):
    r = scaleRange(n,0,len(weights)-0.1)
    val = []
    idx = [math.floor(x) for x in r]
    for x in range(0,n):
        index = int(idx[x])
        val.append(weights[index])
    if np.amin(val) < 0: val -= np.amin(val)
    val = (val/np.sum(val))
    return val

def weight(mode,count):
    if count == 1:
        return [1.0] # If only one frame is weighted, it's weight is always going to be 1.
    else:
        try:
            return {
                "EQUAL"          : equal(count),
                "GAUSSIAN"       : gauss(count, c=settingsJson['gaussian']['standard_deviation'], bound=settingsJson['gaussian']['bound']),
                "GAUSSIAN_SYM"   : gauss_sym(count, c=settingsJson['gaussian']['standard_deviation'], bound=settingsJson['gaussian']['bound']), 
                "PYRAMID"        : pyramid(count, reverse=settingsJson['pyramid']['reverse']),
                "PYRAMID_SYM"    : pyramid_sym(count),
                "CUSTOM_FUNCTION": custom(count, func=settingsJson['custom_function']['function'], bound=settingsJson['custom_function']['bound']),
                "CUSTOM_WEIGHT"  : divide(count, weights=settingsJson['custom_weight']['weight'])
            }[mode.upper()]
        except KeyError:
            raise InvalidBlendMode
