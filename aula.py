from PyQt6.QtWidgets import QDialog, QMessageBox, QLabel
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal, Qt, QDate, QTime
from db_util import conecta, verificar_existencia_id, carregar_combo

class Aula(QDialog):
    aula_atualizada = pyqtSignal()

    def __init__(self, aula_id=0):
        super().__init__()
        loadUi("ui/aula.ui", self)
        self.initUI()

        # Atributo para armazenar o ID da aula
        self.aula_id = aula_id

        # Se o ID for diferente de 0, carregar os dados da aula
        if aula_id:
            self.carregar_dados_aula(aula_id)

    def initUI(self):
        self.carregar_combos()

        # Desmarcar seleções nos combos
        self.comboInscricao.setCurrentIndex(-1)

        self.btnSalvar.clicked.connect(self.salvar_aula)
        self.btnCancelar.clicked.connect(self.fechar_janela)

        # Adicionando atributos de QLabel para exibir nome do aluno, do professor e descrição da disciplina
        self.labelAlunoValue = self.findChild(QLabel, 'labelAlunoValue')
        self.labelProfessorValue = self.findChild(QLabel, 'labelProfessorValue')
        self.labelDisciplinaValue = self.findChild(QLabel, 'labelDisciplinaValue')

        # Conectar o sinal currentIndexChanged do comboInscricao à função atualizar_dados_inscricao
        self.comboInscricao.currentIndexChanged.connect(self.atualizar_dados_inscricao)

    def carregar_combos(self):
        # Carregar dados do combo Inscricao
        carregar_combo(self.comboInscricao, 'inscrição', 'idInscrição', 'idInscrição')

    def atualizar_dados_inscricao(self):
        # Limpar os labels se nenhum item estiver selecionado
        if self.comboInscricao.currentIndex() == -1:
            self.labelAlunoValue.setText("")
            self.labelProfessorValue.setText("")
            self.labelDisciplinaValue.setText("")
            return

        # Obter o ID da inscrição selecionada
        inscricao_id = self.comboInscricao.currentData()

        # Obter dados da inscrição usando a função do MySQL Connector (substitua pelo nome da função real)
        dados_inscricao = self.obter_dados_inscricao(inscricao_id)

        # Atualizar os labels com os dados obtidos
        self.labelAlunoValue.setText(dados_inscricao[0])
        self.labelProfessorValue.setText(dados_inscricao[1])
        self.labelDisciplinaValue.setText(dados_inscricao[2])

    def obter_dados_inscricao(self, inscricao_id):
        # Função para obter dados da inscrição com base no ID
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consulta para obter dados da inscrição
            query = """
                SELECT aluno.Nome AS nome_aluno, professor.Nome AS nome_professor, disciplina.Designacao AS nome_disciplina
                FROM inscrição
                INNER JOIN aluno ON inscrição.Aluno_idAluno = aluno.idAluno
                INNER JOIN professor ON inscrição.Professor_idProfessor = professor.idProfessor
                INNER JOIN disciplina ON inscrição.Disciplina_idDisciplina = disciplina.idDisciplina
                WHERE inscrição.idInscrição = %s
            """
            cursor.execute(query, (inscricao_id,))
            dados_inscricao = cursor.fetchone()

            return dados_inscricao

        except Exception as e:
            print(f"Erro ao obter dados da inscrição: {e}")
            return None

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def salvar_aula(self):
        # Obter os dados do formulário
        inscricao_id = self.comboInscricao.currentData()
        data = self.dateEdit.date().toString(Qt.DateFormat.ISODate)
        hora = self.timeEdit.time().toString()

        # Lógica para verificar se os IDs existem e estão corretos
        if not verificar_existencia_id('inscrição', inscricao_id):
            QMessageBox.warning(self, 'ID Inválido', 'Por favor, insira um ID válido para Inscrição.')
            return

        # Lógica para salvar a aula no banco de dados
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Lógica para salvar a aula no banco de dados

            if self.aula_id == 0:
                # Se aula_id for 0, é uma nova inscrição, fazer a inserção
                query = "INSERT INTO aula (data, hora, Inscrição_idInscrição) VALUES (%s, %s, %s)"
                values = (data, hora, inscricao_id)
            else:
                # Se aula_id for diferente de 0, é uma atualização, fazer o update
                query = "UPDATE aula SET data = %s, hora = %s, Inscrição_idInscrição = %s WHERE idAula = %s"
                values = (data, hora, inscricao_id, self.aula_id)

            cursor.execute(query, values)

            # Commit da transação
            connection.commit()

            # Emitir o sinal indicando que uma nova aula foi adicionada
            self.aula_atualizada.emit()

            # Fechar a janela após a inclusão
            self.accept()

        except Exception as e:
            print("Erro ao incluir aula:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def carregar_dados_aula(self, aula_id):
        # Método para carregar os dados de uma aula existente
        try:
            connection = conecta()
            cursor = connection.cursor()

            # Consultar os dados da aula pelo ID
            query = """
                SELECT aula.data, aula.hora, aula.Inscrição_idInscrição,
                       aluno.Nome AS NomeAluno, professor.Nome AS NomeProfessor, disciplina.Designacao AS Disciplina
                FROM aula
                INNER JOIN inscrição ON aula.Inscrição_idInscrição = inscrição.idInscrição
                INNER JOIN aluno ON inscrição.Aluno_idAluno = aluno.idAluno
                INNER JOIN professor ON inscrição.Professor_idProfessor = professor.idProfessor
                INNER JOIN disciplina ON inscrição.Disciplina_idDisciplina = disciplina.idDisciplina
                WHERE aula.idAula = %s
            """
            cursor.execute(query, (aula_id,))

            aula_data = cursor.fetchone()

            if aula_data:
                # Lógica para carregar os valores nos combos com base nos IDs fornecidos
                inscricao_index = self.comboInscricao.findData(aula_data[2])

                # Selecionar os valores corretos nos combos
                if inscricao_index != -1:
                    self.comboInscricao.setCurrentIndex(inscricao_index)

                # Converter a data e hora para o formato apropriado
                data_formatada = QDate((aula_data[0]).year, (aula_data[0]).month, (aula_data[0]).day)
                self.dateEdit.setDate(data_formatada)

                hora_formatada = QTime.fromString(aula_data[1], "HH:mm:ss")
                self.timeEdit.setTime(hora_formatada)

                # Exibir nome do aluno, do professor e descrição da disciplina nos QLabel correspondentes
                self.labelAlunoValue.setText(aula_data[3])
                self.labelProfessorValue.setText(aula_data[4])
                self.labelDisciplinaValue.setText(aula_data[5])

        except Exception as e:
            print("Erro ao carregar dados da aula:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()