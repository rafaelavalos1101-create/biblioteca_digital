# app.py
# Sistema de la Biblioteca Digital de Instrucciones de Impresos Múltiples.
# Permite registrar, consultar, modificar y eliminar instrucciones de trabajo,
# y muestra un resumen de cuántas están vigentes y cuántas desactualizadas.

import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def conectar():
    # Abre la base de datos y permite leer las columnas por su nombre
    conexion = sqlite3.connect("biblioteca.db")
    conexion.row_factory = sqlite3.Row
    return conexion


def es_numero_valido(texto):
    # Revisa que el texto sea un número entero mayor que cero (1, 2, 3...)
    return texto.isdigit() and int(texto) > 0


def revisar_estado(version, version_aprobada):
    # Decide el estado de UNA instrucción comparando sus versiones
    if version == version_aprobada:
        return "Vigente"
    elif version < version_aprobada:
        return "Desactualizada"
    else:
        return "Por revisar"


@app.route("/")
def inicio():
    return redirect("/instrucciones")


# ---------- CONSULTAR ----------
@app.route("/instrucciones")
def listar():
    conexion = conectar()
    filas = conexion.execute("SELECT * FROM instrucciones ORDER BY codigo").fetchall()
    conexion.close()

    # Armamos una lista con cada instrucción y su estado
    instrucciones = []
    for fila in filas:
        estado = revisar_estado(fila["version"], fila["version_aprobada"])
        instrucciones.append({"datos": fila, "estado": estado})

    return render_template("instrucciones.html", instrucciones=instrucciones)


# ---------- REGISTRAR ----------
@app.route("/instrucciones/nueva", methods=["GET", "POST"])
def nueva():
    error = ""
    datos = {"codigo": "", "nombre": "", "area": "", "version": "", "version_aprobada": ""}

    if request.method == "POST":
        datos["codigo"] = request.form["codigo"].strip().upper()
        datos["nombre"] = request.form["nombre"].strip()
        datos["area"] = request.form["area"].strip()
        datos["version"] = request.form["version"].strip()
        datos["version_aprobada"] = request.form["version_aprobada"].strip()

        # Validación: nada vacío y versiones con números enteros mayores que 0
        if datos["codigo"] == "" or datos["nombre"] == "" or datos["area"] == "":
            error = "El código, el nombre y el área no pueden quedar vacíos."
        elif not es_numero_valido(datos["version"]) or not es_numero_valido(datos["version_aprobada"]):
            error = "Las versiones deben ser números enteros mayores que 0 (por ejemplo 1, 2 o 3)."
        else:
            conexion = conectar()
            # Revisamos que el código no esté repetido
            repetido = conexion.execute(
                "SELECT id FROM instrucciones WHERE codigo = ?", (datos["codigo"],)
            ).fetchone()
            if repetido:
                error = "Ya existe una instrucción con el código " + datos["codigo"] + "."
                conexion.close()
            else:
                conexion.execute(
                    "INSERT INTO instrucciones (codigo, nombre, area, version, version_aprobada, fecha_actualizacion) VALUES (?, ?, ?, ?, ?, ?)",
                    (datos["codigo"], datos["nombre"], datos["area"],
                     int(datos["version"]), int(datos["version_aprobada"]), str(date.today())),
                )
                conexion.commit()
                conexion.close()
                return redirect("/instrucciones")

    return render_template("nueva.html", error=error, datos=datos)


# ---------- MODIFICAR ----------
@app.route("/instrucciones/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexion = conectar()
    instruccion = conexion.execute("SELECT * FROM instrucciones WHERE id = ?", (id,)).fetchone()

    if instruccion is None:
        conexion.close()
        return redirect("/instrucciones")

    error = ""
    if request.method == "POST":
        version = request.form["version"].strip()
        version_aprobada = request.form["version_aprobada"].strip()

        if not es_numero_valido(version) or not es_numero_valido(version_aprobada):
            error = "Las versiones deben ser números enteros mayores que 0 (por ejemplo 1, 2 o 3)."
        else:
            conexion.execute(
                "UPDATE instrucciones SET version = ?, version_aprobada = ?, fecha_actualizacion = ? WHERE id = ?",
                (int(version), int(version_aprobada), str(date.today()), id),
            )
            conexion.commit()
            conexion.close()
            return redirect("/instrucciones")

    conexion.close()
    return render_template("editar.html", instruccion=instruccion, error=error)


# ---------- ELIMINAR ----------
@app.route("/instrucciones/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = conectar()
    conexion.execute("DELETE FROM instrucciones WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()
    return redirect("/instrucciones")


# ---------- RESUMEN (repetición y decisión) ----------
@app.route("/resumen")
def resumen():
    conexion = conectar()
    filas = conexion.execute("SELECT * FROM instrucciones ORDER BY codigo").fetchall()
    conexion.close()

    # Contadores: empiezan en cero
    vigentes = 0
    desactualizadas = 0
    por_revisar = 0
    detalle = []

    # Recorremos TODAS las instrucciones, una por una
    for fila in filas:
        if fila["version"] == fila["version_aprobada"]:
            estado = "Vigente"
            vigentes = vigentes + 1
        elif fila["version"] < fila["version_aprobada"]:
            estado = "Desactualizada"
            desactualizadas = desactualizadas + 1
        else:
            estado = "Por revisar"
            por_revisar = por_revisar + 1
        detalle.append({"datos": fila, "estado": estado})

    total = len(filas)
    return render_template(
        "resumen.html",
        vigentes=vigentes,
        desactualizadas=desactualizadas,
        por_revisar=por_revisar,
        total=total,
        detalle=detalle,
    )


if __name__ == "__main__":
    app.run(debug=True)

//RESUMEN ETC
