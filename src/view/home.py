import flet as ft
from services.tarefa_services import cadastrar_tarefa, listar_tarefas, remover_tarefa

# Classe para representar uma tarefa com funcionalidade de edição e remoção
class Task(ft.Row):
    def __init__(self, tarefa_id, text, situacao, atualizar_lista):
        super().__init__()
        self.tarefa_id = tarefa_id
        self.text_view = ft.Text(text)
        self.text_edit = ft.TextField(value=text, visible=False)
        self.checkbox = ft.Checkbox(value=situacao)
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)
        self.save_button = ft.IconButton(
            visible=False, icon=ft.icons.SAVE, on_click=self.save
        )
        self.delete_button = ft.IconButton(
            icon=ft.icons.DELETE, on_click=self.delete_clicked
        )
        self.atualizar_lista = atualizar_lista
        self.controls = [
            self.checkbox,
            self.text_view,
            self.text_edit,
            self.edit_button,
            self.save_button,
            self.delete_button,
        ]

    def edit(self, e):
        self.edit_button.visible = False
        self.save_button.visible = True
        self.text_view.visible = False
        self.text_edit.visible = True
        self.update()

    def save(self, e):
        self.edit_button.visible = True
        self.save_button.visible = False
        self.text_view.visible = True
        self.text_edit.visible = False
        self.text_view.value = self.text_edit.value
        # Aqui você pode chamar um serviço para atualizar a tarefa no banco de dados
        # Exemplo: editar_tarefa(self.tarefa_id, self.text_edit.value, self.checkbox.value)
        self.atualizar_lista()
        self.update()

    def delete_clicked(self, e):
        # Chama o serviço para remover a tarefa
        sucesso = remover_tarefa(self.tarefa_id)
        if sucesso:
            print(f"Tarefa {self.tarefa_id} removida com sucesso.")
            self.atualizar_lista()
        else:
            print(f"Erro ao remover a tarefa {self.tarefa_id}.")

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.scroll = 'adaptive'
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Função para adicionar uma nova tarefa
    def on_add_tarefa_click(e):
        descricao = descricao_input.value.strip()
        situacao = situacao_input.value

        if not descricao:
            result_text.value = "A descrição da tarefa não pode estar vazia."
            result_text.color = "red"
            page.update()
            return

        # Chama o serviço para cadastrar a tarefa
        nova_tarefa = cadastrar_tarefa(descricao, situacao)
        if nova_tarefa:
            result_text.value = "Tarefa cadastrada com sucesso!"
            result_text.color = "green"
            descricao_input.value = ""
            situacao_input.value = False
            atualizar_lista_tarefas()
        else:
            result_text.value = "Erro ao cadastrar a tarefa."
            result_text.color = "red"

        page.update()

    # Função para atualizar a lista de tarefas
    def atualizar_lista_tarefas():
        tarefas_column.controls.clear()
        tarefas = listar_tarefas()
        if tarefas:
            for tarefa in tarefas:
                tarefas_column.controls.append(
                    Task(
                        tarefa_id=tarefa.id,
                        text=tarefa.descricao,
                        situacao=tarefa.situacao,
                        atualizar_lista=atualizar_lista_tarefas,
                    )
                )
        else:
            tarefas_column.controls.append(ft.Text("Nenhuma tarefa encontrada."))

        page.update()

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