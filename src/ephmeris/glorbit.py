import numpy as np
from .deq import deq
import numpy as np


def glorbit(t, x, acc):
    w = np.zeros((6, 1))
    k1 = deq(np.reshape(x, (6, 1)), acc)
    for i in range(6):
        w[i, 0] = x[i]+k1[i, 0]*t/2
    k2 = deq(w, acc)
    for i in range(6):
        w[i, 0] = x[i]+k2[i, 0]*t/2
    k3 = deq(w, acc)
    for i in range(6):
        w[i, 0] = x[i]+k3[i, 0]*t/2
    k4 = deq(w, acc)
    for i in range(6):
        x[i] = x[i]+(k1[i, 0]+2*k2[i, 0]+2*k3[i, 0]+k4[i, 0])*t/6

    return x
