from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from mysql_connector import conecta

class Professor(QDialog):
    professor_atualizado = pyqtSignal()

    def __init__(self, professor_id=0):
        super().__init__()
        loadUi("ui/professor.ui", self)
        self.initUI()

        # Atributo para armazenar o ID do professor
        self.professor_id = professor_id

        # Se professor_id for diferente de 0, carregar os dados do professor
        if professor_id:
            self.carregar_dados_professor(professor_id)

    def initUI(self):
        self.btnSalvar.clicked.connect(self.salvar_professor)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def salvar_professor(self):
        # Obter os dados do formulário
        nome = self.lineEditNome.text()
        contato = self.lineEditContato.text()
        nif = self.lineEditNIF.text()

        # Verificar se algum campo está vazio
        if not nome or not contato or not nif:
            QMessageBox.warning(self, 'Campos Vazios', 'Todos os campos são obrigatórios.')
            return

        if self.professor_id:
            # Se professor_id existe, atualizar o professor
            self.atualizar_professor(nome, contato, nif)
        else:
            # Caso contrário, incluir um novo professor
            self.incluir_professor(nome, contato, nif)

    def incluir_professor(self, nome, contato, nif):
        # Lógica para incluir um novo professor no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Inserir um novo professor
            query = "INSERT INTO professor (Nome, Contato, Nif) VALUES (%s, %s, %s)"
            values = (nome, contato, nif)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que um novo professor foi adicionado
            self.professor_atualizado.emit()

            # Fechar a janela após a inclusão
            self.accept()

        except Exception as e:
            print("Erro ao incluir professor:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def carregar_dados_professor(self, professor_id):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar os dados do professor pelo ID
            query = "SELECT Nome, Contato, Nif FROM professor WHERE idProfessor = %s"
            cursor.execute(query, (professor_id,))

            professor_data = cursor.fetchone()

            if professor_data:
                # Preencher os campos do formulário com os dados do professor
                self.lineEditNome.setText(professor_data[0])
                self.lineEditContato.setText(professor_data[1])
                self.lineEditNIF.setText(professor_data[2])

        except Exception as e:
            print("Erro ao carregar dados do professor:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def atualizar_professor(self, nome, contato, nif):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Atualizar os dados do professor no banco de dados
            query = "UPDATE professor SET Nome = %s, Contato = %s, Nif = %s WHERE idProfessor = %s"
            values = (nome, contato, nif, self.professor_id)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Fechar a janela após a atualização
            self.accept()

            # Emitir o sinal indicando que um professor foi atualizado
            self.professor_atualizado.emit()

        except Exception as e:
            print("Erro ao atualizar professor:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()