from ..common.global_constants import nav

def decode_navh(nav: nav, fname: str):
    fid = open(fname, "r")
    num_line = 0
    for line in fid:
        num_line = num_line+1
        label = line[60:-1]
        if label.find("ION ALPHA") != -1:
            j = 2
            for i in range(4):
                
                pass
        

    return nav, num_line
