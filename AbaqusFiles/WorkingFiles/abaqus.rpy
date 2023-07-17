# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2022 replay file
# Internal Version: 2021_09_15-10.57.30 176069
# Run by mdulansk on Fri Jul 14 12:40:38 2023
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=178.32568359375, 
    height=188.597229003906)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
openMdb('SandwichPanel - Copy (2).cae')
#: The model database "D:\Documents\SurfboardProj\SurfURS\AbaqusFiles\WorkingFiles\SandwichPanel - Copy (2).cae" has been opened.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Balsa'].parts['BottomSupport']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['Balsa'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['Balsa'].parts['BottomSupport']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
mdb.save()
#: The model database has been saved to "D:\Documents\SurfboardProj\SurfURS\AbaqusFiles\WorkingFiles\SandwichPanel - Copy (2).cae".
mdb.save()
#: The model database has been saved to "D:\Documents\SurfboardProj\SurfURS\AbaqusFiles\WorkingFiles\SandwichPanel - Copy (2).cae".
