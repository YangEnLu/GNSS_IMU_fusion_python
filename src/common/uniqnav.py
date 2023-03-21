from .global_constants import nav, glc
from .uniqeph import uniqeph
from .uniqgeph import uniqgeph
from .satwavelen import satwavelen

def uniqnav(nav: nav):
    if nav.n > 0:
        nav = uniqeph(nav)
        
        
    if nav.ng > 0:
        nav = uniqgeph(nav)
    
    for i in range(glc().MAXSAT):
        for j in range(glc().MAXFREQ):
            nav.lam[i,j] = satwavelen(i+1,j+1,nav)

    return nav
