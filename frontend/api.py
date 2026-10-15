from flask import Flask, jsonify, request
from flask_cors import CORS
from database import Database

app = Flask(__name__)
# O CORS é essencial para permitir que o frontend (HTML/JS) consuma a API
CORS(app) 

@app.route('/api/estado', methods=['GET'])
def obter_estado():
    db = Database()
    db.conectar()
    if not db.conexao:
        return jsonify({"erro": "Falha na conexão com o banco"}), 500

    cursor = db.conexao.cursor(dictionary=True)

    try:
        host = {}
        hardware = {}
        teste_rede = {}

        # 1. Pega a métrica de hardware mais recente para descobrir quem está online AGORA
        cursor.execute("SELECT * FROM metricas_hardware ORDER BY data_hora_coleta DESC LIMIT 1")
        hw = cursor.fetchone()

        if hw:
            id_host = hw['id_host']
            hw['data_hora_coleta'] = str(hw['data_hora_coleta'])
            hardware = hw
            
            # 2. Pega os dados do host que enviou essa métrica
            cursor.execute("SELECT * FROM hosts WHERE id_host = %s", (id_host,))
            host = cursor.fetchone() or {}
            if 'data_cadastro' in host and host['data_cadastro']:
                host['data_cadastro'] = str(host['data_cadastro'])

            # 3. Pega o último teste de rede ESPECÍFICO deste host
            cursor.execute("SELECT * FROM testes_rede WHERE id_host = %s ORDER BY data_hora_teste DESC LIMIT 1", (id_host,))
            tr = cursor.fetchone()
            if tr:
                tr['data_hora_teste'] = str(tr['data_hora_teste'])
                teste_rede = tr

        return jsonify({
            "online": bool(hardware),
            "host": host,
            "hardware": hardware,
            "teste_rede": teste_rede
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        db.fechar()


@app.route('/api/testes-rede', methods=['GET'])
def testes_rede():
    limite = request.args.get('limite', 100, type=int)
    db = Database()
    db.conectar()
    if not db.conexao:
        return jsonify({"erro": "Falha na conexão com o banco"}), 500

    cursor = db.conexao.cursor(dictionary=True)
    try:
        # Traz os testes de rede e o nome da máquina (JOIN com tabela hosts)
        # para popular a tabela do historico.html
        sql = """
            SELECT t.*, h.nome_maquina 
            FROM testes_rede t
            LEFT JOIN hosts h ON t.id_host = h.id_host
            ORDER BY t.data_hora_teste DESC
            LIMIT %s
        """
        cursor.execute(sql, (limite,))
        resultados = cursor.fetchall()

        # Formatando as datas para JSON
        for row in resultados:
            if 'data_hora_teste' in row and row['data_hora_teste']:
                row['data_hora_teste'] = str(row['data_hora_teste'])

        return jsonify(resultados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        db.fechar()

if __name__ == '__main__':
    # Roda a API exposta na rede local na porta 5000 para aceitar conexões externas
    app.run(host='0.0.0.0', port=5000, debug=True)