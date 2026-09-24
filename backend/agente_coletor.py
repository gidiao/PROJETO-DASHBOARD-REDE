import psutil
import platform
import socket
import uuid
import time
import mysql.connector
from mysql.connector import Error
import speedtest
from datetime import datetime

# Configurações da Raspberry Pi
DB_HOST = '192.168.0.110'
DB_USER = 'admin'
DB_PASSWORD = '123456' # Lembre-se de colocar sua senha real
DB_NAME = 'monitoramento'

def obter_mac():
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

def conectar_banco():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Error as e:
        print(f"Erro ao conectar no MariaDB: {e}")
        return None

def registrar_host(cursor, conexao):
    mac = obter_mac()
    nome_maquina = platform.node()
    so = f"{platform.system()} {platform.release()}"
    ## ip = socket.gethostbyname(nome_maquina)
    # Força a descoberta da interface de rede principal
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não chega a enviar pacotes, apenas mapeia a rota local
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()

    cursor.execute("SELECT id_host FROM hosts WHERE endereco_mac = %s", (mac,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]
    
    sql = "INSERT INTO hosts (nome_maquina, sistema_operacional, endereco_ip, endereco_mac) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (nome_maquina, so, ip, mac))
    conexao.commit()
    return cursor.lastrowid

def obter_ip_internet():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Roteia um pacote falso para a internet pública para descobrir qual placa (Wi-Fi) responde
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = None
    finally:
        s.close()
    return ip

def executar_speedtest(id_host, cursor, conexao):
    print("\nIniciando teste de rede (aguarde aprox. 20s)...")
    try:
        conexao.ping(reconnect=True, attempts=3, delay=2)
        
        # Trava de segurança: impede que a biblioteca aguarde eternamente
        socket.setdefaulttimeout(20)
        
        ip_wifi = obter_ip_internet()
        print(f"[DEBUG] IP selecionado pelo Python para a internet: {ip_wifi}")
        
        # secure=True força tráfego HTTPS, ignorando proxies ou bloqueios de rotas locais
        if ip_wifi:
            st = speedtest.Speedtest(source_address=ip_wifi, secure=True)
        else:
            st = speedtest.Speedtest(secure=True)
            
        st.get_best_server()
        
        latencia = st.results.ping
        download = st.download() / 1_000_000 
        upload = st.upload() / 1_000_000

        data_hora_atual_teste = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        sql_rede = """INSERT INTO testes_rede 
                  (id_host, download_mbps, upload_mbps, ping_ms, jitter_ms, pacotes_descartados, data_hora_teste) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                  
        
        cursor.execute(sql_rede, (id_host, download, upload, latencia, 0, 0, data_hora_atual_teste))
        conexao.commit()
        
        print(f"Rede -> Latência: {latencia:.1f}ms | Down: {download:.1f}Mbps | Up: {upload:.1f}Mbps\n")
        
    except Exception as e:
        print(f"Falha isolada na rede (O hardware continuará sendo monitorado): {e}\n")
    finally:
        # Devolve o controle normal de tempo para o resto do sistema
        socket.setdefaulttimeout(None)
        
def iniciar_coleta():
    conexao = conectar_banco()
    if not conexao: return

    cursor = conexao.cursor()
    id_host = registrar_host(cursor, conexao)
    print(f"Máquina registrada com ID: {id_host}")

    contador_ciclos = 0

    try:
        while True:
            # A cada 6 ciclos (aprox. 30 segundos), faz o teste de rede
            # No futuro você pode mudar esse '6' para '60' (a cada 5 minutos)
            if contador_ciclos % 6 == 0:
                executar_speedtest(id_host, cursor, conexao)
            data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            mem_total = mem.total / (1024 * 1024)
            mem_usada = mem.used / (1024 * 1024)

            sql = """INSERT INTO metricas_hardware 
                    (id_host, cpu_percentual, memoria_total_mb, memoria_usada_mb, erros_rede_in, erros_rede_out, data_hora_coleta) 
                    VALUES (%s, %s, %s, %s, 0, 0, %s)"""
            cursor.execute(sql, (id_host, cpu, mem_total, mem_usada, data_hora_atual))
            conexao.commit()
            
            print(f"Hardware -> CPU: {cpu}% | Memória: {mem_usada:.0f}MB")
            
            contador_ciclos += 1
            time.sleep(5)

    except KeyboardInterrupt:
        print("Coleta interrompida.")
    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    iniciar_coleta()