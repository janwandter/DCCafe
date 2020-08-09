from PyQt5.QtCore import QObject, pyqtSignal
from cargar import cargar_mapa, cargar_datos, guardar_datos
from characters import Jugador, Chef, Mesa, Cliente
from micafe import Cafe
import parametros as p
from random import randint

class Logica(QObject):

    senal_comenzar_juego = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.micafe = None
        self.pos_list = []
    
    def instanciar_cafe(self, instancia):
        self.micafe = instancia

    def tipo_partida(self, decision):
        if decision:
            self.nueva_partida()
        else:
            self.continuar_partida()
    
    def rand_pos(self, size_x, size_y):
        sx_copy = size_x
        sy_copy = size_y
        x =  randint(p.ORIGEN_X, p.FIN_X - size_x)
        y = randint(p.ORIGEN_Y, p.FIN_Y - size_y)
        for pos in self.pos_list:
            ajust_x = p.OBJ_SIZE[pos[0]][0]
            ajust_y = p.OBJ_SIZE[pos[0]][1]
            cond_x = (pos[1] - 1.5 * size_x <= x <= pos[1] + 1.5 * ajust_x)
            cond_y = (pos[1] - 1.5 * size_y <= y <= pos[1] + 1.5 * ajust_y)
            if cond_x and cond_y:
                return self.rand_pos(sx_copy, sy_copy)
        return x,y

    def nueva_partida(self):
        mesas = dict()
        chefs = dict()
        money = p.DINERO_INICIAL 
        reputacion = p.REPUTACION_INICIAL
        for chef in range(1, p.CHEFS_INICIALES + 1):
            x, y = self.rand_pos(p.CHEF_SIZE_X, p.CHEF_SIZE_Y)
            chefs[f"{chef}"] = Chef(x, y, 0)
            self.pos_list.append(("chefs", chefs[f"{chef}"].x, chefs[f"{chef}"].y))
        for mesa in range(1, p.MESAS_INICIALES + 1):
            x, y = self.rand_pos(p.MESA_SIZE_X, p.MESA_SIZE_Y)
            mesas[f"{mesa}"] = Mesa(x, y)
        x, y = self.rand_pos(p.MESERO_SIZE_X, p.MESERO_SIZE_Y)
        self.micafe.mesero.x = x
        self.micafe.mesero.y = y
        self.micafe.dinero = money
        self.micafe.reputacion = reputacion
        self.micafe.rondas_terminadas = 0
        self.micafe.calcular_ronda()
        self.micafe.calcular_clientes() 
        self.micafe.chefs = chefs
        self.micafe.mesas = mesas
        self.micafe.starting_round()
        self.senal_comenzar_juego.emit(self.micafe)
        self.save_data()

    def continuar_partida(self):
        mesas = dict()
        chefs = dict()
        clientes = dict()
        mesero_pos, mesa_pos, chef_pos = cargar_mapa(p.PATH_MAPA_CSV)
        cafe_datos, chef_platos = cargar_datos(p.PATH_DATOS_CSV)
        for mesa in mesa_pos:
            pos_x = mesa_pos[mesa][0]
            pos_y = mesa_pos[mesa][1]
            mesas[mesa] = Mesa(pos_x, pos_y)
        for chef in chef_pos:
            pos_x = chef_pos[chef][0]
            pos_y = chef_pos[chef][1]
            platos = chef_platos[chef]
            chefs[chef] = Chef(pos_x, pos_y, platos)
        money = cafe_datos["dinero"]
        reputacion = cafe_datos["reputacion"]
        rounds = cafe_datos["finish_rounds"]
        self.micafe.dinero = money
        self.micafe.reputacion = reputacion
        self.micafe.rondas_terminadas = rounds
        self.micafe.calcular_ronda()
        self.micafe.calcular_clientes() 
        self.micafe.mesero.x = mesero_pos[0]
        self.micafe.mesero.y = mesero_pos[1] 
        self.micafe.chefs = chefs
        self.micafe.mesas = mesas
        self.senal_comenzar_juego.emit(self.micafe)

    def save_data(self):
        c = self.micafe
        guardar_datos(c.mesero, c.mesas, c.chefs, c.dinero,\
             c.reputacion, c.rondas_terminadas, p.PATH_MAPA_CSV,\
                 p.PATH_DATOS_CSV)
    
        

    
    

        
