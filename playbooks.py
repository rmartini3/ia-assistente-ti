# c:\Users\Rafael\Desktop\Desenvolvimento\projetos\DEV\RM_AssistenteIA\IT\playbooks.py

"""
Este arquivo centraliza todos os prompts para os Playbooks de Execução Rápida.
A estrutura de dicionário aninhado permite uma organização clara por categoria e cenário,
facilitando a manutenção e a expansão.
"""

OPERATIONAL_PLAYBOOK_PROMPTS = {
    "Redes (NOC)": {
        "Flapping de Interface (Cisco)": "Gere um procedimento para diagnosticar flapping de interface em um switch Cisco, incluindo comandos para verificar logs, contadores de erro e o status da porta.",
        "Alta Latência BGP (Juniper)": "Preciso de um guia para troubleshooting de alta latência em uma sessão BGP em um roteador Juniper. Inclua comandos para verificar a sessão, a tabela de roteamento e testes de conectividade.",
        "OSPF Neighbors Down": "Forneça um procedimento para investigar por que uma adjacência OSPF caiu, com comandos para verificar o status dos vizinhos, logs e configuração da interface.",
        "VLAN Não Configurada": "Como identificar e resolver um problema de 'VLAN não configurada' ou inconsistente em uma rede de switches? Forneça comandos de verificação.",
        "Roteamento Estático – Troubleshooting": "Gere um guia de troubleshooting para uma rota estática que não está funcionando como esperado, incluindo verificação da tabela de roteamento e testes de conectividade.",
        "VPN Site-to-Site Down": "Preciso de um playbook para diagnosticar uma VPN Site-to-Site (IPsec) que está inativa. Inclua comandos para verificar o status do túnel (fase 1 e fase 2) e o tráfego.",
        "Falhas de Resolução DNS": "Forneça um procedimento para diagnosticar falhas de resolução de DNS a partir de um servidor ou cliente, incluindo o uso de `nslookup` ou `dig` e como verificar o cache.",
        "Conflitos de DHCP": "Como detectar e resolver um conflito de IP (IP duplicado) em uma rede gerenciada por DHCP? Inclua comandos para servidores Windows e Linux.",
        "Firewall Policy Misconfig": "Gere um guia para analisar uma política de firewall (Fortinet/Palo Alto) que pode estar bloqueando tráfego legítimo, incluindo como verificar logs e regras.",
        "Switch Port Security Violation": "Qual o procedimento padrão ao receber um alerta de violação de Port Security em um switch Cisco? Inclua comandos para identificar o MAC e reativar a porta.",
    },
    "Sistemas Operacionais": {
        "Processos de Alto Consumo (Linux)": "Gere um comando para identificar os 5 processos com maior consumo de CPU e memória em um servidor Linux, usando `top` ou `ps`.",
        "Verificar Portas Abertas (Windows)": "Forneça um script PowerShell para listar todas as portas TCP/UDP abertas em um servidor Windows e os processos associados a elas.",
        "Análise Rápida de Logs (Bash)": "Preciso de um comando `grep` e `awk` para encontrar erros ('ERROR' ou 'Failed') em um arquivo de log grande (`/var/log/syslog`) e contar as ocorrências.",
        "Análise de Kernel Panic (macOS)": "Como realizar uma análise inicial de um log de Kernel Panic em um macOS para identificar a possível causa?",
        "Android App Crash Analysis": "Forneça o comando `adb logcat` para filtrar e analisar o log de um aplicativo que está fechando inesperadamente (crash) em um dispositivo Android.",
        "Coletar Sysdiagnose (iOS)": "Qual o procedimento para gerar e coletar um `sysdiagnose` de um iPhone para analisar problemas de performance ou rede?",
        "Análise de Uso de Disco (Linux)": "Gere um comando para listar os diretórios que mais consomem espaço em disco a partir da raiz (`/`), ordenados por tamanho.",
        "Identificar Consumo Anômalo de CPU": "Preciso de um procedimento para investigar um pico anômalo de CPU em um servidor Windows, usando o Gerenciador de Tarefas e o Monitor de Recursos.",
        "Serviço Parado (Windows/Linux)": "Forneça os comandos para verificar o status de um serviço (ex: 'apache2' ou 'w3svc') e reiniciá-lo, tanto em Linux (systemd) quanto em Windows (PowerShell).",
        "Script de Backup Simples (Bash)": "Crie um script bash simples para fazer backup de um diretório (`/var/www`) para um arquivo .tar.gz com data no nome, e como agendá-lo com `cron`.",
    },
    "Cloud Híbrida": {
        "Verificar Status de VM (AWS EC2)": "Gere um comando AWS CLI para verificar o status de uma instância EC2 específica, incluindo os status checks, e como reiniciá-la se necessário.",
        "Inventário de VMs (GCP)": "Forneça um comando `gcloud` para listar todas as instâncias de VM em um projeto GCP, exibindo nome, status, zona e endereço IP.",
        "Latência em API (Azure Web App)": "Qual o procedimento para diagnosticar alta latência em uma Azure Web App, incluindo como verificar os logs e o Health Check?",
        "Auditoria de Política IAM (AWS)": "Preciso de um comando AWS CLI para listar as políticas IAM anexadas a um usuário específico e analisar suas permissões.",
        "Auditoria de Storage (Azure)": "Como verificar se os contêineres de um Azure Storage Account têm acesso público anônimo habilitado, usando Azure CLI?",
        "Análise de Roteamento Cloud (AWS)": "Gere um comando AWS CLI para descrever a tabela de rotas associada a uma subnet específica em uma VPC.",
        "Verificar Integridade de Snapshot (AWS)": "Qual o procedimento para verificar se um snapshot de um volume EBS foi concluído com sucesso e está disponível?",
        "Identificar Recursos Ociosos (GCP)": "Forneça um comando `gcloud` para identificar discos persistentes não anexados a nenhuma instância de VM, para otimização de custos.",
        "Inventário Multi-Region (AWS)": "Crie um script (Bash ou Python) que use AWS CLI para listar todas as instâncias EC2 em todas as regiões da AWS.",
        "Verificar Regras de Firewall (Azure)": "Forneça um comando Azure CLI para listar as regras de um Network Security Group (NSG) específico.",
    },
    "Segurança / SOC": {
        "Supressão de Alertas Duplicados (SIEM)": "Descreva um procedimento padrão para criar uma regra de supressão para um alerta de segurança que está gerando muitos falsos positivos duplicados em um SIEM (ex: Splunk/QRadar).",
        "Análise de Falso Positivo": "Qual o processo para analisar um alerta de 'Malware Detecctado' e classificá-lo como um falso positivo? Inclua passos como análise de hash e comportamento.",
        "Quarentena de Porta (Cisco)": "Gere o procedimento e os comandos para colocar uma porta de switch Cisco em uma VLAN de quarentena em resposta a um alerta de malware.",
        "Análise de Logs IDS/IPS": "Como analisar um log de um alerta do Snort/Suricata para entender um possível ataque? Peça um exemplo de log e como interpretá-lo.",
        "Verificação de Regras WAF": "Preciso de um guia para verificar por que um WAF (ex: Cloudflare/AWS WAF) está bloqueando uma requisição legítima de um usuário.",
        "Investigação de Acesso VPN Anômalo": "Qual o procedimento para investigar um alerta de login VPN bem-sucedido de um local incomum? Inclua passos de verificação e contato com o usuário.",
        "Análise de Alerta de EDR": "Recebi um alerta crítico de um EDR (ex: CrowdStrike/SentinelOne). Qual o playbook de resposta a incidentes imediato? (isolar host, coletar artefatos, etc.)",
        "Correlação de Logs no SIEM": "Como criar uma query de correlação em um SIEM para cruzar logs de firewall, proxy e Active Directory para um usuário específico em uma janela de tempo?",
        "Busca por IOCs": "Forneça um script (PowerShell ou Bash) para buscar uma lista de IOCs (hashes de arquivo, IPs) em um sistema local ou em logs.",
        "Detecção de 'Shadow Credentials'": "Qual o procedimento para detectar o uso de credenciais suspeitas ou não autorizadas, analisando logs de autenticação do Active Directory?",
    },
    "Banco de Dados & Triggers": {
        "Identificar Query Lenta (PostgreSQL)": "Forneça uma query SQL para o PostgreSQL que identifique as consultas mais lentas em execução ou executadas recentemente, usando `pg_stat_activity`.",
        "Sessões Suspeitas (SQL Server)": "Gere uma query para SQL Server que liste todas as sessões ativas, mostrando o usuário, host de origem e a última query executada, para identificar atividades fora do horário comercial.",
        "Auditoria em Tabelas Críticas (Oracle)": "Como habilitar a auditoria padrão do Oracle (`AUDIT`) para todas as operações (SELECT, INSERT, UPDATE, DELETE) em uma tabela crítica como `HR.EMPLOYEES`?",
        "Trigger de Auditoria Universal (MySQL)": "Crie um exemplo de trigger para MySQL/MariaDB que registre qualquer alteração (INSERT, UPDATE, DELETE) em uma tabela específica para uma tabela de log de auditoria.",
        "Trigger de Prevenção de Mass Delete": "Crie um trigger para SQL Server ou PostgreSQL que impeça a exclusão de mais de 100 registros de uma tabela de uma só vez, como medida de segurança.",
        "Exportar Logs para SIEM": "Descreva um método para exportar logs de auditoria de um banco de dados (ex: PostgreSQL) para um formato (como JSON ou CSV) que possa ser ingerido por um SIEM.",
        "Verificar Integridade de Backup": "Qual o comando para verificar a integridade de um arquivo de backup do SQL Server (`.bak`) sem restaurá-lo completamente?",
        "Diagnóstico de Locks e Deadlocks": "Forneça uma query para identificar `locks` e `deadlocks` em um banco de dados PostgreSQL ou SQL Server.",
        "Monitoramento de Operações (MongoDB)": "Qual comando no `mongosh` pode ser usado para monitorar as operações em tempo real em um banco de dados MongoDB?",
        "Trigger em Cloud DB (AWS Aurora)": "Como criar um trigger em um banco de dados AWS Aurora (compatível com MySQL) que invoque uma função Lambda para enviar um alerta ao SIEM?",
    },
    "Shadow IT": {
        "Scan de Hosts Ativos na LAN": "Forneça um script bash de uma linha usando `nmap` para escanear uma sub-rede (ex: 192.168.1.0/24), identificar hosts ativos e exportar a lista para um arquivo CSV.",
        "Descoberta de EC2 não Documentado (AWS)": "Crie um script que use a AWS CLI para listar todas as instâncias EC2 e compare com uma lista de instâncias aprovadas em um arquivo CSV, reportando as não documentadas.",
        "Descoberta de VMs não Documentadas (GCP)": "Forneça um comando `gcloud` para listar todas as VMs e filtre por aquelas que não possuem uma `label` específica, como 'owner' ou 'project'.",
        "Detecção de SaaS via Logs de Firewall": "Como analisar logs de um firewall de borda para identificar tráfego para domínios de serviços SaaS conhecidos e não autorizados (ex: Dropbox, Trello)?",
        "Descoberta de IoT/Raspberry na Rede": "Qual a melhor abordagem com `nmap` para descobrir dispositivos IoT ou Raspberry Pi em uma rede, buscando por portas ou serviços comuns (SSH, VNC, etc.)?",
        "Scan de Containers não Autorizados": "Como escanear uma rede para encontrar hosts executando o Docker Engine (porta 2375/2376) que não deveriam estar lá?",
        "Inventário de VMs Locais (VirtualBox)": "Forneça um comando para listar todas as VMs existentes no VirtualBox em uma máquina local usando `VBoxManage`.",
        "Análise de Tráfego Proxy para SaaS": "Gere um guia sobre como usar os logs de um proxy (ex: Squid) para gerar um relatório dos principais domínios acessados, ajudando a identificar o uso de Shadow SaaS.",
        "Inventário de Agentes em Endpoints": "Como criar um script PowerShell para ser executado em um endpoint Windows e listar todos os softwares instalados, para identificar agentes não autorizados?",
        "Detecção de Shadow Storage (AWS)": "Forneça um comando AWS CLI para listar todos os buckets S3 que estão publicamente acessíveis em uma conta, um sinal comum de Shadow Storage.",
    },
    # Adicione as outras categorias e cenários aqui, seguindo o mesmo padrão.
}