import flet as ft
from services.tarefa_services import criar_tarefa, atualizar_tarefa
from src.connection import Session, engine
from models.tarefa_model import Tarefa

def tarefa_view(page, tarefa_id=None):
    db = Session(bind=engine)
    
    descricao = ft.TextField(label="Descrição da tarefa")
    situacao = ft.Dropdown(options=["Pendente", "Concluída"], label="Situação")

    if tarefa_id:
        tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        if tarefa:
            descricao.value = tarefa.descricao
            situacao.value = tarefa.situacao

    def salvar(event):
        if tarefa_id:
            tarefa_atualizada = atualizar_tarefa(db, tarefa_id, descricao.value, situacao.value)
            page.add(ft.Text(f"Tarefa {tarefa_atualizada.id} atualizada"))
        else:
            nova_tarefa = criar_tarefa(db, descricao.value, situacao.value)
            page.add(ft.Text(f"Tarefa {nova_tarefa.id} criada"))
        
        page.update()
    
    page.add(descricao, situacao, ft.ElevatedButton("Salvar", on_click=salvar))
    
    db.close()

