from PyQt6.QtWidgets import QDialog, QComboBox, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.uic import loadUi
from db_util import conecta, carregar_combo


class AulasPorAluno(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/aulas_por_aluno.ui", self)
        self.initUI()

    def initUI(self):
        # Adicionar opção "Todas" no combo de disciplinas
        self.comboDisciplina.addItem("Todas", userData=-1)

        # Carregar dados nos combos ao abrir a janela
        self.carregar_combos()

        # Ajustar as larguras das colunas
        for column_index in range(self.tableResultados.columnCount()):
            self.tableResultados.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

        # Desmarcar a seleção inicial do combo
        self.comboAluno.setCurrentIndex(-1)
        self.comboDisciplina.setCurrentIndex(-1)

        self.btnConsultar.clicked.connect(self.consultar_aulas)

    def carregar_combos(self):
        # Carregar dados nos combos (alunos e disciplinas)
        carregar_combo(self.comboAluno, 'aluno', 'idAluno', 'Nome')
        carregar_combo(self.comboDisciplina, 'disciplina', 'idDisciplina', 'Designacao', False)

    def consultar_aulas(self):
        # Lógica para consultar aulas por aluno e disciplina
        aluno_id = self.comboAluno.currentData()
        disciplina_id = self.comboDisciplina.currentData()

        # Verificar se algum combo não está selecionado
        if aluno_id is None:
            QMessageBox.warning(self, 'Aviso', 'Selecione um aluno para a consulta.')
            return
        if disciplina_id is None:
            QMessageBox.warning(self, 'Aviso', 'Selecione uma disciplina para a consulta.')
            return

        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter as aulas
            query = """
                SELECT aula.data, aula.hora, disciplina.Designacao
                FROM aula
                INNER JOIN inscrição ON aula.Inscrição_idInscrição = inscrição.idInscrição
                INNER JOIN disciplina ON inscrição.Disciplina_idDisciplina = disciplina.idDisciplina
                WHERE inscrição.Aluno_idAluno = %s
            """

            # Se uma disciplina foi selecionada, adicionar à condição da consulta
            if disciplina_id != -1:
                query += " AND inscrição.Disciplina_idDisciplina = %s"

                # Adicionar valores aos parâmetros da consulta
                cursor.execute(query, (aluno_id, disciplina_id))
            else:
                cursor.execute(query, (aluno_id,))

            # Obter os resultados da consulta
            resultados = cursor.fetchall()

            # Exibir os resultados na tabela
            self.exibir_resultados(resultados)

        except Exception as e:
            print("Erro ao consultar aulas por aluno:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def exibir_resultados(self, resultados):
        # Lógica para exibir os resultados na tabela
        self.tableResultados.clearContents()
        self.tableResultados.setRowCount(0)

        if resultados:
            self.tableResultados.setRowCount(len(resultados))
            for row_index, row_data in enumerate(resultados):
                self.tableResultados.setItem(row_index, 0, QTableWidgetItem(str(row_data[0])))
                self.tableResultados.setItem(row_index, 1, QTableWidgetItem(str(row_data[1])))
                self.tableResultados.setItem(row_index, 2, QTableWidgetItem(str(row_data[2])))

        else:
            # Mensagem avisando
            QMessageBox.information(self, 'Resultado', 'Não há aulas para este aluno e disciplina.')