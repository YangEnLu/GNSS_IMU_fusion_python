import numpy as np
from numpy.linalg import inv


def least_square(v, H, P, nv, ns):
    # normal matrix
    N = np.transpose(H)@P@H

    # compute parameters
    x = inv(N)@np.transpose(H)@P@v

    # sigma0
    sigma0 = np.sqrt(np.transpose(v)@P@v/(nv-ns))

    # covariance of parameter
    VAR = (sigma0**2)*inv(N)

    Q = inv(N)

    return x, Q, VAR
