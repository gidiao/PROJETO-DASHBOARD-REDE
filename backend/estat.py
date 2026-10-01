from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

@app.route('/api/metricas', methods=['GET'])
def get_metricas():
    data_inicio = request.args.get('inicio')
    data_fim = request.args.get('fim')

    # Adiciona as horas extremas para o BETWEEN cobrir os dias inteiros selecionados
    inicio_formatado = f"{data_inicio} 00:00:00"
    fim_formatado = f"{data_fim} 23:59:59"

    conn = mysql.connector.connect(
        host="192.168.0.110", 
        user="admin",      
        password="123456",      
        database="monitoramento" 
    )
    cursor = conn.cursor(dictionary=True)

    # Nova query com CAST na data (para evitar erros de JSON) e os parâmetros %s no BETWEEN
    query = """
        SELECT 
            CAST(DATE(data_hora_coleta) AS CHAR) AS data_da_coleta,
            HOUR(data_hora_coleta) AS hora_do_dia, 
            AVG(cpu_percentual) AS media_cpu,
            AVG(memoria_usada_mb) AS media_memoria 
        FROM metricas_hardware 
        WHERE id_host = 1 or id_host = 3
        AND data_hora_coleta BETWEEN %s AND %s
        GROUP BY DATE(data_hora_coleta), HOUR(data_hora_coleta)
        ORDER BY data_da_coleta, hora_do_dia;
    """
    
    # Executamos passando os parâmetros de data dinâmica
    cursor.execute(query, (inicio_formatado, fim_formatado))
    resultados = cursor.fetchall()

    # Como a função AVG() retorna 'Decimal', convertemos para 'float' para o jsonify não quebrar
    dados_formatados = []
    for linha in resultados:
        dados_formatados.append({
            'data_da_coleta': linha['data_da_coleta'],
            'hora_do_dia': linha['hora_do_dia'],
            'media_cpu': round(float(linha['media_cpu']), 2) if linha['media_cpu'] is not None else 0.0,
            'media_memoria': round(float(linha['media_memoria']), 2) if linha['media_memoria'] is not None else 0.0
        })

    cursor.close()
    conn.close()

    return jsonify(dados_formatados)

if __name__ == '__main__':
    app.run(debug=True, port=5000)