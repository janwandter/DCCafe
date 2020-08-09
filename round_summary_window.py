import sys
import parametros as p

from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QApplication

window_name, base_class = uic.loadUiType("post_round.ui")

class SummaryWindow(window_name, base_class):
    
    senal_continuar = pyqtSignal()
    senal_save = pyqtSignal()
    senal_esconder_gwindow = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.b_exit.clicked.connect(QCoreApplication.instance().quit)
        self.b_continuar.clicked.connect(self.decision)
        self.b_save.clicked.connect(self.decision)
        
    def ronda_completada(self, data):
        if data['win']:
            self.n_round.setText(f"RESUMEN RONDA N°{data['ronda']}")
        else:
            self.n_round.setText(f"HAS PERDIDO EN RONDA N°{data['ronda']}")
            self.b_continuar.setEnabled(False)
            self.b_save.setEnabled(False)
            self.senal_esconder_gwindow.emit()
        self.clients_lost.setText(f"{data['lost']}")
        self.clients_atend.setText(f"{data['atendidos']}")
        self.round_money.setText(f"{data['r_money']}")
        self.total_money.setText(f"{data['money']}")
        self.reputation.setText(f"{data['rep']}/5")

        self.show()

    def decision(self):
        sender = self.sender()
        if 'Guardar' in sender.text():
            self.senal_save.emit()
        else:
            self.senal_continuar.emit()
            self.hide()

if __name__ == '__main__':
    app = QApplication([])
    form = SummaryWindow()
    form.show()
    sys.exit(app.exec_())