from practica1 import joc
from agent_a_estrella import AgentAestrella
from agent_minimax import AgentMiniMaxAlfaBeta
from agent_profunditat import AgentProfunditat
DEBUG = True

def main():
    #agents = [AgentProfunditat("Profunditat")]
    agents = [AgentAestrella("Aestrella")]
    #agents = [AgentMiniMaxAlfaBeta("Jugador 1", 2), AgentMiniMaxAlfaBeta("Jugador 2", 2)]
    quatre = joc.Taulell(agents)
    if DEBUG:
        for a in agents:
            print(str(a.nom) + ": " + str(a.jugador))
    quatre.comencar()

if __name__ == "__main__":
    main()

