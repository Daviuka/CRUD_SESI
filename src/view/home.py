import flet as ft
from services.tarefa_services import cadastrar_tarefa, listar_tarefas, remover_tarefa

# Classe para representar uma tarefa com funcionalidade de edição e remoção
class Task(ft.Row):
    def __init__(self, tarefa_id, text, situacao, atualizar_lista):
        super().__init__()
         # ID da tarefa
        self.tarefa_id = tarefa_id 
        self.text_view = ft.Text(
            text,
            # Faz a descrição ocupar o espaço disponível
            expand=True, 
            # Permite que o texto quebre em várias linhas 
            no_wrap=False,  
            # Define o tamanho da fonte
            size=14  
        )
        # Campo de edição do texto
        self.text_edit = ft.TextField(value=text, visible=False) 
        # Checkbox para marcar a tarefa como concluída 
        self.checkbox = ft.Checkbox(value=situacao) 

        # Botão para salvar a edição
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)  
        self.save_button = ft.IconButton(
            visible=False, icon=ft.icons.SAVE, on_click=self.save  
        )
        # Botão para remover a tarefa
        self.delete_button = ft.IconButton(
            icon=ft.icons.DELETE, on_click=self.delete_clicked  
        )
        # Função para atualizar a lista de tarefas
        self.atualizar_lista = atualizar_lista  
        self.controls = [
            # Componentes visuais da tarefa
            self.checkbox,
            self.text_view,
            self.text_edit,
            self.edit_button,
            self.save_button,
            self.delete_button,
        ]  
    # Função para habilitar o modo de edição
    def edit(self, e):
        # Esconde o botão de edição
        self.edit_button.visible = False
        # Mostra o botão de salvar  
        self.save_button.visible = True  
        # Esconde o texto da tarefa
        self.text_view.visible = False  
        # Mostra o campo de edição
        self.text_edit.visible = True  
        # Atualiza a interface
        self.update()  

    # Função para salvar as alterações feitas na tarefa
    def save(self, e):
        # Mostra o botão de edição  
        self.edit_button.visible = True 
        # Esconde o botão de salvar
        self.save_button.visible = False 
        # Mostra o texto da tarefa
        self.text_view.visible = True  
        # Esconde o campo de edição
        self.text_edit.visible = False  
        # Atualiza o texto da tarefa com o valor editado
        self.text_view.value = self.text_edit.value  
        # Atualiza a lista de tarefas
        self.atualizar_lista() 
        # Atualiza a interface
        self.update()  

    # Função para remover a tarefa
    def delete_clicked(self, e):
        # Chama o serviço para remover a tarefa
        sucesso = remover_tarefa(self.tarefa_id)
        if sucesso:
            # Mensagem de sucesso
            print(f"Tarefa {self.tarefa_id} removida com sucesso.") 
            # Atualiza a lista de tarefas
            self.atualizar_lista()  
        else:
            # Mensagem de erro
            print(f"Erro ao remover a tarefa {self.tarefa_id}.")

# Função principal para configurar a interface
def main(page: ft.Page):
    titulo_principal = ft.Text(
        'Cadastro de Tarefas',
        size=24,
        weight='bold',
        font_family='Anton'
    )
    page.scroll = 'adaptive'  # Habilita o scroll adaptativo
    page.padding = 20  # Define o padding da página
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Alinha os elementos verticalmente ao centro

    
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

    def alterar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            btn_tema.icon = ft.icons.NIGHTS_STAY_OUTLINED
            btn_tema.tooltip = 'Alterar para tema escuro!'
            page.bgcolor = ft.colors.WHITE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            btn_tema.icon = ft.icons.WB_SUNNY_OUTLINED
            btn_tema.tooltip = 'Alterar para o tema claro!'
            page.bgcolor = ft.colors.BLACK
        page.update()

    # Botão para alternar o tema
    btn_tema = ft.IconButton(
        icon=ft.icons.WB_SUNNY_OUTLINED,
        tooltip='Alterar o tema',
        on_click=alterar_tema
    )

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
            ft.Row(
                [btn_tema],  # Adiciona o botão de tema
                alignment=ft.MainAxisAlignment.END  # Alinha o botão ao lado direito
            ),
            ft.Column([
                descricao_input,
                situacao_input,
                add_button,
                result_text,
                tarefas_column
            ])
        ])
    )
    # Inicializa a lista de tarefas
    atualizar_lista_tarefas()