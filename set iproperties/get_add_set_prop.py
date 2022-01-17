#ищем свойство 

def get_prop(part, tab, prop):
    try:
        return part.PropertySets.Item(tab)(prop).Value
    except:
        return False

def add_prop(part, tab, prop):
    part.PropertySets.Item(tab).Add('',prop)  
