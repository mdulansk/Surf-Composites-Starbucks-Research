import sys
sys.path.append('../modules')
sys.path.append('../classes')
from Material import Material
import numpy as np
from abdCalcs import ABD
from ShearAndMoment import shear_and_moment
from MomInertia import moments_of_inertia
import os
from PlotFitTesting import plot_fit_test_data

class TestSpecimen:

    def __init__(self, construction,L,Lw,name):
        self.construction = construction
        self.E = []
        self.materials = {}
        self.abd_materials = {}
        self.yzs = []
        self.name = name
        self.L = L
        self.Lw = Lw
        self.calculate_E()
        self.get_test_data()
        # if not np.isnan(self.max_load):
        #     self.get_shear_moment(self.max_load)
        

    def calculate_E(self):
        mat_thickness = 0  # if multiple materials are given
        num_plies = {}
        for loc,material in self.construction.items():
            if isinstance(material[0], list):
                if loc == 'Top Lam':
                    num_plies['top'] = len(material)
                else:
                    num_plies['bot'] = len(material)
                for mat_info in material:
                    mat = mat_info[0]
                    if len(material) == 1:
                        continue
                    mat_thickness = mat_info[1]
                if len(material) == 1:
                    self.construction[loc] = self.construction[loc][0]
                    continue
                self.get_abd(mat_thickness,loc)
        self.get_geometry(self.construction['Core'][-1],self.construction['Core'][-2],\
            self.construction['Stringer'][1],self.construction['Top Lam'][-1],num_plies)
        self.calculate_moments_of_inertia()

    def get_abd(self,t,location):
        E1s = []
        E2s = []
        G12s = []
        v12s = []
        rhos = []
        for laminate in self.construction[location]:
            E1s.append(laminate[0].E1)
            E2s.append(laminate[0].E2)
            G12s.append(laminate[0].G12)
            v12s.append(laminate[0].v12)
            rhos.append(laminate[0].rho)
        A,B,D = ABD(E1s, E2s, G12s, v12s, [0 for _ in range(len(E1s))], t)
        a = np.linalg.inv(A)
        E1 = 1/(a[0,0]*(len(E1s)*t))
        E2 = 1/(a[1,1]*(len(E1s)*t))
        G12 = 1/(a[2,2]*(len(E1s)*t))
        v12 = -a[1,0]/a[0,0]
        rho = sum(rhos)/len(rhos)
        self.construction[location] = [Material(location,E1,E2,G12,v12,rho),len(E1s)*t]

    def get_geometry(self, w_foam,h_foam,w_string,t,num_plies):
            bot_lam = [[0,w_foam,w_foam,0],[0,0,num_plies['bot']*t,num_plies['bot']*t]]
            top_lam = [[0,w_foam,w_foam,0],\
    [num_plies['bot']*t+h_foam,num_plies['bot']*t+h_foam,num_plies['bot']*t+h_foam+num_plies['top']*t,num_plies['bot']*t+h_foam+num_plies['top']*t]]
            foam_left = [[0, (w_foam/2)-(w_string/2),(w_foam/2)-(w_string/2),0],\
                         [num_plies['bot']*t,num_plies['bot']*t,num_plies['bot']*t+h_foam,num_plies['bot']*t+h_foam]]
            string = [[(w_foam/2)-(w_string/2),(w_foam/2)+(w_string/2),(w_foam/2)+(w_string/2),(w_foam/2)-(w_string/2)],\
                      [num_plies['bot']*t,num_plies['bot']*t,num_plies['bot']*t+h_foam,num_plies['bot']*t+h_foam]]
            foam_right = [[(w_foam/2)+(w_string/2),w_foam,w_foam,(w_foam/2)+(w_string/2)],\
                          [num_plies['bot']*t,num_plies['bot']*t,num_plies['bot']*t+h_foam,num_plies['bot']*t+h_foam]]
            
            self.yzs.append(foam_left)
            self.yzs.append(foam_right)
            self.yzs.append(string)
            self.yzs.append(bot_lam)
            self.yzs.append(top_lam)

    def calculate_moments_of_inertia(self):
        self.materials = {'Foam Left':['silver',self.construction['Core'][0].rho],\
               'Foam Right':['silver',self.construction['Core'][0].rho],\
                'Stringer':['orange',self.construction['Stringer'][0].rho],\
                'Bot Lam':['brown',self.construction['Bot Lam'][0].rho],\
                'Top Lam':['brown',self.construction['Top Lam'][0].rho]}
        self.E = [self.construction[loc][0].E1 for loc in ['Core','Core','Stringer','Bot Lam','Top Lam']]
        self.EIyy, self.EIzz, self.EIyz, self.EA, self.weight, self.zc, self.yc, self.fig = \
            moments_of_inertia(np.array(self.yzs), self.E, self.materials)
    
    def get_test_data(self):
        cwd = os.getcwd()
        pardir = os.path.dirname(os.path.dirname(cwd))
        specimens_fp = os.path.join(pardir,'CouponData','TestingData',f'{self.name}TestData.txt')
        
        if os.path.exists(specimens_fp):
            self.testing_data_fig, self.max_load, self.max_displ = plot_fit_test_data(specimens_fp)
        else:
            print(f'File Path Not Found for test specimen {self.name}.')
            self.testing_data_fig, self.max_load = np.nan, np.nan
        
    def get_shear_moment(self,P):
        self.w_max, self.V_max, self.M_max, self.shear_moment_fig = \
        shear_and_moment(P,self.L,self.Lw)



    

    
