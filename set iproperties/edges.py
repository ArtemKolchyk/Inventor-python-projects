# -*- coding: utf-8 -*-
import math

#обработка ценра круглого или овального ребра
#возвращает координату центра ребра
def edge_center_point(edge): #return [X, Y, Z]
    try:
        X = round(edge.Geometry.Center.X*10,2)
        Y = round(edge.Geometry.Center.Y*10,2)
        Z = round(edge.Geometry.Center.Z*10,2)
        return [X, Y, Z]
    except:
        return False

def ratio_major_minor(edge):
    try:
        ratio = round(edge.Geometry.MinorMajorRatio,5)
        major = round(edge.Geometry.MajorAxisVector.Length*10,2)
        minor = round(major * ratio,2)
        return [ratio, major, minor]
    except:
        ratio = 1
        major = round(edge.Geometry.Radius*10,2)
        minor = round(edge.Geometry.Radius*10,2)
        return [ratio, major, minor]

#площадь сечения ребра
def area(edge):
    area = round(ratio_major_minor(edge)[1] * ratio_major_minor(edge)[2] * 3.1415 * ratio_major_minor(edge)[0],2)
    return area

#все диаметры
def diameter(edge):
    dia = round((area(edge)/3.1415)**0.5*2,1)
    return dia
    
#измеряем расстояние между двумя точками  # plist = [[x1,y1,z1],[x2,y2,z2]]   
def point_to_point_line(plist):    
    #      ((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**0.5
    x1 = plist[0][0]
    x2 = plist[1][0]
    y1 = plist[0][1]
    y2 = plist[1][1]
    z1 = plist[0][2]
    z2 = plist[1][2]
    return round(((abs(x2-x1))**2+(abs(y2-y1))**2+(abs(z2-z1))**2)**0.5,2)

#между точками по кривой # plist = [[x1,y1,z1],[x2,y2,z2]] , D -диаметр
def point_to_point_arc(plist, D):
    X = point_to_point_line(plist) #хорда
    L = D * math.asin(X/D)
    return round(L,2)

