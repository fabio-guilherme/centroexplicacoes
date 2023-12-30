from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from mysql_connector import conecta

class Disciplina(QDialog):
    disciplina_atualizada = pyqtSignal()

    def __init__(self, disciplina_id=0):
        super().__init__()
        loadUi("ui/disciplina.ui", self)
        self.initUI()

        # Atributo para armazenar o ID da disciplina
        self.disciplina_id = disciplina_id

        # Se disciplina_id for diferente de 0, carregar os dados da disciplina
        if disciplina_id:
            self.carregar_dados_disciplina(disciplina_id)

    def initUI(self):
        self.btnSalvar.clicked.connect(self.salvar_disciplina)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def salvar_disciplina(self):
        # Obter os dados do formulário
        designacao = self.lineEditDesignacao.text()
        valor = self.lineEditValor.text()

        if self.disciplina_id:
            # Se disciplina_id existe, atualizar a disciplina
            self.atualizar_disciplina(designacao, valor)
        else:
            # Caso contrário, incluir uma nova disciplina
            self.incluir_disciplina(designacao, valor)

    def incluir_disciplina(self, designacao, valor):
        # Lógica para incluir uma nova disciplina no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Inserir uma nova disciplina
            query = "INSERT INTO disciplina (Designacao, Valor) VALUES (%s, %s)"
            values = (designacao, valor)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que uma nova disciplina foi adicionada
            self.disciplina_atualizada.emit()

            # Fechar a janela após a inclusão
            self.accept()

        except Exception as e:
            print("Erro ao incluir disciplina:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def carregar_dados_disciplina(self, disciplina_id):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar os dados da disciplina pelo ID
            query = "SELECT Designacao, Valor FROM disciplina WHERE idDisciplina = %s"
            cursor.execute(query, (disciplina_id,))

            disciplina_data = cursor.fetchone()

            if disciplina_data:
                # Preencher os campos do formulário com os dados da disciplina
                self.lineEditDesignacao.setText(disciplina_data[0])
                self.lineEditValor.setText(disciplina_data[1])

        except Exception as e:
            print("Erro ao carregar dados da disciplina:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def atualizar_disciplina(self, designacao, valor):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Atualizar os dados da disciplina no banco de dados
            query = "UPDATE disciplina SET Designacao = %s, Valor = %s WHERE idDisciplina = %s"
            values = (designacao, valor, self.disciplina_id)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Fechar a janela após a atualização
            self.accept()

            # Emitir o sinal indicando que uma disciplina foi atualizada
            self.disciplina_atualizada.emit()

        except Exception as e:
            print("Erro ao atualizar disciplina:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()