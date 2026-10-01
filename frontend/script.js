
/*
=====================================
    SELEÇÃO DOS ELEMENTOS HTML
=====================================
*/

// Botão que executa o teste
const newTestButton = document.querySelector(".new-test-button");

// Status geral da rede
const networkStatus = document.querySelector(
    ".summary-card:nth-child(6) strong"
);

// Texto abaixo do status da rede
const networkStatusDescription = document.querySelector(
    ".summary-card:nth-child(6) p"
);

// Status do teste de velocidade
const testStatus = document.querySelector(".test-status");

// Texto da última atualização
const lastUpdated = document.querySelector(".computer-information small");

// Cartões de resumo
const summaryCards = document.querySelectorAll(".summary-card");

// Elementos das métricas do teste de rede
const networkMetrics = document.querySelectorAll(
    ".network-metrics strong"
);

// Círculo de utilização da CPU
const cpuCircle = document.querySelector(".cpu-circle");

// Texto que indica se a CPU está ativa
const cpuActivity = document.querySelector(".cpu-percentage span");

// Porcentagem detalhada da memória RAM
const ramPercentage = document.querySelector(
    ".memory-information .metric-line strong"
);

// Texto detalhado do uso da memória
const ramDescription = document.querySelector(
    ".memory-information .metric-line span"
);

const startMonitoringButton = document.querySelector(
    "#start-monitoring-button"
);

const pauseMonitoringButton = document.querySelector(
    "#pause-monitoring-button"
);

const monitoringStatusText = document.querySelector(
    "#monitoring-status-text"
);

const statusIndicator = document.querySelector(
    ".status-indicator"
);

let monitoringInterval = null;


/*
=====================================
    FUNÇÕES AUXILIARES
=====================================
*/

// Gera um número aleatório entre dois valores
function randomNumber(min, max) {

    return Math.floor(
        Math.random() * (max - min + 1)
    ) + min;

}


// Atualiza o horário exibido no cabeçalho
function updateLastUpdated() {

    const now = new Date();

    const formattedDate = now.toLocaleString("pt-BR");

    lastUpdated.textContent =
        `Última atualização: ${formattedDate}`;

}


/*
=====================================
    ATUALIZAÇÃO DOS DADOS
=====================================
*/

function updateDashboard() {

    // Gera valores simulados
    const cpu = randomNumber(20, 90);

    const ram = randomNumber(40, 95);

    const download = randomNumber(150, 500);

    const upload = randomNumber(30, 150);

    const ping = randomNumber(10, 60);

    const jitter = randomNumber(1, 10);

    const packetLoss = (Math.random() * 0.5).toFixed(1);


    /*
    ---------------------------------
        ATUALIZA OS CARTÕES SUPERIORES
    ---------------------------------
    */

    // Cartão da CPU
    summaryCards[0].querySelector("strong").textContent =
        `${cpu}%`;


    // Cartão da RAM
    summaryCards[1].querySelector("strong").textContent =
        `${ram}%`;


    // Cartão de download
    summaryCards[2].querySelector("strong").textContent =
        `${download} Mbps`;


    // Cartão de upload
    summaryCards[3].querySelector("strong").textContent =
        `${upload} Mbps`;


    // Cartão de ping e jitter
    summaryCards[4].querySelector("strong").textContent =
        `${ping} ms / ${jitter} ms`;


    /*
    ---------------------------------
        ATUALIZA O STATUS DA REDE
    ---------------------------------
    */

    networkStatus.textContent = "ONLINE";

    networkStatusDescription.textContent =
        "Todos os sistemas operacionais";


    /*
    ---------------------------------
        ATUALIZA O TESTE DE VELOCIDADE
    ---------------------------------
    */

    networkMetrics[0].textContent =
        `${download} Mbps`;

    networkMetrics[1].textContent =
        `${upload} Mbps`;

    networkMetrics[2].textContent =
        `${ping} ms`;

    networkMetrics[3].textContent =
        `${jitter} ms`;

    networkMetrics[4].textContent =
        `${packetLoss}%`;


    /*
    ---------------------------------
        ATUALIZA A CPU
    ---------------------------------
    */

    cpuCircle.textContent = `${cpu}%`;

    cpuActivity.textContent = "Ativo";


    /*
    ---------------------------------
        ATUALIZA A MEMÓRIA RAM
    ---------------------------------
    */

    ramPercentage.textContent = `${ram}%`;

    ramDescription.textContent =
        `${(ram * 16 / 100).toFixed(1)} GB usados / 16,0 GB total`;


    /*
    ---------------------------------
        ATUALIZA O HORÁRIO
    ---------------------------------
    */

    updateLastUpdated();

}


/*
=====================================
    EXECUÇÃO DO TESTE
=====================================
*/

function runNetworkTest() {

    // Desativa o botão durante a execução
    newTestButton.disabled = true;

    newTestButton.textContent =
        "↻ Teste em andamento...";


    // Atualiza os status para indicar que o teste começou
    testStatus.textContent = "TESTANDO";

    networkStatus.textContent = "TESTANDO";

    networkStatusDescription.textContent =
        "Teste de rede em andamento";


    /*
    Simula o tempo necessário para realizar
    um teste de rede.
    */

    setTimeout(function () {

        // Atualiza os dados simulados
        updateDashboard();


        // Atualiza os status após o teste
        testStatus.textContent = "APROVADO";

        networkStatus.textContent = "ONLINE";

        networkStatusDescription.textContent =
            "Todos os sistemas operacionais";


        // Reativa o botão
        newTestButton.disabled = false;

        newTestButton.textContent =
            "↻ Executar novo teste";


    }, 2000);

}

function startMonitoring() {
    // Evita iniciar vários monitoramentos ao mesmo tempo
    if (monitoringInterval !== null) {
        return;
    }

    // Executa um teste imediatamente
    runNetworkTest();

    // Executa um novo teste a cada 10 segundos
    monitoringInterval = setInterval(() => {
        runNetworkTest();
    }, 10000);

    // Atualiza o estado dos botões
    startMonitoringButton.disabled = true;
    pauseMonitoringButton.disabled = false;

    monitoringStatusText.textContent = "Monitoramento ativo";
    statusIndicator.style.backgroundColor = "#22c55e";

    console.log("Monitoramento iniciado");
}

function pauseMonitoring() {
    // Verifica se existe um monitoramento ativo
    if (monitoringInterval === null) {
        return;
    }

    // Interrompe a execução automática
    clearInterval(monitoringInterval);

    // Limpa o identificador do intervalo
    monitoringInterval = null;

    // Atualiza o estado dos botões
    startMonitoringButton.disabled = false;
    pauseMonitoringButton.disabled = true;

    monitoringStatusText.textContent = "Monitoramento pausado";
    statusIndicator.style.backgroundColor = "#9ca3af";

    console.log("Monitoramento pausado");
}
/*
=====================================
    EVENTO DO BOTÃO
=====================================
*/

// Executa a função quando o botão for clicado
newTestButton.addEventListener(
    "click",
    runNetworkTest
);

startMonitoringButton.addEventListener(
    "click",
    startMonitoring
);

pauseMonitoringButton.addEventListener(
    "click",
    pauseMonitoring
);