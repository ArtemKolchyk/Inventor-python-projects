#поиск труб
import win32com.client
from win32com.client import gencache, Dispatch, constants, DispatchEx
from get_add_set_prop import get_prop, add_prop
from document_type import is_type
from part_faces_edges_points import pipe_THK, pipe_points

Application = win32com.client.Dispatch('Inventor.Application')
Application.Visible = True
mod = gencache.EnsureModule('{D98A091D-3A0F-4C3E-B36E-61F62068D488}', 0, 1, 0)
Application = mod.Application(Application)
Application.SilentOperation = True
#получаем активный документ
oPart = Application.ActiveDocument
#подключаемся к детали
oPart = mod.PartDocument(oPart)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def calculate_length():
    
    
    if is_type(oPart) == 'part':
        pipe_THK(oPart)
        print("-------------------------------------------------------")
        pipe_points(oPart)
    else: 
            print("not part, swith to part tab")
    
calculate_length()
