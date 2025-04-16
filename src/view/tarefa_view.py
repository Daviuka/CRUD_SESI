from services.tarefa_services import cadastrar_tarefa
import flet as ft
from connection import Session
from models.tarefa_model import Tarefa  # Ajuste de import, caso o seu modelo esteja em models.py

# Função para atualizar a lista de tarefas
def atualizar_lista_tarefas(tarefas_column):
    # Criação de uma nova sessão para pegar as tarefas
    session = Session()
    
    try:
        # Limpa a coluna de tarefas
        tarefas_column.controls.clear()

        # Busca todas as tarefas no banco de dados
        todas_tarefas = session.query(Tarefa).all()

        # Adiciona cada tarefa à coluna de tarefas
        for tarefa in todas_tarefas:
            tarefas_column.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(f"ID: {tarefa.id}", weight="bold", size=14),  # Exibe o ID da tarefa
                        ft.Text(
                            f"Descrição: {tarefa.descricao}",
                            size=14,
                            expand=True,  # Faz a descrição ocupar o espaço disponível
                            no_wrap=False,  # Permite que o texto quebre em várias linhas
                        ),
                        ft.Text(
                            f"Concluída: {'Sim' if tarefa.situacao else 'Não'}",
                            size=14,
                            weight="bold",
                        ),
                    ],
                    alignment="spaceBetween",  # Ajusta o alinhamento dos itens
                )
            )

        # Atualiza a tela com as novas tarefas
        tarefas_column.update()

    finally:
        # Fechar a sessão após o processo
        session.close()


# Função para adicionar uma nova tarefa
def on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tarefas_column):
    descricao = descricao_input.value  # Obtém o valor do campo de descrição
    situacao = situacao_input.value  # Obtém o valor do checkbox (situação da tarefa)
    
    # Chama a função de cadastro da tarefa
    tarefa_cadastrada = cadastrar_tarefa(descricao, situacao)
    
    if tarefa_cadastrada:  # Verifica se a tarefa foi cadastrada com sucesso
        result_text.value = f"Tarefa cadastrada com sucesso! ID: {tarefa_cadastrada.id}"  # Mensagem de sucesso
        # Atualiza a lista de tarefas na tela
        atualizar_lista_tarefas(tarefas_column)
    else:
        result_text.value = "Erro ao cadastrar a tarefa."  # Mensagem de erro
    
    # Atualiza o texto na tela
    result_text.update()


# Função para listar todas as tarefas
def on_listar_tarefas_click(e, tarefas_column):
    # Atualiza a lista de tarefas na tela
    atualizar_lista_tarefas(tarefas_column)

