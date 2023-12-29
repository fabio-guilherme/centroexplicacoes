import sys
from PyQt6.QtWidgets import QApplication
from alunos import Aluno

def main():
    app = QApplication(sys.argv)
    window = Aluno()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()