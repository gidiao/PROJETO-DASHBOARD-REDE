import psutil
import pymysql
import time
import random
import platform
import socket

DB_HOST = "192.168.100.100"  # IP do Raspberry Pi
DB_USER = "banco"
DB_PASS = "banco"
DB_NAME = "monitoramento"

# --- COLETA DE INFORMAÇÕES FIXAS DO HARDWARE ---
HOSTNAME = socket.gethostname()
OS_INFO = f"{platform.system()} {platform.release()}"
CPU_INFO = platform.processor()

# Calcula a RAM total apenas uma vez para o registro
ram_total_gb = round(psutil.virtual_memory().total / (1024**3), 2)
RAM_INFO = f"{ram_total_gb} GB Total"

def registrar_maquina(cursor):
    # Registra ou atualiza o status "online" da máquina
    sql = """INSERT INTO maquinas (hostname, os_info, cpu_info, ram_info) 
             VALUES (%s, %s, %s, %s) 
             ON DUPLICATE KEY UPDATE os_info=%s, cpu_info=%s, ram_info=%s"""
    cursor.execute(sql, (HOSTNAME, OS_INFO, CPU_INFO, RAM_INFO, OS_INFO, CPU_INFO, RAM_INFO))

def get_hardware_data():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    try: disk = psutil.disk_usage('/')
    except:
        try: disk = psutil.disk_usage('C:\\')
        except: disk = None
            
    temp_cpu = 0.0
    if hasattr(psutil, "sensors_temperatures"):
        try:
            temps = psutil.sensors_temperatures()
            if temps: temp_cpu = list(temps.values())[0][0].current
        except: pass
            
    return (HOSTNAME, cpu, mem.total, mem.used, mem.percent, 0, 0, 0, disk.total if disk else 0, disk.used if disk else 0, disk.percent if disk else 0, temp_cpu)

def get_network_data():
    net_io = psutil.net_io_counters()
    dl = random.uniform(200, 250)
    ul = random.uniform(80, 95)
    return (HOSTNAME, net_io.packets_sent, net_io.packets_recv, net_io.errin, net_io.errout, net_io.dropin, net_io.dropout, dl, ul, random.uniform(15, 25), random.uniform(1, 5))

def main():
    print(f"Iniciando monitoramento em: {HOSTNAME}")
    while True:
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
            cursor = conn.cursor()
            
            registrar_maquina(cursor)
            
            hw = get_hardware_data()
            cursor.execute('''INSERT INTO hw_metrics (hostname, cpu_percent, ram_total, ram_used, ram_percent, swap_total, swap_used, swap_percent, disk_total, disk_used, disk_percent, temp_cpu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', hw)
            
            net = get_network_data()
            cursor.execute('''INSERT INTO net_metrics (hostname, packets_sent, packets_recv, errin, errout, dropin, dropout, download_mbps, upload_mbps, ping_ms, jitter_ms) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', net)
            
            conn.commit()
            conn.close()
            print(f"[OK] Dados de {HOSTNAME} enviados com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha de comunicação: {e}")
            
        time.sleep(5) 

if __name__ == "__main__":
    main()