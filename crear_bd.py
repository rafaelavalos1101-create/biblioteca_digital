# crear_bd.py
# Este archivo crea la base de datos "biblioteca.db", crea la tabla
# de instrucciones y guarda 6 instrucciones de ejemplo.
# Se ejecuta una sola vez antes de abrir el sistema: python crear_bd.py

import sqlite3

conexion = sqlite3.connect("biblioteca.db")

# Si la tabla ya existe la borramos, así siempre empezamos con datos limpios
conexion.execute("DROP TABLE IF EXISTS instrucciones")

# Tabla principal: cada fila es una instrucción de trabajo
# version          = la versión que está guardada en la biblioteca
# version_aprobada = la última versión que aprobó el área de calidad
conexion.execute("""
    CREATE TABLE instrucciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL,
        nombre TEXT NOT NULL,
        area TEXT NOT NULL,
        version INTEGER NOT NULL,
        version_aprobada INTEGER NOT NULL,
        fecha_actualizacion TEXT NOT NULL
    )
""")

# Datos de ejemplo (código, nombre, área, versión, versión aprobada, fecha)
ejemplos = [
    ("IT-001", "Calibración de la impresora offset", "Impresión", 3, 3, "2026-09-10"),
    ("IT-002", "Corte de papel en guillotina", "Acabados", 1, 2, "2026-03-15"),
    ("IT-003", "Mezcla de tintas Pantone", "Preprensa", 2, 2, "2026-08-22"),
    ("IT-004", "Limpieza de rodillos", "Mantenimiento", 1, 3, "2025-11-05"),
    ("IT-005", "Empaque de pedidos", "Despacho", 4, 4, "2026-10-01"),
    ("IT-006", "Encuadernado con grapa", "Acabados", 3, 2, "2026-07-18"),
]

for ejemplo in ejemplos:
    conexion.execute(
        "INSERT INTO instrucciones (codigo, nombre, area, version, version_aprobada, fecha_actualizacion) VALUES (?, ?, ?, ?, ?, ?)",
        ejemplo,
    )

conexion.commit()
conexion.close()
print("Base de datos creada con", len(ejemplos), "instrucciones de ejemplo.")

//ejemplos de crear computo
