import numpy as np


def deq(x, acc):
    RE_GLO = 6378136.0
    MU_GLO = 3.9860044e14
    OMGE_GLO = 7.292115e-5
    J2_GLO = 1.0826257e-3

    x = np.reshape(x, -1)
    r2 = np.dot(x, x)
    r3 = r2*np.sqrt(r2)
    omg2 = OMGE_GLO**2

    if r2 <= 0:
        xdot = np.zeros((6, 1))
        return xdot

    a = 1.5*J2_GLO*MU_GLO*RE_GLO ^ 2/r2/r3  # 3/2*J2*mu*Ae^2/r^5
    b = 5.0*x(3)*x(3)/r2  # 5*z^2/r^2
    c = -MU_GLO/r3-a*(1.0-b)  # -mu/r^3-a(1-b)
    xdot[0, 0] = x[3]
    xdot[1, 0] = x[4]
    xdot[2, 0] = x[5]
    xdot[3, 0] = (c+omg2)*x[0]+2*OMGE_GLO*x[4]+acc[0, 0]
    xdot[4, 0] = (c+omg2)*x[1]-2*OMGE_GLO*x[3]+acc[1, 0]
    xdot[5, 0] = (c-2*a)*x[2]+acc[2, 0]

    return xdot
