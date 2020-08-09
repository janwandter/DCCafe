import parametros as p

def cargar_mapa(ruta_mapa):
    mesero_pos = dict()
    mesas_pos = dict()
    chef_pos = dict()
    contador_mesa = 1
    contador_chef = 1
    with open(ruta_mapa, "r", encoding = "utf-8") as archivo:
        for linea in archivo.readlines():
            tipo, pos_x, pos_y  = linea.strip().split(",")
            pos_x = int(pos_x) + p.ORIGEN_X
            pos_y = int(pos_y) + p.ORIGEN_Y
            if tipo == "mesero":
                mesero_pos = (pos_x, pos_y)
            elif tipo == "mesa":
                mesas_pos[str(contador_mesa)] = (pos_x, pos_y)
                contador_mesa += 1
            else:
                chef_pos[str(contador_chef)] = (pos_x, pos_y)
                contador_chef += 1
        return mesero_pos, mesas_pos, chef_pos

def cargar_datos(ruta_datos):
    micafe = dict()
    chef_platos = dict()
    with open(ruta_datos, "r", encoding = "utf-8") as archivo:
        micafe_data = archivo.readline()
        dinero, rep, finish_rounds = micafe_data.strip().split(',')
        for linea in archivo.readlines():
            pass
        chefs_data = linea.strip().split(',')
    for indice, n_platos in enumerate(chefs_data, 1):
        chef_platos[str(indice)] = n_platos
    micafe["dinero"] = int(dinero)
    micafe["reputacion"] = int(rep)
    micafe["finish_rounds"] = int(finish_rounds)
    return micafe, chef_platos

def guardar_datos(mesero, mesas, chefs, dinero,\
         rep, rounds, ruta_mapa, ruta_datos):
    margin_x = p.ORIGEN_X
    margin_y = p.ORIGEN_Y
    with open(ruta_mapa, "w", encoding= "utf-8") as archivo:
        archivo.write(f"mesero,{mesero.x - margin_x},{mesero.y - margin_y}\n")
        for mesa in mesas:
            archivo.write(f"mesa,{mesas[mesa].x - margin_x},"
            f"{mesas[mesa].y - margin_y}\n")
        for chef in chefs:
            archivo.write(f"chef,{chefs[chef].x- margin_x},"
            f"{chefs[chef].y - margin_y}\n")
    with open(ruta_datos, "w", encoding= "utf-8") as archivo:
        archivo.write(f"{dinero},{rep},{rounds}\n")
        chef_str = ""
        for chef in chefs:
            chef_str += f"{chefs[chef].platos_prep},"
        archivo.write(f"{chef_str[:-1]}")
    return
