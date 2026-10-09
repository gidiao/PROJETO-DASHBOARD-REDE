import psutil
import platform
import socket
import uuid
import time
import speedtest
from datetime import datetime
import logging

from database import Database
from models import HostModel, MetricaHardwareModel, TesteRedeModel

# Configuração de logging substituindo a View
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

class AgenteController:
    def __init__(self):
        self.db = Database()
        self.db.conectar()
        self.host_model = HostModel(self.db)
        self.hw_model = MetricaHardwareModel(self.db)
        self.rede_model = TesteRedeModel(self.db)
        self.id_host = None

    def _obter_mac(self):
        mac = uuid.getnode()
        return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

    def _obter_ip_local(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def _obter_ip_internet(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = None
        finally:
            s.close()
        return ip

    def registrar_agente(self):
        mac = self._obter_mac()
        host_existente = self.host_model.ler_por_mac(mac)

        if host_existente:
            self.id_host = host_existente['id_host']
            logging.info(f"Máquina já registrada. ID: {self.id_host}")
        else:
            nome_maquina = platform.node()
            so = f"{platform.system()} {platform.release()}"
            ip = self._obter_ip_local()
            self.id_host = self.host_model.criar(nome_maquina, so, ip, mac)
            logging.info(f"Nova máquina registrada. ID: {self.id_host}")

    def executar_teste_rede(self):
        logging.info("Iniciando teste de rede (aguarde aprox. 20s)...")
        try:
            self.db.conexao.ping(reconnect=True, attempts=3, delay=2)
            socket.setdefaulttimeout(20)
            
            ip_wifi = self._obter_ip_internet()
            st = speedtest.Speedtest(source_address=ip_wifi, secure=True) if ip_wifi else speedtest.Speedtest(secure=True)
            st.get_best_server()
            
            ping = st.results.ping
            download = st.download() / 1_000_000 
            upload = st.upload() / 1_000_000
            data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.rede_model.criar(self.id_host, download, upload, ping, data_hora)
            logging.info(f"Rede -> Latência: {ping:.1f}ms | Down: {download:.1f}Mbps | Up: {upload:.1f}Mbps")

        except Exception as e:
            logging.error(f"Falha na rede: {e}")
        finally:
            socket.setdefaulttimeout(None)

    def iniciar_monitoramento(self):
        if not self.db.conexao:
            logging.error("Sem conexão com o banco. Encerrando.")
            return

        self.registrar_agente()
        contador_ciclos = 0

        try:
            while True:
                if contador_ciclos % 6 == 0:
                    self.executar_teste_rede()

                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory()
                mem_total = mem.total / (1024 * 1024)
                mem_usada = mem.used / (1024 * 1024)
                data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                self.hw_model.criar(self.id_host, cpu, mem_total, mem_usada, data_hora)
                logging.info(f"Hardware -> CPU: {cpu}% | Memória: {mem_usada:.0f}MB")
                
                contador_ciclos += 1
                time.sleep(5)
                
        except KeyboardInterrupt:
            logging.info("Coleta interrompida pelo usuário.")
        finally:
            self.db.fechar()

if __name__ == "__main__":
    controller = AgenteController()
    controller.iniciar_monitoramento()
