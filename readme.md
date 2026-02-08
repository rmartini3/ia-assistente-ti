<div align="center">
  <img src="https://raw.githubusercontent.com/rmartini3/ia-assistente-ti/main/.assets/Logo_RM_Gold.png" alt="Logo" width="100">
  <h1>Assistente de IA para Profissionais de TI</h1>
  <p>
    Copiloto para diagnósticos, troubleshooting e automação operacional.
  </p>
</div>

---

Este projeto é um assistente de IA construído em Streamlit e alimentado pela API da Groq. Ele funciona como um runbook inteligente para analistas N1, N2, N3 e líderes técnicos, entregando comandos, scripts e procedimentos alinhados a ITIL, COBIT e ISO 2700x.

<div align="center">
  <img src="https://raw.githubusercontent.com/rmartini3/ia-assistente-ti/main/.assets/demo.gif" alt="Demonstração do App" width="800">
</div>

## Funcionalidades
- Inteligência especializada: respostas para Redes, Segurança, Cloud, Banco de Dados, Suporte Técnico e mais.
- Respostas rápidas: comandos CLI, scripts (Python, PowerShell, Bash) e queries SQL prontos para uso.
- Guias HOW-TO: padrão (Diagnóstico, Comando, Guia de Execução, Referência Oficial).
- Playbooks operacionais: catálogos para NOC, SOC, Cloud, ERP, ITSM, Infra, Hardware etc.
- Governança: alinhado a ITIL, COBIT, ISO 27001, NIST.
- Interface customizada: chat estilizado via CSS com suporte a temas claro/escuro.

## Tecnologias
| Tecnologia | Propósito |
| :--- | :--- |
| **Python** | Linguagem principal |
| **Streamlit** | Interface web |
| **Groq** | Inferência LLM |
| **Pillow** | Manipulação de imagens do app |
| **python-dotenv** | Variáveis de ambiente (API Key) |

## Execução Local
**Pré-requisitos**: Python 3.8+ e chave de API da Groq.

1. Clone o repositório  
   ```bash
   git clone https://github.com/rmartini3/ia-assistente-ti.git
   cd ia-assistente-ti
   ```
2. Crie e ative o ambiente virtual  
   ```powershell
   # Windows
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```  
   ```bash
   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instale as dependências  
   ```bash
   pip install -r requirements.txt
   ```
4. Configure sua API Key  
   Crie um `.env` na raiz com:  
   ```
   GROQ_API_KEY="SUA_CHAVE_API_AQUI"
   ```
   Se não criar o `.env`, informe a chave na barra lateral do app.
5. Execute a aplicação  
   ```bash
   streamlit run app.py
   ```
   O navegador abre em http://localhost:8501 (por padrão).

## Atalho rápido (Windows)
Se quiser um atalho manual, crie um arquivo `executar-assistente.bat` com:
```
@echo off
rem Ajuste a pasta abaixo para onde o projeto/instalação está:
rem Exemplo recomendado: C:\Windows\Temp\AssistenteIATI
rem Outro exemplo: C:\Users\SeuUsuario\Documents\Projetos\AssistenteIATI
pushd "C:\Windows\Temp\AssistenteIATI"
call .\.venv\Scripts\activate
streamlit run app.py
popd
pause
```
Duplo-clique para iniciar; a URL aparece no console.
Alternativa: execute `instalar-assistente.cmd` para criar atalho automaticamente.

## Instalador simples (.cmd)
Para copiar o app, criar atalho na Área de Trabalho e opcionalmente limpar o zip/origem:
1. Baixe e descompacte o projeto.
2. Execute `instalar-assistente.cmd`.
3. Informe a pasta de instalação (padrão recomendado: `C:\Windows\Temp\AssistenteIATI`). Se preferir, digite outro caminho, por exemplo `C:\Users\SeuUsuario\Documents\Projetos\AssistenteIATI`.
4. O script cria atalho no Desktop apontando para `run_app.exe` ou `app.exe` (se existir) ou para `executar-assistente.bat` após montar venv e instalar dependências.
5. Opcionalmente apaga o zip e a pasta de origem usados na instalação.

## Gerar executável (Windows)
Empacote com PyInstaller (opcional, se quiser distribuir em um único `.exe`):
```powershell
pip install pyinstaller
pyinstaller --noconfirm --onefile ^
  --add-data "style.css;." ^
  --add-data "system_prompt.md;." ^
  --add-data "favicon.ico;." ^
  --add-data "playbooks.py;." ^
  app.py
```
O binário sai em `dist/app.exe`; ao rodar, abre o servidor local e imprime a URL.

## Contribuições
Contribuições são bem-vindas! Abra uma issue para bugs/ideias ou um Pull Request para código.

