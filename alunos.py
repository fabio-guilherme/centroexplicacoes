from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QTableWidget, QAbstractItemView
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from mysql_connector import conecta
from incluir_aluno import IncluirAluno

class Aluno(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/alunos.ui", self)
        self.initUI()

        # Consulta automaticamente os alunos ao abrir a janela
        self.consultar_alunos()

        # Conectar o sinal ao método que atualiza a lista de alunos
        self.janela_incluir_aluno = IncluirAluno()
        self.janela_incluir_aluno.aluno_adicionado.connect(self.atualizar_lista_alunos)

    def initUI(self):
        self.btnConsultar.clicked.connect(self.consultar_alunos)
        self.btnNovoAluno.clicked.connect(self.abrir_janela_novo_aluno)
        self.btnExcluirAluno.clicked.connect(self.excluir_aluno)

        # Configurar a tabela para seleção por linha
        self.tableAlunos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableAlunos.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

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
                    self.tableAlunos.setItem(row_index, col_index, item)

        except Exception as e:
            print("Erro ao consultar alunos:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def abrir_janela_novo_aluno(self):
        self.janela_incluir_aluno.exec()

    def atualizar_lista_alunos(self):
        # Método para atualizar a lista de alunos
        self.consultar_alunos()

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
            self.atualizar_lista_alunos()

        except Exception as e:
            print("Erro ao excluir aluno:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
