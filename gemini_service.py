from google import genai
import json

# ==========================================
# CONFIGURAÇÃO DO GEMINI
# ==========================================

client = genai.Client(
    api_key="AQ.Ab8RN6KYsgq8fK1AqIwfQ1nIhXHXl6eUhIXqBo07JUlrSiPgbg"
)

# ==========================================
# ANÁLISE COM IA
# ==========================================

def analisar_acao(model, line, process, category, defect, cause):

    prompt = f"""
Você é um Engenheiro de Qualidade especialista na fabricação de televisores.

Analise as informações abaixo.

Modelo:
{model}

Linha:
{line}

Processo:
{process}

Categoria:
{category}

Defeito:
{defect}

Possível causa:
{cause}

Com base na análise realizada, determine a ação corretiva mais adequada para eliminar a causa do problema e evitar sua recorrência.

Responda apenas com o texto que deverá preencher o campo "Action".

Regras:

- Responda somente em português.
- Seja objetivo.
- Não utilize listas.
- Não utilize numeração.
- Não utilize títulos.
- Não explique o raciocínio.
- Escreva apenas o conteúdo do campo "Action".
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text.strip()


# ==========================================
# TRADUÇÃO PARA INGLÊS
# ==========================================

def traduzir_relatorio(
    model,
    line,
    process,
    category,
    defect,
    cause,
    action,
    pic
):

    prompt = f"""
Você é um Engenheiro de Qualidade especialista em relatórios técnicos.

Traduza todas as informações abaixo para um inglês técnico utilizado na indústria de fabricação de televisores.

Retorne SOMENTE um JSON válido.

Modelo:
{model}

Linha:
{line}

Processo:
{process}

Categoria:
{category}

Defeito:
{defect}

Causa:
{cause}

Ação:
{action}

PIC:
{pic}

Formato esperado:

{{
    "model":"",
    "line":"",
    "process":"",
    "category":"",
    "defect":"",
    "cause":"",
    "action":"",
    "pic":""
}}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        texto = response.text.strip()

        if texto.startswith("json"):
            texto = texto.replace("json", "")

        if texto.endswith(""):
            texto = texto.replace("", "")

        texto = texto.strip()

        return json.loads(texto)

    except Exception as e:

        print("Erro na tradução:", e)

        return {
            "model": model,
            "line": line,
            "process": process,
            "category": category,
            "defect": defect,
            "cause": cause,
            "action": action,
            "pic": pic
        }