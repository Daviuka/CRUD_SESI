import flet as ft
from services.tarefa_services import cadastrar_tarefa, listar_tarefas, remover_tarefa, editar_tarefa

# Classe para representar uma tarefa com funcionalidade de edição e remoção
class Task(ft.Row):
    def __init__(self, tarefa_id, text, situacao, atualizar_lista):
        super().__init__()
        self.tarefa_id = tarefa_id  # ID da tarefa
        self.atualizar_lista = atualizar_lista  # Função para atualizar a lista de tarefas
        self.texto_original = text  # Texto original da tarefa

        # Checkbox para marcar a tarefa como concluída ou não
        self.checkbox = ft.Checkbox(value=situacao)

        # Exibição do texto da tarefa
        self.text_view = ft.Text(text, expand=True)

        # Campo de edição do texto da tarefa
        self.text_edit = ft.TextField(value=text, visible=False, expand=True)

        # Botão para editar a tarefa
        self.btn_editar = ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=self.toggle_edit)

        # Botão para salvar as alterações feitas na tarefa
        self.btn_salvar = ft.IconButton(icon=ft.icons.SAVE, tooltip="Salvar", visible=False, on_click=self.salvar_edicao)

        # Controles que compõem a tarefa
        self.controls = [
            self.checkbox,
            self.text_view,
            self.text_edit,
            self.btn_editar,
            self.btn_salvar,
        ]

    # Alterna entre o modo de exibição e o modo de edição
    def toggle_edit(self, e):
        self.text_view.visible = False
        self.text_edit.visible = True
        self.btn_editar.visible = False
        self.btn_salvar.visible = True
        self.update()

    # Salva as alterações feitas na tarefa
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

# Função principal que configura a interface do aplicativo
def main(page: ft.Page):
    # Configurações iniciais da página
    page.title = "Task of Lord"  # Título da janela
    page.theme = ft.Theme(font_family="lord_ring")  # Tema com fonte personalizada
    page.window.width = 450  # Largura da janela
    page.window.height = 800  # Altura da janela
    page.fonts = {
        "lord_ring": 'fonts/ringbearer/RINGM___.TTF',  # Fonte personalizada para o título
        "soloist": 'fonts/soloist/soloistacad.ttf',  # Fonte personalizada para outros textos
    }

    # Função para fechar o aplicativo
    def sair_do_aplicativo(e):
        page.window.destroy()

    # Componentes da view "Cadastrar Tarefa"
    resultado = ft.Text()  # Texto para exibir mensagens de sucesso ou erro
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300)  # Campo de entrada para a descrição
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)  # Checkbox para marcar a tarefa como concluída
    tarefas_column = ft.Column()  # Coluna para exibir a lista de tarefas
    tarefas_feito_desfeito_column = ft.Column()  # Coluna para exibir tarefas feitas e não feitas

    # Atualiza a lista de tarefas na view "Cadastrar Tarefa"
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

    # Atualiza a lista de tarefas na view "Feito e Desfeito"
    def atualizar_lista_feito_desfeito():
        tarefas_feito_desfeito_column.controls.clear()
        tarefas = listar_tarefas()
        if tarefas:
            feitas = [t for t in tarefas if t.situacao]
            nao_feitas = [t for t in tarefas if not t.situacao]

            # Adiciona as tarefas feitas
            tarefas_feito_desfeito_column.controls.append(ft.Text("Tarefas Feitas", size=20))
            for tarefa in feitas:
                tarefas_feito_desfeito_column.controls.append(Task(
                    tarefa_id=tarefa.id,
                    text=tarefa.descricao,
                    situacao=tarefa.situacao,
                    atualizar_lista=atualizar_lista_feito_desfeito
                ))

            # Adiciona as tarefas não feitas
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

    # Função para adicionar uma nova tarefa
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

    # Função para remover tarefas selecionadas
    def remover_tarefas_selecionadas(e):
        for tarefa in tarefas_column.controls[:]:
            if isinstance(tarefa, Task) and tarefa.checkbox.value:
                remover_tarefa(tarefa.tarefa_id)
        atualizar_lista_cadastrar()

    # View "Cadastrar Tarefa"
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

    # View "Feito e Desfeito"
    feito_desfeito_view = ft.Column([
        ft.Row([ft.Text("Feito e Desfeito", size=35, font_family="lord_ring", color=ft.colors.YELLOW_ACCENT)],
               alignment=ft.MainAxisAlignment.CENTER),
        tarefas_feito_desfeito_column,
        ft.ElevatedButton(text="Sair", icon=ft.icons.EXIT_TO_APP, on_click=sair_do_aplicativo),
    ])

    # Container principal para alternar entre as views
    content_container = ft.Container(content=cadastrar_view)

    # Função para alternar entre as views
    def on_nav_change(e):
        if nav_bar.selected_index == 0:
            content_container.content = cadastrar_view
            atualizar_lista_cadastrar()
        elif nav_bar.selected_index == 1:
            content_container.content = feito_desfeito_view
            atualizar_lista_feito_desfeito()
        page.update()

    # NavigationBar para alternar entre as views
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.TASK_OUTLINED, label="Cadastrar Tarefa"),
            ft.NavigationBarDestination(icon=ft.icons.TASK_ALT_OUTLINED, label="Feito e Desfeito"),
        ],
        selected_index=0,
        on_change=on_nav_change
    )

    # Layout final da página
    page.navigation_bar = nav_bar
    page.add(content_container)
    atualizar_lista_cadastrar()