# SCAAR - SISTEMA CENTRALIZADO DE COLETA E ANÁLISE DE REDE

Este repositório contém a infraestrutura completa para o projeto de coleta, armazenamento e visualização de dados de uma rede. A aplicação trabalha em um sistema cliente-servidor onde o cliente é uma aplicação chamada de agente que faz coletas contínuas de informações do hardware e da rede e envia estas informações para o servidor onde serão feitas análises e a geração do dashboard de visualização dos resultados

## Arquitetura do Projeto
O projeto está dividido em quatro módulos principais, em arquitetura Monorepo

* **/backend**: Scripts Python estruturados para operar nas duas pontas do sistema (cliente e servidor).
  * **Agente Coletor (`agente_coletor.py`)**: Script que roda na máquina cliente, recolhendo dados de forma contínua e enviando para o servidor MariaDB remoto[cite: 10]. Desenvolvido com padrão arquitetural MVC (Model-View-Controller) e injeção de dependências para separar a lógica de negócio das conexões de base de dados. As suas principais funcionalidades incluem:
    * **Identificação Automática:** Registo do Hostname, Sistema Operacional, IP Local e Endereço MAC.
    * **Métricas de Hardware:** Monitorização do uso de CPU (%) e memória RAM (Total e Usada) em intervalos curtos.
    * **Testes de Conectividade:** Medição de latência (Ping), velocidade de Download e Upload de forma assíncrona.
  * **API Web (`api.py`)**: Script em Python rodando no servidor (usando o framework Flask) focado na análise dos dados e na entrega das métricas consolidadas em formato JSON para o frontend

* **/database**: Banco MariaDB responsável pelo armazenamento das informações enviadas pelo script agente

* **/frontend**: Interface web para visualização dos dados em tempo real

* **/docs**: Diagramas, especificações de hardware, monografia e referências teóricas

## Dependências do Backend (Agente Coletor)
Para o correto funcionamento do arquivo `agente_coletor.py` nas máquinas clientes, o ambiente Python requer a instalação das seguintes bibliotecas externas:
- `psutil` (Para extração dos dados físicos de CPU e Memória)
- `speedtest-cli` (Para testes de taxa de transferência de rede)
- `mysql-connector-python` (Driver para comunicação e inserção de dados no MariaDB)

