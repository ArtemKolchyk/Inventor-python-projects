import win32com.client
from win32com.client import gencache, Dispatch, constants, DispatchEx
from get_add_set_prop import get_prop, add_prop
from iprop_list import custom_properties_list
from fasteners_find import find_fasteners

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
#print(custom_properties_list[0])
for part in oRefDocs:
    for prop in custom_properties_list:
        if get_prop(part, "Inventor User Defined Properties", prop) == False:
            add_prop(part, "Inventor User Defined Properties", prop)
    find_fasteners(part)
    #print(get(part, "Inventor User Defined Properties", prop))
    