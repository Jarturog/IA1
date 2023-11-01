
from practica1.entorn import Accio, TipusCasella

N_CASELLAS_PER_GUANYAR = 4

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
        L'heurística final és un valor entre MAX_VALUE_H (valor positiu) i 0. Quant més petit sigui l'heurística millor.

        Primer calcula el màxim ...
        Tria un valor per a cada tipus de casella, calcula totes les possibles files, columnes i diagonals
        amb les quals es pot guanyar (4 caselles adjacents en el nostre cas) i, per a aconseguir el valor màxim,
        se suposa que totes són del jugador. El càlcul de l'heurística real és anàleg però sense la suposició
        que totes les caselles són les del jugador.

        Returns:
        Sencer que com més a prop estigui del zero, més li convé a l'agent triar l'estat.
        """
        WEIGHT_JUGADOR = 4
        WEIGHT_LLIURE = 1
        WEIGHT_CONTRINCANT = 5
        WEIGHT_ADJACENTS = 10
        FILAS = self.mida[0]
        COLUMNAS = self.mida[1]
        N_FILAS = (FILAS - N_CASELLAS_PER_GUANYAR + 1) * COLUMNAS
        N_COLUMNAS = (COLUMNAS - N_CASELLAS_PER_GUANYAR + 1) * FILAS
        N_DIAGONALES = 2 * (FILAS - N_CASELLAS_PER_GUANYAR + 1) * (COLUMNAS - N_CASELLAS_PER_GUANYAR + 1)
        N_POSIBLES_METAS = N_FILAS + N_COLUMNAS + N_DIAGONALES
        MAX_VALUE_H = N_POSIBLES_METAS * (WEIGHT_JUGADOR * N_CASELLAS_PER_GUANYAR + WEIGHT_ADJACENTS ** (N_CASELLAS_PER_GUANYAR - 1))
        MIN_VALUE_H = -N_POSIBLES_METAS * (WEIGHT_CONTRINCANT * N_CASELLAS_PER_GUANYAR + WEIGHT_ADJACENTS ** (N_CASELLAS_PER_GUANYAR - 1))
        taulell = self.taulell
        h_max = 0
        direcciones = [(di, dj) for di in [-1, 0, 1] for dj in [0, 1] if not (di == 0 and dj == 0) and not (di == -1 and dj == 0)]
        def valorar_soluciones_casilla(i, j):
            h_casella = 0
            for di, dj in direcciones:
                n_lliure = n_jugador = n_contrincant = seguits_jugador = seguits_contrincant = 0
                caselles_adjacents = (TipusCasella.LLIURE, 0)
                ind1, ind2 = i + (N_CASELLAS_PER_GUANYAR - 1) * di, j + (N_CASELLAS_PER_GUANYAR - 1) * dj
                if not self.index_valid(ind1, ind2):
                    continue
                for k in range(N_CASELLAS_PER_GUANYAR):
                    ind1, ind2 = i + (k * di), j + (k * dj)
                    casella = taulell[ind1][ind2]
                    # gestión del número total de casillas                    
                    if casella == TipusCasella.LLIURE:
                        n_lliure += 1
                    elif casella == self.jugador:
                        n_jugador += 1
                    else:
                        n_contrincant += 1
                    # gestión de casillas adyacentes
                    if casella == caselles_adjacents[0]: # si sigue la racha
                        caselles_adjacents = (caselles_adjacents[0], caselles_adjacents[1] + 1)
                        if casella == self.jugador: # del jugador
                            seguits_jugador = max(seguits_jugador, caselles_adjacents[1])
                        elif casella != TipusCasella.LLIURE: # del contrincante
                            seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                    elif caselles_adjacents[0] != TipusCasella.LLIURE: # si era la racha de algún jugador y ha sido parada
                        if casella == self.jugador: # si ha sido parada por el jugador
                            seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                            caselles_adjacents = (casella, 1)
                            seguits_jugador = max(seguits_jugador, caselles_adjacents[1])
                        elif casella != TipusCasella.LLIURE: # si ha sido parada por el contrincante
                            seguits_jugador = max(seguits_jugador, caselles_adjacents[1])
                            caselles_adjacents = (casella, 1)
                            seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                        else: # si ha sido parada por una casilla libre
                            if caselles_adjacents[0] == self.jugador: # ha parado al jugador
                                seguits_jugador = max(seguits_jugador, caselles_adjacents[1])
                            else: # ha parado al contrincante
                                seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                            caselles_adjacents = (casella, 1)
                    else: # si era la racha casillas libres y ha sido parada
                        caselles_adjacents = (casella, 1)
                        if casella == self.jugador: # si ha sido parada por el jugador
                            seguits_jugador = max(seguits_jugador, caselles_adjacents[1])
                        else: # si ha sido parada por el contrincante
                            seguits_contrincant = max(seguits_contrincant, caselles_adjacents[1])
                h_casella += WEIGHT_LLIURE * n_lliure + WEIGHT_JUGADOR * n_jugador - WEIGHT_CONTRINCANT * n_contrincant
                h_casella += WEIGHT_ADJACENTS ** (seguits_jugador - 1) - (WEIGHT_ADJACENTS ** (seguits_contrincant - 1))
            return h_casella
        for i in range(FILAS):
            for j in range(COLUMNAS):
                h_max += valorar_soluciones_casilla(i, j)
        h_normalizada = (h_max - MIN_VALUE_H) * MAX_VALUE_H / (MAX_VALUE_H - MIN_VALUE_H)
        return MAX_VALUE_H - h_normalizada # normalizo el valor de h_max para volverlo un número natural

    def index_valid(self, i, j)-> bool:
        return 0 <= i < self.mida[0] and 0 <= j < self.mida[1]

    def legal(self, accio) -> bool:
        """ 
        Mètode per detectar si una acció és legal.

        Returns:
            true si l'acció es legal
        """
        return self.taulell[accio[0]][accio[1]] == TipusCasella.LLIURE
        

    def es_meta(self) -> bool:
        """ 
        Mètode per evaluar si l'estat és final (qualque jugador guanya).

        Returns:
            true si un jugador ha guanyat
        """
        taulell = self.taulell
        def check_direccio(i, j, di, dj):
            casella = taulell[i][j]
            for k in range(1, N_CASELLAS_PER_GUANYAR):
                if taulell[i + (k * di)][j + (k * dj)] != casella: # si no és del mateix tipus
                    return False
            return True
        # Iterar a través de todas las celdas de la matriz
        filas = len(taulell)
        for i in range(filas):
            columnas = len(taulell[i])
            for j in range(columnas):
                if taulell[i][j] == TipusCasella.LLIURE:
                    continue
                # Verificar las cuatro direcciones posibles: horizontal, vertical, diagonal descendente y diagonal ascendente
                for di, dj in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                    # Comprobar si es posible encontrar N_CASELLAS_PER_GUANYAR casillas en esa dirección
                    if (0 <= i + (N_CASELLAS_PER_GUANYAR - 1) * di < filas and
                        0 <= j + (N_CASELLAS_PER_GUANYAR - 1) * dj < columnas and
                        check_direccio(i, j, di, dj)): # Utilizar la función auxiliar para verificar si hay una línea ganadora en esa dirección
                        return True  # Si se encuentra una línea ganadora, retornar True
        return False  # Si no se encuentra ninguna línea ganadora en ninguna dirección, retornar False

    def genera_fill(self, canvia_turn=False) -> list:
        """
        Mètode per generar els estats fills a partir de l'estat actual.

        Returns:
            Llista d'estats fills generats.
        """
        tipus_casella = (TipusCasella.CREU if self.jugador == TipusCasella.CARA else TipusCasella.CARA) if canvia_turn else self.jugador
        estats_generats = []
        # Iterar a través de todas las celdas de la matriz
        filas = len(self.taulell)
        for i in range(filas):
            columnas = len(self.taulell[i])
            for j in range(columnas):
                acc_actual = i, j
                if not self.legal(acc_actual):
                    continue
                taulell = [fila[:] for fila in self.taulell] # copia de valores, no de referencia
                taulell[i][j] = self.jugador
                acc = self.accions_previes[:]
                acc.append(acc_actual)
                nou_estat = Estat(self.mida, taulell, accions_previes=acc, jugador=tipus_casella)
                estats_generats.append(nou_estat)
        return estats_generats

    def __str__(self):
        return f"taulell: \"{self.taulell}\" | Accio {self.accions_previes}"



