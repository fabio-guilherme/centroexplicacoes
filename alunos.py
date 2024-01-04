from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QTableWidget, QAbstractItemView, \
    QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from mysql_connector import conecta
from aluno import Aluno

class Alunos(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/alunos.ui", self)
        self.initUI()

        # Consulta automaticamente os alunos ao abrir a janela
        self.consultar_alunos()

    def initUI(self):
        self.btnInserirAluno.clicked.connect(self.abrir_janela_aluno)
        self.btnAlterarAluno.clicked.connect(self.abrir_janela_aluno_para_alterar)
        self.btnExcluirAluno.clicked.connect(self.excluir_aluno)

        # Configurar a tabela para seleção por linha
        self.tableAlunos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableAlunos.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableAlunos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Ajustar as larguras das colunas
        for column_index in range(self.tableAlunos.columnCount()):
            self.tableAlunos.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

    def consultar_alunos(self):
        # Configurar a conexão com o banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter todos os alunos
            query = "SELECT * FROM aluno"
            cursor.execute(query)

            # Limpar a tabela antes de adicionar novos dados
            self.tableAlunos.setRowCount(0)

            # Adicionar os resultados na tabela
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableAlunos.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))

                    # Verificar se o valor é numérico antes de ajustar o alinhamento
                    if isinstance(col_data, (int, float)):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    self.tableAlunos.setItem(row_index, col_index, item)

        except Exception as e:
            print("Erro ao consultar alunos:", e)
            # Mostrar mensagem de erro para o utilizador
            QMessageBox.critical(self, 'Erro', f"Erro ao consultar alunos:\n{str(e)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def abrir_janela_aluno(self, aluno_id=0):
        janela_aluno = Aluno(aluno_id)
        janela_aluno.aluno_atualizado.connect(self.consultar_alunos)
        janela_aluno.exec()

    def abrir_janela_aluno_para_alterar(self):
        # Obter a linha selecionada
        selected_row = self.tableAlunos.currentRow()

        if selected_row >= 0:
            # Obter o ID do aluno a partir da coluna 0 (ID)
            aluno_id = int(self.tableAlunos.item(selected_row, 0).text())

            # Abrir a janela do aluno para edição
            self.abrir_janela_aluno(aluno_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione um aluno para editar.')

    def excluir_aluno(self):
        # Obter a linha selecionada
        selected_row = self.tableAlunos.currentRow()

        if selected_row >= 0:
            # Obter o ID do aluno a partir da coluna 0 (ID)
            aluno_id = int(self.tableAlunos.item(selected_row, 0).text())

            # Exibir uma mensagem de confirmação
            reply = QMessageBox.question(
                self,
                'Excluir Aluno',
                'Tem certeza que deseja excluir este aluno?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Confirmado, prosseguir com a exclusão
                self.realizar_exclusao_aluno(aluno_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione um aluno para excluir.')

    def realizar_exclusao_aluno(self, aluno_id):
        # Lógica para excluir um aluno no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Excluir o aluno
            query = "DELETE FROM aluno WHERE idAluno = %s"
            cursor.execute(query, (aluno_id,))

            # Commit da transação
            connection.commit()

            # Atualizar a lista de alunos após a exclusão
            self.consultar_alunos()

        except Exception as e:
            print("Erro ao excluir aluno:", e)
            # Mostrar mensagem de erro para o utilizador
            QMessageBox.critical(self, 'Erro', f"Erro ao excluir aluno:\n{str(e)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
