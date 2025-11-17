import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from game.tablero import Tablero

# -------------------------
#     TESTS resaltar_celda
# -------------------------

def test_resaltar_celda():
    tablero = Tablero()

    tablero.resaltar_celda(2, 3)

    celda = tablero.celdas[2][3]
    estilo = celda.styleSheet()

    assert "#123456" in estilo   # Fuerza el fallo


def test_resaltar_celda_no_colorea_otras():
    tablero = Tablero()

    tablero.resaltar_celda(1, 1)
    celda_no_sel = tablero.celdas[3][4]
    estilo = celda_no_sel.styleSheet()

    assert "#ffcc00" not in estilo, "Otra celda quedó resaltada cuando no debía."


def test_resaltar_celda_celdas_rojas_persisten():
    tablero = Tablero()

    tablero.fila_roja(0)
    tablero.resaltar_celda(4, 2)

    celda_roja = tablero.celdas[0][3]

    assert "#940901" in celda_roja.styleSheet(), "La celda roja perdió su estilo después del resaltado."


# -------------------------
#       TESTS keyPressEvent
# -------------------------

def simulate_key(widget, key):
    """Envía un evento de teclado artificial al widget."""
    event = QKeyEvent(QKeyEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier)
    widget.keyPressEvent(event)

# --- Test movimiento hacia abajo ---
def test_keyPressEvent_abajo():
    tablero = Tablero()
    simulate_key(tablero, Qt.Key.Key_Down)

    assert tablero.sel_fila == 1, "La tecla abajo no movió la selección correctamente."


# --- Test movimiento a la izquierda ---
def test_keyPressEvent_izquierda_no_sale_de_limites():
    tablero = Tablero()

    tablero.sel_fila = 3
    tablero.sel_columna = 0

    simulate_key(tablero, Qt.Key.Key_Left)

    assert tablero.sel_columna == 0, "La selección salió del borde izquierdo."


# --- Test tecla Z imprime celda (y no cambia selección) ---
def test_keyPressEvent_tecla_Z_no_mueve():
    tablero = Tablero()

    tablero.sel_fila = 2
    tablero.sel_columna = 4

    simulate_key(tablero, Qt.Key.Key_Z)

    assert tablero.sel_fila == 2 and tablero.sel_columna == 4, \
        "La tecla Z debería no cambiar la selección."
def test_dummy():
    assert True
