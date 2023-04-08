import numpy as np
import math
import matplotlib.pyplot as plt

def coupon_coord_generator(coup_width, coup_height, quality, graph):

    radius = coup_height/2
    x0 = -coup_width/2
    xend = coup_width/2
    xcenter_neg = x0+radius
    xcenter_pos = xend-radius

    x = np.linspace(x0,xend,quality)
    x = np.append(x,np.flip(x)[1:len(x)])
    y = np.zeros(len(x))
    indexer = -1
    for i in x[0:int(np.round(len(x)/2))+1]:
        indexer+=1
        
        if i <= xcenter_neg:
            y[indexer] = -(radius)*math.sin(np.arccos((i-xcenter_neg)/radius))
        elif (xcenter_neg < i) and (i < xcenter_pos):
            y[indexer] = - radius
        elif i >= xcenter_pos:
            y[indexer] = -(radius)*math.sin(np.arccos((i-xcenter_pos)/radius))


    for i in x[int(np.round(len(x)/2))+1 : len(x)]:
        indexer+=1
        if i <= xcenter_neg:
            y[indexer] = (radius)*math.sin(np.arccos((i-xcenter_neg)/radius))
        elif (xcenter_neg < i) and (i < xcenter_pos):
            y[indexer] =  radius
        elif i >= xcenter_pos:
            y[indexer] = (radius)*math.sin(np.arccos((i-xcenter_pos)/radius))

    if graph:
        plt.scatter(x,y,s=0.25)
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')
        plt.draw()

    x_coupon = x
    y_coupon = y

    return x_coupon,y_coupon
