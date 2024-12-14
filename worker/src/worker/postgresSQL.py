import psycopg2
"""
Importação:

1. Importa a biblioteca do PostgreSQL.
"""


class PostgressDB:
    """
    Classe PostgressDB:

    Gerenciar as operações do banco de dados Postgress.
    Permite conectar, inserir mensagem e desconectar.
    """

    def __init__(self, dbname: str = 'mydatabase', user: str = 'user', password: str = 'password', host: str = 'localhost', port: str = '5410') -> None:
        """
        Construção da classe:

        Inicializa a instância do PostgressDB e estabelece uma conexão com o banco.

        -> Atributos (privados):

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
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._conn = None
        self._cursor = None
        self.connect()

    def connect(self) -> None:
        """
        Método connect:

        Verifica de a variável conn é None.
        Se sim, estabelece conexão com o banco de dados usando 'psycopg2.connect'.
        Inicializa o cursor para executar os comandos SQL.
        Chama o método 'create_table' para criar a tabela caso não exista.
        """
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

    def create_table(self) -> None:
        """
        Método create_table:

        Cria a tabela com as colunas: id, role, message e date.
        O comando 'self._conn.commit()' é usado para salvar as alterações.
        """
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                role VARCHAR(100) NOT NULL,
                message VARCHAR(255) NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._conn.commit()

    def insert(self, dados: list[tuple[str, str]]) -> None:
        """
        Método insert:

        Parâmetro:
        dado (lista[tupla[str, str]]): uma lista de tuplas, na qual cada uma contém dois elementos do tipo string.
            - O primeiro elemento corresponde ao nome de quem enviou a mensagem
            - O segundo elemento corresponde a mensagem que foi enviada

        Verifica se a lista não está vazia.
        Se não, o comando 'executemany' insere multiplas linhas de uma vez só (as duas strings passadas em cada tupla da lista).
        O comando 'self._conn.commit()' é usado para salvar as alterações.
        """
        if (dados):
            self._cursor.executemany("""
                INSERT INTO messages (role, message)
                VALUES (%s, %s)
            """, dados)
            self._conn.commit()

    def select_all(self) -> None:
        """
        Método select_all:

        O comando executado 'SELECT * FROM messages' seleciona todas as linhas da tabela messages.
        No for, é exibido todas as linhas resultante.
        """
        self._cursor.execute("SELECT * FROM messages")
        for row in self._cursor.fetchall():  # Recupera todas as linhas resultantes do comando anterior e retorna como uma lista de tuplas
            print(row)

    def disconnect(self) -> None:
        """
        Método disconnect:

        Fecha o cursor e a conexão (conn) com o banco de dados usando o comando close.
        """
        self._cursor.close()
        self._conn.close()


if (__name__ == "__main__"):
    """
    Bloco Principal:

    Verifica se o script está sendo executado diretamente. 
    Cria uma instância da classe PostgressDB.
    Chama o método select_all para imprimir todas as mensagens no banco de dados.
    """
    banco = PostgressDB()
    # banco.insert([("funcionario", "mensagemOi")])
    banco.select_all()

# TODO: buscar itens no redis e salvar no postgres
