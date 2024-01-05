from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QTableWidget, QAbstractItemView, QHeaderView
from PyQt6.uic import loadUi
from mysql_connector import conecta, imprime_erro_exclusao
from inscricao import Inscricao

class Inscricoes(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/inscricoes.ui", self)
        self.initUI()

        # Atualizar a lista de inscrições ao abrir a janela
        self.atualizar_lista_inscricoes()

    def initUI(self):
        self.btnIncluir.clicked.connect(self.abrir_janela_inscricao)
        self.btnAlterar.clicked.connect(self.abrir_janela_inscricao_para_alterar)
        self.btnExcluir.clicked.connect(self.excluir_inscricao)

        # Configurar a tabela para seleção por linha
        self.tableInscricoes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableInscricoes.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableInscricoes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Ajustar as larguras das colunas
        for column_index in range(self.tableInscricoes.columnCount()):
            self.tableInscricoes.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

        self.atualizar_lista_inscricoes()

    def abrir_janela_inscricao(self, inscricao_id=0):
        # Abrir a janela de inscrição para inclusão ou alteração
        janela_inscricao = Inscricao(inscricao_id)
        janela_inscricao.inscricao_atualizada.connect(self.atualizar_lista_inscricoes)
        janela_inscricao.exec()

    def abrir_janela_inscricao_para_alterar(self):
        # Obter a linha selecionada
        selected_row = self.tableInscricoes.currentRow()

        if selected_row >= 0:
            # Obter o ID da inscrição a partir da coluna 0 (ID)
            inscricao_id = int(self.tableInscricoes.item(selected_row, 0).text())

            # Abrir a janela de inscrição para edição
            self.abrir_janela_inscricao(inscricao_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma inscrição para editar.')

    def excluir_inscricao(self):
        # Obter a linha selecionada
        selected_row = self.tableInscricoes.currentRow()

        if selected_row >= 0:
            # Obter o ID da inscrição a partir da coluna 0 (ID)
            inscricao_id = int(self.tableInscricoes.item(selected_row, 0).text())

            # Exibir uma mensagem de confirmação
            reply = QMessageBox.question(
                self,
                'Excluir Inscrição',
                'Tem certeza que deseja excluir esta inscrição?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Confirmado, prosseguir com a exclusão
                self.realizar_exclusao_inscricao(inscricao_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma inscrição para excluir.')

    def realizar_exclusao_inscricao(self, inscricao_id):
        # Lógica para excluir uma inscrição no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Excluir a inscrição
            query = "DELETE FROM inscrição WHERE idInscrição = %s"
            cursor.execute(query, (inscricao_id,))

            # Commit da transação
            connection.commit()

            # Atualizar a lista de inscrições após a exclusão
            self.atualizar_lista_inscricoes()

        except Exception as e:
            imprime_erro_exclusao(self, e, "a", "inscrição")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def atualizar_lista_inscricoes(self):
        # Lógica para atualizar a lista de inscrições na tabela com JOINS
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter todas as inscrições com informações descritivas
            query = """
                SELECT
                    i.idInscrição,
                    a.Nome AS Aluno,
                    p.Nome AS Professor,
                    s.idSala,
                    d.Designacao AS Disciplina
                FROM inscrição i
                LEFT JOIN aluno a ON i.Aluno_idAluno = a.idAluno
                LEFT JOIN professor p ON i.Professor_idProfessor = p.idProfessor
                LEFT JOIN sala s ON i.Sala_idSala = s.idSala
                LEFT JOIN disciplina d ON i.Disciplina_idDisciplina = d.idDisciplina
            """
            cursor.execute(query)

            # Limpar a tabela antes de adicionar novos dados
            self.tableInscricoes.setRowCount(0)

            # Adicionar os resultados na tabela
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableInscricoes.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))

                    # Verificar se o valor é numérico antes de ajustar o alinhamento
                    if isinstance(col_data, (int, float)):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    self.tableInscricoes.setItem(row_index, col_index, item)

        except Exception as e:
            print("Erro ao consultar inscrições:", e)
            # Mostrar mensagem de erro para o utilizador
            QMessageBox.critical(self, 'Erro', f"Erro ao consultar inscrições:\n{str(e)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()