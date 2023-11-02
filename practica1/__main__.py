from practica1 import joc
from agent_a_estrella import AgentAestrella
from agent_minimax import AgentMiniMaxAlfaBeta
from agent_profunditat import AgentProfunditat


def main():
    #agents = [AgentProfunditat("Profunditat")]
    #agents = [AgentAestrella("Aestrella")]
    agents = [AgentMiniMaxAlfaBeta("Jugador 1", 2), AgentMiniMaxAlfaBeta("Jugador 2", 2)]
    quatre = joc.Taulell(agents)
    quatre.comencar()

if __name__ == "__main__":
    main()
