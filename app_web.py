from werkzeug.utils import secure_filename
import os
from pathlib import Path
import sys
from flask import Flask, render_template, request, send_file, jsonify

from database import create_database, save_report
from ppt_generator import generate_ppt
from ppt_generator_en import generate_ppt_en

from gemini_service import (
    analisar_acao,
    traduzir_relatorio
)
def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static")
)

# ==============================
# Configurações
# ==============================

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("reports", exist_ok=True)

create_database()


# ==============================
# Página inicial
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# Página do relatório
# ==============================

@app.route("/report")
def report():
    return render_template("report.html")


# ==============================
# Download do PowerPoint
# ==============================

from pathlib import Path

@app.route("/download/<filename>")
def download(filename):

    reports_folder = Path.home() / "Documents" / "Quality Reports"

    file_path = reports_folder / filename

    return send_file(
        str(file_path),
        as_attachment=True
    )

# ==============================
# Análise com IA
# ==============================

@app.route("/analisar", methods=["POST"])
def analisar():

    data = request.get_json()

    model = data.get("model")
    line = data.get("line")
    process = data.get("process")
    category = data.get("category")
    defect = data.get("defect")
    cause = data.get("cause")

    action = analisar_acao(
        model=model,
        line=line,
        process=process,
        category=category,
        defect=defect,
        cause=cause
    )

    return jsonify({
        "action": action
    })

# ==============================
# EXPORTAR POWERPOINT EM INGLÊS
# ==============================

@app.route("/export_en", methods=["POST"])
def export_en():

    model = request.form.get("model")
    line = request.form.get("line")
    process = request.form.get("process")
    date = request.form.get("date")
    qty_defect = request.form.get("qty_defect")
    category = request.form.get("category")
    defect = request.form.get("defect")
    cause = request.form.get("cause")
    action = request.form.get("action")
    pic = request.form.get("pic")

    image_path = ""

    if "photo" in request.files:

        photo = request.files["photo"]

        if photo.filename != "":

            filename = secure_filename(photo.filename)

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            photo.save(image_path)

    dados = traduzir_relatorio(
        model=model,
        line=line,
        process=process,
        category=category,
        defect=defect,
        cause=cause,
        action=action,
        pic=pic
    )

    ppt_file = generate_ppt_en(
        model=dados["model"],
        line=dados["line"],
        process=dados["process"],
        date=date,
        qty_defect=qty_defect,
        category=dados["category"],
        defect=dados["defect"],
        cause=dados["cause"],
        action=dados["action"],
        pic=dados["pic"],
        image_path=image_path
    )


    return send_file(
        ppt_file,
        as_attachment=True
    )

# ==============================
# SALVAR RELATÓRIO
# ==============================   

@app.route("/save", methods=["POST"])
def save():

    model = request.form.get("model")
    line = request.form.get("line")
    process = request.form.get("process")
    date = request.form.get("date")
    qty_defect = request.form.get("qty_defect")
    category = request.form.get("category")
    defect = request.form.get("defect")
    cause = request.form.get("cause")
    action = request.form.get("action")
    pic = request.form.get("pic")

    image_path = ""

    if "photo" in request.files:

        photo = request.files["photo"]

        if photo.filename != "":

            filename = secure_filename(photo.filename)

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            photo.save(image_path)
            print("Imagem salva em:", image_path)
            print("Existe?", os.path.exists(image_path))

    save_report(
        model,
        line,
        process,
        date,
        qty_defect,
        category,
        defect,
        cause,
        action,
        pic,
        image_path
    )

    ppt_file = generate_ppt(
        model=model,
        line=line,
        process=process,
        date=date,
        qty_defect=qty_defect,
        category=category,
        defect=defect,
        cause=cause,
        action=action,
        pic=pic,
        image_path=image_path
    )

    filename = os.path.basename(ppt_file)

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Quality Anomaly</title>

        <style>

            body{{
                font-family:Arial;
                text-align:center;
                background:#f2f4f7;
                margin-top:60px;
            }}

            .box{{
                width:700px;
                margin:auto;
                background:white;
                padding:30px;
                border-radius:12px;
                box-shadow:0px 0px 15px rgba(0,0,0,.15);
            }}

            button{{
                background:#005baa;
                color:white;
                border:none;
                border-radius:8px;
                padding:15px 35px;
                font-size:18px;
                cursor:pointer;
            }}

            button:hover{{
                background:#003f7f;
            }}

        </style>

    </head>

    <body>

        <div class="box">

            <h2>PowerPoint gerado com sucesso!</h2>

<br>

<a href="/download/{filename}">
    <button>
        📥 Exportar PowerPoint (PT)
    </button>
</a>

<br><br>

<form action="/export_en"
      method="POST"
      enctype="multipart/form-data">

    <input type="hidden" name="model" value="{model}">
    <input type="hidden" name="line" value="{line}">
    <input type="hidden" name="process" value="{process}">
    <input type="hidden" name="date" value="{date}">
    <input type="hidden" name="qty_defect" value="{qty_defect}">
    <input type="hidden" name="category" value="{category}">
    <input type="hidden" name="defect" value="{defect}">
    <input type="hidden" name="cause" value="{cause}">
    <input type="hidden" name="action" value="{action}">
    <input type="hidden" name="pic" value="{pic}">

    <button type="submit">
        🌎 Exportar PowerPoint (EN)
    </button>

</form>

<br><br>

<a href="/report">
    <button>
        Novo Relatório
    </button>
</a>

        </div>

    </body>

    </body>

    </html>
    """

# ==============================
# Executar aplicação
# ==============================


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )