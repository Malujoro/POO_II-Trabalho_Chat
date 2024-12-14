import os
from .postgresSQL import PostgressDB
from .redis_bd import RedisDB


class Worker:

    def __init__(self):
        self._redisDB = self._connect_redis()
        self._postgres = self._connect_postgress()


    def _connect_postgress(self) -> PostgressDB:
        """
        Função para efetuar uma conexão com o banco Postgres (utiliza valores das variáveis de ambiente existentes no contêiner docker)

        Retorna uma instância do PostgressDB:
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
        Função para efetuar uma conexão com o banco Redis (utiliza valores das variáveis de ambiente existentes no contêiner docker)

        Retorna uma instância do RedisDB:
        """
        try:
            redis_host = os.getenv('REDIS_HOST', 'redis')

            return RedisDB(redis_host, 6379)
        except Exception as e:
            print(f"Erro ao conectar ao Redis: {e}")


    def wait_migrations(self, total_items: int, batch_size: int = 100_000) -> None:
        """
        Função para migrar os dados da fila de mensagens do Redis para o banco Postgres
        Após efetuar a transferência, remove as mensagem do Redis (para evitar duplicatas)
        """

        num_batches = (total_items + batch_size - 1) // batch_size

        for batch_num in range(num_batches):
            print(f"Batch {batch_num + 1}/{num_batches}...")

            current_batch_size = min(batch_size, total_items - batch_num * batch_size)

            messages = self._redisDB.list_messages(current_batch_size)

            print(f"{len(messages)} mensagens no batch {batch_num + 1}")

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