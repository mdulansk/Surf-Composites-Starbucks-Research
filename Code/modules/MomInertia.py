import numpy as np
import matplotlib.pyplot as plt
#from scipy.spatial import Delaunay

def moments_of_inertia(yzs, E, mats):
    # Calculate centroid
    areas = []
    ycs = []
    zcs = []
    ea = []
    plt.ioff()
    fig, ax = plt.subplots()
    length = 24 #inches
    weight = 0
    for i,yz in enumerate(yzs):
        y, z = yz
        areas.append(0.5*np.abs(np.dot(y,np.roll(z,1))-np.dot(z,np.roll(y,1))))
        ycs.append(np.sum(y)/len(y))
        zcs.append(np.sum(z)/len(z))
        ea.append(E[i]*areas[i])
        weight += areas[i]*length*mats[list(mats)[i]][1]
        ax.plot(np.concatenate((y, [y[0]])), np.concatenate((z, [z[0]])),\
                 linewidth=1,color=mats[list(mats)[i]][0])#,label=list(mats)[i])
    EA = sum(ea)
    yc = np.sum([E[i]*areas[i]*ycs[i] for i in range(len(ycs))]) / EA
    zc = np.sum([E[i]*areas[i]*zcs[i] for i in range(len(zcs))]) / EA
    #ax.scatter(yc,zc,color = 'red')#,label='Centroid')
    ax.scatter(yc, zc, color='black', marker='X')  # Black cross
    ax.annotate(f'({yc:.2f}, {zc:.2f})', (yc, zc), textcoords="offset points", xytext=(30,5), ha='center',fontsize=9)  # Display coordinates

    min_y = min(min(inner_list[0]) for inner_list in yzs)
    max_y = max(max(inner_list[0]) for inner_list in yzs)
    min_z = min(min(inner_list[1]) for inner_list in yzs)
    max_z = max(max(inner_list[1]) for inner_list in yzs)
    plt.xlim(min_y-.025,max_y+.025)
    plt.ylim(min_z-.025,max_z+.025)
    plt.xlabel('y-axis')
    plt.ylabel('z-axis')
    plt.axis('equal')

    EIyy = 0.0
    EIzz = 0.0
    EIyz = 0.0

    for yz, e in zip(yzs, E):
        y, z = yz
        # Calculate coordinates relative to centroid

        y_c =  sum(y)/len(y) - yc
        z_c = sum(z)/len(z) - zc
        # Calculate area and second moments of area
        A = 0.5*np.abs(np.dot(y,np.roll(z,1))-np.dot(z,np.roll(y,1)))
        b = np.max(y) - np.min(y)
        h = np.max(z) - np.min(z)
        Iyy = (b * h**3) / 12.0
        Izz = (h * b**3) / 12.0
        EIyy += e * (Iyy + A * z_c**2)
        EIzz += e * (Izz + A * y_c**2)
        EIyz += e * np.sum(y_c * z_c) * A
    return EIyy, EIzz, EIyz, EA, weight, zc, yc, fig