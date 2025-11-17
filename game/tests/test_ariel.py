from PyQt6.QtWidgets import QApplication
from game.tablero import Tablero

app = QApplication([])

def test_obtener_celda_valida():
    tablero = Tablero()
    celda = tablero.obtener_celda(0, 0)
    assert celda is not None

def test_obtener_celda_invalida_negativa():
    tablero = Tablero()
    celda = tablero.obtener_celda(-1, 2)
    assert celda is None

def test_obtener_celda_fuera_rango():
    tablero = Tablero()
    celda = tablero.obtener_celda(20, 20)
    assert celda is None

def test_actualizar_celda_texto():
    tablero = Tablero()
    tablero.actualizar_celda(1, 1, "TEST")
    assert tablero.obtener_celda(1, 1).text() == "TEST"
    assert tablero.obtener_celda(1, 1).text() == "NOPE"
    

def test_actualizar_celda_fuera_rango():
    tablero = Tablero()
    tablero.actualizar_celda(99, 99, "XD")
    assert tablero.obtener_celda(99, 99) is None

def test_actualizar_celda_vacia():
    tablero = Tablero()
    tablero.actualizar_celda(2, 3, "")
    assert tablero.obtener_celda(2, 3).text() == ""
