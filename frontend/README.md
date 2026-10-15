# SCAAR — Frontend

## 1. Sobre o projeto

O **SCAAR (Sistema de Controle e Análise de Ativos de Rede)** possui uma interface web desenvolvida com HTML, CSS e JavaScript para apresentar informações relacionadas ao monitoramento de computadores e redes.

A interface foi projetada para funcionar em conjunto com uma API desenvolvida em Python utilizando Flask, responsável por fornecer os dados armazenados no banco de dados MariaDB.

## 2. Tecnologias utilizadas

- **HTML5:** estrutura das páginas.
- **CSS3:** estilização, organização dos elementos e layout responsivo.
- **JavaScript:** interatividade e comunicação com a API.
- **Fetch API:** realização de requisições HTTP para obter dados do backend.

## 3. Estrutura dos arquivos

```text
frontend/
├── index.html       # Página principal do dashboard
├── historico.html   # Página de histórico dos testes de rede
├── style.css        # Estilos visuais compartilhados
├── script.js        # Funcionalidades JavaScript do dashboard
├── config.js        # Configuração do endereço da API
└── README.md        # Documentação do frontend
```

## 4. Funcionalidades

### Dashboard

A página `index.html` apresenta a interface principal do sistema, organizada em cartões e seções de monitoramento.

O arquivo `script.js` contém as funcionalidades JavaScript associadas ao dashboard.

### Histórico e análise

A página `historico.html` apresenta os registros dos testes de rede armazenados no banco de dados.

Os dados são obtidos por meio de uma requisição à API Flask, utilizando o endpoint:

```http
GET /api/testes-rede?limite=100
```

A resposta contém os registros disponíveis, incluindo informações como:

- Nome do computador monitorado;
- Data e hora do teste;
- Velocidades de download e upload;
- Latência (ping);
- Jitter, quando disponível;
- Quantidade de pacotes descartados, quando disponível.

O histórico depende do funcionamento do backend, do banco de dados e da execução do agente responsável pela coleta dos testes.

### Estilização

O arquivo `style.css` concentra os estilos compartilhados entre as páginas, mantendo a identidade visual e a organização dos componentes da interface.

### Configuração da API

O arquivo `config.js` é utilizado para configurar o endereço da API, permitindo ajustar a comunicação entre o frontend e o backend conforme o ambiente de execução.

## 5. Como executar

O frontend deve ser utilizado em conjunto com o backend do SCAAR.

### Execução integrada

1. Configure o banco de dados MariaDB e o backend Flask conforme as instruções da pasta principal do projeto.
2. Inicie os serviços necessários, incluindo a API e o agente de coleta.
3. Verifique se o endereço configurado no frontend corresponde ao endereço em que a API está disponível.
4. Abra a interface pelo endereço disponibilizado pelo servidor web utilizado na instalação.

Na instalação integrada ao Raspberry Pi, o objetivo é acessar a interface pelo navegador de outro dispositivo conectado à rede, utilizando o endereço do Raspberry Pi e a porta configurada para o serviço web.

### Execução para desenvolvimento

Para testar o frontend separadamente, pode ser utilizado um servidor HTTP local, como a extensão Live Server do Visual Studio Code.

Entretanto, para carregar dados reais, a API Flask precisa estar em execução e acessível pelo navegador. Abrir os arquivos HTML isoladamente não garante que as requisições ao backend funcionarão.

## 6. Comunicação com o backend

O frontend utiliza requisições HTTP para consultar informações disponibilizadas pela API.

| Endpoint | Finalidade |
|---|---|
| `GET /api/testes-rede` | Consulta os registros dos testes de rede. |
| `GET /api/metricas` | Consulta métricas de hardware dentro de um período, conforme os parâmetros aceitos pela API. |

O endpoint de histórico aceita parâmetros como `limite` e, opcionalmente, `id_host`, para limitar os registros retornados ou filtrar os resultados por computador.

Os parâmetros específicos do endpoint de métricas devem seguir a implementação disponível no backend.

## 7. Observações importantes

- O frontend não realiza diretamente a coleta das métricas de hardware ou os testes de velocidade.
- A coleta é responsabilidade do agente Python executado no ambiente monitorado.
- A persistência dos registros é responsabilidade do banco de dados MariaDB.
- A API Flask intermedeia o acesso do frontend aos dados armazenados.
- Informações reais dependem da configuração correta dos serviços e da existência de registros no banco.
- Valores de jitter e pacotes descartados podem não estar disponíveis em todos os registros.

## 8. Fluxo geral do sistema

```text
Agente de coleta Python
          |
          v
Banco de dados MariaDB
          |
          v
API Flask
          |
          v
Frontend web
          |
          v
Navegador do usuário
```

Esse fluxo permite centralizar a coleta e o armazenamento dos dados no ambiente de monitoramento, disponibilizando as informações por meio de uma interface web.

## 9. Manutenção

Alterações na estrutura visual devem ser realizadas principalmente em `style.css` e nos arquivos HTML correspondentes.

Modificações nas interações do dashboard devem ser feitas em `script.js`.

Alterações na forma como os dados são consultados devem respeitar os endpoints e o formato de resposta definidos no backend.

Sempre que houver mudanças nos endpoints ou nos campos retornados pela API, o frontend deverá ser revisado para manter a compatibilidade com o backend.
