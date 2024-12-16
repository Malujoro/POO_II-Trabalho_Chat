import os
from .postgresSQL import PostgressDB
from .redis_bd import RedisDB
"""
Importação:

1. Importa o módulo os para acessar variáveis de ambiente.
2. Importa a classe PostgressDB do módulo postgresSQL para interagir com o banco de dados PostgreSQL.
3. Importa a classe RedisDB do módulo redis_bd para interagir com o banco de dados Redis.
"""


class Worker:
    """
    Classe Worker:

    Gerenciar a interação com um banco de dados Redis.
    Permite a criação de mensagens do Redis para o PostgreSQL, listar e excluir mensagens.
    """

    def __init__(self):
        """
        Construção da classe:

        Inicializa a instância do RedisDB e do PostgreSQL e estabelece uma conexão.

        -> Atributos (privados):
        redisDB (instância do Redis): conecta ao banco.
        postgres (instância do PostgreSQL): conecta ao banco.
        """
        self._redisDB = self._connect_redis()
        self._postgres = self._connect_postgress()

    def _connect_postgress(self) -> PostgressDB:
        """
        Método _connect_postgress:

        Efetua uma conexão com o banco Postgres.
        Utiliza valores das variáveis de ambiente existentes no contêiner docker.
        Retorna uma instância do PostgressDB.
        """
        try:
            postgres_host = os.getenv('POSTGRES_HOST', 'redis')
            postgres_user = os.getenv('POSTGRES_USER', 'user')
            postgres_password = os.getenv('POSTGRES_PASSWORD', 'password')
            postgres_db = os.getenv('POSTGRES_DB', 'mydatabase')

            return PostgressDB(postgres_db, postgres_user, postgres_password, postgres_host, port=5432)
        except Exception as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")

    def _connect_redis(self) -> RedisDB:
        """
        Método _connect_redis:

        Efetua uma conexão com o banco Redis.
        Utiliza valores das variáveis de ambiente existentes no contêiner docker.
        Retorna uma instância do RedisDB.
        """
        try:
            redis_host = os.getenv('REDIS_HOST', 'redis')

            return RedisDB(redis_host, 6379)
        except Exception as e:
            print(f"Erro ao conectar ao Redis: {e}")

    def wait_migrations(self, total_items: int, batch_size: int = 100_000, num_threads: int = 1) -> None:
        """
        Método wait_migrations:

        -> Parâmetros:
        total_items (int): total de mensagens a serem migradas.
        batch_size (int): tamanho do pacote a serem processados (padrão: 100000).
        num_threads (int): quantidade de threads a serem utilizadas (padrão: 1).

        Migra os dados da fila de mensagens do Redis para o banco Postgres.
        Após efetuar a transferência, remove as mensagem do Redis para evitar duplicatas.
        """
        num_batches = (total_items + batch_size - 1) // batch_size

        for batch_num in range(num_batches):
            print(f"Batch {batch_num + 1}/{num_batches}...")

            current_batch_size = min(
                batch_size, total_items - batch_num * batch_size)

            messages = self._redisDB.list_messages(
                current_batch_size, num_threads)

            print(f"{len(messages)} mensagens no batch {batch_num + 1}")

            if (len(messages) == 0):
                print("Não há mensagens")
            else:
                messages_to_insert = []
                keys_to_delete = []
                key = "Não há mensagens"

                for msg in messages:
                    role = msg["role"]
                    message = msg["message"]
                    key = f"message:{role}:{msg['timestamp']}"

                    keys_to_delete.append(key)
                    messages_to_insert.append((role, message))

                try:
                    self._postgres.insert(messages_to_insert)
                    self._redisDB.delete_message(keys_to_delete)
                except Exception as e:
                    print(f"Erro ao processar mensagem '{key}': {e}")

                print(f"Batch {batch_num + 1} finalizado\n")
