from enum import Enum
from ia_2022.entorn import Percepcio
from practica1.agent import Agent
from practica1.estat import Estat
from practica1.entorn import Accio, SENSOR

DEBUG = True

class AgentMiniMaxAlfaBeta(Agent):

    def __init__(self, nom, max_depth=float("+inf"), iteratiu=False):
        """
        Inicialitza l'agent amb una profunditat infinita i emprant l'algorisme recursiu
        """
        super(AgentMiniMaxAlfaBeta, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None # accions només tindrà una única o cap
        self.max_depth = max_depth
        self.iteratiu = iteratiu

    def actua(
            self, percepcio: Percepcio
    ) -> Accio | tuple[Accio, object]:
        if DEBUG:
            print(str(self.jugador).removeprefix("TipusCasella.") + " actua")
        taulell = percepcio[SENSOR.TAULELL]
        mida = percepcio[SENSOR.MIDA]
        estat_inicial = Estat(mida, taulell, jugador=self.jugador)
        if estat_inicial.es_final(): # si no hi ha res que fer
            return Accio.ESPERAR
        self.cerca_recursiva(estat_inicial)
        return Accio.POSAR, self.__accions

    def cerca_recursiva(self, estat_inicial):
        """
        Algorisme MiniMax recursiu. self.__accions només contindrà una acció
        """
        def processar_node(estat, alfa, beta, profunditat, escalar):
            """
            Mètode recursiu que processa cada node
            """
            es_max = escalar > 0
            valor = None
            darrera_accio = None
            self.__oberts.append(estat)
            fills = estat.genera_fill(canvia_torn=True)
            for s in fills: # fa un recorregut dels fills del node
                if s in self.__tancats or s in self.__oberts: # si ja s'ha processat o està pendent de ser-lo
                    continue # passa a un altre fill
                v_subido, d_subida = None, None
                if profunditat + 1 <= self.max_depth:
                    v_subido, d_subida = processar_node(s, alfa, beta, profunditat + 1, -escalar) # el processa a ell i als seus fills
                else:
                    v_subido, d_subida = s.heuristica, s.accions_previes[-1]
                if (valor is None) or (es_max and v_subido > valor) or (not es_max and v_subido < valor):
                    valor = v_subido
                    darrera_accio = d_subida
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
            if darrera_accio is None:
                darrera_accio = estat.accions_previes[-1]
            return valor, darrera_accio
        # l'arrel és MIN perquè quant més petita sigui l'heurística millor és l'estat
        self.__oberts = []
        self.__tancats = set()
        valor, darrera_accio = processar_node(estat_inicial, float("-inf"), float("+inf"), 0, 1) # es processa l'arrel
        self.__accions = darrera_accio # s'assigna l'acció amb la que es pot arribar a l'estat òptim
