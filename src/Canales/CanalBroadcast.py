import simpy
from Canales.Canal import Canal

class CanalBroadcast(Canal):
    def __init__(self, env, capacidad=simpy.core.Infinity):
        self.env = env
        self.capacidad = capacidad
        self.canales = []

    def envia(self, mensaje, vecinos):
        '''Envía mensaje a vecinos'''
        for vecino in vecinos:
            if vecino < len(self.canales):
                self.canales[vecino].put(mensaje)

    def crea_canal_de_entrada(self):
        '''Creamos un canal de entrada'''
        canal_entrada = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada
