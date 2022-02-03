import win32com.client
from win32com.client import gencache, Dispatch, constants, DispatchEx
from get_add_set_prop import get_prop, add_prop, set_prop
from iprop_list import custom_properties_list
from fasteners_find import find_fasteners
from document_type import is_type
from item_type import analize
from pipes_find import set_pipe
from plates import find_plates

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
bar = len(oRefDocs)
count = 0
for item in oRefDocs:
    count = count + 1
    persentage = str(round(count/bar * 100))
    print(persentage + "%")
    part = mod.PartDocument(item)
    if is_type(part) != 'part':
        continue
    for prop in custom_properties_list: #заполняем деталь пустыми свойствами
        if get_prop(part, "Inventor User Defined Properties", prop) == False:
            add_prop(part, "Inventor User Defined Properties", prop)
    case = analize(part)
    if case == 'pipe':
        #set_pipe(part)
        continue
    if case == 'purchase':
        find_fasteners(part) #ищет метизы заполняет свойства
        continue
    if case == 'plate':
        #find_plates(part)
        continue
    
    