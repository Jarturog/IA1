from enum import Enum
from ia_2022.entorn import Percepcio
from practica1.agent import Agent
from practica1.estat import Estat
from practica1.entorn import Accio, SENSOR

DEBUG = True

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

        def __init__(self, estat, interval, tipus: TipusNode, profunditat=0, valor=None, pare=None, fills=None):
            """
            Crea un nou Node, el qual té un estat, uns valors alfa i beta, un tipos de node, una profunditat,
            un valor, una acció relacionada amb l'estat del node que va pujar el valor que té, un booleà que determina
            si hi que realitzar poda i uns nodes fills
            """
            self.estat = estat  
            self.alfa, self.beta = interval
            self.tipus = tipus
            self.valor = valor
            self.profunditat = profunditat
            self.darrera_accio = None
            self.pare = pare
            self.pruning = False
            self.fills = []
            if fills is not None:
                self.fills = fills

        def pujar_valor(self) -> bool:
            """
            Puja un valor des d'el fill cap al pare, també actualitza l'acció que hauria de fer el node pare
            per arribar a l'estat fill

            Returns:
                True si hi ha que realitzar pruning, false en cas contrari
            """
            if self.valor is None:
                self.valor = self.estat.heuristica
            TipusNode = AgentMiniMaxAlfaBeta.Node.TipusNode
            pare = self.pare
            es_max, es_min = pare.tipus == TipusNode.MAX, pare.tipus == TipusNode.MIN
            # si hi ha que canviar el valor del node
            if pare.valor is None or (es_max and self.valor > pare.valor) or (es_min and self.valor < pare.valor):
                pare.valor = self.valor
                pare.darrera_accio = self.estat.accions_previes[-1]
                if es_max: # si és max canvia l'alfa
                    pare.alfa = self.valor
                elif es_min: # si és min canvia la beta
                    pare.beta = self.valor
            pare.pruning = pare.alfa >= pare.beta
        
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
        if self.iteratiu: # si s'ha triat la versió iterativa
            self.cerca_iterativa(estat_inicial)
        else:
            self.cerca_recursiva(estat_inicial)
        return Accio.POSAR, self.__accions

    def cerca_recursiva(self, estat_inicial):
        """
        Algorisme MiniMax recursiu. self.__accions només contindrà una acció
        """
        Node = AgentMiniMaxAlfaBeta.Node
        def processar_node(node):
            """
            Mètode recursiu que processa cada node
            """
            self.__oberts.append(node.estat)
            for s in node.estat.genera_fill(canvia_torn=True): # fa un recorregut dels fills del node
                node_fill = Node(s, (node.alfa, node.beta), node.tipus.get_altre(), profunditat=node.profunditat + 1, pare=node)
                if node_fill.estat in self.__tancats or node_fill.estat in self.__oberts: # si ja s'ha processat o està pendent de ser-lo
                    continue # passa a un altre fill
                if node_fill.profunditat <= self.max_depth:
                    processar_node(node_fill) # el processa a ell i als seus fills
                node_fill.pujar_valor() # el fill intenta pujar el seu valor
                if node.pruning: # si el nou valor ha causat una poda
                    break # es poda
            self.__oberts.pop(-1) # si no es processa es treu dels estats oberts
            self.__tancats.add(node.estat) # i s'afegeix com un estat tancat
        # l'arrel és MIN perquè quant més petita sigui l'heurística millor és l'estat
        arrel = Node(estat_inicial, (float("-inf"), float("+inf")), Node.TipusNode.MIN)
        self.__oberts = []
        self.__tancats = set()
        processar_node(arrel) # es processa l'arrel
        self.__accions = arrel.darrera_accio # s'assigna l'acció amb la que es pot arribar a l'estat òptim

    def cerca_iterativa(self, estat_inicial):
        """
        Algorisme MiniMax iteratiu. self.__accions només contindrà una acció.

        Simula la pila de cridades recursives amb una pila
        """
        Node = AgentMiniMaxAlfaBeta.Node
        # l'arrel és MIN perquè quant més petita sigui l'heurística millor és l'estat
        arrel = Node(estat_inicial, (float("-inf"), float("+inf")), Node.TipusNode.MIN)
        self.__oberts = []
        self.__tancats = set()
        self.__oberts.append(arrel.estat)
        stack = [arrel] # la pila simularà les cridades recursives i contindrà una branca de x nodes a tot moment

        while stack: # mentre quedin nodes per processar
            node = stack[-1] # peek. No es pot fer pop() perquè després de processar el subarbre esquerre 
            # hi ha que tornar al node pare per processar el següent subarbre
            successors = node.estat.genera_fill(canvia_torn=True) # es generen els fills dels estats
            # si no té fills i els fills no es passarien de profunditat
            if len(node.fills) <= 0 and node.profunditat+1 <= self.max_depth: 
                node.fills.extend( # torna els estats a la seva versió de nodes i els afegeix al node com successors d'ell
                    [Node(s, (node.alfa, node.beta), node.tipus.get_altre(), profunditat=node.profunditat + 1, pare=node)
                    for s in successors]
                )
            next_node = None # següent node a afegir a la pila i per tant processar amb els seus fills
            if not node.pruning and len(node.fills) > 0: # si no s'ha de fer pruning i té fills
                node_fill = node.fills.pop() # processa un fill
                pendent_o_ja_processat = node_fill.estat in self.__oberts or node_fill.estat in self.__tancats
                # si el fill ja ha estat processat o està pendent de ser-lo fa un recorregut fins trobar un que no
                while pendent_o_ja_processat and len(node.fills) > 0: 
                    node_fill = node.fills.pop()
                    pendent_o_ja_processat = node_fill.estat in self.__oberts or node_fill.estat in self.__tancats
                if not pendent_o_ja_processat: # si el node fill no ha estat processat ni està pendent
                    self.__oberts.append(node_fill.estat) # l'afegeix a oberts
                    next_node = node_fill # l'assigna com el següent
            if next_node is not None: # si s'ha trobat un fill per processar
                stack.append(next_node) # s'afegeix a la pila
            else: # si no s'ha trobat cap fill
                self.__oberts.pop(-1) # es treu l'estat d'oberts
                self.__tancats.add(node.estat) # i es posa a tancats
                stack.pop() # també es treu el node associat a l'estat ja que els seus fills ja han estat processats
                if node is arrel: # si s'ha arribat al final i per tant s'ha recorregut l'arbre amb la profunditat indicada
                    self.__accions = arrel.darrera_accio # s'assigna l'acció amb la que es pot arribar a l'estat òptim
                    return
                # si el node no és l'arrel intenta pujar el seu valor 
                node.pujar_valor() # i per tant actualitzar possiblement els valors alfa i beta
        