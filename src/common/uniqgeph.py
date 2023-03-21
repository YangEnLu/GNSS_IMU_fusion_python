from .global_constants import glc, nav, geph
import numpy as np
import numpy.matlib as npm

def uniqgeph(nav: nav):
    geph0 = nav.geph
    A = np.zeros((nav.ng, 3))
    geph1 = npm.repmat(geph(), nav.ng, 1)

    # sort
    for i in range(nav.ng):
        A[i, :] = [geph0[i, 0].tof.time, geph0[i, 0].toe.time, geph0[i, 0].sat]

    # sort first:time second: satid
    sorted_indices = np.lexsort((A[:, 1], A[:, 0]))
    for i in range(nav.n):
        geph1[i, 0] = geph0[(sorted_indices.item(i)), 0]

    del geph0

    # unique
    j = 0
    for i in range(1, nav.ng):
        if (geph1[i, 0].sat != geph1[j, 0].sat) or (geph1[i, 0].toe.time != geph1[j, 0].toe.time) or (geph1[i,0].svh != geph1[j,0].svh):
            j = j+1
            geph1[j, 0] = geph1[i, 0]
    
    nav.ng = j+1
    geph2 = npm.repmat(geph(), nav.ng, 1)
    for i in range(nav.ng):
        geph2[i, 0] = geph1[i, 0]
    del geph1
    
    del nav.geph
    nav.geph = geph2
    
    return nav