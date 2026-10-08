import os
import streamlit as st
from groq import Groq

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CareerDev AI - Mentor de Carreira Tech",
    page_icon="🚀",
    layout="centered"
)


# -----------------------------------------------------------------------------
# CARREGAMENTO DO PROMPT EXTERNO
# -----------------------------------------------------------------------------
@st.cache_data
def load_prompt(file_path: str) -> str:
    """Lê e retorna o conteúdo de um arquivo de texto/markdown com cache."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"❌ Erro: O arquivo de prompt não foi encontrado no caminho `{file_path}`.")
        st.info("Certifique-se de criar a pasta `prompts/` e o arquivo `system_prompt.md` na raiz do projeto.")
        return ""
    except Exception as e:
        st.error(f"❌ Erro ao ler o arquivo de prompt: {e}")
        return ""


# Caminho relativo para o arquivo de prompt
PROMPT_PATH = "system_prompt.md"
SYSTEM_PROMPT = load_prompt(PROMPT_PATH)


# -----------------------------------------------------------------------------
# CABEÇALHO DA INTERFACE
# -----------------------------------------------------------------------------
st.title("🚀 CareerDev AI")
st.subheader("Seu mentor inteligente para ingressar no mercado de Tecnologia")


# -----------------------------------------------------------------------------
# GERENCIAMENTO DE CHAVE DA API (GROQ)
# -----------------------------------------------------------------------------
# Tenta obter a chave primeiro do ambiente e depois do st.secrets de forma segura
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    try:
        groq_api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        groq_api_key = None

# Fallback visual caso a chave não esteja definida nas variáveis de ambiente/secrets
if not groq_api_key:
    st.warning("⚠️ Chave de API da Groq não detectada automaticamente.")
    groq_api_key = st.text_input(
        "Insira sua API Key da Groq para testar localmente:",
        type="password",
        help="Crie uma chave gratuita no site console.groq.com"
    )


# -----------------------------------------------------------------------------
# FORMULÁRIO DE ENTRADA DO USUÁRIO
# -----------------------------------------------------------------------------
with st.form("user_profile_form"):
    st.write("### 📋 Conte-nos sobre seus objetivos")

    area = st.selectbox(
        "Qual área da tecnologia você deseja focar?",
        [
            "Desenvolvimento Web Front-End",
            "Desenvolvimento Web Back-End (Python / Node.js)",
            "Desenvolvimento Full-Stack",
            "Ciência / Análise de Dados",
            "Engenharia de Software (Geral)",
            "Mobile (React Native / Flutter / Android)",
            "DevOps & Nuvem"
        ]
    )

    nivel = st.select_slider(
        "Qual o seu nível atual de conhecimento?",
        options=["Iniciante do zero", "Básico (já fiz alguns cursos)", "Intermediário (tenho pequenos projetos)", "Avançado"]
    )

    horas_semana = st.number_input(
        "Quantas horas semanais você pode dedicar aos estudos?",
        min_value=2,
        max_value=60,
        value=10
    )

    objetivo_detalhado = st.text_area(
        "Descreva brevemente suas principais dúvidas ou o tipo de vaga que busca:",
        placeholder="Ex: Quero conseguir meu primeiro estágio como Dev Python nos próximos 6 meses. Já sei lógica e SQL, mas não sei o que estudar depois...",
        height=120
    )

    submitted = st.form_submit_button("🚀 Gerar Plano de Carreira com IA")


# -----------------------------------------------------------------------------
# PROCESSAMENTO E CHAMADA À API DA GROQ
# -----------------------------------------------------------------------------
if submitted:
    if not groq_api_key:
        st.error("Por favor, insira uma API Key válida da Groq para prosseguir.")
    elif not SYSTEM_PROMPT:
        st.error("Não foi possível carregar o System Prompt. Verifique se o arquivo `prompts/system_prompt.md` existe.")
    elif not objetivo_detalhado.strip():
        st.error("Por favor, preencha o campo detalhando seu objetivo de carreira.")
    else:
        try:
            # Inicializa o cliente Groq
            client = Groq(api_key=groq_api_key)

            # Estruturação da mensagem fornecida pelo usuário
            user_message = f"""
            --- DADOS DO PERFIL DO USUÁRIO ---
            Área de interesse: {area}
            Nível atual de conhecimento: {nivel}
            Disponibilidade semanal: {horas_semana} horas
            Objetivo e dúvidas detalhadas: {objetivo_detalhado}
            """

            with st.spinner("O CareerDev AI está estruturando seu plano de estudos e carreira..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message}
                    ],
                    model="openai/gpt-oss-120b",
                    temperature=0.6,
                    max_tokens=2048
                )

                resposta = chat_completion.choices[0].message.content

                st.success("Plano personalizado gerado com sucesso!")
                st.markdown("---")
                st.markdown(resposta)

        except Exception as e:
            st.error(f"Erro ao comunicar com a API da Groq: {str(e)}")
