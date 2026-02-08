<div align="center">
  <img src="https://raw.githubusercontent.com/rmartini3/ia-assistente-ti/main/.assets/Logo_RM_Gold.png" alt="Logo" width="100">
  <h1>Assistente de IA para Profissionais de TI</h1>
  <p>Copiloto para diagnósticos, troubleshooting, automação e análise operacional.</p>
</div>

---

Aplicação em Streamlit integrada à API da Groq para apoiar times de Suporte Técnico, Service Desk, Field Services, NOC e SOC com orientação técnica, playbooks e análise assistida.

## Novidades da versão 1.1
- Central de Ajuda e FAQ no app (fora do chat).
- Validador de Scripts com dois modos:
  - Anexar arquivo completo.
  - Analisar linha/bloco de código (análise superficial/indicativa).
- Suporte de scripts para: `.cmd`, `.bat`, `.sh`, `.ps1`, `.html`, `.css`, `.js`, `.java`, `.py`, `.xml`, `.json`.
- Visualizador e Analisador de Logs com suporte multi-formato (incluindo artefatos binários com metadados/hash).
- Tratamento de erros amigável para integração com Groq, com detalhes técnicos expandíveis.
- FAQ ampliado com comparativo de modelos e referências externas (W3C, NIST, ITIL, COBIT, ISO).

## Funcionalidades
- Assistente conversacional técnico com foco operacional.
- Playbooks para cenários recorrentes (NOC, SOC, Cloud, ITSM, Infra etc.).
- Exportação de conversa em Markdown.
- Validação estática de scripts com checklist de melhorias.
- Investigação assistida de logs para causa raiz e plano de ação.

## Stack
- Python
- Streamlit
- Groq SDK
- python-dotenv
- CSS customizado

## Execução local
Pré-requisitos: Python 3.8+ e chave de API da Groq.

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

4. Configure a chave
Crie um arquivo `.env` na raiz:
```env
GROQ_API_KEY="SUA_CHAVE_API_AQUI"
```

5. Inicie o app
```bash
streamlit run app.py
```

## Segurança e conduta
- Política de segurança: veja `SECURITY.md`.
- Código de conduta: veja `CODE_OF_CONDUCT.md`.
- Este projeto não executa automaticamente scripts enviados; a análise é estática e assistida por IA.

## Limitações importantes
- A análise por linha/bloco de código é parcial e pode não refletir todo o comportamento de execução.
- Resultados do validador e do analisador de logs são indicativos e devem ser validados em ambiente de testes.
- Conformidade formal (W3C/ISO/COBIT/ITIL) depende de processo e auditoria, não apenas da saída da IA.

## Contribuições
Contribuições são bem-vindas via Issues e Pull Requests.

## Contato
- LinkedIn: https://linkedin.com/in/rafael-martiniano
- Email: rmartini3corp@outlook.com
