from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models.tarefa_model import create_tables

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Classe de configuração para armazenar as informações do banco de dados
class Config:
    # Obtém as credenciais do banco de dados a partir das variáveis de ambiente ou usa valores padrão
    DB_USER = os.getenv('DB_USER', 'davibcs').strip()  # Nome do usuário do banco
    DB_PASS = os.getenv('DB_PASS', 'd2a0v0i8').strip()  # Senha do banco
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1').strip()  # Host do banco
    DB_NAME = os.getenv('DB_NAME', 'db_todolistcrud').strip()  # Nome do banco
    DB_PORT = os.getenv('DB_PORT', '3306').strip()  # Porta do banco
    # Monta a URL de conexão com o banco de dados
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Função para criar o engine do SQLAlchemy
def get_engine():
    try:
        # Cria o engine com base na URL de conexão
        engine = create_engine(Config.DATABASE_URL)
        print("Engine criado com sucesso.")  # Mensagem de sucesso
        return engine
    except Exception as e:
        # Exibe uma mensagem de erro caso o engine não seja criado
        print(f"Erro ao criar o engine: {e}")
        raise  # Relança a exceção para depuração

# Função para configurar a sessão do SQLAlchemy
def get_session():
    try:
        # Obtém o engine para configurar a sessão
        engine = get_engine()
        # Configura a sessão com autocommit e autoflush desativados
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("Sessão configurada com sucesso.")  # Mensagem de sucesso
        return Session
    except Exception as e:
        # Exibe uma mensagem de erro caso a sessão não seja configurada
        print(f"Erro ao configurar a sessão: {e}")
        raise  # Relança a exceção para depuração

# Testa a conexão e cria as tabelas no banco de dados
try:
    # Obtém o engine para conectar ao banco de dados
    engine = get_engine()
    with engine.connect() as connection:
        # Testa a conexão com o banco de dados
        print("Conexão bem-sucedida com o banco de dados.")
        # Cria as tabelas no banco de dados com base no modelo
        create_tables(engine)
except Exception as e:
    # Exibe uma mensagem de erro caso a conexão ou criação de tabelas falhe
    print(f"Erro ao conectar ao banco de dados: {e}")