from .global_constants import glc, nav, eph
import numpy as np
import numpy.matlib as npm


def uniqeph(nav: nav):
    eph0 = nav.eph
    A = np.zeros((nav.n, 3))
    eph1 = npm.repmat(eph(), nav.n, 1)

    # sort
    for i in range(nav.n):
        A[i, :] = [eph0[i, 0].ttr.time, eph0[i, 0].toe.time, eph0[i, 0].sat]

    # sort first:time second: satid
    sorted_indices = np.lexsort((A[:, 1], A[:, 0]))
    for i in range(nav.n):
        eph1[i, 0] = eph0[(sorted_indices.item(i)), 0]

    del eph0

    # unique
    j = 0
    for i in range(1, nav.n):
        if (eph1[i, 0].sat != eph1[j, 0].sat) or (eph1[i, 0].iode != eph1[j, 0].iode):
            j = j+1
            eph1[j, 0] = eph1[i, 0]
    nav.n = j+1

    eph2 = npm.repmat(eph(), nav.n, 1)
    for i in range(nav.n):
        eph2[i, 0] = eph1[i, 0]
    del eph1
    
    del nav.eph
    nav.eph = eph2

    return nav
