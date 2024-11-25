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
    
    Inicializa a classe com os parâmentros de conexão do banco de dados, com dados pré definidos caso não seja informado:
    dbname (str): nome do banco (padrão: 'mydatabase');
    user (str): nome do usuário (padrão: 'user');
    password (str): senha do usuário (padrão: 'password');
    host (str): endereço do banco (padrão: 'localhost);
    port (str): porta do banco (padrão: '5410);
    
    conn: atributo que contém a conexão do banco (inicializado com None);
    cursor: atributo que contém o cursor do banco (inicializado com None);
    connect: a conexão com o banco de dados é estabelecida.
    """
    
    def __init__(self, dbname='mydatabase', user='user', password='password', host='localhost', port='5410'):
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
    def connect(self):
        if(self._conn == None):
            self._conn = psycopg2.connect(
                dbname = self._dbname,
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
    def create_table(self):
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                role VARCHAR(100) NOT NULL,
                message VARCHAR(255) NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._conn.commit()


    def insert(self, dados: list[tuple[str, str]]):
        if(dados):
            self._cursor.executemany("""
                INSERT INTO messages (role, message)
                VALUES (%s, %s)
            """, dados)
            self._conn.commit()


    def select_all(self):
        self._cursor.execute("SELECT * FROM messages")
        for row in self._cursor.fetchall():
            print(row)

        
    def disconnect(self):
        self._cursor.close()
        self._conn.close()


if(__name__ == "__main__"):
    banco = PostgressDB()
    # banco.insert([("funcionario", "mensagemOi")])
    banco.select_all()

# TODO: buscar itens no redis e salvar no postgres