
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
        return self.taulell < other.taulell
    
    def __le__(self, other):
        """Overrides the default implementation"""
        return self.taulell <= other.taulell
    
    def __hash__(self):
        return hash(tuple(tuple(fila) for fila in self.taulell))

    def calcHeuristica(self) -> int:
        """
        h = suma de todas las h_casilla
        hay que tener en cuenta el ataque y la defensa:
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
                    if not self.index_valid(idx1, idx2, n): # evita accesos a posiciones fuera del tablero
                        continue
                    casella = taulell[idx1][idx2]
                    if casella == TipusCasella.LLIURE:
                        h_casella += 1.25
                    elif casella == self.jugador:
                        # ataque (ganar)
                        if k == 1:
                            h_casella += 0.5 # casilla ocupada por jugador  a 1 de distancia
                        elif k == 2:
                            h_casella += 1 # casilla ocupada por jugador  a 2 de distancia
                        elif k == 3:
                            h_casella += 2 # casilla ocupada por jugador  a 3 de distancia
                    else:
                        # defensa (no perder)
                        if k == 1:      # el oponente esta a 1 casilla de distancia
                            h_casella += 1.5
                        elif k == 2:    # el oponente esta a 2 casillas de distancia
                            h_casella += 3
                        elif k == 3:       # el oponente esta a 3 casillas de distancia
                            h_casella += 6

            if i in (n // 2 - 1, n // 2) and j in (n // 2 - 1, n // 2): # premia las casillas centrales
                h_casella -= 0.25

            return h_casella

        for i in range(n):
            columnas = len(taulell[i])
            for j in range(n):
                h += check_casella(i, j)
        return h


    def index_valid(self, idx1, idx2, n)-> bool:
        return 0 <= idx1 < n and 0 <= idx2 < n

    def evaluar_taulell(self, taulell):
    # para calcular la h y que el codigo de calc heuristica no sea tan inmenso, pero puede no ser necesario
        pass



    def legal(self, accio) -> bool:

        """ Mètode per detectar si una acció és legal.

        Returns:
            true si l'acció es legal
        """
        return self.taulell[accio[0]][accio[1]] == TipusCasella.LLIURE
        

    def es_meta(self) -> bool:
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
        """ Mètode per generar els estats fills.

        Genera tots els estats fill a partir de l'estat actual.

        Returns:
            Llista d'estats fills generats.
        """
        estats_generats = []
        # Iterar a través de todas las celdas de la matriz
        filas = len(self.taulell)
        for i in range(filas):
            columnas = len(self.taulell[i])
            for j in range(columnas):
                acc_actual = (Accio.POSAR, (i, j))
                if not self.legal(acc_actual[1]):
                    continue
                taulell = [fila[:] for fila in self.taulell] # copia de valores, no de referencia
                taulell[i][j] = self.jugador
                acc = self.accions_previes[:]
                acc.append(acc_actual)
                nou_estat = Estat(self.mida, taulell, acc)
                estats_generats.append(nou_estat)
        return estats_generats

    def __str__(self):
        return f"taulell: \"{self.taulell}\" | Accio {self.accions_previes}"



