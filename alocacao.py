from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from mysql_connector import conecta, verificar_existencia_id

class Alocacao(QDialog):
    alocacao_atualizada = pyqtSignal()

    def __init__(self):
        super().__init__()
        loadUi("ui/alocacao.ui", self)
        self.initUI()

    def initUI(self):
        self.btnSalvar.clicked.connect(self.salvar_alocacao)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def salvar_alocacao(self):
        # Obter os dados do formulário
        # Certifique-se de ajustar os nomes dos widgets conforme o seu arquivo .ui
        professor_id = int(self.lineEditProfessor.text())
        disciplina_id = int(self.lineEditDisciplina.text())
        sala_id = int(self.lineEditSala.text())

        # Lógica para verificar se os IDs existem e estão corretos
        if not self.verificar_existencia_id('professor', professor_id) or \
           not self.verificar_existencia_id('disciplina', disciplina_id) or \
           not self.verificar_existencia_id('sala', sala_id):
            QMessageBox.warning(self, 'IDs Inválidos', 'Por favor, insira IDs válidos para Professor, Disciplina e Sala.')
            return

        # Lógica para salvar a alocação no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Lógica para salvar a alocação no banco de dados
            # Certifique-se de ajustar a query conforme a sua tabela de alocação
            query = "INSERT INTO disciplina_has_professor (Professor_idProfessor, Disciplina_idDisciplina, Sala_idSala) VALUES (%s, %s, %s)"
            values = (professor_id, disciplina_id, sala_id)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que uma nova alocação foi adicionada
            self.alocacao_atualizada.emit()

            # Fechar a janela após a inclusão
            self.accept()

        except Exception as e:
            print("Erro ao incluir alocação:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def carregar_alocacao(self, alocacao_id):
        # Lógica para carregar os dados de uma alocação pelo ID
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Lógica para carregar os dados de uma alocação pelo ID
            # Certifique-se de ajustar a query conforme a sua tabela de alocação
            query = "SELECT Professor_idProfessor, Disciplina_idDisciplina, Sala_idSala FROM disciplina_has_professor WHERE idAlocacao = %s"
            cursor.execute(query, (alocacao_id,))

            alocacao_data = cursor.fetchone()

            if alocacao_data:
                # Preencher os campos do formulário com os dados da alocação
                # Certifique-se de ajustar os widgets conforme o seu arquivo .ui
                self.lineEditProfessor.setText(str(alocacao_data[0]))
                self.lineEditDisciplina.setText(str(alocacao_data[1]))
                self.lineEditSala.setText(str(alocacao_data[2]))

        except Exception as e:
            print("Erro ao carregar dados da alocação:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()