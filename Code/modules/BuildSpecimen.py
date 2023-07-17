import sys
sys.path.append('../classes')
import numpy as np
import sympy as sym
from Material import Material
from SandwichPanel import TestSpecimen
import pandas as pd

def build_specimens_output(fp):

    specimens_df = pd.read_excel(fp)
    specimens_df.head()

    #Defining Materials - Metric
    Eglass6oz = Material("6oz_Eglass", 4305899, 4305899, 7.687E14, 0.17,  0.0903)
    Eglass4oz = Material("4oz_Eglass", 4305899 * 2/3, 4305899 * 2/3,5.3E9*2/3, 0.17,  0.0903*2/3)
    EPS_Foam = Material("EPS_Foam", 5511.56, 5511.56, 2755.78, 0.32, 0.00197)
    PU_Foam = Material("PU_Foam", 31900.46, 31900.46, 0, 0, 0.00866)
    Balsa = Material("Balsa", 319004.63, 319004.63, 15364.21, .25, 0.00903) 
    Basswood = Material("Basswood", 1029013.39, 0, 0, 0.01156)
    Carbon = Material("Carbon", 21760000000, 21760000000, 0, 0.0578)

    #Defining Material Mapping
    material_mapping = {
        'Eglass6oz': Eglass6oz, 
        'Eglass4oz': Eglass4oz, 
        'EPS_Foam': EPS_Foam, 
        'PU_Foam': PU_Foam, 
        'Balsa': Balsa, 
        'Basswood': Basswood, 
        'Carbon': Carbon
    }

    #Defining Output DataFrame
    specimen_results = specimens_df.copy()
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
        #P = ro['Failure Load (lb)']
        L = ro['Half Distance Between Supports']
        Lw = ro['Lw']
        name = ro['ID']
        return TestSpecimen(construction,L,Lw,name)
    # KEEP ADDING NEW THINGS TO specimen_results
    specimen_results['TestSpecimens'] = specimens_df.apply(lambda ro: np.nan if ro.drop('PreLaminated Weight (g)').isna().any()\
                                                        else make_specimen_object(ro),axis=1)
    return specimen_results