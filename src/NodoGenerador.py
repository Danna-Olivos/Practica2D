import simpy
from Nodo import *
from Canales.CanalBroadcast import *

TICK = 1

class NodoGenerador(Nodo):
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.padre = None
        self.hijos = []
        self.expected_msg = 0
        self.es_raiz = (id_nodo == 0)
        self.procesado = False

    def genera_arbol(self, env):
        # Nodo raíz inicia el proceso
        if self.es_raiz and not self.procesado:
            self.procesado = True
            self.padre = self.id_nodo
            self.expected_msg = len(self.vecinos)
            yield env.timeout(TICK)
            self.canal_salida.envia(('GO', self.id_nodo), self.vecinos)

        while True:
            mensaje = yield self.canal_entrada.get()
            
            if mensaje[0] == 'GO':
                emisor = mensaje[1]
                
                if self.padre is None and not self.procesado:
                    self.procesado = True
                    self.padre = emisor
                    self.expected_msg = len(self.vecinos) - 1  # Excluimos al padre
                    
                    if self.expected_msg > 0:
                        # Enviar GO a otros vecinos
                        otros_vecinos = [v for v in self.vecinos if v != self.padre]
                        yield env.timeout(TICK)
                        self.canal_salida.envia(('GO', self.id_nodo), otros_vecinos)
                    else:
                        # No hay mas vecinos, enviar BACK al padre
                        yield env.timeout(TICK)
                        self.canal_salida.envia(('BACK', self.id_nodo), [self.padre])
                else:
                    # Ya tenemos padre, enviar BACK vacio
                    yield env.timeout(TICK)
                    self.canal_salida.envia(('BACK', None), [emisor])
            
            elif mensaje[0] == 'BACK':
                id_hijo = mensaje[1]
                
                # Si recibimos un BACK con ID (no None), es un hijo
                if id_hijo is not None:
                    self.hijos.append(id_hijo)
                
                self.expected_msg -= 1
                
                # Si hemos recibido todas las respuestas y no somos la raiz
                if self.expected_msg == 0 and not self.es_raiz:
                    yield env.timeout(TICK)
                    self.canal_salida.envia(('BACK', self.id_nodo), [self.padre])