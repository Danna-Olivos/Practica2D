import simpy
from Canales.Canal import Canal

class CanalBroadcast(Canal):
    """
    Canal de comunicación para broadcast
    
    Extiende la funcionalidad base de Canal para soportar envíos simultáneos a varios vecinos
    """
    def __init__(self, env, capacidad=simpy.core.Infinity):
        """
        Inicializa el canal de broadcast
        
        Args:
            env: Entorno de simulación Simpy
            capacidad: Capacidad máxima de almacenamiento de mensajes
        """
        self.env = env
        self.capacidad = capacidad
        self.canales = []

    def envia(self, mensaje, vecinos):
        '''
        Envía mensaje a vecinos
        
        Args:
            mensaje: mensaje a enviar
            vecinos: Lista de nodos destinatarios
        '''
        for vecino in vecinos:
            if vecino < len(self.canales):
                self.canales[vecino].put(mensaje)

    def crea_canal_de_entrada(self):
        '''Creamos un canal de entrada
        
        Returns:
            simpy.Store: Canal de entrada para el nodo
        '''
        canal_entrada = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada
