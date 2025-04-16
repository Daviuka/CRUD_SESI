import flet as ft
from services.tarefa_services import cadastrar_tarefa, listar_tarefas, remover_tarefa, editar_tarefa

# Classe para representar uma tarefa com funcionalidade de edição e remoção
class Task(ft.Row):
    def __init__(self, tarefa_id, text, situacao, atualizar_lista):
        super().__init__()
        self.tarefa_id = tarefa_id
        self.atualizar_lista = atualizar_lista
        self.texto_original = text

        self.checkbox = ft.Checkbox(value=situacao)
        self.text_view = ft.Text(text, expand=True)
        self.text_edit = ft.TextField(value=text, visible=False, expand=True)

        self.btn_editar = ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=self.toggle_edit)
        self.btn_salvar = ft.IconButton(icon=ft.icons.SAVE, tooltip="Salvar", visible=False, on_click=self.salvar_edicao)


        self.controls = [
            self.checkbox,
            self.text_view,
            self.text_edit,
            self.btn_editar,
            self.btn_salvar,
        ]

    def toggle_edit(self, e):
        self.text_view.visible = False
        self.text_edit.visible = True
        self.btn_editar.visible = False
        self.btn_salvar.visible = True
        self.update()

    def salvar_edicao(self, e):
        novo_texto = self.text_edit.value.strip()
        if novo_texto and novo_texto != self.texto_original:
            editar_tarefa(self.tarefa_id, novo_texto, self.checkbox.value)
            self.texto_original = novo_texto
        self.text_view.value = self.texto_original
        self.text_view.visible = True
        self.text_edit.visible = False
        self.btn_editar.visible = True
        self.btn_salvar.visible = False
        self.atualizar_lista()



# Função principal
def main(page: ft.Page):
    page.title = "Task of Lord"
    page.theme = ft.Theme(font_family="lord_ring")
    page.window.width = 450
    page.window.height = 800
    page.fonts = {
        "lord_ring": 'fonts/ringbearer/RINGM___.TTF',
        "soloist": 'fonts/soloist/soloistacad.ttf',
    }

    def sair_do_aplicativo(e):
        page.window.destroy()

    # Views
    resultado = ft.Text()
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300)
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)
    tarefas_column = ft.Column()
    tarefas_feito_desfeito_column = ft.Column()

    def atualizar_lista_cadastrar():
        tarefas_column.controls.clear()
        tarefas = listar_tarefas()
        if tarefas:
            for tarefa in tarefas:
                tarefas_column.controls.append(Task(
                    tarefa_id=tarefa.id,
                    text=tarefa.descricao,
                    situacao=tarefa.situacao,
                    atualizar_lista=atualizar_lista_cadastrar
                ))
        else:
            tarefas_column.controls.append(ft.Text("Nenhuma tarefa encontrada."))
        page.update()

    def atualizar_lista_feito_desfeito():
        tarefas_feito_desfeito_column.controls.clear()
        tarefas = listar_tarefas()
        if tarefas:
            feitas = [t for t in tarefas if t.situacao]
            nao_feitas = [t for t in tarefas if not t.situacao]

            tarefas_feito_desfeito_column.controls.append(ft.Text("Tarefas Feitas", size=20))
            for tarefa in feitas:
                tarefas_feito_desfeito_column.controls.append(Task(
                    tarefa_id=tarefa.id,
                    text=tarefa.descricao,
                    situacao=tarefa.situacao,
                    atualizar_lista=atualizar_lista_feito_desfeito
                ))

            tarefas_feito_desfeito_column.controls.append(ft.Text("Tarefas Não Feitas", size=20))
            for tarefa in nao_feitas:
                tarefas_feito_desfeito_column.controls.append(Task(
                    tarefa_id=tarefa.id,
                    text=tarefa.descricao,
                    situacao=tarefa.situacao,
                    atualizar_lista=atualizar_lista_feito_desfeito
                ))
        else:
            tarefas_feito_desfeito_column.controls.append(ft.Text("Nenhuma tarefa encontrada."))
        page.update()

    def on_add_tarefa_click(e):
        descricao = descricao_input.value.strip()
        situacao = situacao_input.value

        if not descricao:
            resultado.value = "A descrição da tarefa não pode estar vazia."
            resultado.color = "red"
        else:
            nova_tarefa = cadastrar_tarefa(descricao, situacao)
            if nova_tarefa:
                resultado.value = "Tarefa cadastrada com sucesso!"
                resultado.color = "green"
                descricao_input.value = ""
                situacao_input.value = False
            else:
                resultado.value = "Erro ao cadastrar a tarefa."
                resultado.color = "red"
        atualizar_lista_cadastrar()
        page.update()

    def remover_tarefas_selecionadas(e):
        for tarefa in tarefas_column.controls[:]:
            if isinstance(tarefa, Task) and tarefa.checkbox.value:
                remover_tarefa(tarefa.tarefa_id)
        atualizar_lista_cadastrar()

    # Views
    cadastrar_view = ft.Column([
        ft.Row([ft.Text("Gerenciador de Tarefas", size=35, font_family="lord_ring", color=ft.colors.YELLOW_ACCENT)],
               alignment=ft.MainAxisAlignment.CENTER),
        descricao_input,
        situacao_input,
        ft.Row([
            ft.ElevatedButton("Cadastrar", on_click=on_add_tarefa_click),
            ft.ElevatedButton("Remover Selecionadas", icon=ft.icons.DELETE, on_click=remover_tarefas_selecionadas)
        ]),
        resultado,
        tarefas_column,
        ft.ElevatedButton(text="Sair", icon=ft.icons.EXIT_TO_APP, on_click=sair_do_aplicativo),
    ])

    feito_desfeito_view = ft.Column([
        ft.Row([ft.Text("Feito e Desfeito", size=35, font_family="lord_ring", color=ft.colors.YELLOW_ACCENT)],
               alignment=ft.MainAxisAlignment.CENTER),
        tarefas_feito_desfeito_column,
        ft.ElevatedButton(text="Sair", icon=ft.icons.EXIT_TO_APP, on_click=sair_do_aplicativo),
    ])

    content_container = ft.Container(content=cadastrar_view)

    # Navegação
    def on_nav_change(e):
        if nav_bar.selected_index == 0:
            content_container.content = cadastrar_view
            atualizar_lista_cadastrar()
        elif nav_bar.selected_index == 1:
            content_container.content = feito_desfeito_view
            atualizar_lista_feito_desfeito()
        page.update()

    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.TASK_OUTLINED, label="Cadastrar Tarefa"),
            ft.NavigationBarDestination(icon=ft.icons.TASK_ALT_OUTLINED, label="Feito e Desfeito"),
        ],
        selected_index=0,
        on_change=on_nav_change
    )

    # Layout final
    page.navigation_bar = nav_bar
    page.add(content_container)
    atualizar_lista_cadastrar()
