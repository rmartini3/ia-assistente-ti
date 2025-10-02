<div align="center">
  <img src="https://raw.githubusercontent.com/rmartini3/ia-assistente-ti/main/.assets/Logo_RM_Gold.png" alt="Logo" width="100">
  <h1>Assistente de IA para Profissionais de TI</h1>
  <p>
    Seu assistente inteligente para auxiliar analistas em diagnósticos, troubleshooting e outras atividades relacionadas à TI.
  </p>
</div>

---

Este projeto é um assistente de IA, construído com Streamlit e alimentado pela API da Groq.
Essa Ferramenta foi desenvolvida para auxiliar analistas de operações (N1, N2, N3) e líderes técnicos. Ele funciona como um *runbook* inteligente, fornecendo comandos, scripts e procedimentos operacionais padronizados (POPs) alinhados às melhores práticas de mercado como ITIL, COBIT e ISO 2700x.

<div align="center">
  <img src="https://raw.githubusercontent.com/rmartini3/ia-assistente-ti/main/.assets/demo.gif" alt="Demonstração do App" width="800">
</div>

## 🎯 Funcionalidades

*   **🧠 Inteligência Especializada:** Treinado com um prompt de sistema robusto para atuar como um especialista em Redes, Segurança, Cloud, Banco de Dados, Suporte Técnico e mais.
*   **⚡ Respostas Rápidas:** Geração de comandos CLI, scripts (Python, PowerShell, Bash) e queries SQL prontos para uso.
*   **📖 Guias HOW-TO:** Cada resposta segue um padrão rigoroso (Diagnóstico, Comando, Guia de Execução, Referência Oficial) para garantir clareza e conformidade.
*   **🗂️ Playbooks Operacionais:** Um vasto catálogo de cenários pré-definidos para NOC, SOC, Cloud, ERP, ITSM, Infraestrutura, Hardware e mais, agilizando a resolução de incidentes.
*   **🔒 Foco em Governança:** As soluções são alinhadas com as melhores práticas de mercado como ITIL, COBIT, ISO 27001 e NIST.
*   **🎨 Interface Intuitiva:** A aparência do chat é customizada via CSS para uma experiência de usuário aprimorada e profissional, com suporte a temas claro e escuro.

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
-```bash
```sh
pip install -r requirements.txt


**4. Configure sua API Key**
Crie um arquivo chamado `.env` na raiz da pasta do projeto, após criar o arquivo .env, adicione sua chave da Groq:
```
.env
GROQ_API_KEY="SUA_CHAVE_API_AQUI"
```
#OBS: Caso não crie o arquivo .env, terá que colocar a chave manualmente!!!!

**5. Execute a Aplicação**
```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador.

## 🤝 Contribuições

Contribuições são bem-vindas! 
Sinta-se à vontade para abrir uma *issue* para relatar bugs ou sugerir novas funcionalidades. 
Se desejar contribuir com código, por favor, abra um *Pull Request*.
