from ia_2022.entorn import Percepcio
from practica1.agent import Agent
from practica1.estat import Estat
from practica1.entorn import Accio, SENSOR

class AgentProfunditat(Agent):
    def __init__(self, nom):
        super(AgentProfunditat, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def actua(
            self, percepcio: Percepcio
    ) -> Accio | tuple[Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        mida = percepcio[SENSOR.MIDA]
        estat_inicial = Estat(mida, taulell, jugador=self.jugador)
        if self.__accions is None:
            self.cerca(estat_inicial)
        if len(self.__accions) <= 0:
            return Accio.ESPERAR
        accio = self.__accions.pop(0)
        return Accio.POSAR, accio
    
    def cerca(self, inicial):
        self.__oberts = [inicial]
        self.__tancats = set()
        self.__accions = []
        while len(self.__oberts) > 0:
            estat = self.__oberts.pop(-1)
            if estat.es_meta():
                self.__accions = estat.accions_previes[:]
                break
            successors = estat.genera_fill()
            self.__tancats.add(estat)
            for s in reversed(successors):
                if s not in self.__tancats and s not in self.__oberts: # if not (any(s.__eq__(sTancat) for sTancat in self.__tancats) or any(s.__eq__(sObert) for sObert in self.__oberts)):
                    self.__oberts.append(s)
