# c:\Users\Rafael\Desktop\Desenvolvimento\projetos\DEV\RM_AssistenteIA\IT\playbooks.py

"""
Este arquivo centraliza todos os prompts para os Playbooks de Execução Rápida.
A estrutura de dicionário aninhado permite uma organização clara por categoria e cenário,
facilitando a manutenção e a expansão.
"""

"""
Estrutura dos playbooks:
- Dicionário de primeiro nível: categorias (ex.: ERP, CRM, ITSM).
- Segundo nível: cenários ou SOPs dentro de cada categoria.
- Cada cenário contém metadados (level, tags, tools, os) e um script ou instrução base.
Use this file to expand or ajustar prompts reutilizados na sidebar do app.
"""

OPERATIONAL_PLAYBOOK_PROMPTS = {
    "ERP (SAP, Oracle, Dynamics)": {
        "SOP: Análise de Job com Falha (SAP)": {
            "description": "Crie um SOP para um analista N2 investigar um job que falhou no SAP. O procedimento deve incluir: 1. Uso da transação SM37 para visualizar o log do job. 2. Identificação da mensagem de erro. 3. Verificação de logs do sistema (ST22 para dumps). 4. Escalonamento para o time N3 com as evidências coletadas.",
            "level": "N2", "tags": ["ERP", "SAP", "Troubleshooting"], "tools": ["SAP GUI"], "os": ["Windows"],
            "script": "# Placeholder para comando ou anotação relevante."
        },
        "Playbook: Monitoramento de Job (Oracle EBS)": {
            "description": "Gere um script SQL para Oracle que verifica o status de 'Concurrent Requests' no Oracle EBS, retornando jobs que estão em execução por mais de X horas ou que terminaram com erro. O script deve ser adaptável para ferramentas de monitoramento.",
            "level": "N3", "tags": ["ERP", "Oracle", "Automation", "Monitoring"], "tools": ["Oracle EBS", "SQL Developer"], "os": ["Linux", "Windows"],
            "script": "SELECT request_id, status_code, phase_code FROM fnd_concurrent_requests WHERE status_code = 'E' OR (phase_code = 'R' AND (SYSDATE - last_update_date) * 24 > 4);"
        },
    },
    "CRM (Salesforce, Dynamics, HubSpot)": {
        "SOP: Cadastro de Lead em Massa (Salesforce)": {
            "description": "Crie um SOP para um analista N1 realizar a importação de uma lista de leads em CSV para o Salesforce usando o 'Data Import Wizard', incluindo a verificação de campos obrigatórios e o tratamento de erros.",
            "level": "N1", "tags": ["CRM", "Salesforce", "Data Import"], "tools": ["Salesforce"], "os": ["Any"],
            "script": "# Procedimento manual, sem script aplicável."
        },
        "Playbook: Script de Extração de Dados via API (Salesforce)": {
            "description": "Crie um script Python que use a API REST do Salesforce (biblioteca simple-salesforce) para extrair todos os contatos de uma determinada conta e salvar em um arquivo JSON.",
            "level": "N3", "tags": ["CRM", "Salesforce", "API", "Automation"], "tools": ["Python", "VS Code"], "os": ["Windows", "Linux", "macOS"],
            "script": "from simple_salesforce import Salesforce\n\nsf = Salesforce(username='user', password='password', security_token='token')\n\n# Exemplo de query\nrecords = sf.query(\"SELECT Id, Name FROM Contact WHERE Account.Name = 'Exemplo Corp'\")"
        },
    },
    "ITSM (ServiceNow, Jira, GLPI)": {
        "SOP: Criação de Ticket Crítico (P1)": {
            "description": "Crie um SOP para um analista N1 registrar um incidente crítico (P1) no ServiceNow, incluindo: 1. Preenchimento dos campos obrigatórios. 2. Associação de CIs (Itens de Configuração) afetados. 3. Acionamento do workflow de incidente maior. 4. Escalonamento imediato para o gestor de incidentes.",
            "level": "N1", "tags": ["ITSM", "ServiceNow", "Incident Management"], "tools": ["ServiceNow"], "os": ["Any"],
            "script": "# Procedimento manual, sem script aplicável."
        },
        "Playbook: Script de Relatório de SLA (Jira)": {
            "description": "Crie um script em Python que use a API REST do Jira para extrair dados de SLA (tickets que violaram o SLA de resolução) de um projeto específico e gerar um relatório em CSV.",
            "level": "N3", "tags": ["ITSM", "Jira", "API", "Reporting"], "tools": ["Python", "Jira API"], "os": ["Windows", "Linux", "macOS"],
            "script": "import requests\n\n# Exemplo de chamada à API do Jira\nresponse = requests.get('https://your-jira.com/rest/api/2/search?jql=project=HELPDESK AND \"SLA\" = breached()')"
        },
    },
    "NOC - Monitoramento e Redes (Zabbix, PRTG)": {
        "[PRTG] SOP: Triagem de Alerta de Banda": {
            "description": "Procedimento para um operador N1 revisar um alerta de alto consumo de banda no PRTG, identificar o host de origem e o destino, e escalar para o time de redes N2 se o tráfego for inesperado.",
            "level": "N1", "tags": ["NOC", "Monitoring", "PRTG"], "tools": ["PRTG"], "os": ["Windows"],
            "script": "# Procedimento de análise no dashboard do PRTG."
        },
        "[Zabbix] Playbook: Script de Manutenção via API": {
            "description": "Crie um script Python que use a API do Zabbix para colocar um grupo de hosts em modo de manutenção por um período determinado, útil para janelas de atualização.",
            "level": "N2", "tags": ["NOC", "Zabbix", "Automation", "API"], "tools": ["Zabbix API", "Python"], "os": ["Linux"],
            "script": "# Exemplo de payload para a API do Zabbix: zabbix_api.maintenance.create(...)"
        },
        "[SolarWinds] Playbook: Monitorar Nós via API": {
            "description": "Gere um script PowerShell que use a API da SolarWinds para consultar o status de um nó específico e retornar informações como CPU, memória e tempo de resposta.",
            "level": "N2", "tags": ["NOC", "SolarWinds", "Monitoring", "API"], "tools": ["SolarWinds"], "os": ["Windows"],
            "script": "# Invoke-RestMethod -Uri 'https://your-solarwinds:17778/SolarWinds/InformationService/v3/Json/Query' ..."
        },
        "[Nagios] Playbook: Checagem de Serviço via NRPE": {
            "description": "Forneça o comando para um analista N1 executar manualmente uma checagem de um serviço (ex: HTTP) em um host remoto usando o `check_nrpe` a partir do servidor Nagios.",
            "level": "N1", "tags": ["NOC", "Nagios", "Troubleshooting"], "tools": ["Nagios"], "os": ["Linux"],
            "script": "/usr/local/nagios/libexec/check_nrpe -H <host_ip> -c check_http"
        },
        "[Grafana] Playbook: Criação de Dashboard via API": {
            "description": "Crie um script Python que use a API REST do Grafana para criar um novo dashboard a partir de um arquivo de modelo JSON, automatizando a configuração de visualizações.",
            "level": "N3", "tags": ["NOC", "Grafana", "Automation", "API"], "tools": ["Grafana"], "os": ["Linux", "Windows", "macOS"],
            "script": "# requests.post('http://your-grafana/api/dashboards/db', json=dashboard_json, headers=headers)"
        },
        "[Prometheus] SOP: Análise de Regra de Alerta": {
            "description": "Crie um SOP para um analista N2 revisar e validar uma regra de alerta (Alerting Rule) em Prometheus, verificando a sintaxe da expressão PromQL e os limiares definidos.",
            "level": "N2", "tags": ["NOC", "Prometheus", "Monitoring"], "tools": ["Prometheus"], "os": ["Linux"],
            "script": "# promtool check rules /path/to/rules.yml"
        },
    },
    "SOC - Segurança (Splunk, QRadar, CrowdStrike)": {
        "SOP: Triagem de Alerta de Segurança (Splunk)": {
            "description": "Procedimento para um operador N1 analisar e classificar um alerta de segurança no Splunk, verificando se é um falso positivo ou um incidente real, e escalando para o N2 com as informações relevantes.",
            "level": "N1", "tags": ["SOC", "Security", "Splunk", "SIEM"], "tools": ["Splunk"], "os": ["Any"],
            "script": "index=wineventlog EventCode=4625 | stats count by src_ip, user | where count > 10"
        },
        "[CrowdStrike] Playbook: Script de Isolamento de Host": {
            "description": "Crie um script Python que use a API do CrowdStrike Falcon para isolar um host da rede com base no seu ID de dispositivo (AID), como uma ação de resposta a incidente.",
            "level": "N2", "tags": ["SOC", "EDR", "CrowdStrike", "Automation"], "tools": ["CrowdStrike API", "Python"], "os": ["Any"],
            "script": "# Exemplo de chamada à API: POST /devices/actions/v1?action_name=contain"
        },
        "[QRadar] Playbook: Criação de Regra de Correlação": {
            "description": "Gere um guia para um especialista N3 criar uma regra de correlação no QRadar que dispare um alerta quando houver 5 falhas de login seguidas de um sucesso para o mesmo usuário em menos de 1 minuto.",
            "level": "N3", "tags": ["SOC", "QRadar", "SIEM", "Correlation"], "tools": ["QRadar"], "os": ["Any"],
            "script": "# Procedimento na interface do QRadar: Rules -> Actions -> New Event Rule."
        },
        "[Elastic Security] Playbook: Busca de Ameaças (Threat Hunting)": {
            "description": "Forneça uma query KQL (Kibana Query Language) para um analista N2 buscar por processos iniciados a partir de um documento do Microsoft Office (winword.exe, excel.exe) nos logs de endpoint.",
            "level": "N2", "tags": ["SOC", "Elastic", "SIEM", "Threat Hunting"], "tools": ["Elastic Security", "Kibana"], "os": ["Any"],
            "script": "process.parent.name: (winword.exe or excel.exe or powerpnt.exe) and process.name: (powershell.exe or cmd.exe or wscript.exe)"
        },
        "[SentinelOne] SOP: Remediação de Ameaça": {
            "description": "Crie um SOP para um analista N1 usar o console do SentinelOne para remediar uma ameaça detectada, incluindo as opções de 'Quarantine', 'Kill' e 'Rollback'.",
            "level": "N1", "tags": ["SOC", "EDR", "SentinelOne", "Response"], "tools": ["SentinelOne"], "os": ["Any"],
            "script": "# Procedimento manual no console do SentinelOne."
        },
        "[Defender ATP] Playbook: Investigação Avançada": {
            "description": "Forneça uma query de 'Advanced Hunting' para o Microsoft Defender ATP para um analista N2 listar todas as conexões de rede de saída feitas pelo processo `powershell.exe` nos últimos 7 dias.",
            "level": "N2", "tags": ["SOC", "EDR", "Defender ATP", "Threat Hunting"], "tools": ["Defender ATP"], "os": ["Windows"],
            "script": "DeviceNetworkEvents | where InitiatingProcessFileName =~ 'powershell.exe' and ActionType == 'ConnectionSuccess'"
        },
    },
    "Infraestrutura & Virtualização (VMware, Hyper-V)": {
        "SOP: Provisionamento de VM (VMware)": {
            "description": "Procedimento para um analista N2 provisionar uma nova máquina virtual no vSphere a partir de um template, incluindo configuração de rede e storage.",
            "level": "N2", "tags": ["Infra", "Virtualization", "VMware"], "tools": ["vSphere", "vCenter"], "os": ["Windows", "Linux"],
            "script": "# Procedimento manual no vCenter."
        },
        "Playbook: Script de Snapshot e Rollback (Hyper-V)": {
            "description": "Crie um script PowerShell para um analista N2 criar um checkpoint (snapshot) de uma VM no Hyper-V antes de uma mudança e, se necessário, realizar o rollback para esse checkpoint.",
            "level": "N2", "tags": ["Infra", "Virtualization", "Hyper-V"], "tools": ["Hyper-V Manager", "PowerShell"], "os": ["Windows"],
            "script": "Checkpoint-VM -Name 'MyVM' -SnapshotName 'Before-Update'\n# Restore-VMSnapshot -Name 'MyVM' -SnapshotName 'Before-Update'"
        },
        "[Proxmox] Playbook: Gerenciamento de Container LXC": {
            "description": "Forneça os comandos da CLI do Proxmox (`pct`) para um analista N2 iniciar, parar e criar um snapshot de um container LXC.",
            "level": "N2", "tags": ["Infra", "Proxmox", "Virtualization", "Container"], "tools": ["Proxmox"], "os": ["Linux"],
            "script": "pct start <vmid>\npct stop <vmid>\npct snapshot <vmid> <snapshot_name>"
        },
        "[Citrix Xen] Playbook: Provisionamento de VM via CLI": {
            "description": "Gere os comandos `xe` para a CLI do XenServer para um especialista N3 criar uma nova VM a partir de um template, configurar sua rede e iniciar a máquina.",
            "level": "N3", "tags": ["Infra", "Citrix", "Xen", "Virtualization"], "tools": ["XenServer"], "os": ["Linux"],
            "script": "# xe vm-install template='MyTemplate' new-name-label='NewVM'\n# xe vif-create ...\n# xe vm-start vm='NewVM'"
        },
        "[Kubernetes] Playbook: Diagnóstico de Pod com Falha": {
            "description": "Forneça os comandos `kubectl` para um analista N2 diagnosticar um pod que está no estado 'CrashLoopBackOff', incluindo como ver os logs, descrever o pod e verificar eventos.",
            "level": "N2", "tags": ["Infra", "Kubernetes", "Container", "Troubleshooting"], "tools": ["kubectl"], "os": ["Linux"],
            "script": "kubectl logs <pod-name>\nkubectl describe pod <pod-name>\nkubectl get events"
        },
        "[Docker] SOP: Limpeza de Recursos Não Utilizados": {
            "description": "Crie um SOP para um analista N2 realizar uma limpeza segura de recursos não utilizados do Docker, como containers parados, imagens 'dangling' e volumes não associados.",
            "level": "N2", "tags": ["Infra", "Docker", "Container", "Maintenance"], "tools": ["Docker"], "os": ["Linux", "Windows"],
            "script": "docker system prune -a"
        },
    },
    "Cloud (AWS, Azure, GCP)": {
        "SOP: Provisionamento de Instância EC2 (AWS)": {
            "description": "Crie um SOP para um analista N2 provisionar uma nova instância EC2 na AWS, incluindo: 1. Seleção da AMI e tipo de instância. 2. Configuração de VPC, subnet e Security Group. 3. Associação de chave SSH. 4. Aplicação de tags de identificação.",
            "level": "N2", "tags": ["Cloud", "AWS", "EC2"], "tools": ["AWS Console"], "os": ["Linux", "Windows"],
            "script": "# Procedimento manual no Console AWS."
        },
        "Playbook: Script de Otimização de Custos (Azure)": {
            "description": "Crie um script PowerShell usando o módulo Az para identificar recursos ociosos no Azure, como discos não anexados ou IPs públicos não associados, e exportar a lista para um CSV.",
            "level": "N3", "tags": ["Cloud", "Azure", "Cost Optimization"], "tools": ["Azure PowerShell"], "os": ["Windows"],
            "script": "Get-AzDisk | Where-Object { $_.ManagedBy -eq $null } | Select-Object Name, ResourceGroupName"
        },
        "[GCP] Playbook: Auditoria de Recursos": {
            "description": "Forneça um comando `gcloud` para um analista N3 listar todas as instâncias de VM em um projeto que não possuem uma `label` específica, como 'owner' ou 'cost-center', para fins de auditoria.",
            "level": "N3", "tags": ["Cloud", "GCP", "Audit", "Governance"], "tools": ["gcloud"], "os": ["Linux", "Windows", "macOS"],
            "script": "gcloud compute instances list --filter='-labels.owner:*'"
        },
        "[Oracle Cloud] Playbook: Gerenciamento de Recursos": {
            "description": "Gere um comando da OCI CLI para um analista N2 listar todas as instâncias de computação em um compartimento específico, exibindo seu estado e forma (shape).",
            "level": "N2", "tags": ["Cloud", "Oracle", "OCI"], "tools": ["OCI CLI"], "os": ["Linux", "Windows"],
            "script": "oci compute instance list -c <compartment_ocid> --query 'data[*].{Name:\"display-name\", State:\"lifecycle-state\", Shape:shape}'"
        },
    },
    "Hardware & Periféricos": {
        "SOP: Busca de Drivers por Modelo": {
            "description": "Crie um SOP para um analista N1 encontrar e baixar drivers para um dispositivo ou periférico (ex: impressora, placa de vídeo, scanner, smartphone) a partir do site oficial do fabricante. O procedimento deve incluir: 1. Identificação correta do modelo do dispositivo. 2. Busca no Google usando termos como '[Fabricante] [Modelo] drivers'. 3. Navegação até a seção de suporte/downloads do site oficial. 4. Seleção do sistema operacional correto antes de baixar.",
            "level": "N1", "tags": ["Hardware", "Drivers", "Troubleshooting", "Desktop Support", "Field Service"], "tools": ["Web Browser"], "os": ["Any"],
            "script": "# Procedimento manual. Focar na busca precisa usando o modelo exato do dispositivo."
        },
        "SOP: Download Seguro de Software": {
            "description": "Crie um SOP para um analista N1 baixar um software comum (ex: 7-Zip, Notepad++, Adobe Reader) de forma segura. O procedimento deve enfatizar: 1. A importância de baixar SEMPRE do site oficial do desenvolvedor. 2. Como identificar o site oficial em uma busca. 3. Os riscos de usar sites de download de terceiros (malware, adware, versões desatualizadas).",
            "level": "N1", "tags": ["Software", "Security", "Desktop Support", "Governance"], "tools": ["Web Browser"], "os": ["Any"],
            "script": "# Procedimento manual. O foco é a segurança e a identificação da fonte oficial."
        }
    },
    "Backup & DR (Veeam, Commvault)": {
        "[Veeam] SOP: Execução de Job de Backup": {
            "description": "Crie um SOP para um analista N2 iniciar manualmente um job de backup no Veeam Backup & Replication e verificar seu status de conclusão.",
            "level": "N2", "tags": ["Backup", "Veeam"], "tools": ["Veeam"], "os": ["Windows"],
            "script": "# Start-VBRJob -Job 'My Backup Job'"
        },
        "[Commvault] Playbook: Automação de Relatório de Job": {
            "description": "Gere um exemplo de como usar a API REST da Commvault com Python para obter o status dos jobs de backup das últimas 24 horas e gerar um relatório simples.",
            "level": "N3", "tags": ["Backup", "Commvault", "Automation", "API"], "tools": ["Commvault"], "os": ["Any"],
            "script": "# requests.get('http://your-commserve/WebConsole/api/Job', headers=headers)"
        },
    },
    "Automation (Ansible, Terraform)": {
        "SOP: Execução de Playbook Ansible": {
            "description": "Crie um SOP para um analista N2 executar um playbook Ansible existente para aplicar uma configuração em um grupo de servidores, incluindo os comandos para checagem de sintaxe e execução em modo 'dry run' antes da aplicação real.",
            "level": "N2", "tags": ["Automation", "Ansible", "Configuration Management"], "tools": ["Ansible"], "os": ["Linux"],
            "script": "ansible-playbook --check my_playbook.yml\nansible-playbook my_playbook.yml"
        },
        "Playbook: Template de Infraestrutura (Terraform)": {
            "description": "Forneça um arquivo `main.tf` do Terraform para um especialista N3 provisionar uma infraestrutura de rede básica na AWS, contendo uma VPC, uma subnet pública e uma subnet privada.",
            "level": "N3", "tags": ["Automation", "IaC", "Terraform", "AWS"], "tools": ["Terraform", "AWS CLI"], "os": ["Any"],
            "script": "provider \"aws\" { region = \"us-east-1\" }\n\nresource \"aws_vpc\" \"main\" { cidr_block = \"10.0.0.0/16\" }"
        },
    },
    "Gestão & Liderança Técnica": {
        "SOP: Gestão de Crise em Incidente Crítico (P1)": {
            "description": "Crie um guia de ação para um Líder Técnico gerenciar um incidente P1. O guia deve focar em: 1. Estabelecer a comunicação (ponte de conferência, war room). 2. Identificar o impacto e os serviços afetados. 3. Acionar as equipes de suporte necessárias. 4. Coordenar a comunicação com stakeholders. 5. Iniciar a documentação do incidente.",
            "level": "Líder Técnico", "tags": ["ITIL", "Incident Management", "Governance"], "tools": ["ServiceNow", "Jira"], "os": ["Any"],
            "script": "# Procedimento de gestão, sem script técnico."
        },
        "SOP: Análise de Causa Raiz (RCA) Pós-Incidente": {
            "description": "Gere um SOP para conduzir uma Análise de Causa Raiz (RCA) após a resolução de um incidente P1. O procedimento deve seguir o método '5 Porquês' e incluir: 1. Linha do tempo do evento. 2. Identificação da causa raiz. 3. Definição de ações corretivas e preventivas. 4. Documentação da lição aprendida.",
            "level": "N3/Líder", "tags": ["ITIL", "Problem Management", "Governance"], "tools": ["Confluence", "Miro"], "os": ["Any"],
            "script": "# Template de documento RCA."
        },
    },
}

