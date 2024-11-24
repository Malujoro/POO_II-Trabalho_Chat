import psycopg2

class PostgressDB:

    def __init__(self, dbname='mydatabase', user='user', password='password', host='localhost', port='5410'):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._conn = None
        self._cursor = None
        self.connect()

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

    def search_redis(self):
        pass


if(__name__ == "__main__"):
    banco = PostgressDB()
    # banco.insert([("funcionario", "mensagemOi")])
    banco.select_all()

# # TODO: buscar itens no redis e salvar no postgres