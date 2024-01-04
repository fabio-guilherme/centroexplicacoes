from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QTableWidget, QAbstractItemView, \
    QApplication, QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from mysql_connector import conecta
from disciplina import Disciplina

class Disciplinas(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/disciplinas.ui", self)
        self.initUI()

        # Consulta automaticamente as disciplinas ao abrir a janela
        self.consultar_disciplinas()

    def initUI(self):
        self.btnInserirDisciplina.clicked.connect(self.abrir_janela_disciplina)
        self.btnAlterarDisciplina.clicked.connect(self.abrir_janela_disciplina_para_alterar)
        self.btnExcluirDisciplina.clicked.connect(self.excluir_disciplina)

        # Configurar a tabela para seleção por linha
        self.tableDisciplinas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableDisciplinas.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Ajustar as larguras das colunas
        for column_index in range(self.tableDisciplinas.columnCount()):
            self.tableDisciplinas.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

    def consultar_disciplinas(self):
        # Configurar a conexão com o banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter todas as disciplinas
            query = "SELECT * FROM disciplina"
            cursor.execute(query)

            # Limpar a tabela antes de adicionar novos dados
            self.tableDisciplinas.setRowCount(0)

            # Adicionar os resultados na tabela
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableDisciplinas.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))

                    # Verificar se o valor é numérico antes de ajustar o alinhamento
                    if isinstance(col_data, (int, float)):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    self.tableDisciplinas.setItem(row_index, col_index, item)

        except Exception as e:
            print("Erro ao consultar disciplinas:", e)
            # Mostrar mensagem de erro para o utilizador
            QMessageBox.critical(self, 'Erro', f"Erro ao consultar disciplinas:\n{str(e)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def abrir_janela_disciplina(self, disciplina_id=0):
        janela_disciplina = Disciplina(disciplina_id)
        janela_disciplina.disciplina_atualizada.connect(self.consultar_disciplinas)
        janela_disciplina.exec()

    def abrir_janela_disciplina_para_alterar(self):
        # Obter a linha selecionada
        selected_row = self.tableDisciplinas.currentRow()

        if selected_row >= 0:
            # Obter o ID da disciplina a partir da coluna 0 (ID)
            disciplina_id = int(self.tableDisciplinas.item(selected_row, 0).text())

            # Abrir a janela da disciplina para edição
            self.abrir_janela_disciplina(disciplina_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma disciplina para editar.')

    def excluir_disciplina(self):
        # Obter a linha selecionada
        selected_row = self.tableDisciplinas.currentRow()

        if selected_row >= 0:
            # Obter o ID da disciplina a partir da coluna 0 (ID)
            disciplina_id = int(self.tableDisciplinas.item(selected_row, 0).text())

            # Exibir uma mensagem de confirmação
            reply = QMessageBox.question(
                self,
                'Excluir Disciplina',
                'Tem certeza que deseja excluir esta disciplina?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Confirmado, prosseguir com a exclusão
                self.realizar_exclusao_disciplina(disciplina_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma disciplina para excluir.')

    def realizar_exclusao_disciplina(self, disciplina_id):
        # Lógica para excluir uma disciplina no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Excluir a disciplina
            query = "DELETE FROM disciplina WHERE idDisciplina = %s"
            cursor.execute(query, (disciplina_id,))

            # Commit da transação
            connection.commit()

            # Atualizar a lista de disciplinas após a exclusão
            self.consultar_disciplinas()

        except Exception as e:
            print("Erro ao excluir disciplina:", e)
            # Mostrar mensagem de erro para o utilizador
            QMessageBox.critical(self, 'Erro', f"Erro ao excluir disciplina:\n{str(e)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()