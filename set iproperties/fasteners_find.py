from get_add_set_prop import set_prop, get_prop
#Здесь находятся признаки крепежа
custom_properties_list = ['(C) DESCRIPTION', 
                          '(C) DIMENSIONS',
                          '(C) MATERIAL',
                          '(C) REMARKS',
                          '(G) DESCRIPTION', 
                          '(G) DIMENSIONS',
                          '(G) MATERIAL',
                          '(G) REMARKS',
                          'iprop_item_type']

hex_bolt_dict = {'(C) DESCRIPTION': "HEX. BOLT", 
                 '(C) MATERIAL': "8.8 / ISO 898-1",
                 '(C) REMARKS': "ISO 4017",
                 '(G) DESCRIPTION': "HEX. BOLT", 
                 '(G) MATERIAL': "8.8 / ISO 898-1",
                 '(G) REMARKS': "ISO 4017",
                 'iprop_item_type' : "HEX. BOLT",
                 '(C) DIMENSIONS' : "",
                 '(G) DIMENSIONS' : ""
                }
hex_nut_dict = { '(C) DESCRIPTION': "HEX. NUT", 
                 '(C) MATERIAL': "8 / ISO 898-2",
                 '(C) REMARKS': "ISO 4032",
                 '(G) DESCRIPTION': "HEX. NUT", 
                 '(G) MATERIAL': "8 / ISO 898-2",
                 '(G) REMARKS': "ISO 4032",
                 'iprop_item_type' : "HEX. NUT",
                 '(C) DIMENSIONS' : "",
                 '(G) DIMENSIONS' : ""
                 }
plain_washer_dict = {'(C) DESCRIPTION': "PLAIN WASHER", 
                     '(C) MATERIAL': "STEEL 200 HV",
                     '(C) REMARKS': "ISO 7089",
                     '(G) DESCRIPTION': "PLAIN WASHER", 
                     '(G) MATERIAL': "STEEL 200 HV",
                     '(G) REMARKS': "ISO 7089",
                     'iprop_item_type' : "PLAIN WASHER",
                     '(C) DIMENSIONS' : "",
                     '(G) DIMENSIONS' : ""
                    }
spring_washer_dict = {'(C) DESCRIPTION': "SPRING WASHER", 
                      '(C) MATERIAL': "CARBON STEEL",
                      '(C) REMARKS': "DIN 127",
                      '(G) DESCRIPTION': "SPRING WASHER", 
                      '(G) MATERIAL': "CARBON STEEL",
                      '(G) REMARKS': "DIN 127",
                      'iprop_item_type' : "SPRING WASHER",
                      '(C) DIMENSIONS' : "",
                      '(G) DIMENSIONS' : ""
                    }
#по каким ключевым словам ищем
item = ("BOLT",
        "NUT",
        "PLAIN",
        "SPRING",
        #ниже пока не ищем
        "PLATE",
        "PIPE")

dictionary = (hex_bolt_dict, hex_nut_dict, plain_washer_dict, spring_washer_dict)

def find_fasteners(part):
    #получаем строку description и ищем в ней совпадения
    dimensions(part)
    descr_string = get_prop(part, "Design Tracking Properties", "Description").lower()
    #проходим по всем подстановкам из item
    for i in item:
        #проверяем совпадение в строке descr_string текущий item
        if descr_string.find(i.lower()) != -1:
            #смотрим в каждом словаре совпадение значения ключ-значение
            for x in dictionary:
                if x["iprop_item_type"].find(i) != -1:
                    #нашли в словаре что за item
                    #проходим по списку всех свойств из custom_properties_list и ищем соответствия
                    for custom_prop in custom_properties_list:
                        #нашли соответсвие и пихаем его в деталь
                        #print(custom_prop + " " + x[custom_prop])
                        set_prop(part, "Inventor User Defined Properties", custom_prop, x[custom_prop])

def dimensions(part):    
    #получаем REMARKS и пхаем в каждый словарь
    for x in dictionary:
        # получаем title
        title_string = get_prop(part, "Inventor Summary Information", "Title").lower()
        x["(C) REMARKS"] = title_string[:title_string.find("-")].upper()
        x["(G) REMARKS"] = x["(C) REMARKS"]
        title_string = title_string[title_string.find("-")+1:].replace(' ', '')
        new_string = title_string.replace('a', 'm')
        if title_string[0].isdigit():
            new_string = "M"+new_string
        x["(C) DIMENSIONS"] = new_string.upper()
        x["(G) DIMENSIONS"] = new_string.upper()

        
    

    