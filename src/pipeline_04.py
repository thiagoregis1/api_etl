import os
import time
import requests
import logging
import logfire
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logging import basicConfig, getLogger
from database import Base, BitcoinPreco




# Configuração Logfire
logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger = getLogger(__name__)
logger.setLevel(logging.INFO)


load_dotenv()


# Variaveis postgree .env
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}{POSTGRES_DB}"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def criar_tabela():
    """Cria a tabela no banco de dados, se não existir."""
    Base.metadata.create_all(engine)
    print("Tabela criada/verificada com sucesso!")

def extrair_dados_bitcoin():
    """Extrai o JSON completo da API da Coinbase."""
    url = 'https://api.coinbase.com/v2/prices/spot'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"Erro na API: {resposta.status_code}")
        return None

def tratar_dados_bitcoin(dados_json):
    """Transforma os dados brutos da API e adiciona timestamp."""
    valor = float(dados_json['data']['amount'])
    criptomoeda = dados_json['data']['base']
    moeda = dados_json['data']['currency']
    timestamp = datetime.now()
    
    dados_tratados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }
    return dados_tratados

def salvar_dados_postgres(dados):
    """Salva os dados no banco PostgreSQL."""
    session = Session()
    novo_registro = BitcoinPreco(**dados)
    session.add(novo_registro)
    session.commit()
    session.close()
    print(f"[{dados['timestamp']}] Dados salvos no PostgreSQL!")

if __name__ == "__main__":
    criar_tabela()
    print("Iniciando ETL com atualização a cada 15 segundos... (CTRL+C para interromper)")

    while True:
        try:
            dados_json = extrair_dados_bitcoin()
            if dados_json:
                dados_tratados = tratar_dados_bitcoin(dados_json)
                print("Dados Tratados:", dados_tratados)
                salvar_dados_postgres(dados_tratados)
            time.sleep(15)
        except KeyboardInterrupt:
            print("\nProcesso interrompido pelo usuário. Finalizando...")
            break
        except Exception as e:
            print(f"Erro durante a execução: {e}")
            time.sleep(15)