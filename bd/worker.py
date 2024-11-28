"""
Importações:

1. Importa as biblioteca os para obter valores das "variáveis de ambiente".
2. Incluir classes e funções para lidar com o banco de dados Postgres.
3. Incluir classes e funções para lidar com o banco de dados Redis.
"""
import os
from postgresSQL import *
from redis_bd import *


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

        return PostgressDB(postgres_db, postgres_user, postgres_password, postgres_host, port = 5432)
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
    Após efetuar a transferência, remove a mensagem do Redis (para evitar duplicatas)

    redisDb (RedisDB): Instância do Redis
    postgres (PostgressDB): Instância do Postgres
    """
    messages = redisDb.list_messages()
    
    for msg in messages:
        
        role = msg["role"]
        message = msg["message"]
        key = f"message:{role}:{msg['timestamp']}"

        try:
            postgres.insert([(role, message)])
            redisDb.delete_message(key)
        except Exception as e:
            print(f"Erro ao processar mensagem '{key}': {e}")

"""
Bloco principal:

Verifica se o worker está sendo executado diretamente. 
Se sim, cria-se uma instância dos bancos que serão utilizados para a transferência (Postgres e Redis)
Utiliza a função wait_migrations para efetuar a migração
"""
if(__name__ == "__main__"):
    postgres = connect_postgress()
    redisDb = connect_redis()
    
    while True:
        wait_migrations(redisDb, postgres)