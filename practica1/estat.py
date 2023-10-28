
from practica1.entorn import Accio, TipusCasella

N_CASELLAS_PER_GUANYAR = 4

class Estat:
    
    def __init__(self, mida, taulell, pes=0, accions_previes=None, jugador=None):
        if accions_previes is None:
            accions_previes = []
        self.accions_previes = accions_previes
        self.taulell = taulell
        self.mida = mida
        self.pes = pes
        self.jugador = jugador
        self.heuristica = self.calcHeuristica()

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.taulell == other.taulell
    
    def __lt__(self, other):
        """Overrides the default implementation"""
        return self.heuristica + self.pes < other.heuristica + other.pes
    
    def __hash__(self):
        return hash(tuple(tuple(fila) for fila in self.taulell))

    def calcHeuristica(self) -> int:
        """
        h = suma de todas las h_casilla
        ataque vs defensa:
            -si estamos cerca de ganar priorizar la victoria
            -si no estamos cerca de ganar y el oponente si, priorizar el bloqueo del contrincante

        """
        taulell = self.taulell
        n = len(taulell)  # longitud filas = longitud columnas (nxn)
        h = 0

        def check_casella(i, j):
            h_casella = 0
            casella = taulell[i][j]
            dirs = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if di != 0 or dj != 0]
            for di, dj in dirs:
                for k in range(1, N_CASELLAS_PER_GUANYAR):
                    idx1, idx2 = i + (k * di), j + (k * dj)
                    if not self.index_valid(idx1, idx2): # evita accesos a posiciones fuera del tablero
                        continue
                    casella = taulell[idx1][idx2]
                    if casella == TipusCasella.LLIURE:
                        h_casella += 1.25
                    elif casella == self.jugador:
                        # ataque (ganar)
                        h_casella += 0.5 * (2 ** (k - 1))
                        # donde k es el número de casillas desde la que se encuentra la ocupada por jugador
                    else:
                        # defensa (no perder)
                        h_casella += 1.5 * (2 ** (k - 1))
                        # donde k es el número de casillas en las que está el oponente

            if i in (n // 2 - 1, n // 2) and j in (n // 2 - 1, n // 2): # premia las casillas centrales
                h_casella -= 0.25

            return h_casella

        for i in range(n):
            columnas = len(taulell[i])
            for j in range(n):
                h += check_casella(i, j)
        return h


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
                nou_estat.pes = self.pes + nou_estat.calcular_cost()
                nou_estat.accions_previes.append(acc_actual)
                estats_generats.append(nou_estat)
        return estats_generats
    
    def calcular_cost(self):
        """
        Mètode per calcular el cost de passar d'un estat a un altre.

        Returns:
            Cost enter de fer la transició cap a l'estat.
        """
        return 1 # no s'especifica, per tant es suposa 1

    def __str__(self):
        return f"taulell: \"{self.taulell}\" | Accio {self.accions_previes}"



