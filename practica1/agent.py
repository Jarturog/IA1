"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, SENSOR, TipusCasella # no sé si TipusCasella se puede importar

CASILLA_GANADORA = TipusCasella.CARA
CASILLA_LIBRE = TipusCasella.LLIURE
NUM_CASILLAS_PARA_GANAR = 4

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
    
    def __init__(self, mida, taulell, accions_previes=None):
        if accions_previes is None:
            accions_previes = []
        self.accions_previes = accions_previes
        self.taulell = taulell
        self.mida = mida
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
        h_casilla = para cada 3 casillas adyacentas (8 direcciones):
            +0 por cada casilla ganadora,
            +1 por cada casilla libre,
            +2 por cada casilla perdedora
            por lo tanto máximo es (1+8*3)*2 para cada casilla y 0 como mínimo
        h = suma de todas las h_casilla
        """
        taulell = self.taulell
        filas = len(taulell)
        columnas = len(taulell[0])
        h = 0

        def check_casella(i, j):
            h_casilla = 0
            casella = taulell[i][j]
            if casella == CASILLA_LIBRE:
                h_casilla += 1
            elif casella != CASILLA_GANADORA: # per tant és casella perdedora
                h_casilla += 2

            direcciones = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if di != 0 or dj != 0]

            for di, dj in direcciones:
                for k in range(1, NUM_CASILLAS_PARA_GANAR):
                    ind1, ind2 = i + (k * di), j + (k * dj)
                    if ind1 < 0 or ind2 < 0 or ind2 >= filas or ind1 >= columnas:
                        continue
                    casella = taulell[ind1][ind2]
                    if casella == CASILLA_LIBRE:
                        h_casilla += 1
                    elif casella != CASILLA_GANADORA: # per tant és casella perdedora
                        h_casilla += 2
            return h_casilla

        for i in range(filas):
            columnas = len(taulell[i])
            for j in range(columnas):
                h += check_casella(i, j)
        return h
    
    def legal(self) -> (bool, str):
        """ Mètode per detectar si un estat és legal.

        Un estat és legal si ...

        Returns:
            Missatge d'error o None en cas de que sigui legal
        """
        taulell = self.taulell
        mida = self.mida
        if mida is None or not isinstance(mida, tuple) or len(mida) != 2:
            return False, "La mida hauria de ser una tupla de dos enters: " + mida
        if taulell is None or not isinstance(taulell, tuple):
            return False, "La taulell hauria de ser una llista de " + str(mida[0]) + " llistes de " + str(mida[1]) + " caselles"
        if len(taulell) != mida[0]:
            return False, "La taulell i la mida no encaixen: " + len(taulell) + " != " + str(mida[0])
        for i in taulell:
            if i is None or len(i) != mida[0]:
                return False, "La taulell hauria de ser una llista de " + str(mida[0]) + " llistes de " + str(mida[1]) + " caselles"
            for j in taulell[i]:
                if j is None:
                    return False, "La taulell hauria de ser una llista de " + str(mida[0]) + " llistes de " + str(mida[1]) + " caselles"
        return True, None

    def es_meta(self) -> bool:
        taulell = self.taulell
        def check_direccio(i, j, di, dj):
            for k in range(NUM_CASILLAS_PARA_GANAR):
                if taulell[i + (k * di)][j + (k * dj)] != CASILLA_GANADORA:
                    return False
            return True
        # Iterar a través de todas las celdas de la matriz
        filas = len(taulell)
        for i in range(filas):
            columnas = len(taulell[i])
            for j in range(columnas):
                if taulell[i][j] == CASILLA_GANADORA:
                    # Verificar las cuatro direcciones posibles: horizontal, vertical, diagonal descendente y diagonal ascendente
                    for di, dj in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        # Comprobar si es posible encontrar NUM_CASILLAS_PARA_GANAR casillas en esa dirección
                        if (0 <= i + (NUM_CASILLAS_PARA_GANAR - 1) * di < filas and
                            0 <= j + (NUM_CASILLAS_PARA_GANAR - 1) * dj < columnas):
                            # Utilizar la función auxiliar para verificar si hay una línea ganadora en esa dirección
                            if check_direccio(i, j, di, dj):
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
                if self.taulell[i][j] == CASILLA_LIBRE:
                    taulell = [fila[:] for fila in self.taulell] # copia de valores, no de referencia
                    taulell[i][j] = CASILLA_GANADORA #.posar(CASILLA_GANADORA)
                    acc = self.accions_previes[:]
                    acc.append((Accio.POSAR, (i, j)))
                    nou_estat = Estat(self.mida, taulell, acc)
                    if nou_estat.legal()[0]:
                        estats_generats.append(nou_estat)
        return estats_generats

    def __str__(self):
        return (f"taulell: \"{self.taulell}\" | Accio {self.accions_previes}")



