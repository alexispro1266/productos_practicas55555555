from flask import Flask, render_template_string, request, redirect
import pandas as pd
import webbrowser
import threading
import os

app = Flask(__name__)
excel_file = "registro_productos.xlsx"

@app.route("/", methods=["GET", "POST"])
def ver_registros():
    # Leer el archivo si existe, si no crear uno vacío con columnas
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
    else:
        df = pd.DataFrame(columns=["ID", "Producto", "Categoría", "Precio"])
        df.to_excel(excel_file, index=False)

    if request.method == "POST":
        try:
            nuevo_registro = {
                "ID": int(request.form["ID"]),
                "Producto": request.form["Producto"],
                "Categoría": request.form["Categoría"],
                "Precio": float(request.form["Precio"])
            }

            df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
            df.to_excel(excel_file, index=False)
            return redirect("/")
        
        except Exception as e:
            return f"<h1>Error procesando el formulario:</h1><pre>{e}</pre>"

    columnas = df.columns.tolist()
    tabla_html = df.to_html(classes='table table-bordered', index=False)

    html = f"""
    <!doctype html>
    <html>
    <head>
        <title>Registros del Excel</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
        <style>
            body {{ padding: 30px; font-family: Arial, sans-serif; }}
        </style>
    </head>
    <body>
        <h2>Columnas del archivo Excel</h2>
        <ul>
            {''.join(f'<li>{col}</li>' for col in columnas)}
        </ul>

        <h2 class="mt-4">Contenido actual del archivo</h2>
        {tabla_html}

        <h2 class="mt-5">Agregar nuevo registro</h2>
        <form method="POST">
            <div class="form-group">
                <label>ID:</label>
                <input type="number" name="ID" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Producto:</label>
                <input type="text" name="Producto" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Categoría:</label>
                <input type="text" name="Categoría" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Precio:</label>
                <input type="number" step="0.01" name="Precio" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Guardar</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

def abrir_navegador():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1, abrir_navegador).start()
    app.run()





