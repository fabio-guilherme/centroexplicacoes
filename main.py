import sys
from PyQt6.QtWidgets import QApplication
from alunos import Alunos

def main():
    app = QApplication(sys.argv)
    window = Alunos()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()