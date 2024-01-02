from PyQt6.QtWidgets import QDialog, QMessageBox, QComboBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal, Qt
from mysql_connector import conecta, verificar_existencia_id

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

        self.btnSalvar.clicked.connect(self.salvar_aula)
        self.btnCancelar.clicked.connect(self.fechar_janela)

    def carregar_combos(self):
        # Carregar dados do combo Inscricao
        self.carregar_combo(self.comboInscricao, 'inscrição', 'idInscrição', 'idInscrição')

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
                combo.addItem(f"{row[0]}", userData=row[0])

        except Exception as e:
            print(f"Erro ao carregar combo {tabela}: {e}")

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
            query = "INSERT INTO aula (data, hora, Inscrição_idInscrição) VALUES (%s, %s, %s)"
            values = (data, hora, inscricao_id)
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
            query = "SELECT data, hora, Inscrição_idInscrição FROM aula WHERE idAula = %s"
            cursor.execute(query, (aula_id,))

            aula_data = cursor.fetchone()

            if aula_data:
                # Lógica para carregar os valores nos combos com base nos IDs fornecidos
                inscricao_index = self.comboInscricao.findData(aula_data[2])

                # Selecionar os valores corretos nos combos
                if inscricao_index != -1:
                    self.comboInscricao.setCurrentIndex(inscricao_index)

                # Converter a data e hora para o formato apropriado
                data_formatada = Qt.QDateTime.fromString(aula_data[0], Qt.DateFormat.ISODate)
                self.dateEdit.setDate(data_formatada.date())

                hora_formatada = Qt.QDateTime.fromString(aula_data[1], Qt.DateFormat.DefaultLocaleLongDate)
                self.timeEdit.setTime(hora_formatada.time())

        except Exception as e:
            print("Erro ao carregar dados da aula:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fechar_janela(self):
        # Fechar a janela sem fazer alterações
        self.reject()