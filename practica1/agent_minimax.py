from enum import Enum
from ia_2022.entorn import Percepcio
from practica1.agent import Agent
from practica1.estat import Estat
from practica1.entorn import Accio, SENSOR, TipusCasella
DEBUG = True

class AgentMiniMaxAlfaBeta(Agent):

    def __init__(self, nom, max_depth=float("+inf")):
        """
        Inicialitza l'agent amb una profunditat infinita i emprant l'algorisme recursiu
        """
        super(AgentMiniMaxAlfaBeta, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None # accions només tindrà una única o cap
        self.max_depth = max_depth

    def actua(
            self, percepcio: Percepcio
    ) -> Accio | tuple[Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        mida = percepcio[SENSOR.MIDA]
        estat_inicial = Estat(mida, taulell, jugador=self.jugador)
        if self.max_depth <= 0 or estat_inicial.es_final(): # si no hi ha res que fer
            return Accio.ESPERAR
        if DEBUG:
            estat_inicial.imprimir()
        self.cerca_recursiva(estat_inicial)
        if DEBUG:
            print(str(self.jugador).removeprefix("TipusCasella.") + " actua: " + str(self.__accions))
        return Accio.POSAR, self.__accions

    def cerca_recursiva(self, estat_inicial):
        """
        Algorisme MiniMax recursiu. self.__accions només contindrà una acció
        """
        def processar_node(estat, alfa, beta, profunditat, es_max):
            """
            Mètode recursiu que processa cada node
            """
            if profunditat >= self.max_depth:
                return estat.heuristica
            valor = None
            self.__oberts.append(estat)
            fills = estat.genera_fill(self.jugador if es_max else getOther(self.jugador))
            for s in fills: # fa un recorregut dels fills del node
                if s in self.__tancats or s in self.__oberts: # si ja s'ha processat o està pendent de ser-lo
                    continue # passa a un altre fill
                v_subido = processar_node(s, alfa, beta, profunditat + 1, not es_max) # el processa a ell i als seus fills
                if (valor is None) or (es_max and v_subido > valor) or (not es_max and v_subido < valor):
                    valor = v_subido
                    if profunditat == 0:
                        if DEBUG:
                            print(str(s.accions_previes[0]) + ": " + str(valor))
                        self.__accions = s.accions_previes[0]
                    if es_max:  # si és max canvia l'alfa
                        alfa = valor
                    else:  # si és min canvia la beta
                        beta = valor
                if alfa >= beta: # si el nou valor ha causat una poda
                    break # es poda
            self.__oberts.pop(-1) # si no es processa es treu dels estats oberts
            self.__tancats.add(estat) # i s'afegeix com un estat tancat
            if valor is None:
                valor = estat.heuristica
            return valor
        # l'arrel és MAX perquè quant més gran sigui l'heurística millor és l'estat
        self.__oberts = []
        self.__tancats = set()
        processar_node(estat_inicial, float("-inf"), float("+inf"), 0, True) # es processa l'arrel


def getOther(casella):
    """
    Retorna l'altre tipus de casella, si és lliure retorna lliure
    """
    if casella == TipusCasella.CARA:
        return TipusCasella.CREU
    if casella == TipusCasella.CREU:
        return TipusCasella.CARA
    return TipusCasella.LLIURE

def custom_move(movesCARA, movesCREU, jugador):
    """
    mètode per realitzar moviments específics i per tant fer DEBUG més fàcilment
    :returns: estat
    """
    s = 8
    t = [[TipusCasella.LLIURE for _ in range(s)] for _ in range(s)]
    for x, y in movesCARA:
        t[x][y] = TipusCasella.CARA
    for x, y in movesCREU:
        t[x][y] = TipusCasella.CREU
    e = Estat((s, s), t, jugador=jugador)
    print(e.heuristica)
    return e
