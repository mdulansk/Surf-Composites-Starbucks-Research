import numpy as np
import math
import scipy
import matplotlib.pyplot as plt

#EPS Foam Compression regression from reseach gate data
#KG/M^3 and MPA
densities = np.array([43, 64, 80, 120])
yields = np.array([0.33, 0.53, 0.70, 1.26])
initial = np.array([10,-2])
def sumedSquares(x):
    a0 = x[0]
    a1 = x[1]
    E = np.sum((np.log(yields) - (a1*np.log(densities) + a0))**2)
    return E

finals = scipy.optimize.minimize(sumedSquares, initial)

def compressiveStrengthEPS(density):
    #Input KG/M^3 returns PSI
    PSIperMPA = 145.038
    A0 = finals.x[0]
    A1 = finals.x[1]
    predicted_strength = A1*math.log(density)+A0
    PSIYeild = np.exp(predicted_strength)*PSIperMPA
    return PSIYeild




#Coupon Sizing Equations
kgm3topcf = 0.062427961
EPSdensity = 20*kgm3topcf #pounds per cubic foot


S = 0#Span in Inches
L = 0#Loading Span in Inches
sigma = 0#Expected facing ultimate strength in PSI
t = 0#Facing Thickness
c = 2.5 #Core thickness in Inches
Fs = 0#Core Shear Allowable Strength in PSI
k = 0.75 #Core shear strength factor to ensure facing failure
Lpad = 0#dimension of loading pad in specimen lengthwise direction in INches
Fc = compressiveStrengthEPS(22) #Core Compression allowable strength PSI

print(Fc)
