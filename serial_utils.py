# serial_utils.py
import hashlib
import os
import datetime
import requests

SERIAL_FILE_PATH = "serial.txt"  # Caminho do arquivo onde o serial será salvo
API_URL = "https://licenciamento-app.onrender.com/validar_serial"  # Substitua pelo seu URL de serviço

def verificar_serial_online(serial: str, usuario_id: str) -> bool:
    """
    Verifica se o serial fornecido é válido consultando a API online.
    """
    try:
        response = requests.post(API_URL, json={"serial": serial, "usuario_id": usuario_id})
        if response.status_code == 200:
            data = response.json()
            if data["valido"]:
                return True
            else:
                print(data.get("mensagem", "Erro desconhecido."))
                return False
        else:
            print("Erro ao conectar-se à API de validação.")
            return False
    except requests.RequestException as e:
        print(f"Erro de conexão: {e}")
        return False

def salvar_serial(serial: str):
    """
    Salva o serial em um arquivo local.
    """
    with open(SERIAL_FILE_PATH, "w") as file:
        file.write(serial)

def carregar_serial() -> str:
    """
    Carrega o serial salvo do arquivo local.
    """
    if os.path.exists(SERIAL_FILE_PATH):
        with open(SERIAL_FILE_PATH, "r") as file:
            return file.read().strip()
    return ""

def verificar_ativacao() -> bool:
    """
    Verifica se o aplicativo já foi ativado consultando o serial salvo.
    """
    serial = carregar_serial()
    usuario_id = "default_user"  # ID de usuário fixo ou pode ser gerado dinamicamente
    return verificar_serial_online(serial, usuario_id)

def obter_validade_serial() -> str:
    """
    Obtém a data de validade do serial atual consultando a API online.
    """
    serial = carregar_serial()
    if serial:
        try:
            response = requests.post(API_URL, json={"serial": serial, "usuario_id": "default_user"})
            if response.status_code == 200:
                data = response.json()
                if data["valido"]:
                    return data.get("validade", "Data de validade não encontrada")
                else:
                    return "Serial inválido ou expirado"
            else:
                return "Erro ao conectar-se à API"
        except requests.RequestException as e:
            return f"Erro de conexão: {e}"
    return "Nenhum serial encontrado"
