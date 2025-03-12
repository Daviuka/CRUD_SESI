from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = 'tarefas'

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(255), nullable=False)
    situacao = Column(String(50), default="Pendente")

    def __repr__(self):
        return f"Tarefa(id={self.id}, descricao={self.descricao}, situacao={self.situacao})"
