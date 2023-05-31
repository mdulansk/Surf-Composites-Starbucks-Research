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

def shearStrengthEPS(density):
    #Input KG/M^3 return PSI
    T=density
    shearStrengthKpa = 0.841*T + 9.9
    shearStrengthPSI = shearStrengthKpa*(0.145038)
    return shearStrengthPSI


#Coupon Sizing Equations
kgm3topcf = 0.062427961
EPSdensity = 20*kgm3topcf #pounds per cubic foot
PSIperMPA = 145.038
meterToInch = 39.3701

######################
#6oz lamina (not accurate Values)
E1_6 = 29.7E9
E2_6 = 29.7E9
G12_6 = 5.3E9
v12_6 = 0.17
t = .25E-3;#meters

#4oz lamina (also not accurate)
E1_4 = E1_6*.85
E2_4 = E2_6*.85
G12_4 = G12_6*.85
v12_4 = v12_6
rho_4 = 539.99 #kg/m^3
###################################






#S = #Derived #Span in Inches
L = 0 #Loading Span in Inches
sigma = 300*PSIperMPA#Expected facing ultimate strength in PSI
t = t * meterToInch#Facing Thickness
c = 2.5 #Core thickness in Inches
Fs = shearStrengthEPS(22) #Core Shear Allowable Strength in PSI
k = 0.75 #Core shear strength factor to ensure facing failure
Lpad = 6 #dimension of loading pad in specimen lengthwise direction in INches
Fc = compressiveStrengthEPS(22) #Core Compression allowable strength PSI

print(Fc)
print(Fs)

#Calculate Span
#S = (2*sigma*t)/(k*Fs) + L

S = (2*(c+t)*sigma*t)/(Lpad * Fc) + L

print(S)



