import requests
from tinydb import TinyDB
from datetime import datetime

def extrair_dados_bitcoin():
    """Extrai o JSON completo da API da Coinbase."""
    url = 'https://api.coinbase.com/v2/prices/spot'
    resposta = requests.get(url)
    return resposta.json()

def tratar_dados_bitcoin(dados_json):
    """Transforma os dados brutos da API e adiciona timestamp."""
    valor = float(dados_json['data']['amount'])
    criptomoeda = dados_json['data']['base']
    moeda = dados_json['data']['currency']
    dados_tratados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda
                }
    return dados_tratados

def salvar_dados_tinydb(dados, db_name="bitcoin_dados.json"):
    """Salva os dados em um banco NoSQL usando TinyDB."""
    db = TinyDB(db_name)
    db.insert(dados)
    print("Dados salvos no TinyDB!")

if __name__ == "__main__":
    dados_json = extrair_dados_bitcoin()
    dados_tratados = tratar_dados_bitcoin(dados_json)

    print("Dados Tratados:")
    print(dados_tratados)

    salvar_dados_tinydb(dados_tratados)