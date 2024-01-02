import mysql.connector

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
