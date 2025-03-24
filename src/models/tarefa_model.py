from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, Boolean

# Criamos a classe base para os modelos
Base = declarative_base()

class Tarefa(Base):
    """
    Modelo representando a tabela 'tarefas' no banco de dados.
    """
    __tablename__ = 'tarefas'

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID único e autoincrementado
    descricao = Column(Text, nullable=True)  # Descrição da tarefa (pode ser nula)
    situacao = Column(Boolean, nullable=False)  # Situação da tarefa (True = concluída, False = pendente)

    def __init__(self, descricao: str, situacao: bool):
        """
        Construtor da classe Tarefa.
        :param descricao: Descrição da tarefa.
        :param situacao: Situação da tarefa (True = concluída, False = pendente).
        """
        self.descricao = descricao
        self.situacao = situacao

def create_tables(engine):
    """
    Cria as tabelas no banco de dados com base nos modelos definidos.
    :param engine: Engine do SQLAlchemy conectada ao banco de dados.
    """
    try:
        Base.metadata.create_all(engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
