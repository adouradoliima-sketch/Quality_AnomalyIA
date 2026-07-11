import sqlite3
import os

# ==========================================
# CONFIGURAÇÃO DO BANCO
# ==========================================

DATABASE_FOLDER = "database"
DATABASE_NAME = os.path.join(DATABASE_FOLDER, "quality_anomaly.db")


# ==========================================
# CRIAR BANCO
# ==========================================

def create_database():

    os.makedirs(DATABASE_FOLDER, exist_ok=True)

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        model TEXT,
        line TEXT,
        process TEXT,
        report_date TEXT,
        qty_defect TEXT,
        category TEXT,
        defect TEXT,
        cause TEXT,
        action TEXT,
        pic TEXT,
        image_path TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# ==========================================
# SALVAR RELATÓRIO
# ==========================================

def save_report(
    model,
    line,
    process,
    report_date,
    qty_defect,
    category,
    defect,
    cause,
    action,
    pic,
    image_path
):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports(

            model,
            line,
            process,
            report_date,
            qty_defect,
            category,
            defect,
            cause,
            action,
            pic,
            image_path

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?)
    """, (

        model,
        line,
        process,
        report_date,
        qty_defect,
        category,
        defect,
        cause,
        action,
        pic,
        image_path

    ))

    conn.commit()
    conn.close()


# ==========================================
# LISTAR RELATÓRIOS
# ==========================================

def get_reports():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reports
        ORDER BY id DESC
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados