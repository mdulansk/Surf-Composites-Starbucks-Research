import numpy as np
import matplotlib.pyplot as plt
from abdCalcs import ABD

def moments_of_inertia(yzs, E, mats):
    # Calculate centroid
    areas = []
    ycs = []
    zcs = []
    fig, ax = plt.subplots()
    length = 14 * .0254 #meters
    weight = 0
    for i,yz in enumerate(yzs):
        y, z = yz
        areas.append(0.5*np.abs(np.dot(y,np.roll(z,1))-np.dot(z,np.roll(y,1))))
        ycs.append(np.sum(y)/len(y))
        zcs.append(np.sum(z)/len(z))
        weight += areas[i]*length*mats[list(mats)[i]][1]
        ax.plot(np.concatenate((y, [y[0]])), np.concatenate((z, [z[0]])),\
                 linewidth=1,color=mats[list(mats)[i]][0])#,label=list(mats)[i])

    area_total = sum(areas)
    yc = np.sum([a*c for a,c in zip(areas,ycs)]) / area_total
    zc = np.sum([a*c for a,c in zip(areas,zcs)]) / area_total

    ax.scatter(yc,zc,color = 'red')#,label='Centroid')
    min_y = min(min(inner_list[0]) for inner_list in yzs)
    max_y = max(max(inner_list[0]) for inner_list in yzs)
    min_z = min(min(inner_list[1]) for inner_list in yzs)
    max_z = max(max(inner_list[1]) for inner_list in yzs)
    plt.xlim(min_y-.025,max_y+.025)
    plt.ylim(min_z-.025,max_z+.025)
    plt.xlabel('y-axis')
    plt.ylabel('z-axis')
    plt.axis('equal')
    #plt.legend(loc='upper right')

    # Calculate moments of inertia
    EIyy = 0.0
    EIzz = 0.0
    EIyz = 0.0
    EA = 0.0
    for yz, e in zip(yzs, E):
        y, z = yz
        # Calculate coordinates relative to centroid
        y_c =  y - yc
        z_c = z - zc
        # Calculate area and second moments of area
        A = 0.5*np.abs(np.dot(y_c,np.roll(z_c,1))-np.dot(z_c,np.roll(y_c,1)))
        EIyy += e*np.sum(z_c**2)*A
        EIzz += e*np.sum(y_c**2)*A
        EIyz += e*np.sum(y_c*z_c)*A
        EA += e*A
    
    return EIyy, EIzz, EIyz, EA, weight