import sys, platform
from practica1 import agent, joc
P = platform.system()
if P == 'Windows': sys.path.append('C:\\Users\\jartu\\Documents\\GitHub\\IA1') # path de arturo
elif P == 'Darwin': pass#sys.path.append('C:\\Users\\jartu\\Documents\\GitHub\\IA1') # path de marta




def main():
    quatre = joc.Taulell([agent.Agent("Miquel")])
    quatre.comencar()


if __name__ == "__main__":
    main()
