Markdown
# Agente de Monitoramento de Hardware e Rede

Este projeto é um agente escrito em Python que coleta métricas de hardware (CPU e Memória) e realiza testes periódicos de velocidade de internet (Ping, Download, Upload), salvando todo o histórico em um banco de dados MySQL/MariaDB centralizado (como uma Raspberry Pi).

## 🚀 Funcionalidades

- **Identificação Automática:** Registra a máquina no banco de dados capturando Hostname, Sistema Operacional, Endereço IP local e Endereço MAC físico.
- **Monitoramento Contínuo de Hardware:** A cada 5 segundos, coleta e envia o uso percentual da CPU e o consumo de memória RAM (Total e Usada) via `psutil`.
- **Testes de Conectividade Inteligentes:** A cada 30 segundos (configurável), executa um teste de velocidade da internet usando a infraestrutura do Speedtest.
- **Tolerância a Falhas:** Caso o teste de rede falhe ou fique sem internet, o script isola o erro e continua monitorando o hardware ininterruptamente.

## 📋 Pré-requisitos

- Python 3.7 ou superior.
- Um servidor MySQL ou MariaDB rodando na rede (ex: em uma Raspberry Pi).

## 🔧 Instalação e Configuração



