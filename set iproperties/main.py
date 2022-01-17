import win32com.client
from win32com.client import gencache, Dispatch, constants, DispatchEx
from get_set_prop import get

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
for part in oRefDocs:
    #descr_prop = part.PropertySets.Item("Design Tracking Properties")('Designer').Value
    print(get(part, "Design Tracking Properties", "bbbb"))
    #print(descr_prop)