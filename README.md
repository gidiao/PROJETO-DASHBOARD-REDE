# SCAAR - SISTEMA CENTRALIZADO DE COLETA E ANÁLISE DE REDE

Este repositório contém a infraestrutura completa para o projeto de coleta, armazenamento e visualização de dados de uma rede. A aplicação trabalha em um sistema cliente-servidor onde o cliente é uma aplicação chamada de agente que faz coletas contínuas de informações do hardware e da rede e envia estas informações para o servidor onde serão feitas análises e a geração do dashboard de visualização dos resultados.

## Arquitetura do Projeto
O projeto está dividido em quatro módulos principais, em arquitetura Monorepo:
* **/backend**: scripts phthon que rodan no cliente, recolhendo dados e enviando para o servior Mariadb remoto. No servidor também haverá script em python para análise de dados.
* **/database**: banco MariaDB responsável pelo armazenamento das informações enviadas pelo script agente.
* **/frontend**: Interface web para visualização dos dados em tempo real.
* **/docs**: Diagramas, especificações de hardware, monografia e referências teóricas.

## Como iniciar o ambiente de desenvolvimento

## Como rodar os testes
 - Na máquina cliente devem estar instalados os scripts agente_colletor.py, database.py e models.py.
  - rodar o script agente_colletor.py

  
