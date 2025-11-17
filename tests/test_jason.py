import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
import sys
from pathlib import Path
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

# Helper necesario para unas pruebas
def simular_tecla(widget, tecla):
    event = QKeyEvent(QEvent.Type.KeyPress, tecla, Qt.KeyboardModifier.NoModifier)
    widget.keyPressEvent(event)

# Pruebas para resaltar_celda
def test_1resaltar_celda(app):
    tablero = Tablero()
    filas = tablero.filas
    columnas = tablero.columnas

    # Intentar resaltar una celda que no existe
    for _ in range(20):
        try:
            tablero.resaltar_celda(-1, 0)
        except:
            pass
        try:
            tablero.resaltar_celda(0, -1)
        except:
            pass

    # (0,0) debe seguir siendo la celda seleccionada
    fila = tablero.sel_fila
    col = tablero.sel_columna

    assert 0 <= fila < filas
    assert 0 <= col < columnas

def test_2resaltar_celda(app):
    tablero = Tablero()

    # Resaltar otra celda
    tablero.resaltar_celda(1, 0)

    estilo_resaltado = tablero.celdas[1][0].styleSheet()
    estilo_otra = tablero.celdas[0][0].styleSheet()

    # Verificar que la celda (1,0) sea la resaltada y que (0,0) no lo este
    assert "border: 3px solid #ffcc00" in estilo_resaltado
    assert "border: 3px solid #ffcc00" not in estilo_otra

def test_3resaltar_celda(app):
    tablero = Tablero()

    # Resaltar la celda (3,3), para que la prueba falle
    tablero.resaltar_celda(2, 3)

    estilo_seleccionado = tablero.celdas[2][3].styleSheet()
    estilo_normal = tablero.celdas[1][1].styleSheet()
    # Verificar si la celda (2,3) está resaltada
    assert "border: 3px solid #ffcc00" in estilo_seleccionado
    assert "border: 3px solid #ffcc00" not in estilo_normal

    # Pruebas para keyPressEvent
def test_1keyPressEvent(app):
    tablero = Tablero()

    event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier)
    tablero.keyPressEvent(event)

    # Verificar que la celda (1,0) sea la seleccionada luego de pulsar abajo
    assert tablero.sel_fila == 1
    assert tablero.sel_columna == 0

def test_2keyPressEvent():
    tablero = Tablero()

    for _ in range(99):
        simular_tecla(tablero, Qt.Key.Key_Down)

    for _ in range(99):
        simular_tecla(tablero, Qt.Key.Key_Right)

    # Verificar si la celda (8,4) es la que está en la esquina de abajo a la derecha
    assert tablero.sel_fila == 8
    assert tablero.sel_columna == 4

def test_3keyPressEvent(app, capsys):
    tablero = Tablero()
    tablero.sel_fila = 3
    tablero.sel_columna = 2

    evento = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Z, Qt.KeyboardModifier.NoModifier)
    tablero.keyPressEvent(evento)

    captured = capsys.readouterr()

    # Verificar que stdout de (3,2) al pulsar la tecla Z

    assert "(3, 2)" in captured.out


