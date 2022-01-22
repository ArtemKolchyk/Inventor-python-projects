#работа с ребрами, поверхностями, точками детали
#принт функция
def print_list(list):
    for item in list:
        print(item)
#length, center point, major, minor, Area, Diameter, type
def edges_all_prop(part):
    #возращает список длин всех ребер детали
    edge_list = [] #ребра и их все параметры
    for item in part.ComponentDefinition.SurfaceBodies:
            for edge in item.Edges:
                if edge.CurveType != 5122: #если ребро не прямая линия, то:
                    rib = [] #список ребра с его параметрами
                    center_points = [] #список центра кривой
                    list = edge.Evaluator.GetParamExtents() #список точек ребра для расчета длины старт и конец
                    edge_length = edge.Evaluator.GetLengthAtParam(list[0], list[1])*10 #идем по кривой между точками и получаем длину ребра
                    rib.append(round(edge_length, 2)) #добавляем длины ребер в массив округляя до стотых
                    #точки центров кривых
                    center_points.append(round(edge.Geometry.Center.X*10,2))
                    center_points.append(round(edge.Geometry.Center.Y*10,2))
                    center_points.append(round(edge.Geometry.Center.Z*10,2))
                    rib.append(center_points)
                    try:
                        major = round(edge.Geometry.MajorAxisVector.Length*10,2)
                        rib.append(major) #major длина
                        MinorMajorRatio = edge.Geometry.MinorMajorRatio
                        minor = round(edge.Geometry.MajorAxisVector.Length*10*MinorMajorRatio,2)
                        rib.append(minor) #minor длина
                    except:
                        major = round(edge.Geometry.Radius*10,2)
                        rib.append(major)#major для круга
                        minor = round(edge.Geometry.Radius*10,2)
                        rib.append(minor)#minor для круга
                    #добавим площади и диаметры кругов
                    if rib[len(rib)-1] == rib[len(rib)-2]:
                        S = round(3.1415 * rib[len(rib)-1] * rib[len(rib)-2],1)
                        rib.append(S)
                        D = round((S/3.1415) **0.5 * 2, 1)
                        rib.append(D)
                        rib.append('circle')
                    else:
                        S = round(3.1415 * rib[len(rib)-1] * rib[len(rib)-2] * MinorMajorRatio, 1)
                        rib.append(S)
                        D = round((S/3.1415) **0.5 * 2, 1)
                        rib.append(D)
                        rib.append('curve')
                    edge_list.append(rib) 
                    print(rib)
                             
    #print(edge_list)
    return edge_list


def pipe_THK(part):
    edge_list = edges_all_prop(part)
    list_thk = []
    for x in range(0, len(edge_list)-1, 1):
        for y in range(0, 3, 1):
            if edge_list[x][1][y] == edge_list[x+1][1][y]:
                list_thk.append(round(abs(edge_list[x][2]-edge_list[x+1][2]),2))
                list_thk.append(round(abs(edge_list[x][3]-edge_list[x+1][3]),2))
    THK = max(set(list_thk), key=list_thk.count) #возвращаем чаще всего встречающуюся толщину                            
    return THK 

def pipe_points(part):
    edge_list = edges_all_prop(part)
    #получаем координаты всех точек
    #points_list = []  #point, area, OD, type
    for x in range(0, len(edge_list)-1, 1):
        points_list = []
        for y in range(x+1, len(edge_list), 1):
            if edge_list[x][1] ==  edge_list[y][1]:
                points_list.append(edge_list[x][1])
                points_list.append(abs(edge_list[x][4]-edge_list[y][4]))
                points_list.append(max(edge_list[x][5], edge_list[y][5]))
                points_list.append(edge_list[x][6])
                print(points_list)

 
