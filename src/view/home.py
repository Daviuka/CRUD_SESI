import flet as ft
from services.tarefa_services import cadastrar_tarefa, listar_tarefas, remover_tarefa

# Classe para representar uma tarefa com funcionalidade de edição e remoção
class Task(ft.Row):
    def __init__(self, tarefa_id, text, situacao, atualizar_lista):
        super().__init__()
        self.tarefa_id = tarefa_id  # ID da tarefa
        self.text_view = ft.Text(text)  # Exibição do texto da tarefa
        self.text_edit = ft.TextField(value=text, visible=False)  # Campo de edição do texto
        self.checkbox = ft.Checkbox(value=situacao)  # Checkbox para marcar a tarefa como concluída
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)  # Botão para editar a tarefa
        self.save_button = ft.IconButton(
            visible=False, icon=ft.icons.SAVE, on_click=self.save  # Botão para salvar a edição
        )
        self.delete_button = ft.IconButton(
            icon=ft.icons.DELETE, on_click=self.delete_clicked  # Botão para remover a tarefa
        )
        self.atualizar_lista = atualizar_lista  # Função para atualizar a lista de tarefas
        self.controls = [
            self.checkbox,
            self.text_view,
            self.text_edit,
            self.edit_button,
            self.save_button,
            self.delete_button,
        ]  # Componentes visuais da tarefa

    # Função para habilitar o modo de edição
    def edit(self, e):
        self.edit_button.visible = False  # Esconde o botão de edição
        self.save_button.visible = True  # Mostra o botão de salvar
        self.text_view.visible = False  # Esconde o texto da tarefa
        self.text_edit.visible = True  # Mostra o campo de edição
        self.update()  # Atualiza a interface

    # Função para salvar as alterações feitas na tarefa
    def save(self, e):
        self.edit_button.visible = True  # Mostra o botão de edição
        self.save_button.visible = False  # Esconde o botão de salvar
        self.text_view.visible = True  # Mostra o texto da tarefa
        self.text_edit.visible = False  # Esconde o campo de edição
        self.text_view.value = self.text_edit.value  # Atualiza o texto da tarefa com o valor editado
        self.atualizar_lista()  # Atualiza a lista de tarefas
        self.update()  # Atualiza a interface

    # Função para remover a tarefa
    def delete_clicked(self, e):
        sucesso = remover_tarefa(self.tarefa_id)  # Chama o serviço para remover a tarefa
        if sucesso:
            print(f"Tarefa {self.tarefa_id} removida com sucesso.")  # Mensagem de sucesso
            self.atualizar_lista()  # Atualiza a lista de tarefas
        else:
            print(f"Erro ao remover a tarefa {self.tarefa_id}.")  # Mensagem de erro

# Função para abrir uma nova página
def open_new_page(page: ft.Page):
    def go_back(e):
        page.views.pop()  # Remove a página atual
        page.update()  # Atualiza a interface

    # Define o conteúdo da nova página
    new_page = ft.View(
        "/new_page",
        [
            ft.Text("Bem-vindo à nova página!", size=20),
            ft.ElevatedButton("Voltar", on_click=go_back),  # Botão para voltar à página principal
        ],
    )
    page.views.append(new_page)  # Adiciona a nova página à pilha de visualizações
    page.update()  # Atualiza a interface

# Função principal para configurar a interface
def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"  # Título da página
    page.scroll = 'adaptive'  # Habilita o scroll adaptativo
    page.padding = 20  # Define o padding da página
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Alinha os elementos verticalmente ao centro

    # Adiciona o NavigationBar à página
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
            ft.NavigationBarDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Bookmarks",
            ),
        ]
    )

    # Função para adicionar uma nova tarefa
    def on_add_tarefa_click(e):
        descricao = descricao_input.value.strip()  # Obtém o valor do campo de descrição
        situacao = situacao_input.value  # Obtém o valor do checkbox

        if not descricao:  # Verifica se a descrição está vazia
            result_text.value = "A descrição da tarefa não pode estar vazia."  # Mensagem de erro
            result_text.color = "red"  # Define a cor da mensagem como vermelha
            page.update()  # Atualiza a interface
            return

        # Chama o serviço para cadastrar a tarefa
        nova_tarefa = cadastrar_tarefa(descricao, situacao)
        if nova_tarefa:  # Verifica se a tarefa foi cadastrada com sucesso
            result_text.value = "Tarefa cadastrada com sucesso!"  # Mensagem de sucesso
            result_text.color = "green"  # Define a cor da mensagem como verde
            descricao_input.value = ""  # Limpa o campo de descrição
            situacao_input.value = False  # Reseta o checkbox
            atualizar_lista_tarefas()  # Atualiza a lista de tarefas
        else:
            result_text.value = "Erro ao cadastrar a tarefa."  # Mensagem de erro
            result_text.color = "red"  # Define a cor da mensagem como vermelha

        page.update()  # Atualiza a interface

    # Função para atualizar a lista de tarefas
    def atualizar_lista_tarefas():
        tarefas_column.controls.clear()  # Limpa a coluna de tarefas
        tarefas = listar_tarefas()  # Obtém a lista de tarefas do banco de dados
        if tarefas:  # Verifica se existem tarefas
            for tarefa in tarefas:
                tarefas_column.controls.append(
                    Task(
                        tarefa_id=tarefa.id,
                        text=tarefa.descricao,
                        situacao=tarefa.situacao,
                        atualizar_lista=atualizar_lista_tarefas,
                    )
                )  # Adiciona cada tarefa à coluna
        else:
            tarefas_column.controls.append(ft.Text("Nenhuma tarefa encontrada."))  # Mensagem caso não existam tarefas

        page.update()  # Atualiza a interface

    # Campo de entrada para a descrição da tarefa
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300)

    # Campo de entrada para a situação (Checkbox)
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)

    # Botão para adicionar a tarefa
    add_button = ft.ElevatedButton("Cadastrar Tarefa", on_click=on_add_tarefa_click)

    # Área de resultado (onde será mostrado se a tarefa foi cadastrada ou não)
    result_text = ft.Text()

    # Coluna para exibir a lista de tarefas
    tarefas_column = ft.Column()

    # Adiciona todos os componentes na página
    page.add(
        ft.Column([
            descricao_input,
            situacao_input,
            add_button,
            result_text,
            tarefas_column
        ])
    )

    # Inicializa a lista de tarefas
    atualizar_lista_tarefas()