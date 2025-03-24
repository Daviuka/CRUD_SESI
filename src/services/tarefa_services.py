from models.tarefa_model import Tarefa
from sqlalchemy.exc import SQLAlchemyError
from connection import get_session


def cadastrar_tarefa(descricao: str, situacao: bool):
    try:
        # Criar uma nova instância do modelo Tarefa com os dados fornecidos
        nova_tarefa = Tarefa(descricao=descricao, situacao=situacao)
        Session = get_session()
        with Session() as session:
            # Adicionar a tarefa na sessão
            session.add(nova_tarefa)
            # Commit para salvar a tarefa no banco de dados
            session.commit()
            # Retorna o objeto Tarefa inserido
            return nova_tarefa
    except SQLAlchemyError as e:
        print(f"Erro ao cadastrar tarefa: {e}")
        return None


def listar_tarefas():
    try:
        Session = get_session()
        with Session() as session:
            # Buscar todas as tarefas do banco de dados
            tarefas = session.query(Tarefa).all()
            return tarefas
    except SQLAlchemyError as e:
        print(f"Erro ao listar tarefas: {e}")
        return None


def listar_tarefa_por_id(tarefa_id: int):
    try:
        Session = get_session()
        with Session() as session:
            # Buscar a tarefa específica por ID no banco de dados
            tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
            return tarefa
    except SQLAlchemyError as e:
        print(f"Erro ao listar tarefa por ID: {e}")
        return None


def editar_tarefa(tarefa_id: int, descricao: str, situacao: bool):
    try:
        Session = get_session()
        with Session() as session:
            # Buscar a tarefa pelo ID
            tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

            # Verifica se a tarefa existe
            if tarefa:
                # Atualizar os dados da tarefa
                tarefa.descricao = descricao
                tarefa.situacao = situacao

                # Commit para salvar as alterações no banco de dados
                session.commit()

                # Retorna a tarefa editada
                return tarefa
            else:
                print("Tarefa não encontrada")
                return None
    except SQLAlchemyError as e:
        print(f"Erro ao editar tarefa: {e}")
        return None


def remover_tarefa(tarefa_id: int):
    try:
        Session = get_session()
        with Session() as session:
            # Buscar a tarefa pelo ID
            tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

            # Verifica se a tarefa existe
            if tarefa:
                # Remover a tarefa da sessão
                session.delete(tarefa)

                # Commit para salvar a remoção no banco de dados
                session.commit()
                print("Tarefa removida com sucesso")
                return True
            else:
                print("Tarefa não encontrada")
                return False
    except SQLAlchemyError as e:
        print(f"Erro ao remover tarefa: {e}")
        return False
    
    
