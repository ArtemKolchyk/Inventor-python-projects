from math import asin

#работа с ребрами, поверхностями, точками детали
#принт функция
def print_list(list):
    for item in list:
        print(item,",")
#между точками
def point_to_point(plist): # plist = [[x1,y1,z1],[x2,y2,z2]]
    #измеряем расстояние между двумя точками
    #      ((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**0.5
    x1 = plist[0][0]
    x2 = plist[1][0]
    y1 = plist[0][1]
    y2 = plist[1][1]
    z1 = plist[0][2]
    z2 = plist[1][2]
    return round(((abs(x2-x1))**2+(abs(y2-y1))**2+(abs(z2-z1))**2)**0.5,2)
#между точками по кривой
def point_to_point_arc(plist, D):
    X = point_to_point(plist) #хорда
    L = D * asin(X/D)
    return round(L,2)
#length, center point, major, minor, Area, Diameter, type
def edges_all_prop(part):
    #возращает список длин всех ребер детали
    edge_list = [] #ребра и их все параметры
    for item in part.ComponentDefinition.SurfaceBodies:
            for edge in item.Edges:
                if edge.CurveType != 5122 and edge.CurveType != 5128: #если ребро не прямая линия, то:
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
                    #print(rib)
                             
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
    points_list = []  #point, area, OD, type   
    for x in range(0, len(edge_list)-1, 1):
        temp_list = []
        for y in range(x+1, len(edge_list), 1):
            if edge_list[x][1] ==  edge_list[y][1]:
                temp_list.append(edge_list[x][1])
                temp_list.append(round(abs(edge_list[x][4]-edge_list[y][4]),2))
                temp_list.append(max(edge_list[x][5], edge_list[y][5]))
                temp_list.append(edge_list[x][6])
                points_list.append(temp_list)
    #print_list(points_list)
    return points_list

def points_dimensions(part):
    #расстояние от каждой точки до остальных
    points_list = pipe_points(part)
    new_list = [] #точки с их расстояниями
    for i in range(0, len(points_list), 1):
        temp_list = []
        temp_list.append(points_list[i][0])
        point1 = points_list[i][0]
        sum_dim = 0
        for k in range(0, len(points_list), 1):
            point2 = points_list[k][0]
            dimension = point_to_point([point1, point2])
            sum_dim = sum_dim + dimension
        temp_list.append(round(sum_dim,2))
        new_list.append(temp_list)
    print_list(new_list)

#все поверхности    
def plane_surface(oPart):
    for item in oPart.ComponentDefinition.SurfaceBodies:
            # определяем центры образующих ребер
            center_edge_points = []
            count_flat_angle_surface = 0
            for face in item.Faces:
                    
                #5891 - cylinder surface
                #5890 - plane surface
                #5895 - torus surface
                if face.SurfaceType == 5890:
                    count_flat_angle_surface = count_flat_angle_surface + 1
                    
                    
                    
                temp_list = []
                for edge in face.Edges:
                    temp_point = []
                    temp_point.append(round(edge.Geometry.Center.X*10,2))
                    temp_point.append(round(edge.Geometry.Center.Y*10,2))
                    temp_point.append(round(edge.Geometry.Center.Z*10,2))
                    if temp_point not in temp_list:
                        temp_list.append(temp_point)
                if face.SurfaceType == 5895:
                    dimension = point_to_point_arc(temp_list, face.Geometry.MajorRadius*2*10)
                    temp_list.append(dimension)
                else:
                    if len(temp_list) == 2:
                        temp_list.append(point_to_point(temp_list))
                if temp_list not in center_edge_points:
                    center_edge_points.append(temp_list)
                
                    
    print_list(center_edge_points)
                
    