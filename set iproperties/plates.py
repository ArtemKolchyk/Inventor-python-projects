
#plates
from get_add_set_prop import set_prop


def find_plates(part):
    for item in part.ComponentDefinition.SurfaceBodies:
        dim1 = item.OrientedMinimumRangeBox.DirectionOne.Length*10
        dim2 = item.OrientedMinimumRangeBox.DirectionTwo.Length*10
        dim3 = item.OrientedMinimumRangeBox.DirectionThree.Length*10
        box = [dim1, dim2, dim3]
        box = sorted(box, reverse = True)
        #print(box)
        length = f'{round(box[0],0):g}'
        width = f'{round(box[1],0):g}'
        thk = f'{round(box[2],0):g}'
        description = 'PLATE '+thk
        dim = length+"x"+width
        set_prop(part, "Inventor User Defined Properties", '(C) DESCRIPTION', description)
        set_prop(part, "Inventor User Defined Properties", '(G) DESCRIPTION', description)
        set_prop(part, "Inventor User Defined Properties", '(C) DIMENSIONS', dim)
        set_prop(part, "Inventor User Defined Properties", '(G) DIMENSIONS', dim)
        set_prop(part, "Inventor User Defined Properties", 'iprop_item_type', 'PLATE')
        