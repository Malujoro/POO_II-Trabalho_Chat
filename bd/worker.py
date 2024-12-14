import os
from postgresSQL import *
from redis_bd import *
"""
Importações:

1. Importa as biblioteca os para obter valores das "variáveis de ambiente".
2. Incluir classes e funções para lidar com o banco de dados Postgres.
3. Incluir classes e funções para lidar com o banco de dados Redis.
"""


def connect_postgress() -> PostgressDB:
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


def connect_redis() -> RedisDB:
    """
    Função para efetuar uma conexão com o banco Redis (utiliza valores das variáveis de ambiente existentes no contêiner docker)

    Retorna uma instância do RedisDB:
    """
    try:
        redis_host = os.getenv('REDIS_HOST', 'redis')

        return RedisDB(redis_host, 6379)
    except Exception as e:
        print(f"Erro ao conectar ao Redis: {e}")


def wait_migrations(redisDb: RedisDB, postgres: PostgressDB) -> None:
    """
    Função para migrar os dados da fila de mensagens do Redis para o banco Postgres
    Após efetuar a transferência, remove as mensagem do Redis (para evitar duplicatas)

    redisDb (RedisDB): Instância do Redis
    postgres (PostgressDB): Instância do Postgres
    """
    messages = redisDb.list_messages()
    messages_to_insert = [] 
    keys_to_delete = []

    for msg in messages:

        role = msg["role"]
        message = msg["message"]
        key = f"message:{role}:{msg['timestamp']}"

        keys_to_delete.append(key)
        messages_to_insert.append((role, message))

        try:
            postgres.insert(messages_to_insert)
            redisDb.delete_message(keys_to_delete)
        except Exception as e:
            print(f"Erro ao processar mensagem '{key}': {e}")


if (__name__ == "__main__"):
    """
    Bloco principal:

    Verifica se o worker está sendo executado diretamente. 
    Se sim, cria-se uma instância dos bancos que serão utilizados para a transferência (Postgres e Redis)
    Utiliza a função wait_migrations para efetuar a migração
    """
    postgres = connect_postgress()
    redisDb = connect_redis()

    while True:
        wait_migrations(redisDb, postgres)
