from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QTableWidget, QAbstractItemView, \
    QHeaderView, QVBoxLayout, QWidget
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from mysql_connector import conecta
from aula import Aula

class Aulas(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/aulas.ui", self)
        self.initUI()

        # Consulta automaticamente as aulas ao abrir a janela
        self.consultar_aulas()

    def initUI(self):
        self.btnIncluirAula.clicked.connect(self.abrir_janela_aula)
        self.btnAlterarAula.clicked.connect(self.abrir_janela_aula_para_alterar)
        self.btnExcluirAula.clicked.connect(self.excluir_aula)

        # Configurar a tabela para seleção por linha
        self.tableAulas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableAulas.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableAulas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Ajustar as larguras das colunas
        for column_index in range(self.tableAulas.columnCount()):
            self.tableAulas.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

    def consultar_aulas(self):
        # Configurar a conexão com o banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter todas as aulas
            query = "SELECT * FROM sala"
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

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def abrir_janela_aula(self, aula_id=0):
        janela_aula = Aula(aula_id)
        janela_aula.aula_atualizada.connect(self.consultar_aulas)
        janela_aula.exec()

    def abrir_janela_aula_para_alterar(self):
        # Obter a linha selecionada
        selected_row = self.tableAulas.currentRow()

        if selected_row >= 0:
            # Obter o ID da aula a partir da coluna 0 (ID)
            aula_id = int(self.tableAulas.item(selected_row, 0).text())

            # Abrir a janela da aula para edição
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
            query = "DELETE FROM sala WHERE idSala = %s"
            cursor.execute(query, (aula_id,))

            # Commit da transação
            connection.commit()

            # Atualizar a lista de aulas após a exclusão
            self.consultar_aulas()

        except Exception as e:
            print("Erro ao excluir aula:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()