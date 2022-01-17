import win32com.client
from win32com.client import gencache, Dispatch, constants, DispatchEx


oApp = win32com.client.Dispatch('Inventor.Application')
oApp.Visible = True
mod = gencache.EnsureModule('{D98A091D-3A0F-4C3E-B36E-61F62068D488}', 0, 1, 0)
oApp = mod.Application(oApp)
oApp.SilentOperation = True
oDoc = oApp.ActiveDocument
oDoc = mod.PartDocument(oDoc)

prop = oApp.ActiveDocument.PropertySets.Item("Design Tracking Properties")

# getting description and designer from iproperties (works)
Descrip = prop('Description').Value
Designer = prop('Designer').Value

print(Descrip)
prop('Description').Value = "40 tooth"
print(Descrip)
print(Designer)



# getting mass and parameters (doesn´t work)
MassProps = oDoc.ComponentDefinition.MassProperties
partDef = oDoc.ComponentDefinition.Parameters

dArea = MassProps.Area
print(dArea)

lNum = partDef.Count
print(lNum)