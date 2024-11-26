"""
Importação:

Importa a biblioteca do PostgreSQL.
"""
import psycopg2


"""
Classe PostgressDB:

Gerenciar as operações do banco de dados, como conectar, inserir e desconectar.
"""


class PostgressDB:

    """
    Construção da classe:

    Atributos (privados):

    Inicializa a classe com os parâmetros de conexão do banco de dados, com dados pré definidos caso não seja informado:
    dbname (str): nome do banco (padrão: 'mydatabase');
    user (str): nome do usuário (padrão: 'user');
    password (str): senha do usuário (padrão: 'password');
    host (str): endereço do banco (padrão: 'localhost);
    port (str): porta do banco (padrão: '5410);

    conn: atributo que contém a conexão do banco (inicializado com None);
    cursor: atributo que contém o cursor do banco (inicializado com None);
    connect: a conexão com o banco de dados é estabelecida.
    """

    def __init__(self, dbname: str = 'mydatabase', user: str = 'user', password: str = 'password', host: str = 'localhost', port: str = '5410') -> None:
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._conn = None
        self._cursor = None
        self.connect()

    """
    Método connect:

    Verifica de a variável conn é None.
    Se sim, estabelece conexão com o banco de dados usando 'psycopg2.connect'.
    Inicializa o cursor para executar os comandos SQL.
    Chama o método 'create_table' para criar a tabela caso não exista.
    """

    def connect(self) -> None:
        if (self._conn == None):
            self._conn = psycopg2.connect(
                dbname=self._dbname,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )

            self._cursor = self._conn.cursor()
            self.create_table()

    """
    Método create_table:

    Cria a tabela com as colunas: id, role, message e date.
    O comando 'self._conn.commit()' é usado para salvar as alterações.
    """

    def create_table(self) -> None:
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                role VARCHAR(100) NOT NULL,
                message VARCHAR(255) NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._conn.commit()

    """
    Método insert:

    Parâmetro:
    dado (lista[tupla[str, str]]): uma lsita de tuplas, na qual cada uma contém dois elementos do tipo string.

    Verifica se a lista não está vazia.
    Se não, o comando 'executemany' insere multiplas linhas de uma vez só (as duas strings passadas em cada tupla da lista).
    O comando 'self._conn.commit()' é usado para salvar as alterações.
    """

    def insert(self, dados: list[tuple[str, str]]) -> None:
        if (dados):
            self._cursor.executemany("""
                INSERT INTO messages (role, message)
                VALUES (%s, %s)
            """, dados)
            self._conn.commit()

    """
    Método select_all:

    O comando executado 'SELECT * FROM messeges' seleciona todas as linhas da tabela messages.
    No for, é exibido todas as linhas resultante.
    """

    def select_all(self) -> None:
        self._cursor.execute("SELECT * FROM messages")
        for row in self._cursor.fetchall():  # Recupera todas as linhas resultantes do comando anterior e retorna como uma lista de tuplas
            print(row)

    """
    Método disconnect:

    Fecha o cursor e a conexão (conn) com o banco de dados usando o comando close.
    """

    def disconnect(self) -> None:
        self._cursor.close()
        self._conn.close()


"""
Bloco Principal:

Verifica se o script está sendo executado diretamente. 
Cria uma instância da classe PostgressDB.
Chama o método select_all para imprimir todas as mensagens no banco de dados.
"""
if (__name__ == "__main__"):
    banco = PostgressDB()
    # banco.insert([("funcionario", "mensagemOi")])
    banco.select_all()

# TODO: buscar itens no redis e salvar no postgres
