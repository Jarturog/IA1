"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, SENSOR, TipusCasella # no sé si TipusCasella se puede importar

N_CASELLAS_PER_GUANYAR = 4

class Agent(joc.Agent):
    
    def __init__(self, nom):
        super(Agent, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        pass

    #@abc.abstractmethod
    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass

class Estat:
    
    def __init__(self, mida, taulell, pes=0, accions_previes=None):
        if accions_previes is None:
            accions_previes = []
        self.accions_previes = accions_previes
        self.taulell = taulell
        self.mida = mida
        self.pes = pes
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
        h_casilla = para cada 3 casillas adyacentas (8 direcciones):
            +0 por cada casilla del jugador,
            +1 por cada casilla libre,
            +2 por cada casilla del contrincante
            por lo tanto máximo es (1+8*3)*2 para cada casilla y 0 como mínimo
        """
        taulell = self.taulell
        filas = len(taulell)
        columnas = len(taulell[0])
        h = 0

        def check_casella(i, j):
            h_casilla = 0
            casella = taulell[i][j]
            if casella == TipusCasella.LLIURE:
                h_casilla += 1
            elif casella != self.jugador: # per tant és casella perdedora
                h_casilla += 2

            direcciones = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if di != 0 or dj != 0]

            for di, dj in direcciones:
                for k in range(1, N_CASELLAS_PER_GUANYAR):
                    ind1, ind2 = i + (k * di), j + (k * dj)
                    if ind1 < 0 or ind2 < 0 or ind2 >= filas or ind1 >= columnas:
                        continue
                    casella = taulell[ind1][ind2]
                    if casella == TipusCasella.LLIURE:
                        h_casilla += 1
                    elif casella != self.jugador: # per tant és casella perdedora
                        h_casilla += 2
            return h_casilla

        for i in range(filas):
            columnas = len(taulell[i])
            for j in range(columnas):
                h += check_casella(i, j)
        return h
    
    def legal(self, accio) -> (bool, str):
        """ Mètode per detectar si una acció és legal.

        Un estat és legal si ...

        Returns:
            true si l'acció es legal
        """
        return self.taulell[accio[0]][accio[1]] == TipusCasella.LLIURE
        

    def es_meta(self) -> bool:
        taulell = self.taulell
        def check_direccio(i, j, di, dj):
            for k in range(N_CASELLAS_PER_GUANYAR):
                if taulell[i + (k * di)][j + (k * dj)] != self.jugador:
                    return False
            return True
        # Iterar a través de todas las celdas de la matriz
        filas = len(taulell)
        for i in range(filas):
            columnas = len(taulell[i])
            for j in range(columnas):
                if taulell[i][j] != self.jugador:
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
                if self.taulell[i][j] != TipusCasella.LLIURE:
                    continue
                taulell = [fila[:] for fila in self.taulell] # copia de valores, no de referencia
                taulell[i][j] = self.jugador #.posar(TIPUS_CASELLA_JUGANT)
                acc = self.accions_previes[:]
                acc.append((Accio.POSAR, (i, j)))
                nou_estat = Estat(self.mida, taulell, acc)
                if nou_estat.legal()[0]:
                    estats_generats.append(nou_estat)
        return estats_generats

    def __str__(self):
        return (f"taulell: \"{self.taulell}\" | Accio {self.accions_previes}")



