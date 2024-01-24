from practica1 import joc
from agent_a_estrella import AgentAestrella
from agent_minimax import AgentMiniMaxAlfaBeta
from agent_profunditat import AgentProfunditat
DEBUG = True

def main():
    #agents = [AgentProfunditat("Profunditat")]
    #agents = [AgentAestrella("Aestrella")]
    agents = [AgentMiniMaxAlfaBeta("Jugador 1", 2), AgentMiniMaxAlfaBeta("Jugador 2", 2)]
    quatre = joc.Taulell(agents)
    if DEBUG:
        print(str(agents[0].nom) + ": " + str(agents[0].jugador))
        print(str(agents[1].nom) + ": " + str(agents[1].jugador))
    quatre.comencar()

if __name__ == "__main__":
    main()

