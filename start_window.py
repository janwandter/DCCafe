import sys

from PyQt5.QtWidgets import QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication
import parametros as p


class StartWindow(QWidget):
    
    senal_nueva_partida = pyqtSignal(bool)
    senal_pedir_instancia = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.init_gui()


    def init_gui(self):

        self.setWindowTitle("Menú DCCafé")
        self.setStyleSheet("background-color: rgba(200,200,200,1)")
        
        self.logo = QLabel(self)
        pixeles_logo = QPixmap(p.PATH_LOGO)
        self.logo.setPixmap(pixeles_logo)
        self.logo.setScaledContents(True)
        self.logo.setFixedSize(p.START_X_SIZE, p.START_Y_SIZE)

        self.bienvenida = QLabel('¡Bienvenido al mejor café virtual!', self)
        self.bienvenida.setAlignment(Qt.AlignCenter)
        self.bienvenida.setFont(QFont("SansSerif", 15, weight=QFont.Bold))
        self.bienvenida.setFixedWidth(p.WELCOME_WIDTH)

        self.cargar_partida = QPushButton('Continuar partida', self)
        self.reiniciar = QPushButton('Nueva partida')
        self.cargar_partida.setFixedSize(p.START_BTTNS_X_SIZE, p.START_BTTNS_Y_SIZE)
        self.reiniciar.setFixedSize(p.START_BTTNS_X_SIZE, p.START_BTTNS_Y_SIZE)
        self.cargar_partida.setFont(QFont("SansSerif", 12))
        self.reiniciar.setFont(QFont("SansSerif", 12,))
        self.cargar_partida.setStyleSheet("background-color: rgba(37, 208, 46, 1);\
             color: rgba(255, 255, 255, 1);")
        self.reiniciar.setStyleSheet("background-color: rgba(252,4,4,1);\
             color: rgba(255, 255, 255, 1);")

        hbox = QHBoxLayout()
        hbox.addWidget(self.cargar_partida)
        hbox.addStretch(1)
        hbox.addWidget(self.reiniciar)
    

        vbox = QVBoxLayout()
        
        vbox.addStretch(2)
        vbox.addWidget(self.logo)
        vbox.addStretch(2)
        vbox.addWidget(self.bienvenida)
        vbox.addStretch(2)
        vbox.addLayout(hbox)
        vbox.addStretch(2)

        hbox_main = QHBoxLayout()
        
        hbox_main.addStretch(1)
        hbox_main.addLayout(vbox)
        hbox_main.addStretch(1)

        self.setLayout(hbox_main)
        self.resize(p.FULL_LAYOUT_X, p.FULL_LAYOUT_Y)
        
        self.cargar_partida.clicked.connect(self.boton_elegido)
        self.reiniciar.clicked.connect(self.boton_elegido)

    def boton_elegido(self):
        self.senal_pedir_instancia.emit()
        sender = self.sender()
        if 'Nueva' in sender.text():
            self.senal_nueva_partida.emit(True)
        else:
            self.senal_nueva_partida.emit(False)
        self.hide()