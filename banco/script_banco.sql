USE monitoramento;

-- Limpa as tabelas antigas (se existirem) para evitar conflitos
DROP TABLE IF EXISTS metricas;
DROP TABLE IF EXISTS maquinas;

-- 1. Tabela Central (Hosts)
CREATE TABLE hosts (
    id_host INT(11) AUTO_INCREMENT PRIMARY KEY,
    nome_maquina VARCHAR(100),
    sistema_operacional VARCHAR(100),
    endereco_ip VARCHAR(45),
    endereco_mac VARCHAR(17),
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela de Desempenho (Hardware)
CREATE TABLE metricas_hardware (
    id_metrica_hw INT(11) AUTO_INCREMENT PRIMARY KEY,
    id_host INT(11),
    data_hora_coleta DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu_percentual DECIMAL(5,2),
    memoria_total_mb DECIMAL(10,2),
    memoria_usada_mb DECIMAL(10,2),
    erros_rede_in INT(11),
    erros_rede_out INT(11),
    FOREIGN KEY (id_host) REFERENCES hosts(id_host)
);

-- 3. Tabela de Conectividade (Testes de Rede)
CREATE TABLE testes_rede (
    id_teste_rede INT(11) AUTO_INCREMENT PRIMARY KEY,
    id_host INT(11),
    data_hora_teste DATETIME DEFAULT CURRENT_TIMESTAMP,
    download_mbps DECIMAL(10,2),
    upload_mbps DECIMAL(10,2),
    ping_ms DECIMAL(8,2),
    jitter_ms DECIMAL(8,2),
    pacotes_descartados INT(11),
    FOREIGN KEY (id_host) REFERENCES hosts(id_host)
);