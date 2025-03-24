import flet as ft
from view.tarefa_view import on_add_tarefa_click, atualizar_lista_tarefas

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Campo de entrada para a descrição da tarefa
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300)
    
    # Campo de entrada para a situação (Checkbox)
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)
    
    # Botão para adicionar a tarefa
    add_button = ft.ElevatedButton("Cadastrar Tarefa", on_click=lambda e: on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tarefas_column))
    
    # Área de resultado (onde será mostrado se a tarefa foi cadastrada ou não)
    result_text = ft.Text()

    # Coluna para exibir a lista de tarefas
    tarefas_column = ft.Column()

    # Adiciona todos os componentes na página
    page.add(descricao_input, situacao_input, add_button, result_text, tarefas_column)

    # Inicializa a lista de tarefas
    atualizar_lista_tarefas(tarefas_column)

