from lang.builtins import *
from lang.state import state

def PonerN(cantidad, color):
    for i in range(cantidad):
        Poner(color)




def DibujarLinea(lado, color, d):
    for i in range(lado - 1):
        Poner(color)
        Mover(d)
    Poner(color)

def Cuadrado(lado, color):
    direc = minDir()
    for i in range(4):
        DibujarLinea(lado, color, direc)
        direc = siguiente(direc)

VaciarTablero()
PonerN(200, Rojo)
Cuadrado(4, Verde)



print(state.board)
