import sys
sys.path.append('../modules')
sys.path.append('../classes')
from Material import Material
import numpy as np
from abdCalcs import ABD
from MomInertia import moments_of_inertia
from scipy.interpolate import interp1d
#from SurfboardGeneration import offset, surfboard_outline
import matplotlib.pyplot as plt

class TestSpecimen:
    def __init__(self, construction):
        self.construction = construction
        self.E = []
        self.materials = {}
        self.abd_materials = {}
        self.yzs = []
        self.calculate_E()

    def calculate_E(self):
        mat_thickness = 0  # if multiple materials are given
        num_plies = {}
        for key in self.construction:
            material_info = self.construction[key]
            if isinstance(material_info[0], list):
                if key == 'topLam':
                    num_plies['top'] = len(material_info)
                else:
                    num_plies['bot'] = len(material_info)
                for mat_info in material_info:
                    mat_name = mat_info[0]
                    if len(material_info) == 1:
                        self.get_material_properties(mat_name)
                        continue
                    mat_thickness = mat_info[1]
                    self.get_abd_material_properties(mat_name)
                if len(material_info) == 1:
                    continue
                self.get_abd([y[0] for y in material_info],mat_thickness)
            else:
                mat_name = material_info[0]
                self.get_material_properties(mat_name)
        self.get_geometry(self.construction['core'][-1],self.construction['core'][-2],\
            self.construction['Stringer'][1],self.construction['topLam'][0][1],num_plies)
        self.calculate_moments_of_inertia()

    def get_material_properties(self, mat_name):
        material = Material(mat_name)
        self.materials[mat_name] = material
        print(mat_name)
        self.E.append(material.E1)
    
    def get_abd_material_properties(self, mat_name):
        abd_materials = Material(mat_name)
        self.abd_materials[mat_name] = abd_materials
        #self.E.append(abd_materials.E1)

    def get_abd(self, abd_mat_names,t):
        E1 = []
        E2 = []
        G12 = []
        v12 = []
        for mat_name in abd_mat_names:
            abd_material = self.abd_materials[mat_name]
            E1.append(abd_material.E1)
            E2.append(abd_material.E2)
            G12.append(abd_material.G12)
            v12.append(abd_material.v12)
        theta =  [0 for _ in range(len(E1))]
        A_top,B_top,D_top = ABD(E1, E2, G12, v12, [0 for i in range(len(E1))], t)
        a = np.linalg.inv(A_top)
        E1_top = 1/(a[0,0]*(2*t))
        print(theta)
        self.E.append(E1_top)

    def get_geometry(self, w_foam,h_foam,w_string,t,num_plies):
            bot_lam = [[0,w_foam,w_foam,0],[0,0,num_plies['bot']*t,num_plies['bot']*t]]
            top_lam = [[0,w_foam,w_foam,0],[num_plies['bot']*t+h_foam,num_plies['bot']*t+h_foam,\
                                              num_plies['bot']*t+h_foam+num_plies['top'],num_plies['bot']*t+h_foam+num_plies['top']]]
            foam_left = [[0, (w_foam/2)-(w_string/2),(w_foam/2)-(w_string/2),0],[num_plies['bot']*t,\
                                                    num_plies['bot']*t,num_plies['bot']*t+h_foam,num_plies['bot']*t+h_foam]]
            string = [[(w_foam/2)-(w_string/2),(w_foam/2)+(w_string/2),(w_foam/2)+(w_string/2),(w_foam/2)-(w_string/2)],\
                      [num_plies['bot']*t,num_plies['bot']*t,num_plies['bot']*t+h_foam,num_plies['bot']*t+h_foam]]
            foam_right = [[(w_foam/2)+(w_string/2),w_foam,w_foam,(w_foam/2)+(w_string/2)],\
                          [num_plies['bot']*t,num_plies['bot']*t,num_plies['bot']*t+h_foam,num_plies['bot']*t+h_foam]]
            self.yzs.append(foam_left)
            self.yzs.append(string)
            self.yzs.append(foam_right)
            self.yzs.append(bot_lam)
            self.yzs.append(top_lam)

    def calculate_moments_of_inertia(self):
        # Fix the inputs to moments_of_inertia to fit better with this class
        self.EIyy, self.EIzz, self.EIyz, self.EA, self.weight = moments_of_inertia(np.array(self.yzs), self.E, self.materials)
