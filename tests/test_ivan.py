import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from pathlib import Path
import sys
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, QEvent

# importar el tablero
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from game.tablero import Tablero

@pytest.fixture(scope="session")
def app():
    return QApplication([])

## pruebas
# resaltar_celda
def test_1resaltar_celda(app):
    tablero = Tablero()

    # Resaltar la celda (2,3)
    tablero.resaltar_celda(2, 3)

    estilo_seleccionado = tablero.celdas[2][3].styleSheet()
    estilo_normal = tablero.celdas[1][1].styleSheet()

    assert "border: 3px solid #ffcc00" in estilo_seleccionado   # resaltado
    assert "border: 3px solid #ffcc00" not in estilo_normal     # no resaltado

def test_2resaltar_celda(app):
    tablero = Tablero()

    # Resaltar otra celda
    tablero.resaltar_celda(1, 0)

    estilo_resaltado = tablero.celdas[1][0].styleSheet()
    estilo_otra = tablero.celdas[0][0].styleSheet()

    # La celda (1,0) debe estar resaltada
    assert "border: 3px solid #ffcc00" in estilo_resaltado

    # Y la celda (0,0) ya NO debe estar resaltada (salvo que sea roja, pero no lo es)
    assert "border: 3px solid #ffcc00" not in estilo_otra

def test_3resaltar_celda(app):
    tablero = Tablero()
    filas = tablero.filas
    columnas = tablero.columnas

    # Llamadas con coordenadas inválidas — no deben romper nada.
    for _ in range(20):
        try:
            tablero.resaltar_celda(-1, 0)    # fila inválida
        except:
            pass

        try:
            tablero.resaltar_celda(0, -1)    # col inválida
        except:
            pass

    # La selección REAL del widget sigue siendo (0,0)
    fila = tablero.sel_fila
    col = tablero.sel_columna

    assert 0 <= fila < filas
    assert 0 <= col < columnas

# keyPressEvent
def test_1keyPressEvent(app):
    tablero = Tablero()

    assert tablero.sel_fila == 0
    assert tablero.sel_columna == 0

    event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier)
    tablero.keyPressEvent(event)

    assert tablero.sel_fila == 1
    assert tablero.sel_columna == 0

def test_2keyPressEvent(app, capsys):
    tablero = Tablero()
    tablero.sel_fila = 3
    tablero.sel_columna = 2

    evento = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Z, Qt.KeyboardModifier.NoModifier)
    tablero.keyPressEvent(evento)

    captured = capsys.readouterr()

    assert "(3, 2)" in captured.out

# No es una prueba, pero es necesario para la siguiente prueba
def simular_tecla(widget, tecla):
    event = QKeyEvent(QEvent.Type.KeyPress, tecla, Qt.KeyboardModifier.NoModifier)
    widget.keyPressEvent(event)

def test_3keyPressEvent():
    tablero = Tablero()

    for _ in range(8):
        simular_tecla(tablero, Qt.Key.Key_Down)

    for _ in range(4):
        simular_tecla(tablero, Qt.Key.Key_Right)

    assert tablero.sel_fila == 8
    assert tablero.sel_columna == 4
