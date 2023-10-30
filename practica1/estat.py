
from practica1.entorn import Accio, TipusCasella

N_CASELLAS_PER_GUANYAR = 4

class Estat:
    
    def __init__(self, mida, taulell, accions_previes=None, jugador=None):
        if accions_previes is None:
            accions_previes = []
        self.accions_previes = accions_previes
        self.taulell = taulell
        self.mida = mida
        self.jugador = jugador
        self.heuristica = self.calcHeuristica()

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.taulell == other.taulell
    
    def __lt__(self, other):
        """Overrides the default implementation"""
        return self.heuristica < other.heuristica
    
    def __hash__(self):
        return hash(tuple(tuple(fila) for fila in self.taulell))

    def calcHeuristica(self) -> int: # not good
        """
        h = máximo valor posible menos suma de todas las h_casilla, donde cuanto mayor sea h_casilla mejor

        Elige un valor para cada tipo de casilla, calcula todas las posibles filas, columnas y diagonales
        con las que se puede ganar (4 casillas adyacentes en nuestro caso) y, para conseguir el valor máximo,
        se supone que todas son del jugador. El cálculo de la heurística real es análogo pero sin la suposición
        de que todas las casillas son las del jugador.

        Returns:
            Entero que cuanto más cerca esté del cero, más le conviene al agente elegir el estado.
        """
        WEIGHT_JUGADOR = 8
        WEIGHT_LLIURE = 4
        WEIGHT_CONTRINCANT = 2
        FILAS = self.mida[0]
        COLUMNAS = self.mida[1]
        N_FILAS = (FILAS - N_CASELLAS_PER_GUANYAR + 1) * COLUMNAS
        N_COLUMNAS = (COLUMNAS - N_CASELLAS_PER_GUANYAR + 1) * FILAS
        N_DIAGONALES = 2 * (FILAS - N_CASELLAS_PER_GUANYAR + 1) * (COLUMNAS - N_CASELLAS_PER_GUANYAR + 1)
        MAX_VALUE_H = (N_FILAS + N_COLUMNAS + N_DIAGONALES) * WEIGHT_JUGADOR * N_CASELLAS_PER_GUANYAR

        taulell = self.taulell
        h_max = 0
        direcciones = [(di, dj) for di in [-1, 0, 1] for dj in [0, 1] if not (di == 0 and dj == 0) and not (di == -1 and dj == 0)]
        def valorar_soluciones_casilla(i, j):
            h_casella = 0
            for di, dj in direcciones:
                n_lliure = 0
                n_jugador = 0
                n_contrincant = 0
                ind1, ind2 = i + (N_CASELLAS_PER_GUANYAR - 1) * di, j + (N_CASELLAS_PER_GUANYAR - 1) * dj
                if not self.index_valid(ind1, ind2):
                    continue
                for k in range(N_CASELLAS_PER_GUANYAR):
                    ind1, ind2 = i + (k * di), j + (k * dj)
                    casella = taulell[ind1][ind2]
                    if casella == TipusCasella.LLIURE:
                        n_lliure += 1
                    elif casella == self.jugador:
                        n_jugador += 1
                    else:
                        n_contrincant += 1
                h_casella += WEIGHT_LLIURE * n_lliure + WEIGHT_JUGADOR * n_jugador + WEIGHT_CONTRINCANT * n_contrincant
            return h_casella
        for i in range(FILAS):
            for j in range(COLUMNAS):
                h_max += valorar_soluciones_casilla(i, j)
        return MAX_VALUE_H - h_max

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

    def genera_fill(self) -> list:
        """
        Mètode per generar els estats fills a partir de l'estat actual.

        Returns:
            Llista d'estats fills generats.
        """
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
                nou_estat = Estat(self.mida, taulell, accions_previes=acc, jugador=self.jugador)
                nou_estat.accions_previes.append(acc_actual)
                estats_generats.append(nou_estat)
        return estats_generats

    def __str__(self):
        return f"taulell: \"{self.taulell}\" | Accio {self.accions_previes}"



