from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QTableWidget, QAbstractItemView, \
    QHeaderView, QVBoxLayout, QWidget
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from mysql_connector import conecta
from sala import Sala

class Salas(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/salas.ui", self)
        self.initUI()

        # Consulta automaticamente as salas ao abrir a janela
        self.consultar_salas()

    def initUI(self):
        self.btnIncluirSala.clicked.connect(self.abrir_janela_sala)
        self.btnAlterarSala.clicked.connect(self.abrir_janela_sala_para_alterar)
        self.btnExcluirSala.clicked.connect(self.excluir_sala)

        # Configurar a tabela para seleção por linha
        self.tableSalas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableSalas.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableSalas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Ajustar as larguras das colunas
        for column_index in range(self.tableSalas.columnCount()):
            self.tableSalas.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

    def consultar_salas(self):
        # Configurar a conexão com o banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter todas as salas
            query = "SELECT * FROM sala"
            cursor.execute(query)

            # Limpar a tabela antes de adicionar novos dados
            self.tableSalas.setRowCount(0)

            # Adicionar os resultados na tabela
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableSalas.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))

                    # Verificar se o valor é numérico antes de ajustar o alinhamento
                    if isinstance(col_data, (int, float)):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    self.tableSalas.setItem(row_index, col_index, item)

        except Exception as e:
            print("Erro ao consultar salas:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def abrir_janela_sala(self, sala_id=0):
        janela_sala = Sala(sala_id)
        janela_sala.sala_atualizada.connect(self.consultar_salas)
        janela_sala.exec()

    def abrir_janela_sala_para_alterar(self):
        # Obter a linha selecionada
        selected_row = self.tableSalas.currentRow()

        if selected_row >= 0:
            # Obter o ID da sala a partir da coluna 0 (ID)
            sala_id = int(self.tableSalas.item(selected_row, 0).text())

            # Abrir a janela da sala para edição
            self.abrir_janela_sala(sala_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma sala para editar.')

    def excluir_sala(self):
        # Obter a linha selecionada
        selected_row = self.tableSalas.currentRow()

        if selected_row >= 0:
            # Obter o ID da sala a partir da coluna 0 (ID)
            sala_id = int(self.tableSalas.item(selected_row, 0).text())

            # Exibir uma mensagem de confirmação
            reply = QMessageBox.question(
                self,
                'Excluir Sala',
                'Tem certeza que deseja excluir esta sala?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Confirmado, prosseguir com a exclusão
                self.realizar_exclusao_sala(sala_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma sala para excluir.')

    def realizar_exclusao_sala(self, sala_id):
        # Lógica para excluir uma sala no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Excluir a sala
            query = "DELETE FROM sala WHERE idSala = %s"
            cursor.execute(query, (sala_id,))

            # Commit da transação
            connection.commit()

            # Atualizar a lista de salas após a exclusão
            self.consultar_salas()

        except Exception as e:
            print("Erro ao excluir sala:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()