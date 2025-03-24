from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models.tarefa_model import create_tables

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    DB_USER = os.getenv('DB_USER', 'davibcs')  # Nome do usuário do banco
    DB_PASS = os.getenv('DB_PASS', 'd2a0v0i8')  # Senha do banco
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')  # Host do banco
    DB_NAME = os.getenv('DB_NAME', 'db_todolistcrud')  # Nome do banco
    DB_PORT = os.getenv('DB_PORT', '3306')  # Porta do banco
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Função para criar o engine do SQLAlchemy
def get_engine():
    try:
        engine = create_engine(Config.DATABASE_URL)
        print("Engine criado com sucesso.")
        return engine
    except Exception as e:
        print(f"Erro ao criar o engine: {e}")
        raise

# Função para configurar a sessão do SQLAlchemy
def get_session(engine):
    try:
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("Sessão configurada com sucesso.")
        return Session
    except Exception as e:
        print(f"Erro ao configurar a sessão: {e}")
        raise

# Testa a conexão e cria as tabelas
try:
    engine = get_engine()
    with engine.connect() as connection:
        print("Conexão bem-sucedida com o banco de dados.")
        create_tables(engine)
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")