import json
import google.auth
from google.auth.credentials import Credentials
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# ==========================================
# CONFIGURAÇÃO DO GEMINI (VERTEX AI NATIVO)
# ==========================================

CHAVE_VERTEX = "AQ.Ab8RN6IbaHdPSJkBaz12rEgfMg2RWJKv7y1T6V4YyUElfPI3eQ"

# Cria uma credencial compatível com o SDK injetando o token Bearer corporativo
class VertexTokenCredentials(Credentials):
    def __init__(self, token):
        super().__init__()
        self.token = token
        
    @property
    def valid(self):
        # Retorna sempre True para passar na validação interna do Google Auth
        return True

    def refresh(self, request):
        pass
        
    def apply(self, headers, token=None):
        headers['Authorization'] = f'Bearer {self.token}'

credenciais = VertexTokenCredentials(CHAVE_VERTEX)

# Inicializa o ambiente usando a nossa credencial e apontando para o projeto do GCP
# IMPORTANTE: Altere 'seu-projeto-gcp-id' para o ID real do seu projeto no Google Cloud
vertexai.init(
    project="gen-lang-client-0204322035", 
    location="us-central1", 
    credentials=credenciais
)

# Instancia o modelo estável do Gemini no ecossistema corporativo
model_vertex = GenerativeModel("gemini-2.5-flash")


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
- Seja objective.
- Não utilize listas.
- Não utilize numeração.
- Não utilize títulos.
- Não explique o raciocínio.
- Escreva apenas o conteúdo do campo "Action".
"""

    response = model_vertex.generate_content(prompt)
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

Retorne obrigatoriamente um JSON puro e válido.

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
"""

    try:
        # Configura a Vertex AI para responder forçadamente em formato JSON
        response = model_vertex.generate_content(
            prompt,
            generation_config=GenerationConfig(response_mime_type="application/json")
        )

        return json.loads(response.text.strip())

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
