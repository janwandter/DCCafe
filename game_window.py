import os
import sys
import parametros as p
from random import random, randint
from collections import defaultdict

from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication

window_name, base_class = uic.loadUiType("dccafe_map.ui")

class GameWindow(window_name, base_class):

    senal_enviar_movimiento = pyqtSignal(str, dict)
    senal_pausa = pyqtSignal(bool)
    senal_crear_chef = pyqtSignal(int, int)
    senal_crear_mesa = pyqtSignal(int, int)
    senal_start_round = pyqtSignal()
    senal_cliente_eliminado = pyqtSignal(int)
    senal_sell = pyqtSignal(str, int, int)
    senal_delete = pyqtSignal(str, str)
    senal_atendido = pyqtSignal()
    senal_trampa = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._frame = 1
        self.setupUi(self)
        self.resize(p.WINDOW_SIZE_X, p.WINDOW_SIZE_Y)
        self.pausado = False
        self.ronda = False
        self.drag = False
        self.box = dict()
        self.trampa = ""
        ####################
        self.exit_button.clicked.connect(QCoreApplication.instance().quit)
        self.start_button.clicked.connect(self.start_round)
        self.stop_button.clicked.connect(self.pausa)
        self.mesero = QLabel(self)

    def cargar_posiciones(self, instancia_cafe):
        self.micafe = instancia_cafe
        self.mesas = dict()
        self.chefs = dict()
        self.box["mesero"] = dict()
        self.box["mesero"]["user"] = 0
        self.mesas_box = dict()
        self.chefs_box = dict()
        self.clientes = dict()
        mesas = self.micafe.mesas
        chefs = self.micafe.chefs
        meserox = self.micafe.mesero
        for mesa in mesas:
            self.crear_mesa_label(mesa)
        for chef in chefs:
            self.crear_chef_label(chef)
        self.mesero.setPixmap(QPixmap(p.PATH_MESERO))
        self.mesero.resize(p.MESERO_SIZE_X, p.MESERO_SIZE_Y)
        self.mesero.setScaledContents(True)
        self.mesero.move(meserox.x, meserox.y)
        self.mesero.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.cargar_menu()
        self.show()

    def cargar_menu(self):
        meserox = self.micafe.mesero
        self.ronda_text.setText(f"RONDA N°{self.micafe.ronda_actual}")
        self.reputation_bar.setProperty('value', self.micafe.reputacion * 20)
        self.dinero_actual.setText(f'{self.micafe.dinero}')
        self.n_atendidos.setText(f'{self.micafe.succes_order_round}')
        self.n_left.setText(f'{self.micafe.left}')
        self.n_lost.setText(f'{self.micafe.lost}')
        self.ronda = self.micafe.open
        self.start_button.setEnabled(not self.ronda)
        self.box["mesero"]["user"] = QRect(meserox.x, meserox.y, p.MESERO_SIZE_X, p.MESERO_SIZE_Y)
        if self.ronda:
            del self.box["mesero"]["user"]
    def pausa(self):
        self.pausado = not self.pausado
        self.senal_pausa.emit(self.pausado)
        #Pausar el juego si self.pausa
        #Si not self.pausa seguir juego
        return

    def keyPressEvent(self, evento):
        mesas = self.micafe.mesas
        chefs = self.micafe.chefs
        mesero = self.micafe.mesero
        if evento.text().lower() in "mfr":
            self.trampa = f"{evento.text().lower()}"
        elif evento.text().lower() in "oit" and len(self.trampa) == 1:
            self.trampa += f"{evento.text().lower()}"
        elif evento.text().lower() in "ng" and len(self.trampa) == 2:
            self.trampa += f"{evento.text().lower()}"
            self.senal_trampa.emit(self.trampa)
        else:
            self.trampa = ""
        if not self.ronda:
            return
        if evento.key() == Qt.Key_P:
            self.pausa()
        if self.pausado:
            return
        if evento.key() == Qt.Key_W:
            self.senal_enviar_movimiento.emit("up", self.box)
        elif evento.key() == Qt.Key_A:
            self.senal_enviar_movimiento.emit("left", self.box)
        elif evento.key() == Qt.Key_S:           
            self.senal_enviar_movimiento.emit("down", self.box)
        elif evento.key() == Qt.Key_D:
            self.senal_enviar_movimiento.emit("right", self.box)
        self.mesero.raise_()
        self.update()
    
    def mousePressEvent(self, evento):
        if not self.ronda:
            mesas = self.micafe.mesas
            copy_box = dict(self.box)
            if evento.button() ==  Qt.LeftButton:
                if p.CHEF_X0_SHOP <= evento.x() <= p.CHEF_X_END_SHOP\
                     and p.CHEF_Y0_SHOP <= evento.y() <= p.CHEF_Y_END_SHOP:
                    self.drag = "chefs"
                elif p.MESA_X0_SHOP <= evento.x() <= p.MESA_X_END_SHOP\
                     and p.MESA_Y0_SHOP <= evento.y() <= p.MESA_Y_END_SHOP:
                    self.drag = "mesas"
                filtro_box = (x for x in copy_box if x not in "mesero")
                for tipo in filtro_box:
                    for objeto in copy_box[tipo]:
                        if copy_box[tipo][objeto].contains(evento.x(), evento.y()):
                            self.delete(tipo, objeto)
                            break      

    def mouseMoveEvent(self, evento):
        if not self.drag:
            return
        elif self.drag == "chefs":
            self.sell_chef.move(evento.pos())
        else:
            self.sell_mesa.move(evento.pos())

    def mouseReleaseEvent(self, evento):
        if not self.drag:
            return
        x = evento.x()
        y = evento.y()
        ajust_x = p.OBJ_SIZE[self.drag][0]
        ajust_y = p.OBJ_SIZE[self.drag][1]
        self.sell_chef.move(p.CHEF_X0_SHOP, p.CHEF_Y0_SHOP)
        self.sell_mesa.move(p.MESA_X0_SHOP, p.MESA_Y0_SHOP)
        if not p.ORIGEN_X <= x <= p.FIN_X - ajust_x or \
                not p.ORIGEN_Y <= y <= p.FIN_Y - ajust_y:
            self.drag = False
            return
        for tipo in self.box:
            for elemento in self.box[tipo]:
                if self.box[tipo][elemento].\
                    intersects(QRect(x, y, ajust_x, ajust_y)):
                    self.drag = False
                    return
        self.senal_sell.emit(self.drag, x, y)
        self.drag = False
            
    def crear_mesa_label(self, mesa):
        mesax = self.micafe.mesas
        self.mesas[mesa] = QLabel(self)
        self.mesas[mesa].setPixmap(QPixmap(p.PATH_MESA))
        self.mesas[mesa].resize(p.MESA_SIZE_X, p.MESA_SIZE_Y)
        self.mesas[mesa].move(mesax[mesa].x, mesax[mesa].y)
        self.mesas[mesa].setScaledContents(True)
        self.mesas[mesa].setStyleSheet("background-color: rgba(0,0,0,0)")
        self.mesas[mesa].show()
        #creamos un box alrededor de la mesa
        self.mesas_box[mesa] = QRect(mesax[mesa].x, mesax[mesa].y, p.MESA_SIZE_X, p.MESA_SIZE_Y)
        self.box["mesas"] = self.mesas_box
        self.update()

    def crear_chef_label(self, chef):
        chefx = self.micafe.chefs
        self.chefs[chef] = QLabel(self)
        self.chefs[chef].setPixmap(QPixmap(p.PATH_CHEF))
        self.chefs[chef].resize(p.CHEF_SIZE_X, p.CHEF_SIZE_Y)
        self.chefs[chef].move(chefx[chef].x, chefx[chef].y)
        self.chefs[chef].setScaledContents(True)
        self.chefs[chef].setStyleSheet("background-color: rgba(0,0,0,0)")
        self.chefs[chef].show()
        #creamos un box alrededor del chef
        self.chefs_box[chef] = QRect(chefx[chef].x, chefx[chef].y,p.CHEF_SIZE_X, p.CHEF_SIZE_Y)
        self.box["chefs"] = self.chefs_box

    def crear_bocadillo_label(self, mesa):
        self.bocadillos = defaultdict()
        mesax = self.micafe.mesas
        tipo = str(randint(p.FIRST_SNACK_FRAME, p.LAST_SNACK_FRAME))
        if int(tipo) < 10:
            tipo = f"0{tipo}"
        self.bocadillos[mesa] = QLabel(self)
        self.bocadillos[mesa].setPixmap(QPixmap(
            f"sprites/bocadillos/bocadillo_{tipo}.png"))
        self.bocadillos[mesa].resize(p.SNACK_SIZE, p.SNACK_SIZE)
        ajust_x = p.MESA_SIZE_X / p.SNACK_MESA_X
        ajust_y = p.MESA_SIZE_Y / p.SNACK_MESA_Y
        self.bocadillos[mesa].move(mesax[mesa].x + ajust_x, mesax[mesa].y + ajust_y)
        self.bocadillos[mesa].setScaledContents(True)
        self.bocadillos[mesa].setStyleSheet("background-color: rgba(0,0,0,0)")
        self.bocadillos[mesa].show()
        self.bocadillos[mesa].raise_()
    
    def actualizar_posicion(self, data_move):
        if data_move.get("sprite"):
            if data_move["snack"]:
                pixmap = QPixmap(
                    f"sprites/{data_move['sprite']}/{data_move['direction']}_"
                    f"snack_0{data_move['frame']}.png")
            else:
                pixmap = QPixmap(
                    f"sprites/{data_move['sprite']}/{data_move['direction']}"
                    f"_0{data_move['frame']}.png")
            pixmap = pixmap.scaled(p.USER_SCALE_X, p.USER_SCALE_Y) ### era 32,32
            self.mesero.setPixmap(pixmap)
        self.mesero.move(data_move['x'], data_move['y'])
        self.update()

    def delete(self, tipo, objeto):
        obj_type = self.chefs
        if tipo == 'mesas':
            obj_type = self.mesas
        if len(obj_type) > 1:
            obj_type[objeto].setPixmap(QPixmap(None))
            del obj_type[objeto]
            del self.box[tipo][objeto]
            self.senal_delete.emit(tipo, objeto)

    def start_round(self):
        if not self.micafe.open:
            self.senal_start_round.emit()
            self.ronda = True
            del self.box["mesero"]["user"]
            self.start_button.setEnabled(False)

    def sentar_cliente(self, cliente, mesa):
        mesax = self.micafe.mesas
        clientex = self.micafe.clientes
        ajuste_x = p.HASMTER_AJUSTE
        if random() <= p.PROB_DOG:
            clientex[cliente].animal = 'perro'
            ajuste_x = p.DOG_AJUSTE
        animal = clientex[cliente].animal
        x = p.CLIENT_SIZE[animal][0]
        y = p.CLIENT_SIZE[animal][1]
        self.clientes[cliente] = QLabel(self)
        self.clientes[cliente].setPixmap(QPixmap(
            f"sprites/clientes/{animal}/{animal}"
                    f"_{clientex[cliente].frame}.png"))
        self.clientes[cliente].resize(x, y)
        self.clientes[cliente].move(mesax[mesa].x - ajuste_x * x, mesax[mesa].y - y * 0.4)
        self.clientes[cliente].setScaledContents(True)
        self.clientes[cliente].setStyleSheet("background-color: rgba(0,0,0,0)")
        self.clientes[cliente].show()
    
    def frame_cliente(self, num, frame, size):
        clientex = self.micafe.clientes
        x = p.CLIENT_SIZE[clientex[num].animal][0]
        y = p.CLIENT_SIZE[clientex[num].animal][1]
        self.clientes[num].setPixmap(QPixmap(
            f"sprites/clientes/{clientex[num].animal}/{clientex[num].animal}"
                    f"_{clientex[num].frame}.png"))
        self.clientes[num].resize(size[0] * x, size[0] * y)
        self.clientes[num].move\
            (self.clientes[num].x() + size[1] , self.clientes[num].y() + size[2])
    
    def frame_chef(self, num, frame):
        self.chefs[num].setPixmap(QPixmap(
            f"sprites/chef/meson_{frame}.png"))

    def delete_client(self, num):
        clientex = self.micafe.clientes
        self.clientes[num].setPixmap(QPixmap(None))
        if clientex[num].atendido:
            self.bocadillos[clientex[num].mesa].setPixmap(QPixmap(None))

    def compra_autorizada(self, answer, x, y):
        if not answer:
            self.drag = False
            return    

    def dinero_actualizado(self, dinero):
        self.dinero_actual.setText(f'{dinero}')
    
    def actualizar_clients_menu(self, data):
        clientex = self.micafe.clientes
        num = data["delete"]
        self.clientes[num].setPixmap(QPixmap(None))
        if clientex[num].atendido:
            self.bocadillos[clientex[num].mesa].setPixmap(QPixmap(None))
        self.n_atendidos.setText(str(data['atendidos']))
        self.n_lost.setText(str(data['lost']))
        self.n_left.setText(str(data['left']))
    
    def cerrar_window(self):
        self.hide()
      

if __name__ == '__main__':
    app = QApplication([])
    form = GameWindow()
    form.show()
    sys.exit(app.exec_())

