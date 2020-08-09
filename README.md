# Tarea 02: DCCafé <img src="cliente/sprites/Logo_1.png" height="10%" width="10%">

## Consideraciones generales :warning:
* El programa comienza como corresponde, con la opción de continuar partida, que se inicia en la pre-ronda, y la opción de una nueva partida, que comienza la ronda automáticamente. La barra de reputación en el menú superior solo se actualiza al comenzar la ronda, los otros cambios, como los son el dinero y los clientes, se van actualizando a medida que avanza la ronda.

* Se consideró el punto inicial del mapa a la esquina superior izquierda, donde está el arbusto. Por lo que el mapa se compone solo del piso de la imagen. Se considera los pies del mesero como punto de choque, por lo que puede pasar por una coordenada Y mas abajo de la mesa y el mesero va a superponerse a la imagen de la mesa sin producir el choque especial. El choque especial en caso de los chefs puede ser doble, por lo que se pueden poner a cocinar dos chef al mismo tiempo. Además con el bocadillo en mano el mesero puede ordenar más platos, con la única condición que los chefs tienen 2 segundos de espera despues de ser retirados los platos, para que puedan descansar. Ante una falla en el proceso de cocina, el chef cambiará su estado al sprite de que se muestra leyendo una carta, asi se puede diferenciar los que se equivocaron a los que estan disponibles, pero su reinicio para que vuelva a cocinar es el mismo al de los que estan disponibles.

* En cuanto a las compras pre-ronda, no se pueden superponer mesas con chefs, ni tampoco en el mesero, por lo que el lugar del mesero es invalido. 

* Finalmente, los clientes aparecen sentados, al segundo piden su orden, después regresan a su estado de espera, cuando pasa la mitad del tiempo se enojan. Si reciben su pedido aparecerá un bocadillo aleatorio, y si han esperado mucho no cambiarán su estado de enojado, pero en principio si lo harán y se demorarán 2 segundos en comer su bocadillo para luego irse. Es importante decir, que no hay un orden de mesas en las que se sientan, sino que se elige una mesa disponble al azar, y se dispone de un tiempo, aleatorio también, para que se sienten, esto fue hecho para darle mas animación al programa y no sea tan repititivo.

* Los front-end son todos los modulos que contienen window en su nombre. Por lo que hay una para el inicio, una para el juego y una para el resumen. Es importante recalcar que, en ```game_window.py``` los labels estan guardados en diccionarios para cada tipo como: ```self.mesas```, ```self.chefs``` y ```self.bocadillos``` para el mesero solo se utiliza la variable ```self.mesero```. Los ```QRect``` fueron hechos para definir los choques especiales, solo se hacen con mesas y chefs en ronda, pero en pre-ronda se agrega una del mesero, y se guardan en el diccionario de diccionarios: ```self.box```.

* El back-end se compone principalmente de ```lógica.py```, ```micafe.py``` y ```characters.py``` y se conectan en ```main.py```, mediante señales, con el front-end.

* Las señales para Chefs, Clientes, Bocadillos, son creadas desde la clase ```Cafe``` y se las entregan en algún punto, ya sea en su creación, u otro momento.

* En la prueba del programa no se encontraron caídas de este mismo. 

### Cosas implementadas y no implementadas :heavy_check_mark: :x:

* **Ventana de incio**:
    * **Visualización**: Hecho completo.
    * **Cargar partida**: Hecho completo.
    * **Reiniciar partida**: Hecho completo.
* **Ventana de juego**:
    * **Visualización, mapa, información de la partida**: Hecho completo.
    * **Pre-ronda**: Hecho completo
    * **Ronda**: Hecho completo.
    * **Post-ronda**: Hecho completo.
* **Entidades**:
    * **Jugador**: Hecho completo.
    * **Chef**: Hecho completo.
    * **Bocadillos**: Hecho completo.
    * **Clientes**: Hecho completo.
    * **DCCafé**: Hecho completo. 
* **Tiempo**:
    * **Reloj**: Hecho completo.
    * **Pausa**: Hecho completo.
* **Funcionalidades Extra**:
    * **M+O+N**: Hecho completo.
    * **F+I+N**: Hecho completo.
    * **R+T+G**: Hecho completo.
* **Generañ**:
    * **Modularización**: Hecho completo.
    * **Modelación**: Hecho completo.
    * **Archivos**: Hecho completo.
    * **parametros.py**: Hecho completo.
* **Bonus**:
    * **SuperMagizoólogo**: No hecho.
    * **Multijugador**: No hecho.
    * **Configuración de parámetros**: No hecho.
    * **Ratones en el café**: No hecho. 
   
   


## Ejecución :rewind: :arrow_forward: :fast_forward:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se deben tener los siguentes archivos:
1. Carpeta ```Sprites```, tal cual fue enviada, en ```directorio```.
2. ```datos.csv``` en ```directorio```.
3. ```mapa.csv``` en ```directorio```.
4. ```dccafe_map.ui``` en ```directorio```.
5. ```post_round.ui``` en ```directorio```.


## Librerías :books:
### Librerías externas utilizadas :closed_book:
Pese a que hay más modulos importados, ya que fueron probados en la creación del código, pero no utilizados finalmente. Pese a esto no afectan en la ejecución del programa. La lista de librerías externas que utilicé finalmente fueron las siguientes:

1. ```random```: ```random()```, ```randint()```,  ```choice()```.
2. ```time```: ```sleep()```, ```abstractmethod``` .
3. ```sys``` : ```exit()```, ```__excepthook__```.
4. ```PyQt5``` : ```uic```.
5. ```PyQt5.QtWidgets``` : ```QLabel```, ```QWidget```, ```QPushButton```, ```QHBoxLayout```, ```QVBoxLayout```.
6. ```PyQt5.QtCore``` : ```QThread```, ```QObject```, ```pyqtSignal```, ```Qt```, ```QCoreApplication```, ```QRect```.
7. ```PyQt5.QtGui``` : ```QPixmap```, ```QFont```.
8. ```PyQt5.QtCore``` : ```QThread```, ```QObject```, ```pyqtSignal```.
9. ```math```: ```floor()```.
10. ```collections```: ```defaultdict```.

### Librerías propias :notebook:
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```parametros.py```: Contiene a todos los parámetros utilizados en el código. En todos los módulos se utilizarán de la forma ```p.NOMBRE_PARAMETRO``` menos en ```cargar.py```.

2. ```characters.py```: Contiene a las clases ```Jugador(QObject)```, ```Chef(QThread)```, ```Mesa```, ```Cliente(QThread)```, ```Bocadillo(QThread)```. Es importante mencionar que el tiempo de preparación es calculado por el Chef, ```nivel_chef``` es un metodo que se llama en el setter ```platos_prep```, la calidad del bocadillo es un metodo de ```Bocadillo``` llamado ```prob_propina```. Y que todos los threads cuentan los segundos de la misma forma. 

3. ```micafe.py```: Contiene a la clase ```Cafe(QThread)```, que a su vez contiene a todas las otras instancias en diccionarios. Es el back-end principal del programa por lo que aca se guardan casi todos los cambios del front-end, como lo son el dinero, crear clientes, chefs, mesas, borrar objetos, procesar choques, trampas, empezar la ronda, etc. Además aca se calcula el número de clientes para la ronda en cuestión en su metodo ```calular_clientes``` y la reputación en ```calcular_reputacion```.

4. ```cargar.py```: Se definen las funciones para cargar los archivos ```mapa.csv``` y ```datos.csv```. Además se define una función para mantenerlos actualizados.

5. ```logica.py```: Contiene a la clase Logica, la cual tiene como principal función es cargar el mapa según la partida que se le indique, y guardar los datos utilizando la función definida en ```cargar.py```.

6. ```start_window.py```: Contiene a la clase ```StartWindow(QWidget)``` y es el primer front-end. Es la primera ventana que aparece cuando se ejecuta el codigo. Da las opciones de continuar la partida guardada o crear una nueva, si es está última se sobreescriben los datos en los archivos automáticamente. Fue creada solo mediante código.

7. ```game_window.py```: Contiene a la clase ```GameWindow``` y es la ventana principal del juego (front-end). Fue creada con Qt Designer, pero las señales fueron creadas fuera de esta aplicación. Se cierra automáticamente al final de la ronda si es que pierde por reputación. Se utilizan en algunas ocaciones variables, para representar la instancia de ese objeto en el back-end. Nunca se cambian estas instancias en el fron-end, solo se utilizan por la información que contienen. Se implementa el drag and drop mediante los metodos ```mousePressEvent```, ```mouseMoveEvent``` y ```mouseReleaseEvent```.

8. ```round_summary_window.py```: Contiene a la clase SummaryWindow, que es la ventana del resumen de la ronda (front-end), donde se muestra si se pasó la ronda o no. Muestra los clientes perdidos, los atendidos, el dinero de la ronda, el dinero total y la reputación.


## Supuestos y consideraciones adicionales :memo:
Los supuestos que realicé durante la tarea son los siguientes:

1. Las claves son combinaciones de letras escritas en orden.

2. El jugador, en la ventana de resumen de la ronda, tiene que elegir una opción, si la cierra sin haber elegido ninguna, se queda en la vista final de la última ronda.

3. La trampa R+T+G otorga 5 puntos de reputación en el momento de ejecutarla, por lo que no asegura tener esos 5 puntos al final de la ronda.

4. El mesero puede hacer pedidos al chef con un bocadillo en mano.

5. Se cuentan los platos preparados por el chef independientmente estos son servidos o no.

6. El tiempo del bocadillo que inicia cuando lo terminan de cocinar y termina cuando lo entregan a un cliente se mide en decimas de segundo.

7. El mapa se creo en un tamaño fijo, por lo que todo está en relación a ese tamaño.
-------




## Referencias de código externo :link:

Para la realización de la tarea no hubo utilización de códigos externos.
