import mysql.connector
from PyQt6.QtWidgets import QMessageBox


def conecta():
    return mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="centroexplicacoes2"
            )

def verificar_existencia_id(tabela, id):
    # Lógica para verificar se um ID existe em uma tabela específica
    try:
        connection = conecta()
        cursor = connection.cursor()

        # Lógica para verificar se um ID existe em uma tabela específica
        query = f"SELECT COUNT(*) FROM {tabela} WHERE id{tabela.capitalize()} = %s"
        cursor.execute(query, (id,))
        count = cursor.fetchone()[0]

        return count > 0

    except Exception as e:
        print(f"Erro ao verificar existência de ID na tabela {tabela}:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def imprime_erro_exclusao(self, e, artigo, entidade):
    mensagem_erro = f"Erro ao excluir {entidade}:"
    print(mensagem_erro, e)
    # Mostrar mensagem de erro para o utilizador
    if e.errno == 1451:
        # Utilizar expressão regular para extrair o nome da tabela referenciada
        tabela_referenciada = str(e).split("`, CONSTRAINT `")[0].split(".`")[1]
        mensagem = f"Não é possível excluir {artigo} {entidade}. A referência à tabela '{tabela_referenciada}' não permite a exclusão."
        QMessageBox.critical(self, 'Erro de Integridade Referencial', mensagem)
    else:
        QMessageBox.critical(self, 'Erro', mensagem_erro + f"\n{str(e)}")
