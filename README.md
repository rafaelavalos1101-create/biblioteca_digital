# Biblioteca Digital de Instrucciones – Impresos Múltiples (Fase 2)

## Qué hace el sistema

Es una página web para guardar las **instrucciones de trabajo** de Impresos Múltiples y saber cuáles se pueden usar y cuáles ya están viejas.

Con el sistema se puede:

- **Registrar** una instrucción nueva.
- **Consultar** el listado de instrucciones con su versión.
- **Modificar** (actualizar) la versión de una instrucción.
- **Eliminar** una instrucción.
- Ver un **resumen** que cuenta cuántas instrucciones están vigentes, cuántas están desactualizadas y cuántas hay que revisar.

Los datos se guardan en una base de datos SQLite (`biblioteca.db`), no dentro del código.

## Cómo ejecutarlo

1. Instalar Flask (solo la primera vez):

   ```
   pip install flask
   ```

2. Crear la base de datos con los datos de ejemplo:

   ```
   python crear_bd.py
   ```

3. Abrir el sistema:

   ```
   python app.py
   ```

4. Abrir en el navegador:

   - Listado: http://127.0.0.1:5000/instrucciones
   - Registrar: http://127.0.0.1:5000/instrucciones/nueva
   - Resumen: http://127.0.0.1:5000/resumen

> Si se vuelve a ejecutar `crear_bd.py`, la base de datos se borra y vuelve a quedar con los 6 datos de ejemplo.

## Estructura de archivos

```
biblioteca_digital/
|-- app.py                 # rutas de Flask y lógica del sistema
|-- crear_bd.py            # crea la tabla y carga 6 instrucciones de ejemplo
|-- README.md              # esta documentación
|-- .gitignore             # evita subir la base de datos a GitHub
|-- templates/
|   |-- base.html          # parte común de todas las páginas (menú y hoja de estilos)
|   |-- instrucciones.html # listado de instrucciones
|   |-- nueva.html         # formulario para registrar
|   |-- editar.html        # formulario para actualizar la versión
|   |-- resumen.html       # resumen con los contadores
|-- static/
|   |-- style.css          # hoja de estilos de todo el sitio
```

## Rutas

| Ruta | Método | Qué hace |
|---|---|---|
| `/` | GET | Manda al listado de instrucciones |
| `/instrucciones` | GET | **Consultar:** muestra todas las instrucciones con su versión y su estado |
| `/instrucciones/nueva` | GET y POST | **Registrar:** GET muestra el formulario, POST valida y guarda |
| `/instrucciones/editar/<id>` | GET y POST | **Modificar:** GET muestra el formulario, POST valida y actualiza la versión |
| `/instrucciones/eliminar/<id>` | POST | **Eliminar:** borra la instrucción (antes pide confirmación) |
| `/resumen` | GET | Recorre todas las instrucciones, las clasifica y las cuenta |

Todas las sentencias SQL usan `?` para los datos. Así el texto que escribe el usuario nunca se mete directo dentro de la sentencia.

| Mantenimiento | Sentencia SQL |
|---|---|
| Registrar | `INSERT INTO instrucciones (codigo, nombre, area, version, version_aprobada, fecha_actualizacion) VALUES (?, ?, ?, ?, ?, ?)` |
| Consultar | `SELECT * FROM instrucciones ORDER BY codigo` |
| Modificar | `UPDATE instrucciones SET version = ?, version_aprobada = ?, fecha_actualizacion = ? WHERE id = ?` |
| Eliminar | `DELETE FROM instrucciones WHERE id = ?` |

## Base de datos

Archivo: `biblioteca.db` · Tabla: `instrucciones`

| Campo | Tipo | Qué guarda |
|---|---|---|
| `id` | INTEGER | Número único de cada fila (se pone solo) |
| `codigo` | TEXT | Código de la instrucción, por ejemplo IT-001 (no se puede repetir) |
| `nombre` | TEXT | Nombre de la instrucción |
| `area` | TEXT | Área de la empresa que la usa (Impresión, Acabados, etc.) |
| `version` | INTEGER | Versión que está guardada en la biblioteca |
| `version_aprobada` | INTEGER | Última versión que aprobó el área de calidad |
| `fecha_actualizacion` | TEXT | Fecha del último cambio |

## Validaciones de los formularios

Antes de guardar, el programa revisa los datos. Si algo está mal, muestra un mensaje en rojo y **no guarda**:

- El código, el nombre y el área no pueden quedar vacíos.
- Las dos versiones tienen que ser números enteros mayores que 0 (1, 2, 3...). Si se escribe "dos", "0" o "-1", sale error.
- No se puede registrar un código que ya existe.

Si todo está bien, guarda y regresa al listado.

## Cómo funciona el resumen

La ruta `/resumen` hace esto:

1. Lee **todas** las instrucciones de la base de datos.
2. Pone tres contadores en cero: `vigentes`, `desactualizadas` y `por_revisar`.
3. Con un `for` recorre las instrucciones una por una.
4. En cada vuelta compara la versión guardada con la versión aprobada usando `if / elif / else`:
   - **if** son iguales → la instrucción está **Vigente** (se puede usar) → suma 1 a `vigentes`.
   - **elif** la guardada es menor → está **Desactualizada** (hay una más nueva) → suma 1 a `desactualizadas`.
   - **else** (la guardada es mayor que la aprobada) → **Por revisar**, porque es una versión que calidad todavía no aprobó → suma 1 a `por_revisar`.
5. Muestra en pantalla cuántas hay de cada tipo, cada una con su color: verde (vigente), rojo (desactualizada) y amarillo (por revisar).

```python
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
```

## Estilos

Todas las páginas usan una sola hoja de estilos: `static/style.css`. Se enlaza una vez en `templates/base.html` y las demás páginas heredan esa parte con `{% extends "base.html" %}`, así ninguna página repite estilos.

## Equipo: parte de código desarrollada por cada integrante

- **Integrante 1 (nombre):** conexión a la base de datos y `crear_bd.py`.
- **Integrante 2 (nombre):** registrar instrucción con validación (`/instrucciones/nueva`, `nueva.html`).
- **Integrante 3 (nombre):** listado, modificar y eliminar (`/instrucciones`, `/instrucciones/editar`, `/instrucciones/eliminar`).
- **Integrante 4 (nombre):** resumen con el `for`, las decisiones y los contadores (`/resumen`, `resumen.html`).
- **Integrante 5 (nombre):** hoja de estilos `style.css` y `base.html`.
