import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

# La unidad de tiempo
TICK = 1


class NodoBroadcast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje

# Si el el nodo envia el mensaje a todos sus hijos en el árbol, en otro caso espera el mensaje, lo almacena y reenvia a sus vecinos excepto al que lo envió.
    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.
            El nodo raíz inicia el broadcast enviando el mensaje a todos sus vecinos
            Los nodos reciben el mensaje y lo reenvían a sus vecinos
            
            Args:
                env: Entorno de simulación Simpy
        '''
        # Tú código aquí
        if self.id_nodo == 0:
            yield env.timeout(TICK)
            self.canal_salida.envia(self.mensaje, self.vecinos)
        else:
            while True:
                mensaje = yield self.canal_entrada.get()
                self.mensaje = mensaje
                yield env.timeout(TICK)
                self.canal_salida.envia(self.mensaje, self.vecinos)
                break