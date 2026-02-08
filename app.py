# app.py

import os
import json
import hashlib
import streamlit as st
from datetime import datetime
from groq import Groq, APIError
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

# Importações refatoradas
from playbooks import OPERATIONAL_PLAYBOOK_PROMPTS

MAX_HISTORY_MESSAGES = 20  # limita o contexto enviado para o modelo
MAX_SCRIPT_REVIEW_CHARS = 60000  # evita estouro de tokens em arquivos grandes
MAX_LOG_REVIEW_CHARS = 80000  # limite para análise de logs
SUPPORTED_SCRIPT_EXTENSIONS = ["cmd", "bat", "sh", "ps1", "html", "css", "js", "java", "py", "xml", "json"]
SUPPORTED_LOG_EXTENSIONS = [
    "log", "txt", "out", "err", "trace", "evtx", "dmp", "mdmp", "dump",
    "json", "xml", "yaml", "yml", "csv", "ini", "conf",
]
TEXT_LIKE_EXTENSIONS = {
    "cmd", "bat", "sh", "ps1", "html", "css", "js", "java", "py",
    "xml", "json", "log", "txt", "out", "err", "trace", "yaml",
    "yml", "csv", "ini", "conf",
}

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
if "current_view" not in st.session_state:
    st.session_state.current_view = "assistant"
if not SYSTEM_PROMPT:
    st.warning("Arquivo system_prompt.md não encontrado ou vazio; o prompt de sistema não será aplicado.")

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


def get_recent_history(messages: list, limit: int = MAX_HISTORY_MESSAGES) -> list:
    """Retorna apenas as últimas mensagens para evitar estouro de tokens."""
    if limit <= 0:
        return []
    return messages[-limit:]


def decode_uploaded_text(file_bytes: bytes) -> tuple[str, str]:
    """Tenta decodificar bytes de arquivo texto usando encodings comuns."""
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return file_bytes.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return file_bytes.decode("utf-8", errors="replace"), "utf-8 (com substituições)"


def parse_groq_error(e: APIError) -> dict:
    """Extrai dados úteis do erro da API da Groq para exibição amigável."""
    status_code = getattr(e, "status_code", None)
    body = getattr(e, "body", None)

    error_code = None
    error_message = None
    error_type = None

    if isinstance(body, dict):
        error_obj = body.get("error", {})
        if isinstance(error_obj, dict):
            error_code = error_obj.get("code")
            error_message = error_obj.get("message")
            error_type = error_obj.get("type")
        if not error_message:
            error_message = body.get("message")
    elif body:
        error_message = str(body)

    if not error_code:
        error_code = str(status_code) if status_code is not None else "N/A"
    if not error_message:
        error_message = "Sem detalhes fornecidos pela API."

    if status_code == 401:
        friendly = "Falha de autenticação: verifique se a API Key da Groq está correta e ativa."
    elif status_code == 429:
        friendly = "Limite de uso atingido temporariamente. Aguarde alguns instantes e tente novamente."
    elif status_code == 400:
        friendly = "Requisição inválida. Revise os parâmetros enviados para a API."
    elif status_code == 503:
        friendly = "Serviço temporariamente indisponível na Groq. Tente novamente em breve."
    else:
        friendly = "A API da Groq retornou um erro ao processar sua solicitação."

    explanation = (
        "Erro de integração com o modelo de IA. Você pode tentar novamente, reduzir o conteúdo enviado "
        "ou trocar o modelo selecionado."
    )
    technical_payload = body if isinstance(body, dict) else {"raw_body": str(body)}

    return {
        "friendly": friendly,
        "code": error_code,
        "status": status_code,
        "message": error_message,
        "type": error_type or "N/A",
        "explanation": explanation,
        "technical": technical_payload,
    }


def render_friendly_error(context: str, error_code: str, explanation: str, technical_details: str):
    """Exibe erro em formato amigável com detalhes técnicos opcionais."""
    st.error(context)
    st.markdown(f"**Código:** `{error_code}`")
    st.markdown(f"**Explicação:** {explanation}")
    with st.expander("Detalhes técnicos"):
        st.code(technical_details)


def format_groq_error_for_ui(context: str, e: APIError):
    """Renderiza um erro da Groq com texto amigável + diagnóstico técnico."""
    data = parse_groq_error(e)
    try:
        technical_json = json.dumps(data["technical"], ensure_ascii=False, indent=2)
    except Exception:
        technical_json = str(data["technical"])
    details = (
        f"status={data['status']}\n"
        f"type={data['type']}\n"
        f"message={data['message']}\n"
        f"payload={technical_json}"
    )
    render_friendly_error(
        context=f"{context} {data['friendly']}",
        error_code=data["code"],
        explanation=data["explanation"],
        technical_details=details,
    )


def format_unexpected_error_for_ui(context: str, e: Exception):
    """Renderiza erro inesperado sem ocultar detalhes para diagnóstico."""
    render_friendly_error(
        context=f"{context} Ocorreu um erro inesperado.",
        error_code="UNEXPECTED_ERROR",
        explanation="Revise os dados de entrada e tente novamente. Se persistir, consulte os detalhes técnicos.",
        technical_details=f"{type(e).__name__}: {e}",
    )


def clear_script_snippet_inputs():
    """Limpa os campos de entrada do modo de análise por linha/bloco."""
    st.session_state["script_review_snippet_label"] = ""
    st.session_state["script_review_line_reference"] = ""
    st.session_state["script_review_snippet_text"] = ""


def get_binary_summary(file_bytes: bytes) -> str:
    """Gera resumo de binário para análise inicial de logs/artefatos."""
    md5_hash = hashlib.md5(file_bytes).hexdigest()  # noqa: S324 - uso diagnóstico
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()
    header_hex = file_bytes[:96].hex(" ")
    return (
        f"Tamanho (bytes): {len(file_bytes)}\n"
        f"MD5: {md5_hash}\n"
        f"SHA256: {sha256_hash}\n"
        f"Header hex (primeiros 96 bytes):\n{header_hex}"
    )


def normalize_structured_content(content: str, extension: str) -> tuple[str, str]:
    """Normaliza JSON/XML para melhorar leitura e análise."""
    if extension == "json":
        try:
            parsed = json.loads(content)
            normalized = json.dumps(parsed, ensure_ascii=False, indent=2)
            return normalized, "JSON válido e normalizado para leitura."
        except Exception as e:
            return content, f"JSON não pôde ser normalizado: {e}"

    if extension == "xml":
        try:
            root = ET.fromstring(content)
            summary = f"XML válido. Tag raiz: `{root.tag}`."
            return content, summary
        except Exception as e:
            return content, f"XML não pôde ser validado estruturalmente: {e}"

    return content, "Conteúdo textual pronto para análise."


def truncate_for_model(text: str, max_chars: int) -> tuple[str, bool]:
    """Trunca texto para evitar estouro de contexto do modelo."""
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars], True


def render_script_review_center(client, selected_model: str):
    """Renderiza um validador de scripts fora do chat."""
    st.title("Validador de Scripts")
    st.caption("Envie um script para avaliação técnica com foco em qualidade, segurança e confiabilidade.")

    if st.button("Voltar para a tela do Assistente de IA", type="primary", key="back_from_script_review"):
        st.session_state.current_view = "assistant"
        st.rerun()

    st.markdown(
        "Formatos aceitos: `.cmd`, `.bat`, `.sh`, `.ps1`, `.html`, `.css`, `.js`, `.java`, `.py`, `.xml`, `.json`."
    )

    st.markdown("### Integração com validadores externos")
    st.markdown(
        "- HTML: [W3C Nu Checker](https://validator.w3.org/nu/)\n"
        "- CSS: [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)\n"
        "- PowerShell: [Invoke-ScriptAnalyzer](https://learn.microsoft.com/powershell/module/psscriptanalyzer/invoke-scriptanalyzer?view=ps-modules)\n"
        "- Python: [py_compile](https://docs.python.org/3/library/py_compile.html)\n"
        "- Java: [javac](https://docs.oracle.com/en/java/javase/19/docs/specs/man/javac.html)\n"
        "- JavaScript: [Node `--check`](https://nodejs.org/api/cli.html) e [ESLint](https://eslint.org/)\n"
        "- Shell: [ShellCheck](https://www.shellcheck.net/)"
    )
    st.caption(
        "O validador interno complementa essas ferramentas e ajuda no diagnóstico unificado para as linguagens suportadas."
    )

    st.markdown("### Manual do Analisador de Scripts")
    st.markdown(
        """
1. Escolha o modo: `Anexar arquivo` ou `Linha/bloco de código`.
2. Defina o nível da revisão (`Rápida`, `Padrão` ou `Profunda`).
3. Escolha o foco da análise (segurança, sintaxe, performance etc.).
4. Clique em **Avaliar Script Agora**.
5. Revise os achados críticos primeiro, depois correções e checklist.
6. Baixe o relatório em `.md` para documentação.
        """
    )
    st.info(
        "Importante: a análise é estática (não executa o código). Sempre valide em ambiente de teste antes de produção."
    )

    st.markdown("### FAQ do Analisador de Scripts")
    with st.expander("1) O analisador executa o script?"):
        st.markdown(
            "Não. A avaliação é apenas estática e baseada no conteúdo do arquivo enviado."
        )

    with st.expander("2) Quais riscos ele consegue identificar melhor?"):
        st.markdown(
            "Uso inseguro de comandos, validações ausentes, riscos de injeção, lógica frágil, "
            "problemas comuns de sintaxe e pontos de manutenção."
        )

    with st.expander("3) Qual nível de revisão devo usar?"):
        st.markdown(
            "- **Rápida:** triagem inicial.\n"
            "- **Padrão:** equilíbrio entre profundidade e velocidade.\n"
            "- **Profunda:** revisão ampla para mudanças sensíveis."
        )

    with st.expander("4) Posso pedir reescrita do script?"):
        st.markdown(
            "Sim. Ative **Sugerir versão corrigida** para receber melhorias e trechos ajustados."
        )

    with st.expander("5) Existe limite para arquivos grandes?"):
        st.markdown(
            f"Sim. Conteúdos muito grandes são truncados em até `{MAX_SCRIPT_REVIEW_CHARS}` caracteres "
            "para caber na janela de análise."
        )

    with st.expander("6) A análise por linha/bloco é completa?"):
        st.markdown(
            "Não. É uma análise **superficial/indicativa**, pois não há contexto completo do arquivo. "
            "Use para triagem rápida e confirme com revisão de arquivo completo."
        )

    with st.expander("7) Posso afirmar conformidade oficial (W3C/ISO/COBIT/ITIL) com esse validador?"):
        st.markdown(
            "Não como certificação formal. O validador fornece **indícios técnicos** e referências de boas práticas. "
            "Conformidade oficial exige auditoria/processos formais da organização e validação com ferramentas e critérios específicos."
        )

    with st.expander("8) Ordem recomendada de uso com o Assistente"):
        st.markdown(
            "1. Use o **Assistente** para desenhar a solução.\n"
            "2. Use o **Validador de Scripts** para revisar riscos e qualidade.\n"
            "3. Volte ao **Assistente** para ajustar pontos encontrados.\n"
            "4. Reavalie no **Validador** até estabilizar.\n"
            "5. Execute somente após validação em ambiente de teste."
        )

    st.markdown("### Envio para análise")
    analysis_mode = st.radio(
        "Escolha o modo de análise",
        options=["1 - Anexar arquivo completo", "2 - Analisar linha/bloco de código"],
        horizontal=True,
        key="script_review_mode",
    )

    language_labels = {
        "cmd": "CMD",
        "bat": "BAT",
        "sh": "Shell",
        "ps1": "PowerShell",
        "html": "HTML",
        "css": "CSS",
        "js": "JavaScript",
        "java": "Java",
        "py": "Python",
        "xml": "XML",
        "json": "JSON",
    }

    file_name = ""
    extension = ""
    script_content = ""
    detected_encoding = "n/a"
    analysis_scope = "completo"

    if analysis_mode.startswith("1"):
        uploaded_file = st.file_uploader(
            "Envie o script para análise",
            type=SUPPORTED_SCRIPT_EXTENSIONS,
            help="O arquivo será analisado pela IA sem execução do código.",
            key="script_review_uploader",
        )
        if uploaded_file:
            file_name = uploaded_file.name
            extension = os.path.splitext(file_name)[1].lower().lstrip(".")
            file_bytes = uploaded_file.getvalue()
            script_content, detected_encoding = decode_uploaded_text(file_bytes)
            normalized_hint = ""
            if extension in ("json", "xml"):
                script_content, normalized_hint = normalize_structured_content(script_content, extension)

            if script_content.strip():
                st.caption(
                    f"Arquivo: `{file_name}` | Tipo: `{extension}` | Encoding detectado: `{detected_encoding}` | "
                    f"Tamanho: `{len(file_bytes)} bytes`"
                )
                if normalized_hint:
                    st.caption(normalized_hint)
                with st.expander("Visualizar conteúdo enviado"):
                    st.code(script_content, language=extension or None)
            else:
                st.warning("O arquivo está vazio ou sem conteúdo legível.")
        else:
            st.info("Selecione um arquivo para iniciar a avaliação.")
    else:
        extension = st.selectbox(
            "Linguagem do trecho",
            options=SUPPORTED_SCRIPT_EXTENSIONS,
            format_func=lambda value: f"{language_labels.get(value, value.upper())} (.{value})",
            key="script_review_snippet_language",
        )
        snippet_label = st.text_input(
            "Nome de referência (opcional)",
            placeholder="Ex.: trecho_login.ps1",
            key="script_review_snippet_label",
        )
        line_reference = st.text_input(
            "Linha(s) de referência (opcional)",
            placeholder="Ex.: 42-58",
            key="script_review_line_reference",
        )
        script_content = st.text_area(
            "Cole a linha ou bloco de código",
            height=260,
            key="script_review_snippet_text",
        )
        file_name = snippet_label.strip() or f"snippet.{extension}"
        detected_encoding = "entrada manual"
        analysis_scope = "parcial"

        col_snippet_1, col_snippet_2 = st.columns([1, 1])
        with col_snippet_1:
            if st.button("Limpar campos do trecho", key="clear_script_snippet_fields", use_container_width=True):
                clear_script_snippet_inputs()
                st.rerun()
        with col_snippet_2:
            if st.button("Limpar última avaliação", key="clear_last_script_review", use_container_width=True):
                st.session_state["script_review_result"] = ""
                st.session_state["script_review_result_file_name"] = ""
                st.rerun()

        if line_reference.strip():
            st.caption(f"Linha(s) informadas: `{line_reference.strip()}`")

        if script_content.strip():
            if extension in ("json", "xml"):
                script_content, normalized_hint = normalize_structured_content(script_content, extension)
                if normalized_hint:
                    st.caption(normalized_hint)
            st.warning(
                "Modo parcial: a avaliação é superficial e pode não refletir o comportamento real do arquivo completo."
            )
            with st.expander("Visualizar trecho enviado"):
                st.code(script_content, language=extension or None)
        else:
            st.info("Cole uma linha ou bloco de código para iniciar a avaliação.")

    col1, col2 = st.columns(2)
    with col1:
        review_depth = st.selectbox(
            "Nível da revisão",
            options=["Rápida", "Padrão", "Profunda"],
            index=1,
            key="script_review_depth",
        )
    with col2:
        include_rewrite = st.checkbox(
            "Sugerir versão corrigida",
            value=True,
            help="Quando habilitado, a IA inclui sugestões de trechos melhorados.",
            key="script_review_include_rewrite",
        )

    review_focus = st.multiselect(
        "Foco da análise",
        options=[
            "Sintaxe e bugs",
            "Segurança",
            "Performance",
            "Legibilidade e manutenção",
            "Boas práticas da linguagem",
        ],
        default=["Sintaxe e bugs", "Segurança", "Legibilidade e manutenção"],
        key="script_review_focus",
    )

    can_review = bool(script_content and script_content.strip())

    if st.button(
        "Avaliar Script Agora",
        use_container_width=True,
        key="run_script_review",
        disabled=not can_review,
    ):
        if not st.session_state.groq_api_key:
            st.warning("Insira sua API Key da Groq na barra lateral antes de executar a avaliação.")
            return

        if not client:
            try:
                client = Groq(api_key=st.session_state.groq_api_key)
            except Exception as e:
                format_unexpected_error_for_ui(
                    "Falha ao inicializar cliente Groq.",
                    e,
                )
                return

        content_for_review, was_truncated = truncate_for_model(script_content, MAX_SCRIPT_REVIEW_CHARS)
        if was_truncated:
            st.warning(
                f"O arquivo excede {MAX_SCRIPT_REVIEW_CHARS} caracteres e foi truncado para análise."
            )

        focus_text = ", ".join(review_focus) if review_focus else "análise geral"
        rewrite_instruction = (
            "Inclua também uma versão sugerida (ou trechos corrigidos) quando necessário."
            if include_rewrite
            else "Não gere versão reescrita completa; foque em diagnóstico e recomendações."
        )

        review_prompt = f"""
Você é um revisor técnico de scripts para operações de TI.
Analise o arquivo abaixo de forma estática (sem executar código).

Arquivo: {file_name}
Linguagem/extensão: {extension}
Nível da revisão: {review_depth}
Foco principal: {focus_text}
Escopo da análise: {analysis_scope}
Encoding de entrada: {detected_encoding}

Instruções obrigatórias:
1) Resumo executivo (2-5 linhas).
2) Achados críticos e riscos (priorize por severidade).
3) Problemas de sintaxe/lógica e possíveis falhas em runtime.
4) Melhorias de segurança, robustez e manutenção.
5) Recomendações práticas e checklist de validação.
6) {rewrite_instruction}
7) Para cada ponto crítico, classifique:
   - Funcionamento provável: `Funciona`, `Pode falhar` ou `Inconclusivo`.
   - Segurança do trecho: `Adequado`, `Pode melhorar` ou `Não seguro`.
8) Se o escopo for parcial, destaque explicitamente as limitações por falta de contexto.

Script para análise:
```{extension}
{content_for_review}
```
"""

        with st.spinner("Avaliando script..."):
            try:
                messages_for_api = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": review_prompt},
                ]
                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model=selected_model,
                    temperature=0.2,
                    max_tokens=4096,
                )
                review_response = chat_completion.choices[0].message.content

                st.session_state["script_review_result"] = review_response
                st.session_state["script_review_result_file_name"] = file_name
                st.success("Avaliação concluída.")
                render_response_with_copy_button(review_response)

                st.download_button(
                    label="Baixar avaliação",
                    data=review_response,
                    file_name=f"avaliacao_{os.path.splitext(file_name)[0]}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
            except APIError as e:
                format_groq_error_for_ui("Erro ao avaliar script.", e)
            except Exception as e:
                format_unexpected_error_for_ui("Erro ao avaliar script.", e)

    elif st.session_state.get("script_review_result"):
        if st.session_state.get("script_review_result_file_name"):
            st.caption(f"Última avaliação: `{st.session_state['script_review_result_file_name']}`")
        st.markdown("### Última avaliação gerada")
        render_response_with_copy_button(st.session_state["script_review_result"])


def render_log_analysis_center(client, selected_model: str):
    """Renderiza visualizador e analisador de logs multi-formato."""
    st.title("Visualizador e Analisador de Logs")
    st.caption(
        "Interprete logs e artefatos de erro com apoio de IA para causa raiz, impacto e próximos passos."
    )

    if st.button("Voltar para a tela do Assistente de IA", type="primary", key="back_from_log_review"):
        st.session_state.current_view = "assistant"
        st.rerun()

    st.markdown(
        "Suporta, entre outros: `.log`, `.txt`, `.json`, `.xml`, `.evtx`, `.dmp`, `.mdmp`, `.trace`, `.out`, `.err`."
    )
    st.info(
        "Para arquivos binários (ex.: `.evtx`, `.dmp`, `.mdmp`), a análise usa metadados/hash e interpretação indicativa."
    )

    input_mode = st.radio(
        "Escolha a origem dos logs",
        options=["1 - Anexar arquivo de log", "2 - Colar trecho de log"],
        horizontal=True,
        key="log_review_mode",
    )

    artifact_name = ""
    artifact_extension = ""
    artifact_encoding = "n/a"
    analysis_scope = "arquivo"
    normalized_hint = ""
    content_for_analysis = ""

    if input_mode.startswith("1"):
        uploaded_log = st.file_uploader(
            "Envie o arquivo de log/artefato",
            type=SUPPORTED_LOG_EXTENSIONS,
            key="log_review_uploader",
        )
        if uploaded_log:
            artifact_name = uploaded_log.name
            artifact_extension = os.path.splitext(artifact_name)[1].lower().lstrip(".")
            file_bytes = uploaded_log.getvalue()

            if artifact_extension in TEXT_LIKE_EXTENSIONS:
                raw_content, artifact_encoding = decode_uploaded_text(file_bytes)
                normalized_content, normalized_hint = normalize_structured_content(raw_content, artifact_extension)
                content_for_analysis = normalized_content
                st.caption(
                    f"Arquivo: `{artifact_name}` | Tipo: `{artifact_extension}` | Encoding: `{artifact_encoding}` | "
                    f"Tamanho: `{len(file_bytes)} bytes`"
                )
                if normalized_hint:
                    st.caption(normalized_hint)
                with st.expander("Visualizar conteúdo enviado"):
                    st.code(content_for_analysis, language=artifact_extension or None)
            else:
                analysis_scope = "binário"
                artifact_encoding = "binário"
                binary_summary = get_binary_summary(file_bytes)
                content_for_analysis = (
                    f"Arquivo binário recebido: {artifact_name}\n"
                    f"Extensão: {artifact_extension}\n"
                    f"{binary_summary}"
                )
                st.caption(
                    f"Arquivo binário: `{artifact_name}` | Tipo: `{artifact_extension}` | "
                    f"Tamanho: `{len(file_bytes)} bytes`"
                )
                with st.expander("Resumo técnico do binário"):
                    st.code(content_for_analysis)
        else:
            st.info("Selecione um arquivo para iniciar a análise de logs.")
    else:
        artifact_extension = st.selectbox(
            "Tipo do trecho",
            options=["log", "txt", "json", "xml", "trace", "out", "err"],
            key="log_snippet_extension",
        )
        artifact_name = st.text_input(
            "Nome de referência (opcional)",
            placeholder="Ex.: erro_api.log",
            key="log_snippet_name",
        ).strip() or f"snippet_log.{artifact_extension}"
        content_for_analysis = st.text_area(
            "Cole o trecho de log",
            height=260,
            key="log_snippet_text",
        )
        artifact_encoding = "entrada manual"
        analysis_scope = "trecho"

        if st.button("Limpar trecho de log", key="clear_log_snippet", use_container_width=True):
            st.session_state["log_snippet_name"] = ""
            st.session_state["log_snippet_text"] = ""
            st.rerun()

        if content_for_analysis.strip():
            if artifact_extension in ("json", "xml"):
                normalized_content, normalized_hint = normalize_structured_content(
                    content_for_analysis, artifact_extension
                )
                content_for_analysis = normalized_content
                if normalized_hint:
                    st.caption(normalized_hint)
            with st.expander("Visualizar trecho enviado"):
                st.code(content_for_analysis, language=artifact_extension or None)
        else:
            st.info("Cole um trecho de log para iniciar a análise.")

    col_a, col_b = st.columns(2)
    with col_a:
        log_focus = st.selectbox(
            "Objetivo da análise",
            options=[
                "Causa raiz",
                "Erro de aplicação",
                "Segurança e incidentes",
                "Performance e latência",
                "Resumo executivo",
            ],
            index=0,
            key="log_review_focus",
        )
    with col_b:
        environment_hint = st.text_input(
            "Ambiente (opcional)",
            placeholder="Ex.: Windows Server 2022, Linux Ubuntu 22.04, Kubernetes",
            key="log_review_environment",
        )

    include_timeline = st.checkbox(
        "Incluir linha do tempo dos eventos (se possível)",
        value=True,
        key="log_review_timeline",
    )
    include_actions = st.checkbox(
        "Incluir plano de ação priorizado",
        value=True,
        key="log_review_actions",
    )

    can_analyze = bool(content_for_analysis and content_for_analysis.strip())
    if st.button(
        "Analisar Logs Agora",
        use_container_width=True,
        disabled=not can_analyze,
        key="run_log_review",
    ):
        if not st.session_state.groq_api_key:
            st.warning("Insira sua API Key da Groq na barra lateral antes de executar a análise.")
            return

        if not client:
            try:
                client = Groq(api_key=st.session_state.groq_api_key)
            except Exception as e:
                format_unexpected_error_for_ui("Falha ao inicializar cliente Groq.", e)
                return

        trimmed_content, was_truncated = truncate_for_model(content_for_analysis, MAX_LOG_REVIEW_CHARS)
        if was_truncated:
            st.warning(
                f"O conteúdo excede {MAX_LOG_REVIEW_CHARS} caracteres e foi truncado para análise."
            )

        timeline_instruction = (
            "Inclua linha do tempo de eventos quando houver dados temporais no conteúdo."
            if include_timeline
            else "Não é necessário montar linha do tempo."
        )
        action_instruction = (
            "Inclua plano de ação priorizado com passos imediatos, curto e médio prazo."
            if include_actions
            else "Forneça apenas diagnóstico técnico sem plano de ação detalhado."
        )

        prompt = f"""
Você é um analista SRE/DevOps/SecOps especializado em investigação de logs.
Faça análise estática do conteúdo enviado.

Artefato: {artifact_name}
Tipo: {artifact_extension}
Escopo: {analysis_scope}
Encoding: {artifact_encoding}
Objetivo principal: {log_focus}
Ambiente informado: {environment_hint or "não informado"}

Requisitos de saída:
1) Resumo do incidente em linguagem simples.
2) Principais erros/códigos/sinais com severidade (alta, média, baixa).
3) Hipótese de causa raiz (com nível de confiança).
4) Possíveis impactos (serviço, segurança, dados, disponibilidade).
5) {timeline_instruction}
6) {action_instruction}
7) Se o conteúdo for parcial/binário, explicite limitações e próximos dados necessários.

Conteúdo para análise:
```{artifact_extension or "text"}
{trimmed_content}
```
"""

        with st.spinner("Analisando logs..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    model=selected_model,
                    temperature=0.2,
                    max_tokens=4096,
                )
                analysis = chat_completion.choices[0].message.content
                st.session_state["log_review_result"] = analysis
                st.session_state["log_review_result_name"] = artifact_name
                st.success("Análise de logs concluída.")
                render_response_with_copy_button(analysis)
                st.download_button(
                    label="Baixar análise de logs",
                    data=analysis,
                    file_name=f"analise_logs_{os.path.splitext(artifact_name)[0]}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
            except APIError as e:
                format_groq_error_for_ui("Erro ao analisar logs.", e)
            except Exception as e:
                format_unexpected_error_for_ui("Erro ao analisar logs.", e)
    elif st.session_state.get("log_review_result"):
        if st.session_state.get("log_review_result_name"):
            st.caption(f"Última análise: `{st.session_state['log_review_result_name']}`")
        st.markdown("### Última análise de logs")
        render_response_with_copy_button(st.session_state["log_review_result"])


def render_help_center():
    """Renderiza uma central de ajuda completa no corpo principal da aplicação."""
    st.title("Central de Ajuda e FAQ")
    st.caption("Guia completo para usar o assistente com mais qualidade, rapidez e segurança.")

    if st.button("Voltar para a tela do Assistente de IA", type="primary"):
        st.session_state.current_view = "assistant"
        st.rerun()

    st.markdown("### Comece por aqui")
    st.markdown(
        """
1. Configure sua API Key da Groq na barra lateral.
2. Escolha o modelo de IA conforme velocidade e profundidade da resposta.
3. Escreva sua solicitação com contexto técnico (erro, ambiente e objetivo).
4. Use Playbooks para cenários recorrentes e automações.
5. Exporte o histórico para registrar evidências e decisões.
        """
    )

    st.markdown("### Boas práticas para obter respostas melhores")
    st.markdown(
        """
- Informe sistema operacional, versão, stack e restrições de ambiente.
- Inclua mensagens de erro completas e comandos já executados.
- Peça resposta em formato de checklist quando for executar em produção.
- Solicite validação pós-ação (como confirmar que a correção funcionou).
- Quando necessário, peça plano de rollback junto com o procedimento.
        """
    )

    st.markdown("### FAQ detalhado")

    with st.expander("1) Onde configuro a API Key da Groq?"):
        st.markdown(
            "Na barra lateral, na seção **Configurações da IA**, preencha "
            "**Insira sua API Key Groq**. Sem a chave, o assistente não envia requisições."
        )

    with st.expander("2) Qual modelo devo escolher?"):
        st.markdown(
            "- `llama-3.1-8b-instant`: menor latência para dúvidas rápidas.\n"
            "- `llama-3.1-70b-versatile`: melhor para troubleshooting complexo.\n"
            "- `mixtral-8x7b-32768`: útil quando você precisa de contexto maior.\n"
            "- Dica prática: teste dois modelos em perguntas críticas para comparar qualidade."
        )

    with st.expander("3) Como usar Playbooks de Execução Rápida?"):
        st.markdown(
            "Selecione **Área de Foco** e **Cenário**, revise nível/ferramentas/tags e clique "
            "em **Executar Playbook de Comando**. O app envia um prompt estruturado ao assistente."
        )

    with st.expander("4) O que fazer quando a resposta vier genérica?"):
        st.markdown(
            "Refaça a pergunta com detalhes: objetivo, logs, comando executado, saída obtida, "
            "impacto no negócio e limite de tempo para solução."
        )

    with st.expander("5) Como limpar e exportar o histórico?"):
        st.markdown(
            "Na seção **Ações da Conversa**:\n"
            "- **Exportar Conversa** gera um arquivo `.md` com todo o histórico.\n"
            "- **Limpar Histórico** reinicia a sessão atual."
        )

    with st.expander("6) Meus dados da conversa são persistidos no app?"):
        st.markdown(
            "As mensagens ficam em `st.session_state` durante a sessão atual no navegador. "
            "Ao limpar o histórico, o contexto local é removido."
        )

    with st.expander("7) Como pedir scripts com mais segurança?"):
        st.markdown(
            "Peça sempre:\n"
            "- Pré-requisitos,\n"
            "- Comando de validação antes da mudança,\n"
            "- Rollback,\n"
            "- Critérios objetivos de sucesso."
        )

    with st.expander("8) Por que o app pode reduzir contexto automaticamente?"):
        st.markdown(
            "Para evitar estouro de tokens. O app considera apenas as últimas mensagens "
            "quando o histórico cresce demais."
        )

    with st.expander("9) O que é cada modelo disponível e como eles trabalham?"):
        st.markdown(
            "Todos os modelos funcionam como LLMs autoregressivos: eles analisam o contexto "
            "da conversa e geram a resposta token por token."
        )
        st.markdown(
            "- `llama-3.1-8b-instant`: prioriza velocidade e respostas objetivas para tarefas do dia a dia.\n"
            "- `llama-3.1-70b-versatile`: mais robusto para análises profundas, decisões e troubleshooting complexo.\n"
            "- `llama3-8b-8192`: opção leve para perguntas rápidas com contexto menor.\n"
            "- `llama3-70b-8192`: maior qualidade de raciocínio mantendo janela de contexto moderada.\n"
            "- `mixtral-8x7b-32768`: arquitetura Mixture-of-Experts, boa para instruções longas e multi-etapas.\n"
            "- `gemma-7b-it`: modelo enxuto para interações curtas, com boa eficiência."
        )

    with st.expander("10) Comparativo entre modelos por funcionalidade"):
        model_catalog = {
            "llama-3.1-8b-instant": {
                "Velocidade": "Alta",
                "Profundidade técnica": "Média",
                "Contexto": "Médio",
                "Melhor para": "Diagnóstico rápido e respostas objetivas",
            },
            "llama-3.1-70b-versatile": {
                "Velocidade": "Média",
                "Profundidade técnica": "Alta",
                "Contexto": "Alto",
                "Melhor para": "Troubleshooting avançado e decisões complexas",
            },
            "llama3-8b-8192": {
                "Velocidade": "Alta",
                "Profundidade técnica": "Média",
                "Contexto": "Moderado",
                "Melhor para": "Perguntas diretas e scripts curtos",
            },
            "llama3-70b-8192": {
                "Velocidade": "Média",
                "Profundidade técnica": "Alta",
                "Contexto": "Moderado",
                "Melhor para": "Análises com melhor qualidade de resposta",
            },
            "mixtral-8x7b-32768": {
                "Velocidade": "Média",
                "Profundidade técnica": "Alta",
                "Contexto": "Muito alto",
                "Melhor para": "Procedimentos longos, runbooks e prompts extensos",
            },
            "gemma-7b-it": {
                "Velocidade": "Alta",
                "Profundidade técnica": "Média",
                "Contexto": "Moderado",
                "Melhor para": "Suporte rápido e orientação inicial",
            },
        }

        funcionalidade = st.selectbox(
            "Escolha a funcionalidade para comparar recomendações:",
            options=[
                "Diagnóstico rápido",
                "Troubleshooting avançado",
                "Geração de scripts",
                "Documentação e runbooks",
                "Contexto longo de conversa",
            ],
            key="help_model_functionality",
        )

        ranking_por_funcionalidade = {
            "Diagnóstico rápido": ["llama-3.1-8b-instant", "llama3-8b-8192", "gemma-7b-it"],
            "Troubleshooting avançado": ["llama-3.1-70b-versatile", "llama3-70b-8192", "mixtral-8x7b-32768"],
            "Geração de scripts": ["llama-3.1-70b-versatile", "mixtral-8x7b-32768", "llama-3.1-8b-instant"],
            "Documentação e runbooks": ["mixtral-8x7b-32768", "llama-3.1-70b-versatile", "llama3-70b-8192"],
            "Contexto longo de conversa": ["mixtral-8x7b-32768", "llama-3.1-70b-versatile", "llama-3.1-8b-instant"],
        }

        st.markdown("**Top recomendações para a funcionalidade selecionada:**")
        for posicao, model_name in enumerate(ranking_por_funcionalidade[funcionalidade], start=1):
            st.markdown(f"{posicao}. `{model_name}`")

        modelos_escolhidos = st.multiselect(
            "Selecione modelos para comparar lado a lado:",
            options=list(model_catalog.keys()),
            default=["llama-3.1-8b-instant", "llama-3.1-70b-versatile"],
            key="help_model_compare",
        )

        if modelos_escolhidos:
            tabela_comparativa = []
            for model_name in modelos_escolhidos:
                row = {"Modelo": model_name}
                row.update(model_catalog[model_name])
                tabela_comparativa.append(row)
            st.dataframe(tabela_comparativa, use_container_width=True, hide_index=True)
        else:
            st.info("Selecione ao menos um modelo para visualizar o comparativo.")

    with st.expander("11) O que é o Validador de Scripts e qual ordem recomendada de uso?"):
        st.markdown(
            "O **Validador de Scripts** é uma área fora do chat para revisão técnica estática de "
            "arquivos `.cmd`, `.bat`, `.sh`, `.ps1`, `.html`, `.css`, `.js`, `.java`, `.py`, `.xml` e `.json`."
        )
        st.markdown(
            "Ele identifica riscos, bugs prováveis, melhorias de segurança e manutenção, sem executar o código."
        )
        st.markdown(
            "Ele pode ser combinado com validadores externos (como W3C para HTML/CSS) sem alterar o fluxo atual do app."
        )
        st.markdown(
            "Importante: o resultado é uma **análise assistida**, não uma certificação formal de conformidade."
        )
        st.markdown("**Ordem recomendada (Assistente + Validador):**")
        st.markdown(
            "1. Defina o objetivo com o **Assistente** (escopo, requisitos e estratégia).\n"
            "2. Gere ou refine o script com o **Assistente**.\n"
            "3. Envie o arquivo no **Validador de Scripts**.\n"
            "4. Corrija os pontos críticos encontrados.\n"
            "5. Reavalie no Validador até reduzir riscos.\n"
            "6. Execute apenas após testes em ambiente controlado."
        )

    with st.expander("12) Como funciona o Visualizador de Logs?"):
        st.markdown(
            "O **Visualizador de Logs** aceita arquivos e trechos para investigação de incidentes, "
            "incluindo logs textuais e artefatos binários (`.evtx`, `.dmp`, `.mdmp`)."
        )
        st.markdown(
            "Ele monta diagnóstico com causa raiz provável, severidade, impacto e plano de ação. "
            "Para binários, a análise é indicativa com base em metadados/hash."
        )
        st.markdown(
            "Fluxo recomendado:\n"
            "1. Coletar logs relevantes.\n"
            "2. Analisar no Visualizador.\n"
            "3. Refinar hipóteses no Assistente.\n"
            "4. Implementar correções e revalidar."
        )

    with st.expander("13) O que significa erro amigável + detalhe técnico?"):
        st.markdown(
            "A aplicação mostra uma explicação clara para o usuário (erro amigável), "
            "com código e ação recomendada."
        )
        st.markdown(
            "Também exibe um bloco técnico expandível com o payload/erro bruto da API para facilitar troubleshooting."
        )

    st.markdown("### Saiba mais e links úteis")
    st.caption("Referências externas alinhadas às práticas e funcionalidades suportadas pelo assistente.")
    st.markdown(
        "- **W3C Nu Checker (HTML):** validação de marcação HTML. "
        "[Acessar](https://validator.w3.org/nu/)\n"
        "- **W3C CSS Validator:** validação de folhas de estilo CSS. "
        "[Acessar](https://jigsaw.w3.org/css-validator/)\n"
        "- **Windows Event Log (conceitos):** referência para interpretação de eventos Windows. "
        "[Acessar](https://learn.microsoft.com/windows/win32/wes/windows-event-log)\n"
        "- **journalctl (Linux):** consulta e investigação de logs do systemd. "
        "[Acessar](https://www.freedesktop.org/software/systemd/man/journalctl.html)\n"
        "- **ShellCheck:** boas práticas e lint para shell scripts. "
        "[Acessar](https://www.shellcheck.net/)\n"
        "- **ESLint:** análise estática de JavaScript. "
        "[Acessar](https://eslint.org/)\n"
        "- **NIST Cybersecurity Framework (CSF):** base para gestão de risco e controles de cibersegurança. "
        "[Acessar](https://www.nist.gov/cyberframework)\n"
        "- **ISO/IEC 27001 (segurança da informação):** referência para SGSI e governança de segurança. "
        "[Acessar](https://www.iso.org/isoiec-27001-information-security.html)\n"
        "- **COBIT (ISACA):** governança e gestão de TI orientada a objetivos e controles. "
        "[Acessar](https://www.isaca.org/resources/cobit)\n"
        "- **ITIL (AXELOS):** boas práticas para gestão de serviços de TI e operação contínua. "
        "[Acessar](https://www.axelos.com/certifications/itil-service-management)\n"
        "- **MITRE ATT&CK:** matriz de táticas e técnicas para investigação e defesa. "
        "[Acessar](https://attack.mitre.org/)\n"
        "- **OWASP:** guias e padrões para segurança de aplicações. "
        "[Acessar](https://owasp.org/)\n"
        "- **CIS Benchmarks:** hardening e configurações seguras para sistemas e plataformas. "
        "[Acessar](https://www.cisecurity.org/cis-benchmarks)\n"
        "- **Microsoft Learn (PowerShell):** automação e scripts para ambientes Windows. "
        "[Acessar](https://learn.microsoft.com/powershell/)\n"
        "- **Python Docs:** referência oficial para automações e scripts usados no dia a dia. "
        "[Acessar](https://docs.python.org/3/)"
    )

    st.markdown("### Checklist rápido para incidentes")
    st.markdown(
        """
- Definir impacto e prioridade.
- Coletar logs e sintomas objetivos.
- Formular hipótese técnica.
- Executar diagnóstico incremental.
- Aplicar correção com validação.
- Registrar evidências no histórico exportado.
        """
    )

# ----------------------------------------------------------------------
# 2. BARRA LATERAL (SIDEBAR)
# ----------------------------------------------------------------------

with st.sidebar:
    # Logo + apresentação curta
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
            format_unexpected_error_for_ui("Erro ao inicializar cliente Groq.", e)

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
            playbook_data = OPERATIONAL_PLAYBOOK_PROMPTS[categoria_selecionada][cenario_selecionado]
            
            # Exibe os metadados do playbook selecionado
            level = playbook_data.get('level', 'N/A')
            tools = ', '.join(playbook_data.get('tools', []))
            tags = ', '.join(playbook_data.get('tags', []))
            
            st.caption(f"**Nível:** {level} | **Ferramentas:** {tools}")
            st.caption(f"**Tags:** {tags}")
            
            # Constrói o prompt para a IA usando a descrição e o script
            prompt_pronto = (
                f"Gere um procedimento detalhado para a seguinte tarefa:\n\n"
                f"**Descrição:** {playbook_data['description']}\n\n"
                f"**Exemplo de Script/Comando Relacionado (use como base):**\n```\n{playbook_data['script']}\n```"
            )
            
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
            export_content += f"## {role}\n\n"
            export_content += f"{message['content']}\n\n---\n\n"
        return export_content

    # Botão para exportar a conversa (só aparece se houver mensagens)
    if st.session_state.get("messages"):
        st.download_button(
            label="Exportar Conversa",
            data=format_chat_for_export(st.session_state.messages),
            file_name=f"historico_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            help="Baixe o histórico completo da conversa em formato Markdown."
        )

    # Botão para limpar o histórico
    if st.button("Limpar Histórico", help="Apaga todas as mensagens da sessão atual."):
        st.session_state.messages = []
        st.rerun()


    st.divider()
    # --- Seção de Ajuda ---
    st.subheader("Ajuda e FAQ")
    st.caption("Abra um guia completo no painel principal e volte quando quiser.")
    if st.button("Abrir Central de Ajuda", use_container_width=True):
        st.session_state.current_view = "help"
        st.rerun()

    st.divider()
    # --- Seção de Validação de Scripts ---
    st.subheader("Validador de Scripts")
    st.caption("Faça upload de scripts para avaliação técnica fora do chat.")
    if st.button("Abrir Validador de Scripts", use_container_width=True):
        st.session_state.current_view = "script_review"
        st.rerun()

    st.divider()
    # --- Seção de Visualizador de Logs ---
    st.subheader("Visualizador de Logs")
    st.caption("Analise logs e artefatos técnicos para causa raiz e plano de ação.")
    if st.button("Abrir Visualizador de Logs", use_container_width=True):
        st.session_state.current_view = "log_review"
        st.rerun()

    st.divider()
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

if st.session_state.current_view == "help":
    render_help_center()
    st.stop()

if st.session_state.current_view == "script_review":
    render_script_review_center(client, selected_model)
    st.stop()

if st.session_state.current_view == "log_review":
    render_log_analysis_center(client, selected_model)
    st.stop()

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
            format_unexpected_error_for_ui(
                "Falha ao inicializar cliente Groq. Verifique sua chave de API.",
                e,
            )
            st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):
            try:
                # Prepara as mensagens para a API com limite de contexto para evitar estouro de tokens
                history = get_recent_history(st.session_state.messages)
                if len(history) < len(st.session_state.messages):
                    st.caption(f"Contexto reduzido para {len(history)} últimas mensagens para caber no limite do modelo.")
                messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + history

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
                format_groq_error_for_ui("Erro ao processar resposta do assistente.", e)
            except Exception as e:
                format_unexpected_error_for_ui("Erro durante o processamento da resposta.", e)

# --- Rodapé ---
st.markdown(
    '''
    <div style="text-align: center; color: gray;">
        <hr>
        <p>Assistente de IA para Profissionais de TI v1.1</p>
        <p style="text-align: center;">Criado por: Rafael Martiniano</p>
    </div>
    ''',
    unsafe_allow_html=True
)

