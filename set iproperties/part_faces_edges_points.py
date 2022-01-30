# -*- coding: utf-8 -*-
from math import asin
from edges import edge_center_point, point_to_point_line, point_to_point_arc, ratio_major_minor, area, diameter

#работа с ребрами, поверхностями, точками детали
#принт функция
def print_list(list):
    for item in list:
        print(item,",")
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
    return edge_list


#все поверхности    
def plane_surface(part):
    for item in part.ComponentDefinition.SurfaceBodies:
            # определяем центры образующих ребер
            faces_list = []
            length = 0
            for face in item.Faces:
                if face.SurfaceType == 5893:
                    return False
                #5891 - cylinder surface
                #5890 - plane surface
                #5895 - torus surface
                temp = []
                dia = []
                points = []
                count = 0
                for edge in face.Edges:
                    if edge.GeometryType == 5128:
                        count = count + 1
                        continue
                    dia.append(diameter(edge))
                    if edge_center_point(edge) not in points:
                        points.append(edge_center_point(edge))
                        ratio = ratio_major_minor(edge)[0]
                if count == face.Edges.Count:
                    continue
                temp.append(points)
                temp.append(dia)
                temp.append(ratio)
                temp.append(face_type(face))
                if len(points) == 2:
                    if face_type(face) == 'torus':
                        D = face.Geometry.MajorRadius*2*10
                        dimension = point_to_point_arc(points, D)    
                    else:
                        dimension = point_to_point_line(points)
                    temp.append(dimension)
                else:
                    temp.append(0)
                OD = max(dia)
                try:
                    THK = abs((dia[0]- dia[1])/2)
                except:
                    THK = 0
                temp.append(OD)
                temp.append(THK)
                temp.append(ratio_major_minor(edge)[1])
                faces_list.append(temp)
    table = faces_list
    length = pipe_length(table)
    OD = pipe_OD(faces_list)
    THK = pipe_thk(faces_list)
    add = add_length(faces_list, OD)
    length = length + add
    #print_list(faces_list)
    #print(length)
    #[points, ratio, surface, length, OD, THK, major]
    return [OD, THK, length]
    

        
def face_type(face):
    x = face.SurfaceType
    return {
        5891: "cylinder",
        5890: "plane",
        5895: "torus"
    }.get(x, False)    # False will be returned default if x is not found

def pipe_length(table):
    l = table[0][4]
    temp_length_list = []
    temp_length_list.append(table[0][0])
    for i in range(0, len(table)-1, 1):
        for y in range(i+1, len(table), 1):
            if table[y][0] not in temp_length_list and table[y][4] != 0 and shift_points(table[y][0]) not in temp_length_list:
                l = l + table[y][4]
                temp_length_list.append(table[y][0])
                
    return l 

def pipe_thk(table):
    thk_list = []
    for i in range(0, len(table), 1):
        thk_list.append(table[i][6])
    thk = max(thk_list)
    return thk

def pipe_OD(table):
    od_list = []
    for i in range(0, len(table), 1):
        od_list.append(table[i][5])
    od = max(od_list)
    return od

def add_length(table, OD):
    add_length = 0
    for i in range(0, len(table), 1):
        if table[i][2] < 1:
            add_length = add_length + (table[i][7]**2 - (OD/2)**2)**0.5
    return add_length

def shift_points(list):
    a = list[0]
    b = list[1]
    return [b, a]
    