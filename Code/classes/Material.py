import numpy as np
class Material:

    def __init__(self,Name,E1=np.nan,E2=np.nan,G12=np.nan,v12=np.nan,rho=np.nan):
        self.Name = Name
        self.E1 = E1
        self.E2 = E2
        self.G12 = G12
        self.v12 = v12
        self.rho = rho
        
    
