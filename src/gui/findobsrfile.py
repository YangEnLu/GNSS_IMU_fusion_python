from ..common.global_constants import gls, ftime
import os
def findobsrfile(filepath,sitename):
    fullname = ""
    file_time = ftime()
    #search the obsr file
    fileExt = "O"
    files = [f for f in os.listdir(filepath) if f.endswith(fileExt)]
    if not files:
        fileExt = "o"
        files = [f for f in os.listdir(filepath) if f.endswith(fileExt)]
    
    nf = len(files)
    if nf == 0:
        return True
    
    for i in range(nf):
        
        pass