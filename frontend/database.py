import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = '192.168.0.110'
        self.user = 'admin'
        self.password = '123456'
        self.database = 'monitoramento'
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host, user=self.user,
                password=self.password, database=self.database
            )
            return self.conexao
        except Error as e:
            print(f"Erro ao conectar no MariaDB: {e}")
            return None

    def fechar(self):
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
