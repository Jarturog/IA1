"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, SENSOR


class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        mida = percepcio[SENSOR.MIDA]
        #accio = self.depthFirstSearch(taulell, mida)
        accio = self.aSearch(taulell, mida)
        return accio

    def depthFirstSearch(self, taulell, mida):

            pass

    """
    Algoritmo A*
    """
    def aSearch(self, taulell, mida):
        def heuristica(taulell, jugador_actual):

            pass
        pass




