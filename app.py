import streamlit as st
from src.agent_controller import AgentController

# Configuração da página Streamlit
st.set_page_config(
    page_title="TechFix - Agente de Suporte TI",
    page_icon="🛠️",
    layout="centered"
)

# Inicialização do Controller e Histórico na Sessão
if "history" not in st.session_state:
    st.session_state.history = []

try:
    controller = AgentController()
except Exception as e:
    st.error(f"Erro na inicialização do serviço: {e}")
    st.stop()

# Header da Aplicação
st.title("🛠️ TechFix - Suporte Técnico em TI")
st.caption("Seu assistente virtual para diagnóstico de rede, hardware, SO e softwares.")

# Botão para limpar histórico na barra lateral
with st.sidebar:
    st.header("Opções")
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.history = []
        st.rerun()
    st.markdown("---")
    st.markdown("**Modelo:** OpenAI GPT-OSS 120B (Groq)")

# Exibição do histórico de mensagens
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada de texto do usuário
if prompt := st.chat_input("Descreva seu problema de TI (ex: 'Minha internet está caindo toda hora')..."):
    # Exibe a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processa e exibe a resposta do agente
    with st.chat_message("assistant"):
        with st.spinner("Analisando o problema técnico..."):
            response, updated_history = controller.process_user_message(prompt, st.session_state.history)
            st.markdown(response)
            st.session_state.history = updated_history