import flet as ft
from services.tarefa_services import cadastrar_tarefa, listar_tarefas, remover_tarefa, editar_tarefa

# Classe para representar uma tarefa com funcionalidade de edição e remoção
class Task(ft.Row):
    def __init__(self, tarefa_id, text, situacao, atualizar_lista):
        super().__init__()
        self.tarefa_id = tarefa_id
        self.atualizar_lista = atualizar_lista
        self.texto_original = text

        self.checkbox = ft.Checkbox(
            label="", value=situacao, fill_color=ft.Colors.GREEN_100
        )
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


def main(page: ft.Page):
    page.title = "Task of Lord"
    page.bgcolor = ft.Colors.BLACK
    page.scroll = "adaptive"
    page.window.width = 450
    page.window.height = 800

    # Mantém a fonte personalizada
    page.fonts = {
        "lord_ring": 'fonts/ringbearer/RINGM___.TTF',
        "soloist": 'fonts/soloist/soloistacad.ttf',
    }
    page.theme = ft.Theme(
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(
                font_family="lord_ring",
                weight=ft.FontWeight.BOLD,
                italic=True
            )
        )
    )
    page.theme_mode = ft.ThemeMode.DARK

    # Título
    titulo = ft.Text(
        "Gerenciador de Tarefas",
        size=40,
        font_family="lord_ring",
        text_align="center",
        italic=True,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.AMBER_500,
        expand=True
    )

    # Inputs e botões
    descricao_input = ft.TextField(
        label="Descrição da Tarefa",
        label_style=ft.TextStyle(color=ft.Colors.AMBER_500),
        autofocus=True,
        expand=True,
        bgcolor=ft.Colors.BLACK,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.YELLOW_ACCENT_400,
        text_style=ft.TextStyle(color=ft.Colors.YELLOW_ACCENT_700),
        max_length=80
    )
    situacao_input = ft.Checkbox(
        label="Tarefa concluída", value=False,
        fill_color=ft.Colors.GREEN_100,
        label_style=ft.TextStyle(color=ft.Colors.YELLOW_ACCENT_400)
    )
    result_text = ft.Text(color=ft.Colors.AMBER_500)
    result_container = ft.Container(
        content=result_text,
        bgcolor=ft.Colors.WHITE,
        opacity=0.5,
        padding=ft.Padding(10,10,10,10)
    )

    tarefas_column = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    )

    def atualizar_lista():
        tarefas_column.controls.clear()
        tarefas = listar_tarefas()
        if tarefas:
            for t in tarefas:
                tarefas_column.controls.append(
                    Task(t.id, t.descricao, t.situacao, atualizar_lista)
                )
        else:
            tarefas_column.controls.append(ft.Text("Nenhuma tarefa encontrada.", color=ft.Colors.AMBER_500))
        page.update()

    def on_add(e):
        desc = descricao_input.value.strip()
        if not desc:
            result_text.value = "A descrição não pode estar vazia"
        else:
            novo = cadastrar_tarefa(desc, situacao_input.value)
            result_text.value = "Tarefa cadastrada!" if novo else "Erro ao cadastrar"
            descricao_input.value = ""
            situacao_input.value = False
        atualizar_lista()
        page.update()

    add_button = ft.ElevatedButton(
        "Cadastrar",
        on_click=on_add,
        color=ft.Colors.YELLOW,
        bgcolor=ft.Colors.YELLOW_ACCENT_200,
        opacity=0.8
    )

    # Botão de atualizar
    refresh_button = ft.ElevatedButton(
        "Atualizar",
        on_click=lambda e: [atualizar_lista()],
        color=ft.Colors.YELLOW,
        bgcolor=ft.Colors.YELLOW_ACCENT_200,
        opacity=0.8
    )

    # Imagem de fundo (mantém src e tamanho)
    fundo = ft.Container(
        content=ft.Image(
            src='assets/img/lord_rings.png',
            fit=ft.ImageFit.COVER,
            width=page.width,
            height=page.height
        ),
        expand=True,
        opacity=0.2
    )

    # Conteúdo principal
    conteudo = ft.Container(
        content=ft.Column(
            [
                ft.Row([titulo], alignment=ft.MainAxisAlignment.CENTER),
                descricao_input,
                ft.Row([situacao_input, add_button], alignment=ft.MainAxisAlignment.START),
                tarefas_column,
                ft.Row([refresh_button], alignment=ft.MainAxisAlignment.CENTER),
                result_container
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        ),
        margin=ft.Margin(20,20,20,20)
    )

    page.add(ft.Stack(controls=[fundo, conteudo]))
    page.on_resize = lambda e: (setattr(fundo.content, 'width', page.width), setattr(fundo.content, 'height', page.height), page.update())
    atualizar_lista()

