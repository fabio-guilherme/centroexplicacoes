import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt6.uic import loadUi
import mysql.connector

class AlunoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/alunos.ui", self)
        self.initUI()

    def initUI(self):
        self.btnConsultar.clicked.connect(self.consultar_alunos)
        self.btnNovoAluno.clicked.connect(self.abrir_janela_novo_aluno)

    def consultar_alunos(self):
        # Configurar a conexão com o banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter todos os alunos
            query = "SELECT * FROM aluno"
            cursor.execute(query)

            # Limpar a tabela antes de adicionar novos dados
            self.tableAlunos.setRowCount(0)

            # Adicionar os resultados na tabela
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableAlunos.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.tableAlunos.setItem(row_index, col_index, item)

        except Exception as e:
            print("Erro ao consultar alunos:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def abrir_janela_novo_aluno(self):
        # Cria uma instância da janela para incluir um novo aluno
        nova_janela = IncluirAlunoWindow()
        nova_janela.exec()

class IncluirAlunoWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/incluir_aluno.ui", self)
        self.initUI()

    def initUI(self):
        self.btnSalvar.clicked.connect(self.incluir_novo_aluno)

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

            # Fechar a janela após a inclusão
            self.accept()

        except Exception as e:
            print("Erro ao incluir aluno:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def conecta():
    return mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="centroexplicacoes2"
            )
def main():
    app = QApplication(sys.argv)
    window = AlunoApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
