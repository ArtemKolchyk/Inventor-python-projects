# -*- coding: utf-8 -*-
import win32com.client
from win32com.client import gencache, Dispatch, constants, DispatchEx



Application = win32com.client.Dispatch('Inventor.Application')
Application.Visible = True
mod = gencache.EnsureModule('{D98A091D-3A0F-4C3E-B36E-61F62068D488}', 0, 1, 0)
Application = mod.Application(Application)
Application.SilentOperation = True
#получаем активный документ
oPart = Application.ActiveDocument
#подключаемся к детали
oPart = mod.PartDocument(oPart)

def item_type(oPart):
    print(oPart.ComponentDefinition.BOMStructure)
    
item_type(oPart)