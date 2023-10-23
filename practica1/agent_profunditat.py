from ia_2022.entorn import Percepcio
from practica1 import joc, entorn
from practica1.agent import Agent, Estat
from practica1.entorn import Accio, SENSOR

class AgentProfunditat(Agent):
    def __init__(self, nom):
        super(AgentProfunditat, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def actua(
            self, percepcio: Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        mida = percepcio[SENSOR.MIDA]
        estat_inicial = Estat(mida, taulell)
        if self.__accions is None:
            self.cerca(estat_inicial)
        if len(self.__accions) <= 0:
            return Accio.ESPERAR
        accio = self.__accions.pop(-1)
        return Accio.POSAR, accio
    
    def cerca(self, inicial):
        self.__oberts = [inicial]
        self.__tancats = set()
        self.__accions = []
        while len(self.__oberts) > 0:
            estat = self.__oberts.pop()
            if estat.es_meta():
                self.__accions = estat.accions_previes[:]
                break
            succ = estat.genera_fill()
            self.__tancats.add(estat)
            for s in succ:
                ja_processat = any(s.__eq__(sTancat) for sTancat in self.__tancats)
                if ja_processat:
                    continue
                ja_plantejat = any(s.__eq__(sObert) for sObert in self.__oberts)
                if not ja_plantejat:
                    self.__oberts.append(s)