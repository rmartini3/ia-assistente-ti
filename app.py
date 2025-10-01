# app.py

import os
import streamlit as st
from datetime import datetime
from groq import Groq, APIError
from dotenv import load_dotenv

# Importações refatoradas
from playbooks import OPERATIONAL_PLAYBOOK_PROMPTS

# ----------------------------------------------------------------------
# 1. CONFIGURAÇÃO INICIAL E CARREGAMENTO DE RECURSOS
# ----------------------------------------------------------------------

# Cache para otimizar o carregamento de recursos que não mudam.
@st.cache_data
def load_system_prompt(file_name: str) -> str:
    """Carrega o prompt do sistema de um arquivo de texto."""
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Arquivo de prompt do sistema '{file_name}' não encontrado.")
        return "" # Retorna uma string vazia para evitar que o app quebre
    
@st.cache_data
def load_css(file_name: str):
    """Carrega um arquivo CSS externo."""
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo de estilo '{file_name}' não encontrado.")

# --- Carregamento de Ícone, Título e CSS ---
st.set_page_config(
    page_title="Assistente de IA para Profissionais de TI",
    page_icon="favicon.ico", # Streamlit pode carregar o ícone diretamente pelo caminho
    layout="wide",
    initial_sidebar_state="auto"
)

load_css("style.css")
SYSTEM_PROMPT = load_system_prompt("system_prompt.md")

# ----------------------------------------------------------------------
# 4. FUNÇÕES AUXILIARES DO CHAT
# ----------------------------------------------------------------------

def render_response_with_copy_button(response: str):
    """
    Renderiza a resposta da IA, separando texto de blocos de código.
    Usa st.code() para blocos de código, que inclui um botão de copiar.
    """
    # Divide a resposta em partes, usando o delimitador de bloco de código ```
    parts = response.split("```")
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Ímpar: é um bloco de código
            # A primeira linha pode conter a linguagem (ex: python, bash)
            lines = part.split('\n', 1)
            language = lines[0].strip()
            code = lines[1] if len(lines) > 1 else ""
            st.code(code, language=language or None)
        else:  # Par: é texto normal
            if part.strip():
                st.markdown(part)

# ----------------------------------------------------------------------
# 2. BARRA LATERAL (SIDEBAR)
# ----------------------------------------------------------------------

with st.sidebar:
    # Verifica se o arquivo de logo existe antes de tentar exibi-lo
    if os.path.exists("favicon.ico"):
        st.image("favicon.ico", width=100)
    
    # Título e descrição
    st.title("Assistente de IA para TI")
    st.markdown("Seu copiloto para diagnósticos, *troubleshooting* e automação.")
    st.divider()

    # --- Seção de Configuração da API e Modelo ---
    st.subheader("Configurações da IA")
    load_dotenv()

    # A chave API é lida do estado da sessão para persistir entre re-execuções
    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")

    st.session_state.groq_api_key = st.text_input(
        "Insira sua API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys",
        value=st.session_state.groq_api_key
    )

    # Adicionado seletor de modelo
    selected_model = st.selectbox(
        "Escolha o Modelo de IA",
        options=[
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile",
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it",
        ],
        index=0, # Padrão para o modelo mais rápido
        help="Modelos maiores podem ser mais lentos, mas mais capazes."
    )

    client = None
    if st.session_state.groq_api_key:
        try:
            client = Groq(api_key=st.session_state.groq_api_key)
        except Exception as e:
            st.error(f"Erro ao inicializar cliente Groq: {e}")

    st.divider()

    # --- Seção de Playbooks ---
    st.subheader("Playbooks de Execução Rápida")
    st.caption("Use para cenários comuns ou scripts de automação.")
    
    categoria_selecionada = st.selectbox(
        "Selecione a Área de Foco:",
        options=list(OPERATIONAL_PLAYBOOK_PROMPTS.keys()),
        index=None, # Permite que nenhum item seja selecionado inicialmente
        placeholder="Selecione a Área..."
    )
    
    if categoria_selecionada:
        cenario_selecionado = st.selectbox(
            f"Selecione o Cenário em '{categoria_selecionada}':",
            options=list(OPERATIONAL_PLAYBOOK_PROMPTS[categoria_selecionada].keys()),
            index=None,
            placeholder="Selecione o Cenário..."
        )
        
        if cenario_selecionado:
            prompt_pronto = OPERATIONAL_PLAYBOOK_PROMPTS[categoria_selecionada][cenario_selecionado]
            
            if st.button("Executar Playbook de Comando"):
                st.session_state["execute_playbook"] = prompt_pronto

    st.divider()

    # --- Seção de Ações da Conversa ---
    st.subheader("Ações da Conversa")

    def format_chat_for_export(messages: list) -> str:
        """Formata o histórico do chat para exportação em Markdown."""
        export_content = f"# Histórico da Conversa - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        for message in messages:
            role = "Usuário" if message["role"] == "user" else "Assistente"
            export_content += f"## 💬 {role}\n\n"
            export_content += f"{message['content']}\n\n---\n\n"
        return export_content

    # Botão para exportar a conversa (só aparece se houver mensagens)
    if st.session_state.get("messages"):
        st.download_button(
            label="📥 Exportar Conversa",
            data=format_chat_for_export(st.session_state.messages),
            file_name=f"historico_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            help="Baixe o histórico completo da conversa em formato Markdown."
        )

    # Botão para limpar o histórico
    if st.button("🗑️ Limpar Histórico", help="Apaga todas as mensagens da sessão atual."):
        st.session_state.messages = []
        st.rerun()


    st.divider()

    # --- Seção de Contato ---
    st.subheader("Criado por")
    st.markdown("Rafael Martiniano")
    st.markdown('''
        <div style="display: flex; flex-direction: column; gap: 10px;">
            <a href="https://github.com/rmartini3" target="_blank" style="display: flex; align-items: center; text-decoration: none; color: var(--sidebar-text-color);">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
                <span style="margin-left: 10px;">GitHub</span>
            </a>
            <a href="https://www.linkedin.com/in/rafael-martiniano/" target="_blank" style="display: flex; align-items: center; text-decoration: none; color: var(--sidebar-text-color);">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
                <span style="margin-left: 10px;">LinkedIn</span>
            </a>
        </div>
    ''', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 3. INTERFACE PRINCIPAL E LÓGICA DO CHAT
# ----------------------------------------------------------------------

st.title("Assistente de IA para Profissionais de TI")
st.caption("Seu copiloto para diagnósticos, scripts e procedimentos operacionais.")

# Mensagem de boas-vindas ou instrução inicial
if not st.session_state.get("messages"):
    st.info("Bem-vindo! Insira sua chave da API Groq na barra lateral para começar ou selecione um Playbook.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        render_response_with_copy_button(message["content"])

# --- Captura de entrada e lógica principal ---
prompt = None
if "execute_playbook" in st.session_state and st.session_state["execute_playbook"]:
    prompt = st.session_state["execute_playbook"]
    st.session_state["execute_playbook"] = None # Limpa para evitar re-execução
elif chat_input := st.chat_input("Qual comando de diagnóstico ou script você precisa?"):
    prompt = chat_input

if prompt:
    if not st.session_state.groq_api_key:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Garante que o cliente Groq seja inicializado antes do uso
    if not client:
        try:
            client = Groq(api_key=st.session_state.groq_api_key)
        except Exception as e:
            st.error(f"Falha ao inicializar o cliente Groq. Verifique sua chave de API. Erro: {e}")
            st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):
            try:
                # Prepara as mensagens para a API, garantindo que o prompt do sistema esteja sempre presente
                messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model=selected_model,
                    temperature=0.5,
                    max_tokens=4096, # Aumentado para respostas ainda mais completas
                )
                response = chat_completion.choices[0].message.content
                render_response_with_copy_button(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except APIError as e:
                st.error(f"Erro da API Groq: {e.status_code} - {e.body.get('error', {}).get('message', 'Sem detalhes')}")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")

# --- Rodapé ---
st.markdown(
    '''
    <div style="text-align: center; color: gray;">
        <hr>
        <p>Assistente de IA para Profissionais de TI v1.0</p>
        <p style="text-align: center;">Criado por: Rafael Martiniano</p>
    </div>
    ''',
    unsafe_allow_html=True
)
