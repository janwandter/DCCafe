import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from logica import Logica
from characters import Jugador, Mesa, Chef
from micafe import Cafe
from start_window import StartWindow
from game_window import GameWindow
from round_summary_window import SummaryWindow
from cargar import cargar_mapa, cargar_datos
import parametros as p


if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    game = QApplication([])

    #instancias
    start_window = StartWindow()
    logica_dccafe = Logica()
    game_window = GameWindow()
    cafe = Cafe()
    user = cafe.mesero
    summary = SummaryWindow()

    #conectar señales iniciales
    start_window.senal_pedir_instancia.connect(cafe.mandar_instancia)
    cafe.senal_mandar_instancia.connect(logica_dccafe.instanciar_cafe)
    start_window.senal_nueva_partida.connect(logica_dccafe.tipo_partida)
    logica_dccafe.senal_comenzar_juego.connect(game_window.cargar_posiciones)

    #señales pre-round
    game_window.senal_sell.connect(cafe.comprar)
    cafe.senal_chef_creado.connect(game_window.crear_chef_label)
    cafe.senal_mesa_creada.connect(game_window.crear_mesa_label)
    cafe.senal_autorizar_compra.connect(game_window.compra_autorizada)
    cafe.senal_actualizar_dinero.connect(game_window.dinero_actualizado)
    game_window.senal_delete.connect(cafe.delete)
    
    #Comienzo Ronda
    game_window.senal_start_round.connect(cafe.starting_round)
    cafe.senal_cliente_mesa.connect(game_window.sentar_cliente)

    #Moviemiento Usuario
    game_window.senal_enviar_movimiento.connect(user.move)
    user.senal_actualizar_posicion.connect(game_window.actualizar_posicion)
    user.senal_choque_especial.connect(cafe.choque_especial)
    
    #Ronda
    cafe.senal_actualizar_frame.connect(game_window.frame_cliente)
    cafe.senal_client_exit.connect(cafe.actualizar_menu_clientes)
    cafe.senal_n_clientes.connect(game_window.actualizar_clients_menu)
    cafe.senal_bocadillo.connect(game_window.crear_bocadillo_label)
    cafe.senal_frame_chef.connect(game_window.frame_chef)
    
    cafe.senal_propina.connect(cafe.propina)

    game_window.senal_pausa.connect(cafe.pausa)

    game_window.senal_trampa.connect(cafe.trampa)

    #Pasar de ronda
    cafe.senal_round_succeded.connect(summary.ronda_completada)
    summary.senal_esconder_gwindow.connect(game_window.cerrar_window)
    summary.senal_continuar.connect(cafe.next_round)
    summary.senal_save.connect(logica_dccafe.save_data)
    cafe.senal_nxt_round.connect(game_window.cargar_menu)
#------------------------------------------------------
    start_window.show()
    sys.exit(game.exec())    
