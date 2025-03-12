import flet as ft
from services.tarefa_services import listar_tarefas
from src.connection import Session, engine
from models.tarefa_model import Tarefa

def home_view(page):
    db = Session(bind=engine)
    tarefas = listar_tarefas(db)

    page.add(ft.Text("Lista de Tarefas"))
    
    for tarefa in tarefas:
        page.add(ft.Row([
            ft.Text(f"ID: {tarefa.id} - {tarefa.descricao} - {tarefa.situacao}")
        ]))
    
    db.close()
