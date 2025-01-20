import requests
from datetime import datetime

def extrair_dados_bitcoin():
    """Extrai o JSON completo da API da Coinbase."""
    url = 'https://api.coinbase.com/v2/prices/spot'
    resposta = requests.get(url)
    return resposta.json()

def tratar_dados_bitcoin(dados_json):
    """Transforma os dados brutos da API, renomeia colunas e adiciona timestamp."""
    valor = dados_json['data']['amount']
    criptomoeda = dados_json['data']['base']
    moeda = dados_json['data']['currency']
                
    dados_tratados = [{
            "valor": valor,
            "criptomoeda": criptomoeda,
            "moeda": moeda
        }]
        
    return dados_tratados


if __name__ == "__main__":
    # Extração dos dados
    dados_json = extrair_dados_bitcoin()
    dados_tratados = tratar_dados_bitcoin(dados_json)
    print(dados_tratados)