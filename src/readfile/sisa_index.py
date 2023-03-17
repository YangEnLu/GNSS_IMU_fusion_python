import numpy as np


def sisa_index(value):
    if value < 0.0 or value > 6.0:
        ind = 255
        return ind
    elif value <= 0.5:
        ind = np.fix(value/0.01)
        return ind
    elif value <= 1:
        ind = np.fix((value-0.5)/0.02)+50
        return ind
    elif value <=2:
        ind = np.fix((value-1.0)/0.04)+75
        return ind
    else:
        ind=np.fix(np.fix(value-2.0)/0.16+100)
        return ind
    
