<div align="center">
  <img src="https://raw.githubusercontent.com/rmartini3/RM_AssistenteIA/main/IT/favicon.ico" alt="Logo" width="100">
  <h1>Assistente de IA para Profissionais de TI</h1>
  <p>
    Seu assistente inteligente para auxiliar analistas em diagnósticos, troubleshooting e outras atividades relacionadas à TI.
  </p>
</div>

---

Este projeto é um assistente de IA, construído com Streamlit e alimentado pela API da Groq.
Essa Ferramenta foi desenvolvida para auxiliar analistas de operações (N1, N2, N3) e líderes técnicos. Ele funciona como um *runbook* inteligente, fornecendo comandos, scripts e procedimentos operacionais padronizados (POPs) alinhados às melhores práticas de mercado como ITIL, COBIT e ISO 2700x.

<div align="center">
  <img src="https://raw.githubusercontent.com/rmartini3/RM_AssistenteIA/main/IT/.assets/demo.gif" alt="Demonstração do App" width="800">
</div>

## 🎯 Funcionalidades

*   **🧠 Inteligência Especializada:** Treinado com um prompt de sistema robusto para atuar como um especialista em Redes, Segurança, Cloud, Banco de Dados, Suporte Técnico e mais.
*   **⚡ Respostas Rápidas:** Geração de comandos CLI, scripts (Python, PowerShell, Bash) e queries SQL prontos para uso imediato.
*   **📖 Guias HOW-TO:** Cada resposta inclui um guia detalhado explicando o propósito, o funcionamento e a justificativa de governança da solução proposta.
*   **🗂️ Playbooks Operacionais:** Menus de acesso rápido para cenários comuns, agilizando a resolução de incidentes recorrentes.
*   **🎨 Interface Customizável:** A aparência do chat e dos ícones é personalizada via CSS para uma experiência de usuário aprimorada e profissional.
*   **🌓 Tema Adaptativo:** Os estilos customizados se adaptam perfeitamente aos temas claro e escuro nativos do Streamlit.

## 🛠️ Tecnologias

| Tecnologia | Propósito |
| :--- | :--- |
| **Python** | Linguagem principal do projeto. |
| **Streamlit** | Framework para a criação da interface web interativa. |
| **Groq** | API de inferência de LLMs para respostas em tempo real. |
| **Pillow** | Manipulação de imagens para o ícone da aplicação. |
| **python-dotenv**| Gerenciamento de variáveis de ambiente (API Key). |

## 🚀 Executando Localmente

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

**Pré-requisitos:**
*   Python 3.8+
*   Uma chave de API da Groq

**1. Clone o Repositório**
Clone o repositório em um diretório de sua preferência:
```sh
git clone https://github.com/rmartini3/ia-assistente-ti.git
cd ia-assistente-ti
```

**2. Crie e Ative um Ambiente Virtual**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as Dependências**
```bash
pip install -r requirements.txt
```

**4. Configure sua API Key**
Crie um arquivo chamado `.env` na raiz da pasta do projeto, crie um arquivo .env e adicione sua chave da Groq:
```
.env
GROQ_API_KEY="SUA_CHAVE_API_AQUI"
```

**5. Execute a Aplicação**
```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador.

## 🤝 Contribuições

Contribuições são bem-vindas! 
Sinta-se à vontade para abrir uma *issue* para relatar bugs ou sugerir novas funcionalidades. 
Se desejar contribuir com código, por favor, abra um *Pull Request*.