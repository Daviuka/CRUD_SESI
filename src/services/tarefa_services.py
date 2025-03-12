from sqlalchemy.orm import Session
from models.tarefa_model import Tarefa

def criar_tarefa(db: Session, descricao: str, situacao: str = "Pendente"):
    nova_tarefa = Tarefa(descricao=descricao, situacao=situacao)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

def listar_tarefas(db: Session):
    return db.query(Tarefa).all()

def atualizar_tarefa(db: Session, tarefa_id: int, descricao: str, situacao: str):
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if tarefa:
        tarefa.descricao = descricao
        tarefa.situacao = situacao
        db.commit()
        db.refresh(tarefa)
    return tarefa

def excluir_tarefa(db: Session, tarefa_id: int):
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if tarefa:
        db.delete(tarefa)
        db.commit()
    return tarefa
