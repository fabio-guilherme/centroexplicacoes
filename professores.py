from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QTableWidget, QAbstractItemView, \
    QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from mysql_connector import conecta
from professor import Professor

class Professores(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/professores.ui", self)
        self.initUI()

        # Consulta automaticamente os professores ao abrir a janela
        self.consultar_professores()

    def initUI(self):
        self.btnInserirProfessor.clicked.connect(self.abrir_janela_professor)
        self.btnAlterarProfessor.clicked.connect(self.abrir_janela_professor_para_alterar)
        self.btnExcluirProfessor.clicked.connect(self.excluir_professor)

        # Configurar a tabela para seleção por linha
        self.tableProfessores.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableProfessores.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableProfessores.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Ajustar as larguras das colunas
        for column_index in range(self.tableProfessores.columnCount()):
            self.tableProfessores.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

    def consultar_professores(self):
        # Configurar a conexão com o banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter todos os professores
            query = "SELECT * FROM professor"
            cursor.execute(query)

            # Limpar a tabela antes de adicionar novos dados
            self.tableProfessores.setRowCount(0)

            # Adicionar os resultados na tabela
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableProfessores.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))

                    # Verificar se o valor é numérico antes de ajustar o alinhamento
                    if isinstance(col_data, (int, float)):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    self.tableProfessores.setItem(row_index, col_index, item)

        except Exception as e:
            print("Erro ao consultar professores:", e)
            # Mostrar mensagem de erro para o utilizador
            QMessageBox.critical(self, 'Erro', f"Erro ao consultar professores:\n{str(e)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def abrir_janela_professor(self, professor_id=0):
        janela_professor = Professor(professor_id)
        janela_professor.professor_atualizado.connect(self.consultar_professores)
        janela_professor.exec()

    def abrir_janela_professor_para_alterar(self):
        # Obter a linha selecionada
        selected_row = self.tableProfessores.currentRow()

        if selected_row >= 0:
            # Obter o ID do professor a partir da coluna 0 (ID)
            professor_id = int(self.tableProfessores.item(selected_row, 0).text())

            # Abrir a janela do professor para edição
            self.abrir_janela_professor(professor_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione um professor para editar.')

    def excluir_professor(self):
        # Obter a linha selecionada
        selected_row = self.tableProfessores.currentRow()

        if selected_row >= 0:
            # Obter o ID do professor a partir da coluna 0 (ID)
            professor_id = int(self.tableProfessores.item(selected_row, 0).text())

            # Exibir uma mensagem de confirmação
            reply = QMessageBox.question(
                self,
                'Excluir Professor',
                'Tem certeza que deseja excluir este professor?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Confirmado, prosseguir com a exclusão
                self.realizar_exclusao_professor(professor_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione um professor para excluir.')

    def realizar_exclusao_professor(self, professor_id):
        # Lógica para excluir um professor no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Excluir o professor
            query = "DELETE FROM professor WHERE idProfessor = %s"
            cursor.execute(query, (professor_id,))

            # Commit da transação
            connection.commit()

            # Atualizar a lista de professores após a exclusão
            self.consultar_professores()

        except Exception as e:
            print("Erro ao excluir professor:", e)
            # Mostrar mensagem de erro para o utilizador
            QMessageBox.critical(self, 'Erro', f"Erro ao excluir professor:\n{str(e)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()