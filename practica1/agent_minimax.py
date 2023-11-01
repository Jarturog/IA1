from enum import Enum
from ia_2022.entorn import Percepcio
from practica1.agent import Agent
from practica1.estat import Estat
from practica1.entorn import Accio, SENSOR

class AgentMiniMaxAlfaBeta(Agent):
    class Node:
        class TipusNode(Enum):
            MIN = 0
            MAX = 1

            def get_altre(self):
                TipusNode = AgentMiniMaxAlfaBeta.Node.TipusNode
                if self is TipusNode.MIN:
                    return TipusNode.MAX
                else: # self is TipusNode.MAX
                    return TipusNode.MIN

        def __init__(self, estat, interval, tipus: TipusNode, profunditat=0, valor=None):
            self.estat = estat  
            self.alfa, self.beta = interval
            self.tipus = tipus
            self.valor = valor
            self.profunditat = profunditat
            self.darrera_accio = None

        def pujar_valor(self, node_fill) -> bool:
            """
            Returns:
                True if pruning is needed, false if not
            """
            valor = node_fill.valor
            accio = node_fill.estat.accions_previes[0]
            TipusNode = AgentMiniMaxAlfaBeta.Node.TipusNode
            es_max, es_min = self.tipus == TipusNode.MAX, self.tipus == TipusNode.MIN
            if self.valor is None or (es_max and valor > self.valor) or (es_min and valor < self.valor):
                self.valor = valor
                self.darrera_accio = accio
                if es_max:
                    self.alfa = valor
                elif es_min:
                    self.beta = valor
            return self.alfa >= self.beta
        
    def __init__(self, nom, max_depth=float("+inf")):
        super(AgentMiniMaxAlfaBeta, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None
        self.max_depth = max_depth

    def actua(
            self, percepcio: Percepcio
    ) -> Accio | tuple[Accio, object]:
        self.max_depth = 1 # quitar ---------------------------------------------------------
        taulell = percepcio[SENSOR.TAULELL]
        mida = percepcio[SENSOR.MIDA]
        estat_inicial = Estat(mida, taulell, jugador=self.jugador)
        if estat_inicial.accions_previes is None:
            return Accio.ESPERAR
        self.__oberts = []
        self.__tancats = set()
        self.__oberts.append(estat_inicial)
        Node = AgentMiniMaxAlfaBeta.Node
        nodo = Node(estat_inicial, (float("-inf"), float("+inf")), Node.TipusNode.MIN)
        self.__accions = self.procesar_nodo(nodo) # cerca
        return Accio.ESPERAR if self.__accions is None else (Accio.POSAR, self.__accions)

    def procesar_nodo(self, nodo):
        successors = nodo.estat.genera_fill(canvia_turn=True)
        for s in reversed(successors):
            if s in self.__tancats or s in self.__oberts:
                break
            self.__oberts.append(s)
            node_fill = AgentMiniMaxAlfaBeta.Node(s, (nodo.alfa, nodo.beta), nodo.tipus.get_altre(), profunditat=nodo.profunditat + 1)
            if node_fill.profunditat <= self.max_depth:
                self.procesar_nodo(node_fill)
            if node_fill.valor is None:
                node_fill.valor = node_fill.estat.heuristica
            pruning = nodo.pujar_valor(node_fill)
            if pruning:
                break ## poda++ (aunque no queden más hijos)
        self.__tancats.add(nodo.estat)
        return nodo.darrera_accio
