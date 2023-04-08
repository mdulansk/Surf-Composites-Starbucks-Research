import numpy as np
import math
import matplotlib as plt

#Make sure x and y are multiple dimension ndarrays: [[], []]
def EI_from_Scatter_Section(x,y,E):
    Areas = np.array([])
    for i in range(len(x)):
        coord_x = x[i]
        coord_y = y[i]
        Area = np.array([])
        for j in range(coord_x.shape[0]-2):
            area_element1 = (coord_x[0]*(coord_y[j+1] - coord_y[j+2]))
            area_element2 = (coord_x[j+1]*(coord_y[j+2] - coord_y[0]))
            area_element3 = (coord_x[j+2]*(coord_y[0] - coord_y[j+1]))
            area_element = (1/2)*(area_element1 + area_element2 + area_element3)
            Area = np.append(Area, np.array(area_element))
        Areas = np.append(Areas, np.sum(Area))

    return Areas

def EI_from_Scatter_Thinwalled(x,y,E,t):
    Areas = np.array([])
    EIxxs = np.array([])
    EIyys = np.array([])
    EIxys = np.array([])
    for i in range(len(x)):
        coord_x = x[i]
        coord_y = y[i]
        E_element = E[i]
        t_element = t[i]
        Area = np.array([])
        EIxx = np.array([])
        EIyy = np.array([])
        EIxy = np.array([])
        for j in range(coord_x.shape[0]-1):
            x1 = coord_x[j]
            x2 = coord_x[j+1]
            y1 = coord_y[j]
            y2 = coord_y[j+1]
            area_element1 = (x2 - x1)**2
            area_element2 = (y2 - y1)**2
            area_element = t_element*(area_element1 + area_element2)**(1/2)

            EIxx_element = E_element*(area_element/6)*(y1*(2*y1 + y2) + y2*(y1 + 2*y1))
            EIyy_element = E_element*(area_element/6)*(x1*(2*x1 + x2) + x2*(x1 + 2*x1))
            EIxy_element = E_element*(area_element/6)*(x1*(2*y1 + y2) + x2*(y1 + 2*y1))

            Area = np.append(Area, np.array(area_element))
            EIxx = np.append(EIxx, np.array(EIxx_element))
            EIyy = np.append(EIyy, np.array(EIyy_element))
            EIxy = np.append(EIxy, np.array(EIxy_element))

        Areas = np.append(Areas, np.sum(Area))
        EIxxs = np.append(EIxxs, np.sum(EIxx))
        EIyys = np.append(EIyys, np.sum(EIyy))
        EIxys = np.append(EIxys, np.sum(EIxy))

    return Areas, EIxxs, EIyys, EIxys
