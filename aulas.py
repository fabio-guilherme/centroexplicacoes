from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QTableWidget, QAbstractItemView, QHeaderView
from PyQt6.uic import loadUi
from mysql_connector import conecta, imprime_erro_exclusao
from aula import Aula

class Aulas(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/aulas.ui", self)
        self.initUI()

        # Atualizar a lista de aulas ao abrir a janela
        self.atualizar_lista_aulas()

    def initUI(self):
        self.btnIncluir.clicked.connect(self.abrir_janela_aula)
        self.btnAlterar.clicked.connect(self.abrir_janela_aula_para_alterar)
        self.btnExcluir.clicked.connect(self.excluir_aula)

        # Configurar a tabela para seleção por linha
        self.tableAulas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableAulas.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableAulas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Ajustar as larguras das colunas
        for column_index in range(self.tableAulas.columnCount()):
            self.tableAulas.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

        self.atualizar_lista_aulas()

    def abrir_janela_aula(self, aula_id=0):
        # Abrir a janela de aula para inclusão
        janela_aula = Aula(aula_id)

        if aula_id == 0:
            # Se é uma nova aula, definir a data atual
            data_atual = QDateTime.currentDateTime().date()
            janela_aula.dateEdit.setDate(data_atual)

        janela_aula.aula_atualizada.connect(self.atualizar_lista_aulas)
        janela_aula.exec()

    def abrir_janela_aula_para_alterar(self):
        # Obter a linha selecionada
        selected_row = self.tableAulas.currentRow()

        if selected_row >= 0:
            # Obter o ID da aula a partir da coluna 0 (ID)
            aula_id = int(self.tableAulas.item(selected_row, 0).text())

            # Abrir a janela de aula para alteração
            self.abrir_janela_aula(aula_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma aula para editar.')

    def excluir_aula(self):
        # Obter a linha selecionada
        selected_row = self.tableAulas.currentRow()

        if selected_row >= 0:
            # Obter o ID da aula a partir da coluna 0 (ID)
            aula_id = int(self.tableAulas.item(selected_row, 0).text())

            # Exibir uma mensagem de confirmação
            reply = QMessageBox.question(
                self,
                'Excluir Aula',
                'Tem certeza que deseja excluir esta aula?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Confirmado, prosseguir com a exclusão
                self.realizar_exclusao_aula(aula_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma aula para excluir.')

    def realizar_exclusao_aula(self, aula_id):
        # Lógica para excluir uma aula no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Excluir a aula
            query = "DELETE FROM aula WHERE idAula = %s"
            cursor.execute(query, (aula_id,))

            # Commit da transação
            connection.commit()

            # Atualizar a lista de aulas após a exclusão
            self.atualizar_lista_aulas()

        except Exception as e:
            imprime_erro_exclusao(self, e, "a", "aula")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def atualizar_lista_aulas(self):
        # Lógica para atualizar a lista de aulas na tabela
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter todas as aulas com informações relacionadas
            query = """
                SELECT aula.idAula, aula.data, aula.hora, aula.Inscrição_idInscrição, 
                       aluno.Nome AS NomeAluno, professor.Nome AS NomeProfessor, disciplina.Designacao AS Disciplina
                FROM aula
                INNER JOIN inscrição ON aula.Inscrição_idInscrição = inscrição.idInscrição
                INNER JOIN aluno ON inscrição.Aluno_idAluno = aluno.idAluno
                INNER JOIN professor ON inscrição.Professor_idProfessor = professor.idProfessor
                INNER JOIN disciplina ON inscrição.Disciplina_idDisciplina = disciplina.idDisciplina
            """
            cursor.execute(query)

            # Limpar a tabela antes de adicionar novos dados
            self.tableAulas.setRowCount(0)

            # Adicionar os resultados na tabela
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableAulas.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))

                    # Verificar se o valor é numérico antes de ajustar o alinhamento
                    if isinstance(col_data, (int, float)):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    self.tableAulas.setItem(row_index, col_index, item)

        except Exception as e:
            print("Erro ao consultar aulas:", e)
            # Mostrar mensagem de erro para o utilizador
            QMessageBox.critical(self, 'Erro', f"Erro ao consultar aulas:\n{str(e)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()