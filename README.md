# SCAAR - Sistema de Monitorização de Hardware e Rede

Este projeto é um agente escrito em Python que recolhe métricas de hardware (CPU e Memória) e realiza testes periódicos de velocidade de internet (Ping, Download, Upload), salvando todo o histórico numa base de dados MySQL/MariaDB centralizada (como uma Raspberry Pi)[cite: 9]. O sistema foi expandido para uma arquitetura distribuída, contando com uma API RESTful (Flask) e um Dashboard Web interativo.

## 🏗️ Arquitetura do Sistema

O projeto está estruturado em três componentes principais interligadas:
1. **Agente de Coleta (Client-side):** Script Python desenvolvido em padrão MVC que corre nas estações de trabalho monitorizadas, utilizando injeção de dependências.
2. **Servidor Central (Raspberry Pi):** Alojamento da base de dados MariaDB, do servidor web Apache e da API em Flask.
3. **Frontend (Dashboard):** Interface HTML/JS que consome a API do Flask de forma assíncrona para exibir estatísticas em tempo real ao Administrador.

## 🚀 Funcionalidades

- **Identificação Automática:** Regista a máquina na base de dados capturando Hostname, Sistema Operacional, Endereço IP local e Endereço MAC físico[cite: 9].
- **Monitorização Contínua de Hardware:** A cada 5 segundos, recolhe e envia o uso percentual da CPU e o consumo de memória RAM (Total e Usada) via `psutil`[cite: 9].
- **Testes de Conectividade Inteligentes:** Executa testes de velocidade da internet utilizando a infraestrutura do Speedtest para obter latência, taxas de download e upload[cite: 9].
- **API de Dados em Tempo Real:** Fornecimento de métricas estruturadas em JSON através de endpoints Flask (ex: `/api/estado`).
- **Dashboard Interativo:** Apresentação visual atualizada dinamicamente através de chamadas JavaScript (Fetch API).
- **Tolerância a Falhas:** Caso o teste de rede falhe ou fique sem internet, o script isola o erro e continua a monitorizar o hardware ininterruptamente[cite: 9].

## 📋 Pré-requisitos

**Para as Estações Cliente (Agentes):**
- Python 3.7 ou superior[cite: 9].
- Bibliotecas Python: `psutil`, `speedtest-cli`, `mysql-connector-python`.

**Para o Servidor Central (Raspberry Pi):**
- Um servidor MySQL ou MariaDB a correr na rede local[cite: 9].
- Ambiente Python com `Flask` e `Flask-CORS`.
- Servidor web Apache (para alojar os ficheiros estáticos HTML/CSS/JS do Dashboard).

## 🔧 Instalação e Configuração

