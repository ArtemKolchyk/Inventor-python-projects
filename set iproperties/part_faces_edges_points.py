#работа с ребрами, поверхностями, точками детали

L = [] #список длин ребер

def edges_length(part):
    #возращает список длин всех ребер детали
    for item in part.ComponentDefinition.SurfaceBodies:
            for edge in item.Edges:
                #center_coord = []
                list = edge.Evaluator.GetParamExtents() #список точек ребра для расчета длины старт и конец
                edge_length = edge.Evaluator.GetLengthAtParam(list[0], list[1])*10 #идем по кривой между точками и получаем длину ребра
                center_coord_X = edge.Geometry.Center.X
                center_coord_Y = edge.Geometry.Center.X
                L.append(round(edge_length, 2)) #добавляем длины ребер в массив округляя до стотых
    return L