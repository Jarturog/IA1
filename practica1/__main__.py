import sys, platform
P = platform.system()
if P == 'Windows': sys.path.append('C:\\Users\\jartu\\Documents\\GitHub\\IA1') # path vscode arturo
from practica1 import agent, joc#, agent_a_estrella, agent_minimax, agent_profunditat
from agent_a_estrella import AgentAestrella
from agent_minimax import AgentMiniMaxAlfaBeta
from agent_profunditat import AgentProfunditat


def main():
    #quatre = joc.Taulell([agent.Agent("Iker")]) # arturo y marta??? pq quatre?
    #a = joc.Taulell([AgentAestrella("Aestrella")])
    #min = joc.Taulell([AgentMiniMaxAlfaBeta("Min")])
    #max = joc.Taulell([AgentMiniMaxAlfaBeta("Max")])
    p = joc.Taulell([AgentProfunditat("Profunditat")])
    p.comencar()
    #quatre.comencar()

if __name__ == "__main__":
    main()
