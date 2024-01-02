from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QTableWidget, QAbstractItemView, QHeaderView
from PyQt6.uic import loadUi
from mysql_connector import conecta

from alocacao import Alocacao

class Alocacoes(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/alocacoes.ui", self)
        self.initUI()

        # Atualizar a lista de alocações ao abrir a janela
        self.atualizar_lista_alocacoes()

    def initUI(self):
        self.btnAlterar.hide()

        self.btnIncluir.clicked.connect(self.abrir_janela_alocacao)
        self.btnAlterar.clicked.connect(self.abrir_janela_alocacao_para_alterar)
        self.btnExcluir.clicked.connect(self.excluir_alocacao)

        # Configurar a tabela para seleção por linha
        self.tableAlocacoes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableAlocacoes.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableAlocacoes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Ajustar as larguras das colunas
        for column_index in range(self.tableAlocacoes.columnCount()):
            self.tableAlocacoes.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

        self.atualizar_lista_alocacoes()

    def abrir_janela_alocacao(self, disciplina_id=0, professor_id=0):
        janela_alocacao = Alocacao(disciplina_id, professor_id)
        janela_alocacao.alocacao_atualizada.connect(self.atualizar_lista_alocacoes)
        janela_alocacao.exec()

    def abrir_janela_alocacao_para_alterar(self):
        # Obter a linha selecionada
        selected_row = self.tableAlocacoes.currentRow()

        if selected_row >= 0:
            # Obter os IDs da disciplina e do professor a partir das coluna 0 e 2
            disciplina_id = int(self.tableAlocacoes.item(selected_row, 0).text())
            professor_id = int(self.tableAlocacoes.item(selected_row, 2).text())

            # Abrir a janela de alocação para edição
            self.abrir_janela_alocacao(disciplina_id, professor_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma alocação para editar.')

    def excluir_alocacao(self):
        # Obter a linha selecionada
        selected_row = self.tableAlocacoes.currentRow()

        if selected_row >= 0:
            # Obter os IDs da disciplina e do professor a partir das coluna 0 e 2
            disciplina_id = int(self.tableAlocacoes.item(selected_row, 0).text())
            professor_id = int(self.tableAlocacoes.item(selected_row, 2).text())

            # Exibir uma mensagem de confirmação
            reply = QMessageBox.question(
                self,
                'Excluir Alocação',
                'Tem certeza que deseja excluir esta alocação?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Confirmado, prosseguir com a exclusão
                self.realizar_exclusao_alocacao(professor_id, disciplina_id)
        else:
            # Nenhuma linha selecionada, exibir mensagem informativa
            QMessageBox.information(self, 'Seleção Necessária', 'Por favor, selecione uma alocação para excluir.')

    def realizar_exclusao_alocacao(self, disciplina_id, professor_id):
        # Lógica para excluir uma alocação no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Excluir a alocação
            query = "DELETE FROM disciplina_has_professor WHERE Disciplina_idDisciplina = %s AND Professor_idProfessor = %s"
            cursor.execute(query, (disciplina_id, professor_id,))

            # Commit da transação
            connection.commit()

            # Atualizar a lista de alocações após a exclusão
            self.atualizar_lista_alocacoes()

        except Exception as e:
            print("Erro ao excluir alocação:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def atualizar_lista_alocacoes(self):
        # Lógica para atualizar a lista de alocações na tabela
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter todas as alocações com informações adicionais
            query = """
                SELECT 
                    a.Disciplina_idDisciplina,
                    d.Designacao,
                    a.Professor_idProfessor,
                    p.Nome
                FROM disciplina_has_professor a
                INNER JOIN professor p ON a.Professor_idProfessor = p.idProfessor
                INNER JOIN disciplina d ON a.Disciplina_idDisciplina = d.idDisciplina
            """
            cursor.execute(query)

            # Limpar a tabela antes de adicionar novos dados
            self.tableAlocacoes.setRowCount(0)

            # Adicionar os resultados na tabela
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableAlocacoes.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))

                    # Verificar se o valor é numérico antes de ajustar o alinhamento
                    if isinstance(col_data, (int, float)):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    self.tableAlocacoes.setItem(row_index, col_index, item)

        except Exception as e:
            print("Erro ao consultar alocações:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()