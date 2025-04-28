import flet as ft
from services.tarefa_services import cadastrar_tarefa, listar_tarefas, remover_tarefa, editar_tarefa


class Task(ft.Row):
    def __init__(self, tarefa_id, text, situacao, atualizar_lista_cadastrar):
        super().__init__()
        self.tarefa_id = tarefa_id
        self.atualizar_lista_cadastrar = atualizar_lista_cadastrar
        self.texto_original = text

        self.checkbox = ft.Checkbox(value=situacao)
        self.text_view = ft.Text(text, expand=True)
        self.text_edit = ft.TextField(value=text, visible=False, expand=True)
        self.btn_editar = ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=self.edicao)
        self.btn_salvar = ft.IconButton(icon=ft.icons.SAVE, tooltip="Salvar", visible=False, on_click=self.salvar_edicao)

        self.controls = [
            self.checkbox,
            self.text_view,
            self.text_edit,
            self.btn_editar,
            self.btn_salvar,
        ]

    def edicao(self, e):
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
        self.atualizar_lista_cadastrar()
        self.update()


def main(page: ft.Page):
    # Configurações iniciais da página
    page.title = "Task of Lord"  # Título da janela
    page.theme_mode = ft.ThemeMode.DARK  # Modo escuro
    page.theme = ft.Theme(font_family="lord_ring")  # Tema com fonte personalizada
    page.window.width = 450  # Largura da janela
    page.window.height = 800  # Altura da janela
    page.fonts = {
        "lord_ring": 'fonts/ringbearer/RINGM___.TTF',  # Fonte personalizada para o título
        "soloist": 'fonts/soloist/soloistacad.ttf',  # Fonte personalizada para outros textos
    }

    # Plano de fundo
    img = ft.Container(
        expand=True,
        opacity=1.0,
        content=ft.Image(
            src="https://i.postimg.cc/W3S2zxbt/lord-rings.webp",
            fit=ft.ImageFit.COVER,
            width=page.width,
            height=page.height,
        ),
    )

    # Componentes da view "Cadastrar Tarefa"
    resultado = ft.Text()  # Texto para exibir mensagens de sucesso ou erro
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300)  # Campo de entrada para a descrição
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)  # Checkbox para marcar a tarefa como concluída
    tarefas_column = ft.Column()  # Coluna para exibir a lista de tarefas

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
                    atualizar_lista_cadastrar=atualizar_lista_cadastrar
                ))
        else:
            tarefas_column.controls.append(ft.Text("Nenhuma tarefa encontrada."))
        page.update()


    def on_add_tarefa(e):
        texto = descricao_input.value.strip()
        if not texto:
            resultado.value = "A descrição não pode estar vazia."
            resultado.color = ft.colors.RED
        else:
            if cadastrar_tarefa(texto, situacao_input.value):
                resultado.value = "Tarefa cadastrada!"
                resultado.color = ft.colors.GREEN
                descricao_input.value = ""
                situacao_input.value = False
            else:
                resultado.value = "Erro ao cadastrar."
                resultado.color = ft.colors.RED
        atualizar_lista_cadastrar()
        page.update()

    def on_remove_selected(e):
        for tarefa in list(tarefas_column.controls):
            if isinstance(tarefa, Task) and tarefa.checkbox.value:
                remover_tarefa(tarefa.tarefa_id)
        atualizar_lista_cadastrar()

    cadastrar_view = ft.Column([
        ft.Row([
            ft.Text(
                "The Task of the Rings",
                size=35,
                font_family="lord_ring",
                color=ft.colors.YELLOW_ACCENT,
            )
        ], alignment=ft.MainAxisAlignment.CENTER),
        descricao_input,
        situacao_input,
        ft.Row([
            ft.ElevatedButton("Cadastrar", on_click=on_add_tarefa),
            ft.ElevatedButton(
                "Remover Selecionadas", icon=ft.icons.DELETE, on_click=on_remove_selected
            ),
        ]),
        resultado,
        tarefas_column,
    ])

    page.add(ft.Stack([img, cadastrar_view]))

    def on_page_resize(e):
        img.width = page.width
        img.height = page.height

    page.on_resize = on_page_resize

    atualizar_lista_cadastrar()