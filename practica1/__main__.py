from practica1 import joc
from agent_a_estrella import AgentAestrella
from agent_minimax import AgentMiniMaxAlfaBeta
from agent_profunditat import AgentProfunditat


def main():
    #agent = joc.Taulell([AgentProfunditat("Profunditat")])
    #agent = joc.Taulell([AgentAestrella("Aestrella")])
    agent = joc.Taulell([AgentMiniMaxAlfaBeta("Jugador 1", 2), AgentMiniMaxAlfaBeta("Jugador 2", 2)])
    agent.comencar()

if __name__ == "__main__":
    main()
