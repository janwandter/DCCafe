from random import random, randint, choice
import parametros as p
from time import sleep, time
from math import floor
from collections import defaultdict
from characters import Jugador, Cliente, Chef, Mesa
from PyQt5.QtCore import QThread, pyqtSignal

class Cafe(QThread):
    
    senal_cliente_mesa = pyqtSignal(int, str)
    senal_mandar_instancia = pyqtSignal(object)
    senal_chef_creado = pyqtSignal(str)
    senal_mesa_creada = pyqtSignal(str)
    senal_atendido = pyqtSignal(bool, int)
    senal_actualizar_frame = pyqtSignal(int, str, tuple)
    senal_atendido = pyqtSignal(bool, int, int)
    senal_client_exit = pyqtSignal(bool, int)
    senal_n_clientes = pyqtSignal(dict)
    senal_delete_client = pyqtSignal(int)
    senal_round_succeded = pyqtSignal(dict)
    senal_actualizar_dinero = pyqtSignal(int)
    senal_autorizar_compra = pyqtSignal(bool, int, int)
    senal_retirar_plato = pyqtSignal()
    senal_frame_chef = pyqtSignal(str, str)
    senal_bocadillo = pyqtSignal(str)
    senal_propina = pyqtSignal()
    senal_nxt_round = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__dinero = 0
        self.reputacion = 0
        self.rondas_terminadas = 0
        self.ronda_actual = 0
        self.succes_order_round = 0
        self.lost = 0
        self.total_orders_round = 0
        self.open = False #pre-round, post-round False **** round True
        self.pause = False
        self.round_money = 0
        self.mesero = Jugador()
        self.chefs = dict()
        self.clientes = dict()
        self.mesas = dict()
        self.bocadillo = dict()
        self.can_pay = True
        self.mesa_cliente = defaultdict(lambda: None)
        self.end = False

    @property
    def dinero(self):
        return self.__dinero

    @dinero.setter
    def dinero(self, cambio_dinero):
        self.copia_dinero = self.__dinero
        if cambio_dinero < 0:
            self.can_pay = False
        else:
            self.__dinero = cambio_dinero 
            self.can_pay = True

    def calcular_reputacion(self):
        relacion_order = 4 * self.succes_order_round / self.total_orders_round
        formula_min = min(5, (self.reputacion + floor(relacion_order - 2)))
        self.reputacion = max(0, formula_min)
    
    def calcular_ronda(self):
        self.ronda_actual = self.rondas_terminadas + 1

    def calcular_clientes(self):
        self.total_orders_round = 5 * (1 + self.ronda_actual) 
        self.left = self.total_orders_round - self.succes_order_round - self.lost

    def starting_round(self):
        self.open = True
        self.start()

    def next_round(self):
        self.open = False
        self.calcular_ronda()
        self.lost = 0
        self.succes_order_round = 0
        self.calcular_clientes()
        self.senal_nxt_round.emit()
        self.end = False

    def run(self):
        win = True
        finish = False
        n_cliente = 0
        while n_cliente < self.total_orders_round:
            while self.pause:
                pass
            mesa = choice(list(self.mesas.keys()))
            if self.mesas[mesa].disponible:
                self.crear_cliente(n_cliente, mesa)
                self.mesas[mesa].disponible = False
                n_cliente += 1
            if self.end:
                break
        n_mesa_cerradas = 0
        while n_mesa_cerradas < len(self.mesas):
            if self.end:
                break
            while self.pause:
                pass
            for table in self.mesas:
                if not self.mesas[table].disponible:
                    n_mesa_cerradas = 0
                else:
                    n_mesa_cerradas += 1
        self.calcular_reputacion()
        if self.reputacion == 0:
            win = False
        data = {
            "win": win,
            "ronda": self.ronda_actual,
            "lost": self.lost,
            "atendidos": self.succes_order_round,
            "r_money": self.round_money,
            "money": self.dinero,
            "rep": self.reputacion
        }
        for chef in self.chefs:
            self.chefs[chef].plato_retirado()
        self.senal_round_succeded.emit(data)
        self.rondas_terminadas += 1

    def crear_mesa(self, x, y):
        for last in self.mesas:
            pass
        nueva = str(int(last) + 1)
        self.mesas[nueva] = Mesa(x, y)
        self.senal_mesa_creada.emit(nueva)

    def crear_chef(self, x, y):
        for last in self.chefs:
            pass
        nueva = str(int(last) + 1)
        self.chefs[nueva] = Chef(x, y, 0)
        self.senal_chef_creado.emit(nueva)   

    def crear_cliente(self, num, mesa):
        tipo = 'apurado'
        if random() <= p.PROB_RELAJADO:
            tipo = 'relajado'
        espera = randint(p.LLEGADA_CLIENTES_MIN, p.LLEGADA_CLIENTES_MAX)
        sleep(espera)
        if self.end:
            return
        while self.pause:
            pass
        cliente = Cliente(num, tipo, mesa)
        cliente.senal_actualizar_frame = self.senal_actualizar_frame
        self.clientes[num] = cliente
        self.senal_cliente_mesa.emit(num, mesa)
        self.mesa_cliente[mesa] = num
        cliente.senal_atendido = self.senal_atendido
        cliente.senal_client_exit = self.senal_client_exit

    def delete(self, tipo, objeto):
        dict_to_clean = self.mesas
        if tipo == "chefs":
            dict_to_clean = self.chefs
        del dict_to_clean[objeto]

    def mandar_instancia(self):
        self.senal_mandar_instancia.emit(self)

    def comprar(self, tipo, x, y):
        self.dinero -= p.PRECIOS[tipo]
        if not self.can_pay:
            return
        if tipo == "chefs":
            self.crear_chef(x, y)
        else:
            self.crear_mesa(x, y)
        self.actualizar_dinero()
    
    def propina(self):
        self.dinero += p.PROPINA
        self.round_money += p.PROPINA
        self.actualizar_dinero()
    
    def actualizar_dinero(self):
        self.senal_actualizar_dinero.emit(self.dinero)
    
    def choque_especial(self, data):
        tipo = data[0]
        numero = data[1]
        #chef
        if tipo == 'chefs':
            self.chefs[numero].senal_frame_chef = self.senal_frame_chef
            if self.chefs[numero].plato_listo and not self.mesero.snack:
                self.mesero.snack = True
                self.mesero.bocadillo = self.chefs[numero].bocadillo
                self.chefs[numero].retirado = True
            elif self.chefs[numero].plato_listo == None:
                self.chefs[numero].plato_listo = False
                self.chefs[numero].reputacion = self.reputacion
                self.chefs[numero].num = numero
                self.chefs[numero].start()
                self.chefs[numero].senal_propina = self.senal_propina
            elif not self.chefs[numero].plato_listo:
                return
        else:
            cliente = self.mesa_cliente[numero]
            if self.mesero.snack:
                if cliente != None:
                    if not self.clientes[cliente].atendido:
                        self.clientes[cliente].atendido = True
                        self.mesero.bocadillo.entregado = True
                        self.mesero.snack = False
                        self.dinero += p.PRECIO_BOCADILLO
                        self.round_money += p.PRECIO_BOCADILLO
                        self.actualizar_dinero()
                        self.senal_bocadillo.emit(numero)

    def actualizar_menu_clientes(self, atendido, cliente):
        if atendido:
            self.succes_order_round += 1
        else:
            self.lost += 1
        self.calcular_clientes()
        data = {"delete": cliente,
            'atendidos': self.succes_order_round,
            'lost': self.lost,
            'left': self.left}
        self.senal_n_clientes.emit(data)
        #Desocupar mesa
        self.mesas[self.clientes[cliente].mesa].disponible = True
        self.mesa_cliente[self.clientes[cliente].mesa] = None

    def pausa(self, señal):
        self.pause = señal
        for cliente in self.clientes:
            if not self.clientes[cliente].finish:
                self.clientes[cliente].pause = señal
        for chef in self.chefs:
            self.chefs[chef].pause = señal
        
    def trampa(self, tipo):
        if tipo.lower() == "mon":
            self.dinero += p.DINERO_TRAMPA
            self.actualizar_dinero()
        elif tipo.lower() == "fin" and self.open:
            self.end = True
            for cliente in self.clientes:
                self.clientes[cliente].end = True
                self.clientes[cliente].delete_me()
            for mesa in self.mesas:
                self.mesas[mesa].disponible = False
        else:
            self.reputacion += p.REPUTACION_TRAMPA


