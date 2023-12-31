from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from PyQt6.QtGui import QAction, QIcon
from PyQt6.uic import loadUi

from alunos import Alunos
from disciplinas import Disciplinas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Carregar a interface principal
        loadUi("ui/main.ui", self)

        # Configurar as ações dos menus
        self.setup_menu_actions()

        # Inicializar o QStackedWidget para gerenciar as telas
        self.stacked_widget = QStackedWidget()
        self.verticalLayout.addWidget(self.stacked_widget)

        # Adicionar as telas ao QStackedWidget
        self.alunos_screen = Alunos()
        self.disciplinas_screen = Disciplinas()
        self.stacked_widget.addWidget(self.alunos_screen)
        self.stacked_widget.addWidget(self.disciplinas_screen)

        # Definir a tela inicial como um widget vazio
        #self.stacked_widget.setCurrentWidget(None)

    def setup_menu_actions(self):
        # Ação do menu para abrir a tela de Alunos
        self.action_alunos = QAction('Alunos', self)
        self.action_alunos.triggered.connect(self.show_alunos_screen)
        self.menuAlunos.addAction(self.action_alunos)

        # Ação do menu para abrir a tela de Disciplinas
        self.action_disciplinas = QAction('Disciplinas', self)
        self.action_disciplinas.triggered.connect(self.show_disciplinas_screen)
        self.menuDisciplinas.addAction(self.action_disciplinas)

    def show_alunos_screen(self):
        self.stacked_widget.setCurrentWidget(self.alunos_screen)

    def show_disciplinas_screen(self):
        self.stacked_widget.setCurrentWidget(self.disciplinas_screen)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()