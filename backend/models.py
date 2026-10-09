from database import Database

class HostModel:
    def __init__(self, db: Database):
        self.db = db

    def criar(self, nome_maquina, so, ip, mac):
        cursor = self.db.conexao.cursor()
        sql = "INSERT INTO hosts (nome_maquina, sistema_operacional, endereco_ip, endereco_mac) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome_maquina, so, ip, mac))
        self.db.conexao.commit()
        id_host = cursor.lastrowid
        cursor.close()
        return id_host

    def ler_por_mac(self, mac):
        cursor = self.db.conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hosts WHERE endereco_mac = %s", (mac,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado

    def ler_todos(self):
        cursor = self.db.conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hosts")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def atualizar(self, id_host, nome_maquina, ip):
        cursor = self.db.conexao.cursor()
        sql = "UPDATE hosts SET nome_maquina = %s, endereco_ip = %s WHERE id_host = %s"
        cursor.execute(sql, (nome_maquina, ip, id_host))
        self.db.conexao.commit()
        cursor.close()

    def deletar(self, id_host):
        cursor = self.db.conexao.cursor()
        cursor.execute("DELETE FROM hosts WHERE id_host = %s", (id_host,))
        self.db.conexao.commit()
        cursor.close()

class MetricaHardwareModel:
    def __init__(self, db: Database):
        self.db = db

    def criar(self, id_host, cpu, mem_total, mem_usada, data_hora):
        cursor = self.db.conexao.cursor()
        sql = "INSERT INTO metricas_hardware (id_host, cpu_percentual, memoria_total_mb, memoria_usada_mb, erros_rede_in, erros_rede_out, data_hora_coleta) VALUES (%s, %s, %s, %s, 0, 0, %s)"
        cursor.execute(sql, (id_host, cpu, mem_total, mem_usada, data_hora))
        self.db.conexao.commit()
        cursor.close()

class TesteRedeModel:
    def __init__(self, db: Database):
        self.db = db

    def criar(self, id_host, download, upload, ping, data_hora):
        cursor = self.db.conexao.cursor()
        sql = "INSERT INTO testes_rede (id_host, download_mbps, upload_mbps, ping_ms, jitter_ms, pacotes_descartados, data_hora_teste) VALUES (%s, %s, %s, %s, 0, 0, %s)"
        cursor.execute(sql, (id_host, download, upload, ping, data_hora))
        self.db.conexao.commit()
        cursor.close()
