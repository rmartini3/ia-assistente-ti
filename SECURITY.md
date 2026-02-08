# Política de Segurança

Obrigado por ajudar a manter o **Assistente de IA para Profissionais de TI** seguro.

## Versões com suporte

| Versão | Suporte |
| :--- | :--- |
| 1.1.x | ✅ Suportada |
| < 1.1 | ⚠️ Sem suporte ativo |

## Como reportar vulnerabilidades

Se você identificar uma vulnerabilidade de segurança:

1. **Não abra issue pública** com detalhes sensíveis.
2. Envie um email para: **rmartini3corp@outlook.com**
3. Inclua, se possível:
   - Descrição do problema.
   - Passos para reproduzir.
   - Impacto estimado.
   - Evidências (logs, prints, payloads, POC mínima).

## O que esperar após o reporte

- Confirmação de recebimento em até **5 dias úteis**.
- Triagem inicial com classificação de severidade.
- Plano de correção conforme impacto.
- Atualização sobre status até a resolução.

## Boas práticas para usuários

- Não compartilhe chaves de API em commits, screenshots ou logs públicos.
- Use `.env` para segredos e mantenha-o fora do versionamento.
- Valide scripts e recomendações da IA em ambiente de testes antes de produção.
- Revise permissões e impacto de automações antes de execução.

## Escopo desta política

Esta política cobre principalmente:
- Código e configurações deste repositório.
- Fluxo de integração com API de IA.
- Superfícies de entrada de scripts e logs analisados no app.

Não cobre incidentes de terceiros fora do controle do projeto (provedores externos, contas pessoais comprometidas, etc.).
