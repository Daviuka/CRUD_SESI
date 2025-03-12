import flet as ft
from view.home import home_view
from view.tarefa_view import tarefa_view

def main(page):
    page.add(home_view(page))
    page.add(ft.ElevatedButton("Criar Tarefa", on_click=lambda e: tarefa_view(page)))

ft.app(target=main)
