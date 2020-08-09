from random import random, randint
import parametros as p
from time import sleep, time
from PyQt5.QtCore import QThread, QObject, pyqtSignal

class Jugador(QObject):

    senal_actualizar_posicion = pyqtSignal(dict)
    senal_choque_especial = pyqtSignal(tuple)
    
    def __init__(self):
        super().__init__()
        self.__x = 0
        self.__y = 0
        self.speed = p.VEL_MOVIMIENTO
        self.__frame = p.FRAME_INICIAL
        self.direction = "down"
        self.snack = False
        self.bocadillo = None
        self.box = dict()

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        if 3 < value:
            self.__frame = 1
        else:
            self.__frame = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.choque = False
        signo_mov = 0
        if self.direction in 'right':
            signo_mov = 1
        if p.ORIGEN_X < value < p.FIN_X - p.MESERO_SIZE_X:
            for tipo in self.box:
                for objeto in self.box[tipo]:
                    if self.box[tipo][objeto].contains(value + signo_mov * p.MESERO_SIZE_X,\
                         self.y + p.MESERO_SIZE_Y):
                        data = (tipo, objeto)
                        self.senal_choque_especial.emit(data)
                        self.choque = True
            if not self.choque:
                self.__x = value
        self.senal_actualizar_posicion.emit(
            {"x": self.x,
            "y": self.y,
            "frame": self.frame,
            "sprite": 'mesero',
            "direction": self.direction,
            "snack": self.snack
            })

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.choque = False
        if p.ORIGEN_Y < value < p.FIN_Y - p.MESERO_SIZE_Y:
            for tipo in self.box:
                for objeto in self.box[tipo]:
                    if self.box[tipo][objeto].x() > self.x:
                        if self.box[tipo][objeto].contains(self.x \
                            + p.MESERO_SIZE_X, value\
                            + p.MESERO_SIZE_Y):
                            data = (tipo, objeto)
                            self.senal_choque_especial.emit(data)
                            self.choque = True
                    else:
                        if self.box[tipo][objeto].contains(self.x, value\
                            + p.MESERO_SIZE_Y):
                            self.choque = True
                            data = (tipo, objeto)
                            self.senal_choque_especial.emit(data)
            if not self.choque:
                self.__y = value   
        self.senal_actualizar_posicion.emit(
            {'x': self.x,
                'y': self.y,
                "frame": self.frame,
                "sprite": 'mesero',
                "direction": self.direction,
                "snack": self.snack
                })
         
    def move(self, direction, boxes):
        self.frame += 1
        self.box = boxes
        self.direction = direction
        if direction == 'up':
            self.y -= p.VEL_MOVIMIENTO
        elif direction == 'left':
            self.x -= p.VEL_MOVIMIENTO
        elif direction == 'down':
            self.y += p.VEL_MOVIMIENTO
        elif direction == 'right':
            self.x += p.VEL_MOVIMIENTO


class Chef(QThread):

    def __init__(self, pos_x, pos_y, platos_prep):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.__frame = p.FRAME_INICIAL
        self.__platos_prep = int(platos_prep)
        self.nivel = self.nivel_chef(int(platos_prep))
        self.reputacion = p.REPUTACION_INICIAL
        self.num = None
        self.pause = False
        self.retirado = False
        self.bocadillos = dict()
        self.plato_listo = None #False cocinando, True listo

    @property
    def platos_prep(self):
        return self.__platos_prep
        
    @platos_prep.setter
    def platos_prep(self, platos):
        self.nivel_chef(platos)
        self.__platos_prep = platos

    def nivel_chef(self, platos_prep):
        if platos_prep >= p.PLATOS_EXPERTO:
            self.nivel = 3
            return 3
        elif platos_prep >= p.PLATOS_INTERMEDIO:
            self.nivel = 2
            return 2
        self.nivel = 1
        return 1

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        if 15 < value:
            self.__frame = 2
        else:
            self.__frame = value
    
    def run(self):
        tiempo = self.tiempo_pedido()
        self.senal_frame_chef.emit(f"{self.num}", '02')
        seg_fail = randint(p.SEG_FAIL_MIN, tiempo - 1)
        for segundos in range(tiempo):
            if segundos == seg_fail:
                if self.fail():
                    return
            for i in range(5):
                self.frame += 1
                frame = f"0{self.frame}"
                if self.frame > 9:
                    frame = f"{self.frame}"
                self.senal_frame_chef.emit(f"{self.num}", frame)   
                sleep(0.2)
                if self.plato_listo == None:
                    return
                while self.pause:
                    pass
        self.senal_frame_chef.emit(f"{self.num}", '16')
        self.plato_listo = True
        self.platos_prep += 1
        bocadillo = Bocadillo(self.nivel)
        bocadillo.senal_propina = self.senal_propina
        self.bocadillo = bocadillo 
        while not self.retirado:
            pass
        self.senal_frame_chef.emit(f"{self.num}", '01')
        sleep(p.TIME_ENTRE_PLATOS)
        self.plato_listo = None
        self.retirado = False
        return

    def fail(self):
        p_fail = 0.3 / (self.nivel + 1)
        if random() <= p_fail:
            self.senal_frame_chef.emit(f"{self.num}", '17') 
            self.plato_listo = None
            return True
        return False

    def tiempo_pedido(self):
        t = max(0, 15 - self.reputacion - self.nivel * 2)
        return t

    def fallo_chef(self):
        if random() <= 0.3/(self.nivel + 1):
            return True
        return False
    
    def plato_retirado(self):
        if self.plato_listo != None:
            self.senal_frame_chef.emit(f"{self.num}", '01')
            self.plato_listo = None


class Mesa:

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.disponible = True
    

class Cliente(QThread):

    def __init__(self, num, tipo, mesa):
        super().__init__()
        self.numero = num
        self.tipo = tipo
        self.mesa = mesa
        self.wait_time = self.tiempo_espera()
        self.atendido = False
        self.pause = False
        self.frame = '01'
        self.animal = 'hamster'
        self.finish = False
        self.end = False
        self.start()

    def tiempo_espera(self):
        if self.tipo == 'Relajado':
            return p.TIEMPO_ESPERA_RELAJADO
        return p.TIEMPO_ESPERA_APURADO
    
    def run(self):
        for segundos in range(self.wait_time):
            size = p.HAPPY_SIZE
            if self.end:
                return
            if segundos == 1:
                self.frame = '32'
                size = p.ORDERING_SIZE
            elif segundos == 2:
                self.frame = '01'
                size = p.HAPPY_AFTER_ANGRY_SIZE
            elif segundos == self.wait_time // 2:
                self.frame = '27'
            while self.pause:
                pass #Antes de emitir la señal vemos si está pausado
            if self.atendido:
                self.frame = '01'
                self.senal_actualizar_frame.emit(self.numero, self.frame, size)
                break
            if segundos > 0:
                self.senal_actualizar_frame.emit(self.numero, self.frame, size)
            if self.end:
                return
            sleep(1)
        while self.pause:
            pass #Si pausa en el ultimo ciclo para que no se vaya el cliente pausado
        self.finish = True
        if self.atendido:
            sleep(p.EATING_TIME)
            self.senal_client_exit.emit(True, self.numero)
            return
        self.senal_client_exit.emit(False, self.numero)
        return
    
    def delete_me(self):
        self.senal_client_exit.emit(False, self.numero)

class Bocadillo(QThread):

    def __init__(self, chef_level):
        super().__init__()
        self.chef_level = chef_level
        self.entregado = False
        self.start()

    def run(self):
        milisegundo = 0
        while not self.entregado:
            sleep(0.1)
            milisegundo += 0.1
        self.prob_propina(milisegundo)
        return
    
    def prob_propina(self, tiempo): #Calidad del pedido
        prob = max(0, (self.chef_level * (1 - tiempo * 0.05) / 3))
        if random() <= prob:
            self.senal_propina.emit()        