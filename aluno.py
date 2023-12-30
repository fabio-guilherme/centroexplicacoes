from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from mysql_connector import conecta

class Aluno(QDialog):
    aluno_atualizado = pyqtSignal()

    def __init__(self, aluno_id=0):
        super().__init__()
        loadUi("ui/aluno.ui", self)
        self.initUI()

        # Atributo para armazenar o ID do aluno
        self.aluno_id = aluno_id

        # Se aluno_id for diferente de 0, carregar os dados do aluno
        if aluno_id:
            self.carregar_dados_aluno(aluno_id)

    def initUI(self):
        self.btnSalvar.clicked.connect(self.salvar_aluno)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def salvar_aluno(self):
        # Obter os dados do formulário
        nome = self.lineEditNome.text()
        contato = self.lineEditContato.text()
        n_ensino = self.lineEditNEnsino.text()
        nif = self.lineEditNIF.text()

        if self.aluno_id:
            # Se aluno_id existe, atualizar o aluno
            self.atualizar_aluno(nome, contato, n_ensino, nif)
        else:
            # Caso contrário, incluir um novo aluno
            self.incluir_aluno(nome, contato, n_ensino, nif)

    def incluir_aluno(self, nome, contato, n_ensino, nif):
        # Lógica para incluir um novo aluno no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Inserir um novo aluno
            query = "INSERT INTO aluno (Nome, Contato, Nensino, Nif) VALUES (%s, %s, %s, %s)"
            values = (nome, contato, n_ensino, nif)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que um novo aluno foi adicionado
            self.aluno_atualizado.emit()

            # Fechar a janela após a inclusão
            self.accept()

        except Exception as e:
            print("Erro ao incluir aluno:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def carregar_dados_aluno(self, aluno_id):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar os dados do aluno pelo ID
            query = "SELECT Nome, Contato, Nensino, Nif FROM aluno WHERE idAluno = %s"
            cursor.execute(query, (aluno_id,))

            aluno_data = cursor.fetchone()

            if aluno_data:
                # Preencher os campos do formulário com os dados do aluno
                self.lineEditNome.setText(aluno_data[0])
                self.lineEditContato.setText(aluno_data[1])
                self.lineEditNEnsino.setText(aluno_data[2])
                self.lineEditNIF.setText(aluno_data[3])

        except Exception as e:
            print("Erro ao carregar dados do aluno:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def atualizar_aluno(self, nome, contato, n_ensino, nif):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Atualizar os dados do aluno no banco de dados
            query = "UPDATE aluno SET Nome = %s, Contato = %s, Nensino = %s, Nif = %s WHERE idAluno = %s"
            values = (nome, contato, n_ensino, nif, self.aluno_id)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Fechar a janela após a atualização
            self.accept()

            # Emitir o sinal indicando que um aluno foi atualizado
            self.aluno_atualizado.emit()

        except Exception as e:
            print("Erro ao atualizar aluno:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()