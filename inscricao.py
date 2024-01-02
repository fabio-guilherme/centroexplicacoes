from PyQt6.QtWidgets import QDialog, QMessageBox, QComboBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from mysql_connector import conecta, verificar_existencia_id

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
        self.carregar_combo(self.comboAlunos, 'aluno', 'idAluno', 'Nome')
        self.carregar_combo(self.comboProfessores, 'professor', 'idProfessor', 'Nome')
        self.carregar_combo(self.comboSalas, 'sala', 'idSala', 'idSala')  # Não especificado um campo descritivo
        self.carregar_combo(self.comboDisciplinas, 'disciplina', 'idDisciplina', 'Designacao')

    def carregar_combo(self, combo: QComboBox, tabela: str, id_coluna: str, nome_coluna: str):
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Selecionar todos os registros da tabela
            query = f"SELECT {id_coluna}, {nome_coluna} FROM {tabela}"
            cursor.execute(query)

            # Limpar o combo antes de adicionar novos itens
            combo.clear()

            # Adicionar itens ao combo
            for row in cursor.fetchall():
                if id_coluna == nome_coluna:
                    combo.addItem(f"{row[0]}", userData=row[0])
                else:
                    combo.addItem(f"{row[0]} - {row[1]}", userData=row[0])

        except Exception as e:
            print(f"Erro ao carregar combo {tabela}: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

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