/*
 * Dashboard SCAAR
 * Os dados vêm da API Flask; este arquivo não gera métricas fictícias.
 */
const API_BASE_URL = (window.SCAAR_API_BASE_URL || "http://127.0.0.1:5000").replace(/\/$/, "");

const byId = (id) => document.getElementById(id);
const newTestButton = document.querySelector(".new-test-button");
const startMonitoringButton = byId("start-monitoring-button");
const pauseMonitoringButton = byId("pause-monitoring-button");
const monitoringStatusText = byId("monitoring-status-text");
const statusIndicator = document.querySelector(".status-indicator");
const testStatus = byId("test-status");

let monitoringInterval = null;
let requestInProgress = false;

function numero(valor, casas = 1) {
    if (valor === null || valor === undefined || valor === "") return "N/D";
    const n = Number(valor);
    return Number.isFinite(n)
        ? n.toLocaleString("pt-BR", { minimumFractionDigits: 0, maximumFractionDigits: casas })
        : "N/D";
}

function dataHora(valor) {
    if (!valor) return "Sem coleta registrada";
    const data = new Date(String(valor).replace(" ", "T"));
    if (Number.isNaN(data.getTime())) return String(valor);
    return data.toLocaleString("pt-BR");
}

function setText(id, value) {
    const element = byId(id);
    if (element) element.textContent = value;
}

function setWidth(selector, percentage) {
    const element = document.querySelector(selector);
    if (element) element.style.width = `${Math.max(0, Math.min(100, Number(percentage) || 0))}%`;
}

function setStatus(online, hasData) {
    const status = byId("network-status");
    if (status) status.textContent = online ? "ONLINE" : (hasData ? "SEM ATUALIZAÇÃO" : "SEM DADOS");
    setText("network-status-description",
        online ? "O agente está enviando dados recentes" :
        (hasData ? "A última coleta está antiga; verifique o agente" : "Aguardando a primeira coleta do agente"));
    if (statusIndicator) statusIndicator.style.backgroundColor = online ? "#22c55e" : "#9ca3af";
}

async function obterJSON(caminho) {
    const response = await fetch(`${API_BASE_URL}${caminho}`, { cache: "no-store" });
    const dados = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(dados.detalhe || dados.erro || `Erro HTTP ${response.status}`);
    }
    return dados;
}

async function updateDashboard() {
    if (requestInProgress) return;
    requestInProgress = true;
    if (newTestButton) {
        newTestButton.disabled = true;
        newTestButton.textContent = "↻ Atualizando...";
    }

    try {
        const dados = await obterJSON("/api/estado");
        const host = dados.host || {};
        const hardware = dados.hardware || {};
        const teste = dados.teste_rede || {};

        const cpu = hardware.cpu_percentual;
        const memoriaUsada = hardware.memoria_usada_mb;
        const memoriaTotal = hardware.memoria_total_mb;
        const ram = Number(memoriaTotal) > 0 ? Number(memoriaUsada) / Number(memoriaTotal) * 100 : null;
        const ramUsadaGB = Number(memoriaUsada) / 1024;
        const ramTotalGB = Number(memoriaTotal) / 1024;

        setText("host-name", host.nome_maquina || "Host sem nome");
        setText("host-os", host.sistema_operacional || "Sistema operacional não informado");
        setText("host-ip", host.endereco_ip || "IP não informado");
        setText("last-updated", `Última coleta: ${dataHora(hardware.data_hora_coleta)}`);

        setText("summary-cpu", cpu == null ? "—" : `${numero(cpu)}%`);
        setText("summary-ram", ram == null ? "—" : `${numero(ram)}%`);
        setText("summary-ram-detail", memoriaTotal == null ? "Sem dados de memória" : `${numero(ramUsadaGB, 2)} / ${numero(ramTotalGB, 2)} GB`);
        setText("cpu-circle", cpu == null ? "—" : `${numero(cpu)}%`);
        setText("cpu-activity", dados.online ? "Ativo" : "Sem atualização");
        setText("ram-description", memoriaTotal == null ? "Sem dados de memória" : `${numero(ramUsadaGB, 2)} GB usados / ${numero(ramTotalGB, 2)} GB total`);
        setText("ram-percentage", ram == null ? "—" : `${numero(ram)}%`);
        setWidth(".ram-progress", ram || 0);

        setText("summary-download", teste.download_mbps == null ? "—" : `${numero(teste.download_mbps)} Mbps`);
        setText("summary-upload", teste.upload_mbps == null ? "—" : `${numero(teste.upload_mbps)} Mbps`);
        setText("summary-ping-jitter", teste.ping_ms == null ? "—" : `${numero(teste.ping_ms)} ms / ${numero(teste.jitter_ms)} ms`);
        setText("network-download", teste.download_mbps == null ? "—" : `${numero(teste.download_mbps)} Mbps`);
        setText("network-upload", teste.upload_mbps == null ? "—" : `${numero(teste.upload_mbps)} Mbps`);
        setText("network-ping", teste.ping_ms == null ? "—" : `${numero(teste.ping_ms)} ms`);
        setText("network-jitter", teste.jitter_ms == null ? "N/D" : `${numero(teste.jitter_ms)} ms`);
        setText("network-loss", teste.pacotes_descartados == null ? "N/D" : String(teste.pacotes_descartados));
        setText("test-status", teste.id_teste_rede ? "CONCLUÍDO" : "SEM TESTE");
        setText("speedtest-server", teste.data_hora_teste ? `Último teste: ${dataHora(teste.data_hora_teste)}` : "Nenhum teste de velocidade registrado");
        setText("errors-in", hardware.erros_rede_in == null ? "—" : String(hardware.erros_rede_in));
        setText("errors-out", hardware.erros_rede_out == null ? "—" : String(hardware.erros_rede_out));
        setText("packets-loss-interface", teste.pacotes_descartados == null ? "N/D" : String(teste.pacotes_descartados));

        setStatus(Boolean(dados.online), hardware.data_hora_coleta != null);
    } catch (error) {
        console.error("Falha ao atualizar dashboard:", error);
        setStatus(false, false);
        setText("network-status-description", `Não foi possível acessar a API: ${error.message}`);
        setText("test-status", "API INDISPONÍVEL");
        if (monitoringStatusText) monitoringStatusText.textContent = "API indisponível";
    } finally {
        requestInProgress = false;
        if (newTestButton) {
            newTestButton.disabled = false;
            newTestButton.textContent = "↻ Atualizar dados";
        }
    }
}

function startMonitoring() {
    if (monitoringInterval !== null) return;
    updateDashboard();
    monitoringInterval = window.setInterval(updateDashboard, 10000);
    if (startMonitoringButton) startMonitoringButton.disabled = true;
    if (pauseMonitoringButton) pauseMonitoringButton.disabled = false;
    if (monitoringStatusText) monitoringStatusText.textContent = "Atualização automática ativa";
    if (statusIndicator) statusIndicator.style.backgroundColor = "#22c55e";
}

function pauseMonitoring() {
    if (monitoringInterval === null) return;
    window.clearInterval(monitoringInterval);
    monitoringInterval = null;
    if (startMonitoringButton) startMonitoringButton.disabled = false;
    if (pauseMonitoringButton) pauseMonitoringButton.disabled = true;
    if (monitoringStatusText) monitoringStatusText.textContent = "Atualização automática pausada";
    if (statusIndicator) statusIndicator.style.backgroundColor = "#9ca3af";
}

if (newTestButton) newTestButton.addEventListener("click", updateDashboard);
if (startMonitoringButton) startMonitoringButton.addEventListener("click", startMonitoring);
if (pauseMonitoringButton) pauseMonitoringButton.addEventListener("click", pauseMonitoring);

if (pauseMonitoringButton) pauseMonitoringButton.disabled = true;
updateDashboard();
