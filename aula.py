from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from mysql_connector import conecta

class Aula(QDialog):
    aula_atualizada = pyqtSignal()

    def __init__(self, aula_id=0):
        super().__init__()
        loadUi("ui/aula.ui", self)
        self.initUI()

        # Atributo para armazenar o ID da aula
        self.aula_id = aula_id

        # Se aula_id for diferente de 0, carregar os dados da aula
        if aula_id:
            self.carregar_dados_aula(aula_id)

    def initUI(self):
        self.btnSalvar.clicked.connect(self.salvar_aula)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def salvar_aula(self):
        # Obter os dados do formulário
        capacidade = self.spinBoxCapacidade.value()

        if self.aula_id:
            # Se aula_id existe, atualizar a aula
            self.atualizar_aula(capacidade)
        else:
            # Caso contrário, incluir uma nova aula
            self.incluir_aula(capacidade)

    def incluir_aula(self, capacidade):
        # Lógica para incluir uma nova aula no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Inserir uma nova aula
            query = "INSERT INTO sala (Capacidade) VALUES (%s)"
            values = (capacidade,)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que uma nova aula foi adicionada
            self.aula_atualizada.emit()

            # Fechar a janela após a inclusão
            self.accept()

        except Exception as e:
            print("Erro ao incluir aula:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def carregar_dados_aula(self, aula_id):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar os dados da aula pelo ID
            query = "SELECT Capacidade FROM sala WHERE idSala = %s"
            cursor.execute(query, (aula_id,))

            aula_data = cursor.fetchone()

            if aula_data:
                # Preencher os campos do formulário com os dados da aula
                self.spinBoxCapacidade.setValue(aula_data[0])

        except Exception as e:
            print("Erro ao carregar dados da aula:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def atualizar_aula(self, capacidade):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Atualizar os dados da aula no banco de dados
            query = "UPDATE sala SET Capacidade = %s WHERE idSala = %s"
            values = (capacidade, self.aula_id)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Fechar a janela após a atualização
            self.accept()

            # Emitir o sinal indicando que uma aula foi atualizada
            self.aula_atualizada.emit()

        except Exception as e:
            print("Erro ao atualizar aula:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()