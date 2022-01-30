# -*- coding: utf-8 -*-
#поиск труб
from get_add_set_prop import get_prop, add_prop, set_prop
from part_faces_edges_points import plane_surface

def set_pipe(part):
    pipe = plane_surface(part)
    if pipe != False:
        OD = f'{round(pipe[0],1):g}'
        THK = f'{round(pipe[1],1):g}'
        LENGTH = round(pipe[2])
        if THK == '0':
            description = "BAR Ø"+str(OD)
        else:
            description = "PIPE Ø"+OD+"x"+THK
        length = "L="+str(LENGTH)
        set_prop(part, "Inventor User Defined Properties", '(C) DESCRIPTION', description)
        set_prop(part, "Inventor User Defined Properties", '(G) DESCRIPTION', description)
        set_prop(part, "Inventor User Defined Properties", '(C) DIMENSIONS', length)
        set_prop(part, "Inventor User Defined Properties", '(G) DIMENSIONS', length)
        set_prop(part, "Inventor User Defined Properties", 'iprop_item_type', 'BAR/PIPE')
