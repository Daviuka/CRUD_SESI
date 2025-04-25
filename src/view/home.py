import flet as ft
from services.tarefa_services import cadastrar_tarefa, listar_tarefas, remover_tarefa, editar_tarefa

class Task(ft.Row):
    def __init__(self, tarefa_id, text, situacao, atualizar_lista):
        super().__init__()
        self.tarefa_id = tarefa_id
        self.atualizar_lista = atualizar_lista
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
        self.atualizar_lista()
        self.update()

def main(page: ft.Page):
    # registrar as fontes antes de definir o tema
    page.fonts = {
        "lord_ring": "assets/fonts/ringbearer/RINGM___.TTF",  
        "soloist":   "assets/fonts/soloist/soloistacad.ttf",
    }

    page.title = "The Task of the Rings"
    page.window.width = 450
    page.window.height = 800
    page.scroll = "adaptive"

    # theme geral já com reference à fonte default (se quiser)
    page.theme = ft.Theme(
        font_family="lord_ring",
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(
                font_family="lord_ring",
                weight=ft.FontWeight.BOLD,
                italic=True
            )
        ),
        
        color_theme=ft.ThemeMode.DARK
    )

    img = ft.Container(
        content=ft.Image(
            src="https://i.postimg.cc/W3S2zxbt/lord-rings.webp",
            fit=ft.ImageFit.COVER,
            width=page.width,
            height=page.height
        ),
        expand=True,
        opacity=0.5
    )

    def sair_do_aplicativo(e):
        page.window.destroy()

    resultado = ft.Text()
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300)
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)
    tarefas_column = ft.Column()

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

    cadastrar_view = ft.Column([
        ft.Row([
            ft.Text(
                "Gerenciador de Tarefas",
                size=35,
                font_family="lord_ring",  # usa a fonte registrada
                color=ft.colors.YELLOW_ACCENT
            )
        ], alignment=ft.MainAxisAlignment.CENTER),
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

    page.add(
        ft.Stack([img, cadastrar_view])
    )

    def on_page_resize(e):
        img.width = page.width
        img.height = page.height

    page.on_resize = on_page_resize

    atualizar_lista_cadastrar()