from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from db_util import conecta

class Sala(QDialog):
    sala_atualizada = pyqtSignal()

    def __init__(self, sala_id=0):
        super().__init__()
        loadUi("ui/sala.ui", self)
        self.initUI()

        # Atributo para armazenar o ID da sala
        self.sala_id = sala_id

        # Se sala_id for diferente de 0, carregar os dados da sala
        if sala_id:
            self.carregar_dados_sala(sala_id)

    def initUI(self):
        self.btnSalvar.clicked.connect(self.salvar_sala)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def salvar_sala(self):
        # Obter os dados do formulário
        capacidade = self.spinBoxCapacidade.value()

        if self.sala_id:
            # Se sala_id existe, atualizar a sala
            self.atualizar_sala(capacidade)
        else:
            # Caso contrário, incluir uma nova sala
            self.incluir_sala(capacidade)

    def incluir_sala(self, capacidade):
        # Lógica para incluir uma nova sala no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Inserir uma nova sala
            query = "INSERT INTO sala (Capacidade) VALUES (%s)"
            values = (capacidade,)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que uma nova sala foi adicionada
            self.sala_atualizada.emit()

            # Fechar a janela após a inclusão
            self.accept()

        except Exception as e:
            print("Erro ao incluir sala:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def carregar_dados_sala(self, sala_id):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar os dados da sala pelo ID
            query = "SELECT Capacidade FROM sala WHERE idSala = %s"
            cursor.execute(query, (sala_id,))

            sala_data = cursor.fetchone()

            if sala_data:
                # Preencher os campos do formulário com os dados da sala
                self.spinBoxCapacidade.setValue(sala_data[0])

        except Exception as e:
            print("Erro ao carregar dados da sala:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def atualizar_sala(self, capacidade):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Atualizar os dados da sala no banco de dados
            query = "UPDATE sala SET Capacidade = %s WHERE idSala = %s"
            values = (capacidade, self.sala_id)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Fechar a janela após a atualização
            self.accept()

            # Emitir o sinal indicando que uma sala foi atualizada
            self.sala_atualizada.emit()

        except Exception as e:
            print("Erro ao atualizar sala:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()