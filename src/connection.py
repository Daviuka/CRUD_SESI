from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "mysql+mysqlconnector://username:password@localhost/db_name"

# Criação da engine
engine = create_engine(DATABASE_URI)

# Criando a sessão
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
