# -*- coding: utf-8 -*-
#анализ типа детали

def analize(part):
    if part.ComponentDefinition.BOMStructure == 51973:
        return 'purchase'

    flat_area = 0
    other_area = 0
    for item in part.ComponentDefinition.SurfaceBodies:
        for face in item.Faces:
            if face.SurfaceType == 5890:
                flat_area = flat_area + face.Evaluator.Area
                continue
            other_area = other_area + face.Evaluator.Area
    if flat_area > other_area:
        return 'plate'
    return 'pipe'