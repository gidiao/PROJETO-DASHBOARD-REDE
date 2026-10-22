# 🗄️ Documentação do Banco de Dados - Sistema de Monitoramento

Este documento descreve a estrutura de dados relacional utilizada no projeto da disciplina de Laboratório de Desenvolvimento de Software para o armazenamento das métricas de hardware e testes de rede coletados pelas estações.

---

## 📌 Visão Geral
* **Sistema Gerenciador de Banco de Dados (SGBD):** MariaDB
* **Nome do Banco de Dados:** `monitoramento`
* **Arquitetura:** Modelo Relacional Normalizado (1:N entre Host e Métricas)

---

## 📊 Estrutura das Tabelas

### 1. `hosts`
Armazena as informações cadastrais de cada dispositivo/estação que envia dados para o sistema de monitoramento.

| Coluna | Tipo de Dado | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id_host` | INT / Long | Chave Primária (PK), Auto Increment | Identificador único da estação. |
| `nome_maquina` | VARCHAR | NOT NULL | Nome de identificação do host na rede. |
| `sistema_operacional`| VARCHAR | - | Sistema operacional em execução na máquina. |
| `endereco_ip` | VARCHAR | - | Endereço IP atual do host. |
| `endereco_mac` | VARCHAR | - | Endereço MAC da interface de rede. |
| `data_cadastro` | DATETIME | NOT NULL | Data e hora em que o host foi registado no sistema. |

---

### 2. `metricas_hardware`
Armazena o histórico periódico de utilização dos recursos de hardware (como CPU e Memória) enviados pelo agente de coleta Python.

| Coluna | Tipo de Dado | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INT / Long | Chave Primária (PK), Auto Increment | Identificador único da métrica. |
| `id_host` | INT / Long | Chave Estrangeira (FK), NOT NULL | Relaciona a métrica à tabela `hosts`. |
| `cpu_percentual` | DOUBLE | NOT NULL | Percentual de uso atual da CPU. |
| `memoria_total_mb` | DOUBLE | NOT NULL | Capacidade total de memória RAM em MB. |
| `memoria_usada_mb` | DOUBLE | NOT NULL | Quantidade de memória RAM em uso em MB. |
| `data_hora_coleta` | DATETIME | NOT NULL | Timestamp local da estação no momento da captura. |
| `pacotes_enviados` | BIGINT | DEFAULT 0 | Total de pacotes de rede enviados acumulados. |
| `pacotes_recebidos` | BIGINT | DEFAULT 0 | Total de pacotes de rede recebidos acumulados. |

---

### 3. `testes_rede`
Armazena os resultados dos testes periódicos de latência, velocidade de download e upload coletados na rede.

| Coluna | Tipo de Dado | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INT / Long | Chave Primária (PK), Auto Increment | Identificador único do teste de rede. |
| `id_host` | INT / Long | Chave Estrangeira (FK), NOT NULL | Relaciona o teste ao `host` correspondente. |
| `latencia_ms` | DOUBLE | - | Tempo de resposta (ping) em milissegundos. |
| `download_mbps` | DOUBLE | - | Taxa de transferência de download em Mbps. |
| `upload_mbps` | DOUBLE | - | Taxa de transferência de upload em Mbps. |
| `data_hora_coleta` | DATETIME | NOT NULL | Timestamp local em que o teste de rede foi executado. |

---

## 🔗 Relacionamentos (Cardinalidade)
* **`hosts` (1) ──< (`metricas_hardware`):** Um host pode gerar múltiplos registos de métricas de hardware ao longo do tempo.
* **`hosts` (1) ──< (`testes_rede`):** Um host pode realizar múltiplos testes de rede periódicos.