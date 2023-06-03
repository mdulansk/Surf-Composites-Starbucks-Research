import sys
sys.path.append('../classes')
import numpy as np
import sympy as sym
from Material import Material
# from abdCalcs import ABDs
from SandwichPanel import TestSpecimen
from MomInertia import moments_of_inertia
import os
import pandas as pd


################# Testing Moment of Inertia originally ##########################33
#Test is moments of Inertia works
E1 = 100
rho_1 = 2
E2 = 50
rho_2 = 5
top_lam = [[0,5,5,0],[4,4,6,6]] #Inches
string = [[2,3,3,2],[0,0,4,4]]
yzs = np.array([top_lam,string])
E = [E1,E2]
mats = mats = {'Top Lam':['orange',rho_1],'Bot Lam':['brown',rho_2]}
q,w,e,r,t,y,u,fig = moments_of_inertia(yzs,E,mats)

######################## Testing TestSpeciemn #######################################
#Material('Name',E1,E2,G12,v12,rho)
Eglass6oz = Material("6oz_Eglass", 4305899, 4305899, 7.687E14, 0.17,  0.0903)
Eglass4oz = Material("4oz_Eglass", 4305899 * 2/3, 4305899 * 2/3,5.3E9*2/3, 0.17,  0.0903*2/3)
EPS_Foam = Material("EPS_Foam", 5511.56, 5511.56, 2755.78, 0.32, 0.00197)
PU_Foam = Material("PU_Foam", 31900.46, 31900.46, 0, 0, 0.00866)
Balsa = Material("Balsa", 319004.63, 319004.63, 15364.21, .25, 0.00903) 
Basswood = Material("Basswood", 1029013.39, 0, 0, 0.01156)
Carbon = Material("Carbon", 21760000000, 21760000000, 0, 0.0578)
material_mapping = {'Eglass6oz':Eglass6oz}
material_mapping = {
    'Eglass6oz': Eglass6oz, 
    'Eglass4oz': Eglass4oz, 
    'EPS_Foam': EPS_Foam, 
    'PU_Foam': PU_Foam, 
    'Balsa': Balsa, 
    'Basswood': Basswood, 
    'Carbon': Carbon
}
w_balsa = 0.125
t = .25E-3*1/(0.0254)
h_eps = 2.5
w_eps = 6

construction = {'Stringer':[Balsa,w_balsa],'Top Lam':[[Eglass4oz,t],[Eglass6oz,t]],\
            'Core':[EPS_Foam,h_eps,w_eps],'Bot Lam':[[Eglass4oz,t]]}
P = 300
L = 11
Lw = 2
TDid_Test = TestSpecimen(construction,P,L,Lw)

######################### Testing BuildSpecimen.py ##################################

#Material('Name',E1,E2,G12,v12,rho)
Eglass6oz = Material("6oz_Eglass", 4305899, 4305899, 7.687E14, 0.17,  0.0903)
Eglass4oz = Material("4oz_Eglass", 4305899 * 2/3, 4305899 * 2/3,5.3E9*2/3, 0.17,  0.0903*2/3)
EPS_Foam = Material("EPS_Foam", 5511.56, 5511.56, 2755.78, 0.32, 0.00197)
PU_Foam = Material("PU_Foam", 31900.46, 31900.46, 0, 0, 0.00866)
Balsa = Material("Balsa", 319004.63, 319004.63, 15364.21, .25, 0.00903) 
Basswood = Material("Basswood", 1029013.39, 0, 0, 0.01156)
Carbon = Material("Carbon", 21760000000, 21760000000, 0, 0.0578)
material_mapping = {'Eglass6oz':Eglass6oz}
material_mapping = {
    'Eglass6oz': Eglass6oz, 
    'Eglass4oz': Eglass4oz, 
    'EPS_Foam': EPS_Foam, 
    'PU_Foam': PU_Foam, 
    'Balsa': Balsa, 
    'Basswood': Basswood, 
    'Carbon': Carbon
}
w_balsa = 0.125
t = .25E-3*1/(0.0254)
h_eps = 2.5
w_eps = 6
#Reading in Coupond Data Sheet
cwd = os.getcwd()
pardir = os.path.dirname(os.path.dirname(cwd))
specimens_fp = os.path.join(pardir,'CouponData','CouponIDDataSheetReformat.xlsx')
specimens_df = pd.read_excel(specimens_fp)
specimens_df.head()
#Defining Output DataFrame
specimen_results = specimens_df.copy()
#Test making one specimen object out of the first index
def make_specimen_object(ro):
    construction = {'Stringer':[],'Top Lam':[],\
            'Core':[],'Bot Lam':[]}
    construction['Stringer'].append(material_mapping[ro['Stringer Material']])
    construction['Stringer'].append(ro['Stringer Width (in)'])
    construction['Core'].append(material_mapping[ro['Foam Material']])
    construction['Core'].append(ro['Foam Height'])
    construction['Core'].append(ro['Foam Width'])
    for toplam in ro['Top Lamina'].split(','):
        construction['Top Lam'].append([material_mapping[toplam],ro['Lamina Thickness']])
    for botLam in ro['Bottom Lamina'].split(','):
        construction['Bot Lam'].append([material_mapping[botLam],ro['Lamina Thickness']])
    P = ro['Failure Load (lb)']
    L = ro['Half Distance Between Supports']
    Lw = ro['Lw']
    return TestSpecimen(construction,P,L,Lw)