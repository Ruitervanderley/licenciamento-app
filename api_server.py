# api_server.py
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Acessa a chave secreta da variável de ambiente
api_secret_key = os.getenv('API_SECRET_KEY', 'default-secret-key')

# Simula uma base de dados de seriais
seriais_db = {
    "SERIAL1234": {"usuario_id": "default_user", "validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")},
    "SERIAL5678": {"usuario_id": "outro_usuario", "validade": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")},
}

@app.route('/validar_serial', methods=['POST'])
def validar_serial():
    data = request.json
    serial = data.get('serial')
    usuario_id = data.get('usuario_id')

    if serial in seriais_db and seriais_db[serial]["usuario_id"] == usuario_id:
        validade = datetime.strptime(seriais_db[serial]["validade"], "%Y-%m-%d")
        if datetime.now() <= validade:
            return jsonify({"valido": True, "validade": seriais_db[serial]["validade"]})
        else:
            return jsonify({"valido": False, "mensagem": "Serial expirado"})
    else:
        return jsonify({"valido": False, "mensagem": "Serial inválido ou não encontrado"})

if __name__ == '__main__':
    app.run(debug=True)
