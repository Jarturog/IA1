from enum import Enum
from ia_2022.entorn import Percepcio
from practica1.agent import Agent
from practica1.estat import Estat
from practica1.entorn import Accio, SENSOR

class AgentMiniMaxAlfaBeta(Agent):
    class Node:
        """
        Node del qual estarà fet l'arbre que recorrerà l'agent
        """
        class TipusNode(Enum):
            """
            Un node pot ser MIN o MAX
            """
            MIN = 0
            MAX = 1

            def get_altre(self):
                """
                Returns:
                    Si el tipus pel qual es crida el mètode és MIN retornarà MAX i viceversa 
                """
                TipusNode = AgentMiniMaxAlfaBeta.Node.TipusNode
                if self is TipusNode.MIN:
                    return TipusNode.MAX
                elif self is TipusNode.MAX:
                    return TipusNode.MIN

        def __init__(self, estat, interval, tipus: TipusNode, profunditat=0, valor=None):
            """
            Crea un nou Node, el qual té un estat, uns valors alfa i beta, un tipos de node, una profunditat,
            un valor i una acció relacionada amb l'estat del node que va pujar el valor que té
            """
            self.estat = estat  
            self.alfa, self.beta = interval
            self.tipus = tipus
            self.valor = valor
            self.profunditat = profunditat
            self.darrera_accio = None

        def pujar_valor(self, node_fill) -> bool:
            """
            Returns:
                True si hi ha que realitzar pruning, false en cas contrari
            """
            valor = node_fill.valor
            accio = node_fill.estat.accions_previes[0]
            TipusNode = AgentMiniMaxAlfaBeta.Node.TipusNode
            es_max, es_min = self.tipus == TipusNode.MAX, self.tipus == TipusNode.MIN
            # si hi ha que canviar el valor del node
            if self.valor is None or (es_max and valor > self.valor) or (es_min and valor < self.valor):
                self.valor = valor
                self.darrera_accio = accio
                if es_max: # si és max canvia l'alfa
                    self.alfa = valor
                elif es_min: # si és min canvia la beta
                    self.beta = valor
            return self.alfa >= self.beta
        
    def __init__(self, nom, max_depth=float("+inf")):
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
        self.__oberts = []
        self.__tancats = set()
        self.__oberts.append(estat_inicial)
        Node = AgentMiniMaxAlfaBeta.Node
        # l'arrel és MIN perquè quant més petita sigui l'heurística millor és l'estat
        arrel = Node(estat_inicial, (float("-inf"), float("+inf")), Node.TipusNode.MIN) 
        self.__accions = self.processar_node(arrel) # cerca la millor acció
        # si no hi ha acció espera, si hi ha posa
        return Accio.ESPERAR if self.__accions is None else (Accio.POSAR, self.__accions)

    def processar_node(self, nodo):
        successors = nodo.estat.genera_fill(canvia_turn=True)
        for s in reversed(successors):
            if s in self.__tancats or s in self.__oberts:
                break
            self.__oberts.append(s)
            node_fill = AgentMiniMaxAlfaBeta.Node(s, (nodo.alfa, nodo.beta), nodo.tipus.get_altre(), profunditat=nodo.profunditat + 1)
            if node_fill.profunditat <= self.max_depth:
                self.processar_node(node_fill)
            if node_fill.valor is None:
                node_fill.valor = node_fill.estat.heuristica
            pruning = nodo.pujar_valor(node_fill)
            if pruning:
                break ## poda++ (aunque no queden más hijos)
        self.__tancats.add(nodo.estat)
        return nodo.darrera_accio
