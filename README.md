# SCAAR - Sistema de Monitorização de Hardware e Rede

Este projeto é um agente escrito em Python que recolhe métricas de hardware (CPU e Memória) e realiza testes periódicos de velocidade de internet (Ping, Download, Upload), salvando todo o histórico numa base de dados MySQL/MariaDB centralizada (como uma Raspberry Pi). O sistema foi expandido para uma arquitetura distribuída, contando com uma API RESTful (Flask) e um Dashboard Web interativo.

##  Arquitetura do Sistema

O projeto está estruturado em três componentes principais interligadas:
1. **Agente de Coleta (Client-side):** Script Python desenvolvido em padrão MVC que corre nas estações de trabalho monitorizadas, utilizando injeção de dependências.
2. **Servidor Central (Raspberry Pi):** Alojamento da base de dados MariaDB, do servidor web Apache e da API em Flask.
3. **Frontend (Dashboard):** Interface HTML/JS que consome a API do Flask de forma assíncrona para exibir estatísticas em tempo real ao Administrador.

##  Funcionalidades

- **Identificação Automática:** Regista a máquina na base de dados capturando Hostname, Sistema Operacional, Endereço IP local e Endereço MAC físico.
- **Monitorização Contínua de Hardware:** A cada 5 segundos, recolhe e envia o uso percentual da CPU e o consumo de memória RAM (Total e Usada) via `psutil`.
- **Testes de Conectividade Inteligentes:** Executa testes de velocidade da internet utilizando a infraestrutura do Speedtest para obter latência, taxas de download e upload.
- **API de Dados em Tempo Real:** Fornecimento de métricas estruturadas em JSON através de endpoints Flask (ex: `/api/estado`).
- **Dashboard Interativo:** Apresentação visual atualizada dinamicamente através de chamadas JavaScript (Fetch API).
- **Tolerância a Falhas:** Caso o teste de rede falhe ou fique sem internet, o script isola o erro e continua a monitorizar o hardware ininterruptamente.

##  Estrutura de Pastas do Projeto

O projeto utiliza uma arquitetura Monorepo, devendo ser organizado da seguinte forma:

```text
scaar/
├── backend/
│   ├── agente_coletor.py    # Script contínuo que roda na máquina cliente
│   ├── api.py               # API Flask que roda no servidor (porta 5000)
│   ├── database.py          # Classe de conexão e persistência
│   └── models/              # Classes do padrão MVC (Hardware, Host, Rede)
├── database/
│   └── schema.sql           # Script de criação das tabelas no MariaDB
├── frontend/
│   ├── index.html           # Estrutura do Dashboard
│   ├── style.css            # Estilização visual (CSS)
│   └── script.js            # Lógica de consumo da API (Fetch)
└── docs/                    # Diagramas PlantUML, ETP e monografia
```

##  Instalação e Configuração

### 1. Configuração do Servidor Central (Raspberry Pi / Linux)

O servidor atua como o cérebro do sistema, armazenando os dados e servindo a interface web.

**Instalação dos softwares base:**
Abra o terminal e instale o MariaDB, o Apache e o ambiente Python:
```bash
sudo apt update
sudo apt install mariadb-server apache2 python3 python3-pip
```

**Configuração do Banco de Dados MariaDB:**
1. Aceda ao terminal do MariaDB: `sudo mysql -u root -p`
2. Crie o banco de dados e as tabelas importando o script SQL:
   ```sql
   source /caminho/para/scaar/database/schema.sql;
   ```
3. Garanta que o utilizador do banco tem privilégios de acesso remoto para receber os dados dos agentes.

**Instalação das Bibliotecas da API (Flask):**
A API do servidor exige o Flask e conectores de banco. No terminal, execute:
```bash
pip install Flask Flask-CORS mysql-connector-python
```

**Hospedagem do Frontend (Apache):**
Copie todo o conteúdo da pasta `/frontend` do repositório para o diretório raiz do servidor web:
```bash
sudo cp -r scaar/frontend/* /var/www/html/
```

### 2. Configuração das Estações Cliente (Agente)

Os computadores a serem monitorizados precisam apenas da instalação do Python 3 e de três bibliotecas de sistema.

**Instalação das Bibliotecas Python:**
No terminal (Linux) ou no Prompt de Comando/PowerShell (Windows), instale as dependências executando:
```bash
pip install psutil speedtest-cli mysql-connector-python
```
*(Certifique-se de configurar o arquivo `database.py` no cliente para apontar para o IP local do servidor MariaDB).*

##  Como Executar o Sistema

Siga esta ordem rigorosa para iniciar todo o ecossistema:

**Passo 1: Iniciar a API Web (Servidor Central)**
Navegue até à pasta `/backend` no servidor e inicie a API para que ela comece a responder aos pedidos JSON na porta 5000:
```bash
cd scaar/backend
python3 api.py
```
*Nota: A mensagem `Running on all addresses (0.0.0.0)` indicará sucesso.*

**Passo 2: Iniciar o Agente de Coleta (Cliente)**
Na máquina que será monitorizada, acesse a pasta `/backend` e inicie o loop de hardware/rede:
- **No Linux:**
  ```bash
  python3 agente_coletor.py
  ```
- **No Windows:**
  ```cmd
  python agente_coletor.py
  ```
*Nota: O terminal exibirá mensagens de Log confirmando a inserção de métricas a cada 5 segundos.*

**Passo 3: Aceder ao Dashboard (Administrador)**
Com o Apache e a API Flask a correr no servidor central, o Administrador pode visualizar o sistema a partir de qualquer dispositivo na rede local. Basta abrir um navegador web e digitar o Endereço IP da Raspberry Pi:
```text
http://<IP_DA_RASPBERRY>/
```
A página `index.html` será carregada, o script efetuará a ligação automática com a API e os gráficos em ecrã começarão a ser alimentados em tempo real com os dados processados!
