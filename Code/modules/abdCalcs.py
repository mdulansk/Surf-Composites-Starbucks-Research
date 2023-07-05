import numpy as np
import math

def StressStrainTransform(theta):
    Tsigma = np.zeros((3, 3), dtype=float)
    Tsigma[0,0] = math.cos(math.radians(theta))**2
    Tsigma[0,1] = math.sin(math.radians(theta))**2
    Tsigma[0,2] = 2*math.cos(math.radians(theta))*math.sin(math.radians(theta))
    Tsigma[1,0] = Tsigma[0,1]
    Tsigma[1,1] = Tsigma[0,0]
    Tsigma[1,2] = -Tsigma[0,2]
    Tsigma[2,0] = -math.cos(math.radians(theta))*math.sin(math.radians(theta))
    Tsigma[2,1] = -Tsigma[2,0]
    Tsigma[2,2] = math.cos(math.radians(theta))**2 - math.sin(math.radians(theta))**2

    Tstrain = Tsigma.copy()
    
    Tstrain[0,2] = Tsigma[2,1]
    Tstrain[1,2] = Tsigma[2,0]
    Tstrain[2,0] = Tsigma[1,2]
    Tstrain[2,1] = Tsigma[0,2]
    return Tsigma, Tstrain

def QandS(E1,E2,G12,v12,theta):
    S11 = 1/E1
    S12 = -v12/E1
    S16 = 0
    S21 = S12
    S22 = 1/E2
    S26 = 0
    S61 = 0
    S62 = 0
    S66 = 1/G12
    S = np.array([[S11,S12,S16],[S21,S22,S26],[S61,S62,S66]])
    Q = np.linalg.inv(S)
    [Tsigma, Tstrain] = StressStrainTransform(theta)
    Q_bar = Tstrain.T@Q@Tstrain
    S_bar = Tsigma.T@S@Tsigma
    return Q, S, Q_bar, S_bar

def ABD(E1,E2,G12,v12,theta, t):
    t_total = t*len(theta)
    z_bottom = -t_total/2
    z_index = 0
    z = np.zeros((len(theta),len(theta)),dtype=float)
    for j in range(len(theta)):
        z[j,0] = z_bottom + z_index*(j)
        z_index = t
    
    z_index = 0
    for j in range(len(theta)):
        z[j,1] = z_bottom + t + z_index*(j)
        z_index = t

    Q = np.zeros((3,3,len(theta)))
    S = np.zeros((3,3,len(theta)))
    Q_bar = np.zeros((3,3,len(theta)))
    S_bar = np.zeros((3,3,len(theta)))
    for i in range(len(theta)):
        Q_i,S_i,Q_bar_i,S_bar_i = QandS(E1[i],E2[i],G12[i],v12[i],theta[i])
        Q[:, :, i] = Q_i
        S[:, :, i] = S_i
        Q_bar[:, :, i] = Q_bar_i
        S_bar[:, :, i] = S_bar_i

    A = np.zeros((3, 3))
    B = np.zeros((3, 3))
    D = np.zeros((3, 3))

    for k in range(len(theta)):
        A = A + np.dot(Q_bar[:,:,k],(z[k,1]-z[k,0]))
        B = B + np.dot(Q_bar[:,:,k],(z[k,1]**2-z[k,0]**2))
        D = D + np.dot(Q_bar[:,:,k],(z[k,1]**3-z[k,0]**3))
    
    
    B = (1/2)*B
    D = (1/3)*D

    # delta = inv(D-(B*inv(A)*B));
    # beta = -(inv(A)*B*delta);
    # alpha = inv(A) + (inv(A)*B*delta*B*inv(A));
    return A,B,D