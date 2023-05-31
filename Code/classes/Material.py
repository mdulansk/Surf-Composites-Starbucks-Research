class Material:
    material_properties = {
    "6oz_Eglass": {"E1": 29.7E9, "E2": 29.7E9, "G12": 5.3E9, "v12": 0.17},
    "4oz_Eglass": {"E1": 29.7E9 * 2/3, "E2": 29.7E9 * 2/3, "G12": 5.3E9 * 2/3, "v12": .17},
    "EPS_Foam": {"E1": 3.80E7, "E2": 3.80E7, "G12": 1.9E7, "v12": 0.32},
    "PU_Foam": {"E1": .220E9, "E2": .220E9, "G12": 0, "v12": 0, "rho": .240 * 1000},
    "Balsa": {"E1": 2.20E9, "E2": 2.20E9, "G12": .106E9, "v12": .25},
    "Basswood": {"E1": 7.1E9, "E2": 7.1E9, "G12": 0, "v12": 0, "rho": 320},
    "Carbon": {"E1": 150E9, "E2": 0, "G12": 0, "v12": 0, "rho": 1600}
}

    def __init__(self, material_name):
        if material_name in Material.material_properties:
            self.material_name = material_name
        else:
            raise ValueError("Material '{}' properties has not been recorded.".format(material_name))

    def __getattr__(self, name):
        if name in Material.material_properties[self.material_name]:
            return Material.material_properties[self.material_name][name]
        else:
            raise AttributeError("'Material' object has no attribute '{}'".format(name))
