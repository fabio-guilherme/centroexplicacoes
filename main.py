from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from PyQt6.QtGui import QAction, QIcon
from PyQt6.uic import loadUi

from alunos import Alunos
from disciplinas import Disciplinas
from professores import Professores
from salas import Salas
from alocacoes import Alocacoes
from inscricoes import Inscricoes

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
        self.professores_screen = Professores()
        self.salas_screen = Salas()
        self.alocacoes_screen = Alocacoes()
        self.inscricoes_screen = Inscricoes()
        self.stacked_widget.addWidget(self.alunos_screen)
        self.stacked_widget.addWidget(self.disciplinas_screen)
        self.stacked_widget.addWidget(self.professores_screen)
        self.stacked_widget.addWidget(self.salas_screen)
        self.stacked_widget.addWidget(self.alocacoes_screen)
        self.stacked_widget.addWidget(self.inscricoes_screen)

        # Definir a tela inicial como um widget vazio
        #self.stacked_widget.setCurrentWidget(None)

    def setup_menu_actions(self):
        # Ação do menu para abrir a tela de Alunos
        self.action_alunos = QAction('Alunos', self)
        self.action_alunos.triggered.connect(self.show_alunos_screen)
        self.menuCadastros.addAction(self.action_alunos)

        # Ação do menu para abrir a tela de Disciplinas
        self.action_disciplinas = QAction('Disciplinas', self)
        self.action_disciplinas.triggered.connect(self.show_disciplinas_screen)
        self.menuCadastros.addAction(self.action_disciplinas)

        # Ação do menu para abrir a tela de Professores
        self.action_professores = QAction('Professores', self)
        self.action_professores.triggered.connect(self.show_professores_screen)
        self.menuCadastros.addAction(self.action_professores)

        # Ação do menu para abrir a tela de Salas
        self.action_salas = QAction('Salas', self)
        self.action_salas.triggered.connect(self.show_salas_screen)
        self.menuCadastros.addAction(self.action_salas)

        # Ação do menu para abrir a tela de Alocações
        self.action_alocacoes = QAction('Alocações', self)
        self.action_alocacoes.triggered.connect(self.show_alocacoes_screen)
        self.menuCadastros.addAction(self.action_alocacoes)

        # Ação do menu para abrir a tela de Inscrições
        self.action_inscricoes = QAction('Inscrições', self)
        self.action_inscricoes.triggered.connect(self.show_inscricoes_screen)
        self.menuCadastros.addAction(self.action_inscricoes)

    def show_alunos_screen(self):
        self.stacked_widget.setCurrentWidget(self.alunos_screen)

    def show_disciplinas_screen(self):
        self.stacked_widget.setCurrentWidget(self.disciplinas_screen)

    def show_professores_screen(self):
        self.stacked_widget.setCurrentWidget(self.professores_screen)

    def show_salas_screen(self):
        self.stacked_widget.setCurrentWidget(self.salas_screen)

    def show_alocacoes_screen(self):
        self.stacked_widget.setCurrentWidget(self.alocacoes_screen)

    def show_inscricoes_screen(self):
        self.stacked_widget.setCurrentWidget(self.inscricoes_screen)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()