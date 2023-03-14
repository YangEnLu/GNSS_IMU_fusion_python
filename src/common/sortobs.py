from .global_constants import glc, gls, obsd, obs
from ..common.timediff import timediff
import numpy as np
import numpy.matlib as npm


def sortobs(obs: obs):
    A = np.zeros((obs.n, 3))
    data1 = npm.repmat(obsd(), obs.n, 1)

    # sort obs
    for i in range(obs.n):
        A[i, :] = [obs.data.item(i).time.time, obs.data.item(
            i).time.sec, obs.data.item(i).sat]

    # sort first:time second: satid
    sorted_indices = np.lexsort((A[:, 2], A[:, 0]))

    for i in range(obs.n):
        data1[i, 0] = obs.data[(sorted_indices.item(i)), 0]

    # delete duplicated data
    j = 0
    for i in range(1, obs.n):
        t = timediff(data1[i, 0].time, data1[j, 0].time)
        if (data1[i, 0].sat != data1[j, 0].sat) or (t != 0):
            j = j+1
            data1[j, 0] = data1[i, 0]

    obs.n = j+1
    data2 = npm.repmat(obsd(), obs.n, 1)

    for i in range(0, obs.n):
        data2[i, 0] = data1[i, 0]

    del obs.data
    obs.data = data2
    del data1, data2

    # count obs
    i = 1
    nepoch = 0
    dt = 0
    while i < obs.n:
        for j in range(i, obs.n):
            t = timediff(obs.data[j, 0].time, obs.data[i, 0].time)
            if t > glc().DTTOL:
                dt = t
                break
        nepoch = nepoch + 1
        i = j + 1

    obs.nepoch = nepoch
    obs.dt = dt

    return obs
