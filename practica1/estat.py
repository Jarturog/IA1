
from practica1.entorn import Accio, TipusCasella

N_CASELLAS_PER_GUANYAR = 4
WEIGHT_GUANYAR = 10000
WEIGHT_JUGADOR = 4
WEIGHT_LLIURE = 1
WEIGHT_CONTRINCANT = 4
WEIGHT_ADJACENTS = 10
DIRECCIONS = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == 0 and dj == 0)]
#DIRECCIONS = [(di, dj) for di in [-1, 0, 1] for dj in [0, 1] if not (di == 0 and dj == 0) and not (di == -1 and dj == 0)]

class Estat:
    
    def __init__(self, mida, taulell, accions_previes=None, jugador=None):
        """
        Un Estat té una mida (x, y), un taulell de x y dimensions, unes accions prèvies per arribar a l'estat,
        un jugador el qual va fer la darrera acció i una heurística.
        """
        if accions_previes is None:
            accions_previes = []
        self.accions_previes = accions_previes
        self.taulell = taulell
        self.mida = mida
        self.jugador = jugador
        self.heuristica = self.calcular_heuristica()

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.taulell == other.taulell
    
    def __lt__(self, other):
        """Overrides the default implementation"""
        return self.heuristica < other.heuristica
    
    def __hash__(self):
        return hash(tuple(tuple(fila) for fila in self.taulell))

    def calcular_heuristica(self) -> int:
        """

        Calcula el valor de totes les caselles i les suma

        Returns:
            Nombre positiu que com més gran sigui millor.
        """
        FILES = self.mida[0]
        COLUMNES = self.mida[1]
        taulell = self.taulell
        h = 0 # acumulador creixent de h_caselles
        def valorar_solucions_casella(i, j):
            """
            Puntua cada casella per les combinacions que pot realitzar amb les caselles a les direccions indicades

            Returns:
                Puntuació que quant més gran sigui millor
            """
            h_casella = 0 # acumulador de valoracions des de aquesta casella
            # DIRECCIONS = [(-1, 1), (0, 1), (1, 0), (1, 1)] que són dos diagonals i les direccions vertical i horitzontal
            for di, dj in DIRECCIONS: # dj és la direcció de l'índex j i di la de l'índex i
                # s'inicialitzen el nombre de caselles i caselles consecutives a 0
                n_lliure = n_jugador = n_contrincant = seguits_jugador = seguits_contrincant = 0
                # s'inicialitza el registre de les caselles que han estat adjacents com 0 i amb una lliure
                caselles_adjacents = (TipusCasella.LLIURE, 0) 
                ind1, ind2 = i + (N_CASELLAS_PER_GUANYAR - 1) * di, j + (N_CASELLAS_PER_GUANYAR - 1) * dj
                # si es voldrà arribar a una casella fora del taulell passa a la següent direcció
                if not self.index_valid(ind1, ind2): 
                    continue
                for k in range(N_CASELLAS_PER_GUANYAR): # comprova cada casella d'aquesta direcció (di, dj)
                    ind1, ind2 = i + (k * di), j + (k * dj)
                    casella = taulell[ind1][ind2]
                    # gestió del nombre total de caselles                    
                    if casella == TipusCasella.LLIURE:
                        n_lliure += 1
                    elif casella == self.jugador:
                        n_jugador += 1
                    else:
                        n_contrincant += 1
                    # gestió de caselles adjacents
                    if casella == caselles_adjacents[0]: # si la casella actual és del mateix tipus que l'anterior
                        caselles_adjacents = (caselles_adjacents[0], caselles_adjacents[1] + 1) # incrementa el nombre d'adjacents
                        if casella == self.jugador: # si la casella és la del jugador
                            # actualitza la quantitat màxima de caselles del seu tipus consecutives.
                            # si ja es tenia un conjunt de consecutives (seguits_jugador) major no es canvia,
                            # però si les consecucions d'ara superen l'anterior llavors s'actualitza el valor amb caselles_adjacents[1]
                            seguits_jugador = max(seguits_jugador, caselles_adjacents[1]) 
                        elif casella != TipusCasella.LLIURE: # si és la del contrincant
                            # actualitza la quantitat màxima de caselles del seu tipus consecutives
                            seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                    elif caselles_adjacents[0] != TipusCasella.LLIURE: # si la casella era de qualque jugador y ha estat interrompuda per altra
                        if casella == self.jugador: # si el contrincant ha estat interromput pel jugador
                            # actualitza la quantitat màxima de caselles del contrincant
                            seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                            caselles_adjacents = (casella, 1) # inicialitza el registre amb una casella del seu tipus
                            # i actualitza la quantitat màxima de caselles del seu tipus consecutives
                            seguits_jugador = max(seguits_jugador, caselles_adjacents[1])
                        elif casella != TipusCasella.LLIURE: # si el jugador ha estat interromput pel contrincant
                            # actualitza la quantitat màxima de caselles del jugador
                            seguits_jugador = max(seguits_jugador, caselles_adjacents[1])
                            caselles_adjacents = (casella, 1) # inicialitza el registre amb una casella del seu tipus
                            # i actualitza la quantitat màxima de caselles del seu tipus consecutives
                            seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                        else: # si ha estat interrompuda per una casella lliure
                            if caselles_adjacents[0] == self.jugador: # si ha interromput al jugador
                                # actualitza la quantitat màxima de caselles del jugador
                                seguits_jugador = max(seguits_jugador, caselles_adjacents[1])
                            else: # si ha interromput al contrincant
                                # actualitza la quantitat màxima de caselles del contrincant
                                seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                            caselles_adjacents = (casella, 1) # inicialitza el registre amb una casella lliure
                    else: # si la casella era lliure i ha estat interrompuda per un dels dos jugadors
                        caselles_adjacents = (casella, 1) # inicialitza el registre amb una casella del tipus del jugador que ha interromput
                        if casella == self.jugador: # si ha estat el jugador
                            # actualitza la quantitat màxima de caselles del jugador
                            seguits_jugador = max(seguits_jugador, caselles_adjacents[1])
                        else: # si ha estat el contrincant
                            # actualitza la quantitat màxima de caselles del contrincant
                            seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                # finalment aplica les càlculs de l'heurística i passa a la següent direcció
                if n_jugador >= N_CASELLAS_PER_GUANYAR:
                    h_casella += WEIGHT_GUANYAR
                elif n_contrincant >= N_CASELLAS_PER_GUANYAR:
                    h_casella -= WEIGHT_GUANYAR
                h_casella += WEIGHT_JUGADOR * n_jugador - WEIGHT_CONTRINCANT * n_contrincant
                h_casella += WEIGHT_ADJACENTS ** seguits_jugador - WEIGHT_ADJACENTS ** seguits_contrincant
            return h_casella
        # recorre tot el taulell
        for i in range(FILES):
            for j in range(COLUMNES):
                h += valorar_solucions_casella(i, j)
        return h

    def index_valid(self, i, j)-> bool:
        """
        Returns:
            True si l'índex està dins el taulell
        """
        return 0 <= i < self.mida[0] and 0 <= j < self.mida[1]

    def legal(self, accio) -> bool:
        """ 
        Mètode per detectar si una acció és legal.

        Returns:
            True si l'acció es legal, False si no
        """
        return self.taulell[accio[0]][accio[1]] == TipusCasella.LLIURE
        

    def es_final(self, es_meta=False) -> bool:
        """ 
        Mètode per evaluar si l'estat és final (qualque jugador guanya o no es pot jugar més).

        Returns:
            True si un jugador ha guanyat o totes les caselles estan ocupades
        """
        taulell = self.taulell
        def check_direccio(i, j, di, dj):
            """
            Comprova si en la direcció hi ha qualque casella diferent
            """
            casella = taulell[i][j]
            for k in range(1, N_CASELLAS_PER_GUANYAR):
                if taulell[i + (k * di)][j + (k * dj)] != casella: # si no és del mateix tipus
                    return False
            return True
        hi_ha_casella_lliure = False
        # Recorregut de la matriu
        for i in range(self.mida[0]):
            for j in range(self.mida[1]):
                if taulell[i][j] == TipusCasella.LLIURE: # si és lliure ningú ha guanyat amb aquesta casella
                    hi_ha_casella_lliure = True
                    continue
                # Verifica les quatre direccions possibles: horitzontal, vertical, diagonal descendent i diagonal ascendent
                for di, dj in DIRECCIONS:#[(0, 1), (1, 0), (1, 1), (1, -1)]:
                    # Comprova si és possible encontrar N_CASELLAS_PER_GUANYAR caselles en aquesta direcció
                    ind1, ind2 = i + (N_CASELLAS_PER_GUANYAR - 1) * di, j + (N_CASELLAS_PER_GUANYAR - 1) * dj
                    if self.index_valid(ind1, ind2) and check_direccio(i, j, di, dj):
                        return True # Si es troba una línia guanyadora, retorna True
        if es_meta: # Si no es troba cap línia guanyadora en cap direcció, hi ha espai per posar i es vol comprovar que es meta
            return False # retorna false
        else: # si només es vol comprovar que sigui final (ningú ha guanyat i encara hi ha espai) retorna aquest cas
            return False or not hi_ha_casella_lliure 

    def genera_fill(self, casella) -> list:
        """
        Mètode per generar els estats fills a partir de l'estat actual.

        Returns:
            Llista d'estats fills generats.
        """
        # assigna el tipus de casella per l'estat fill com la del mateix jugador si no es vol canviar de torn
        # si es vol canviar de torn s'assignarà el tipus de casella de l'altre jugador
        estats_generats = []
        # S'itera a través de tota la matriu
        for i in range(self.mida[0]):
            for j in range(self.mida[1]):
                acc_actual = i, j # acció actual
                if not self.legal(acc_actual): # si no és legal passa a la següent
                    continue
                taulell = [fila[:] for fila in self.taulell] # còpia de valors, no de referència
                taulell[i][j] = casella # s'aplica l'acció
                acc = self.accions_previes[:]
                acc.append(acc_actual) # es plasma l'acció al registre d'accions prèvies
                nou_estat = Estat(self.mida, taulell, accions_previes=acc, jugador=self.jugador)
                estats_generats.append(nou_estat) # es crea l'estat i s'afegeix
        return estats_generats

    def __str__(self):
        """
        Per tornar el taulell en un string
        """
        return f"taulell: \"{self.taulell}\" | Accio {self.accions_previes}"

    def imprimir(self):
        taulell_str = str(self)
        taulell_str = taulell_str.replace("<TipusCasella.LLIURE: 0>", " ")
        taulell_str = taulell_str.replace("<TipusCasella.CREU: 1>", "x")
        taulell_str = taulell_str.replace("<TipusCasella.CARA: 2>", "o")
        taulell_str = taulell_str.replace("], [", "\n")
        taulell_str = taulell_str.removesuffix("]]\" | Accio []")
        taulell_str = taulell_str.removeprefix("taulell: \"[[")
        print(taulell_str)


