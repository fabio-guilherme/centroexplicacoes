from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from mysql_connector import conecta

class IncluirAluno(QDialog):
    aluno_adicionado = pyqtSignal()

    def __init__(self):
        super().__init__()
        loadUi("ui/incluir_aluno.ui", self)
        self.initUI()

    def initUI(self):
        self.btnSalvar.clicked.connect(self.incluir_novo_aluno)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def incluir_novo_aluno(self):
        # Obter os dados do formulário
        nome = self.lineEditNome.text()
        contato = self.lineEditContato.text()

        # Lógica para incluir um novo aluno no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Inserir um novo aluno
            query = "INSERT INTO aluno (Nome, Contato) VALUES (%s, %s)"
            values = (nome, contato)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que um novo aluno foi adicionado
            self.aluno_adicionado.emit()

            # Fechar a janela após a inclusão
            self.accept()

        except Exception as e:
            print("Erro ao incluir aluno:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()