from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from db_util import conecta, verificar_existencia_id, carregar_combo

class Inscricao(QDialog):
    inscricao_atualizada = pyqtSignal()

    def __init__(self, inscricao_id=0):
        super().__init__()
        loadUi("ui/inscricao.ui", self)
        self.initUI()

        # Atributo para armazenar o IDsda inscrição
        self.inscricao_id = inscricao_id

        # Se todos os IDs forem diferentes de 0, carregar os dados da inscrição
        if inscricao_id:
            self.carregar_dados_inscricao(inscricao_id)

    def initUI(self):
        self.carregar_combos()

        # Desmarcar seleções nos combos
        self.comboAlunos.setCurrentIndex(-1)
        self.comboProfessores.setCurrentIndex(-1)
        self.comboSalas.setCurrentIndex(-1)
        self.comboDisciplinas.setCurrentIndex(-1)

        self.btnSalvar.clicked.connect(self.salvar_inscricao)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def carregar_combos(self):
        # Carregar dados das tabelas Aluno, Professor, Sala e Disciplina nos combos
        carregar_combo(self.comboAlunos, 'aluno', 'idAluno', 'Nome')
        carregar_combo(self.comboProfessores, 'professor', 'idProfessor', 'Nome')
        carregar_combo(self.comboSalas, 'sala', 'idSala', 'idSala')  # Não especificado um campo descritivo
        carregar_combo(self.comboDisciplinas, 'disciplina', 'idDisciplina', 'Designacao')

    def salvar_inscricao(self):
        # Obter os dados do formulário
        aluno_id = self.comboAlunos.currentData()
        professor_id = self.comboProfessores.currentData()
        sala_id = self.comboSalas.currentData()
        disciplina_id = self.comboDisciplinas.currentData()

        # Lógica para verificar se os IDs existem e estão corretos
        if not verificar_existencia_id('aluno', aluno_id) or \
                not verificar_existencia_id('professor', professor_id) or \
                not verificar_existencia_id('sala', sala_id) or \
                not verificar_existencia_id('disciplina', disciplina_id):
            QMessageBox.warning(self, 'IDs Inválidos',
                                'Por favor, insira IDs válidos para Aluno, Professor, Sala e Disciplina.')
            return

        # Lógica para verificar se a sala atingiu a capacidade máxima
        if not self.verificar_capacidade_sala(sala_id):
            QMessageBox.warning(self, 'Capacidade Excedida',
                                'A sala atingiu a capacidade máxima de alunos. Escolha outra sala.')
            return

        # Lógica para verificar se a alocação de professor na disciplina está cadastrada
        if not self.verificar_alocacao_professor_disciplina(professor_id, disciplina_id):
            QMessageBox.warning(self, 'Alocação Inválida',
                                'A alocação do Professor na Disciplina não está cadastrada.')
            return

        # Lógica para verificar se já existe um professor na mesma sala
        if not self.verificar_outro_professor_na_sala(professor_id, sala_id):
            QMessageBox.warning(self, 'Professor Existente',
                                'Já existe outro professor na sala. Escolha outra sala ou remova o professor existente.')
            return

        # Lógica para salvar a inscrição no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            if self.inscricao_id == 0:
                # Se inscricao_id for 0, é uma nova inscrição, fazer a inserção
                query = """
                    INSERT INTO inscrição (Aluno_idAluno, Professor_idProfessor, Sala_idSala, Disciplina_idDisciplina)
                    VALUES (%s, %s, %s, %s)
                """
                values = (aluno_id, professor_id, sala_id, disciplina_id)
            else:
                # Se inscricao_id for diferente de 0, é uma atualização, fazer o update
                query = """
                    UPDATE inscrição
                    SET Aluno_idAluno = %s, Professor_idProfessor = %s, Sala_idSala = %s, Disciplina_idDisciplina = %s
                    WHERE idInscrição = %s
                """
                values = (aluno_id, professor_id, sala_id, disciplina_id, self.inscricao_id)

            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que uma nova inscrição foi adicionada ou atualizada
            self.inscricao_atualizada.emit()

            # Fechar a janela após a inclusão ou atualização
            self.accept()

        except Exception as e:
            print("Erro ao incluir/atualizar inscrição:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def verificar_capacidade_sala(self, sala_id):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar a capacidade da sala
            query = "SELECT Capacidade FROM sala WHERE idSala = %s"
            cursor.execute(query, (sala_id,))
            capacidade_sala = cursor.fetchone()[0]

            # Consultar o número atual de inscrições na sala
            query = "SELECT COUNT(*) FROM inscrição WHERE Sala_idSala = %s"
            cursor.execute(query, (sala_id,))
            inscricoes_na_sala = cursor.fetchone()[0]

            return inscricoes_na_sala < capacidade_sala

        except Exception as e:
            print("Erro ao verificar capacidade da sala:", e)
            return False

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def verificar_alocacao_professor_disciplina(self, professor_id, disciplina_id):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar se a alocação de professor na disciplina está cadastrada
            query = """
                SELECT * FROM disciplina_has_professor
                WHERE Disciplina_idDisciplina = %s AND Professor_idProfessor = %s
            """
            cursor.execute(query, (disciplina_id, professor_id))

            return cursor.fetchone() is not None

        except Exception as e:
            print("Erro ao verificar alocação de Professor na Disciplina:", e)
            return False

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def verificar_outro_professor_na_sala(self, professor_id, sala_id):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar se já existe outro professor na sala
            query = """
                SELECT * FROM inscrição
                WHERE Professor_idProfessor != %s AND Sala_idSala = %s
            """
            cursor.execute(query, (professor_id, sala_id))

            return cursor.fetchone() is None

        except Exception as e:
            print("Erro ao verificar professor na sala:", e)
            return False

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def carregar_dados_inscricao(self, inscricao_id):
        # Método para carregar os dados de uma inscrição existente
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar os dados da sala pelo ID
            query = """
                SELECT 
                    Aluno_idAluno, 
                    Professor_idProfessor, 
                    Sala_idSala, 
                    Disciplina_idDisciplina 
                FROM inscrição 
                WHERE idInscrição = %s
            """
            cursor.execute(query, (inscricao_id,))

            inscricao_data = cursor.fetchone()

            if inscricao_data:
                # Lógica para carregar os valores nos combos com base nos IDs fornecidos
                aluno_index = self.comboAlunos.findData(inscricao_data[0])
                professor_index = self.comboProfessores.findData(inscricao_data[1])
                sala_index = self.comboSalas.findData(inscricao_data[2])
                disciplina_index = self.comboDisciplinas.findData(inscricao_data[3])

                # Selecionar os valores corretos nos combos
                if aluno_index != -1:
                    self.comboAlunos.setCurrentIndex(aluno_index)

                if professor_index != -1:
                    self.comboProfessores.setCurrentIndex(professor_index)

                if sala_index != -1:
                    self.comboSalas.setCurrentIndex(sala_index)

                if disciplina_index != -1:
                    self.comboDisciplinas.setCurrentIndex(disciplina_index)

        except Exception as e:
            print("Erro ao carregar dados da inscrição:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()