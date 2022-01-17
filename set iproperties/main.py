import win32com.client
from win32com.client import gencache, Dispatch, constants, DispatchEx

Application = win32com.client.Dispatch('Inventor.Application')
Application.Visible = True
mod = gencache.EnsureModule('{D98A091D-3A0F-4C3E-B36E-61F62068D488}', 0, 1, 0)
Application = mod.Application(Application)
Application.SilentOperation = True
#получаем активный документ
oAssembly = Application.ActiveDocument
#подключаемся к сборке
oAssembly = mod.AssemblyDocument(oAssembly)
#получаем список файлов сборки (все детали)
oRefDocs = oAssembly.AllReferencedDocuments
#итерация по всем деталям
for x in oRefDocs:
    descr_prop = x.PropertySets.Item("Design Tracking Properties")('Designer').Value
    print(descr_prop)

#descr_prop = oAssembly.PropertySets.Item("Design Tracking Properties")('Designer').Value
#print(descr_prop)
# getting description and designer from iproperties (works)
#Descrip = prop('Description').Value
#Designer = prop('Designer').Value
'''
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
print(lNum)'''