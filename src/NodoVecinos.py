import simpy
from Nodo import *
from Canales.CanalBroadcast import *

TICK = 1

class NodoVecinos(Nodo):
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.identifiers = set([id_nodo])

    def conoceVecinos(self, env):
        '''Algoritmo para conocer vecinos de vecinos'''
        # Esperamos un tick
        yield env.timeout(TICK)
        
        self.canal_salida.envia(self.vecinos, self.vecinos)
        
        # Recibimos mensajes de TODOS los vecinos
        for _ in range(len(self.vecinos)):
            mensaje = yield self.canal_entrada.get()
            self.identifiers.update(mensaje)