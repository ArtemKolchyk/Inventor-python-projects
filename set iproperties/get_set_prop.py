#ищем свойство 

def get(part, tab, property):
    try:
        return part.PropertySets.Item(tab)(property).Value
    except:
        return False
    
