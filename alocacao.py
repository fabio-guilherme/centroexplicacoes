from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from mysql.connector import IntegrityError
from db_util import conecta, verificar_existencia_id, carregar_combo

class Alocacao(QDialog):
    alocacao_atualizada = pyqtSignal()

    def __init__(self, disciplina_id=0, professor_id=0):
        super().__init__()
        loadUi("ui/alocacao.ui", self)
        self.initUI()

        # Atributos para armazenar os IDs da alocação
        self.disciplina_id = disciplina_id
        self.professor_id = professor_id

        # Se sala_id for diferente de 0, carregar os dados da sala
        if disciplina_id and professor_id:
            self.carregar_dados_alocacao(disciplina_id, professor_id)

    def initUI(self):
        self.carregar_combos()

        # Desmarcar seleções nos combos
        self.comboDisciplinas.setCurrentIndex(-1)
        self.comboProfessores.setCurrentIndex(-1)

        self.btnSalvar.clicked.connect(self.salvar_alocacao)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def carregar_combos(self):
        # Carregar dados das tabelas Disciplina e Professor nos combos
        carregar_combo(self.comboDisciplinas, 'disciplina', 'idDisciplina', 'Designacao')
        carregar_combo(self.comboProfessores, 'professor', 'idProfessor', 'Nome')

    def salvar_alocacao(self):
        # Obter os dados do formulário
        professor_id = self.comboProfessores.currentData()
        disciplina_id = self.comboDisciplinas.currentData()

        # Lógica para verificar se os IDs existem e estão corretos
        if not verificar_existencia_id('professor', professor_id) or \
                not verificar_existencia_id('disciplina', disciplina_id):
            QMessageBox.warning(self, 'IDs Inválidos', 'Por favor, insira IDs válidos para Professor e Disciplina.')
            return

        # Lógica para salvar a alocação no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Lógica para salvar a alocação no banco de dados
            query = "INSERT INTO disciplina_has_professor (Professor_idProfessor, Disciplina_idDisciplina) VALUES (%s, %s)"
            values = (professor_id, disciplina_id)
            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que uma nova alocação foi adicionada
            self.alocacao_atualizada.emit()

            # Fechar a janela após a inclusão
            self.accept()

        except IntegrityError as e:
            # Chave duplicada, exibir aviso
            QMessageBox.warning(self, 'Chave Duplicada',
                                'Esta alocação já existe. Por favor, escolha valores diferentes.')

        except Exception as e:
            print("Erro ao incluir alocação:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def carregar_dados_alocacao(self, disciplina_id, professor_id):
        # Método para carregar os dados de uma alocação existente

        # Lógica para carregar os valores nos combos com base nos IDs fornecidos
        disciplina_index = self.comboDisciplinas.findData(disciplina_id)
        professor_index = self.comboProfessores.findData(professor_id)

        # Selecionar os valores corretos nos combos
        if disciplina_index != -1:
            self.comboDisciplinas.setCurrentIndex(disciplina_index)

        if professor_index != -1:
            self.comboProfessores.setCurrentIndex(professor_index)

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()