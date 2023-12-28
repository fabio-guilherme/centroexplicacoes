import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi
import mysql.connector

class AlunoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("sua_interface.ui", self)  # Substitua "sua_interface.ui" pelo caminho do seu arquivo .ui
        self.initUI()

    def initUI(self):
        self.btnConsultar.clicked.connect(self.consultar_alunos)

    def consultar_alunos(self):
        # Configurar a conexão com o banco de dados
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="`centroexplicacoes2"
            )

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

def main():
    app = QApplication(sys.argv)
    window = AlunoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
