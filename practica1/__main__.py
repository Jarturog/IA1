from practica1 import joc
from agent_a_estrella import AgentAestrella
from agent_minimax import AgentMiniMaxAlfaBeta
from agent_profunditat import AgentProfunditat


def main():
    agents = [AgentProfunditat("Profunditat")]
    #agents = [AgentAestrella("Aestrella")]
    #agents = [AgentMiniMaxAlfaBeta("Jugador 1", 2), AgentMiniMaxAlfaBeta("Jugador 2", 2)]
    #agents = [AgentMiniMaxAlfaBeta("Jugador 1 iteratiu", 2, True), AgentMiniMaxAlfaBeta("Jugador 2 iteratiu", 2, True)]
    quatre = joc.Taulell(agents)
    quatre.comencar()

if __name__ == "__main__":
    main()
