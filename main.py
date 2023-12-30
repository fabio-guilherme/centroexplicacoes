import sys
from PyQt6.QtWidgets import QApplication
from alunos import Alunos
from disciplinas import Disciplinas

def main():
    app = QApplication(sys.argv)
    window = Disciplinas()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()