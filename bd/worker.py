import os
from postgresSQL import *
from bd.redis import *

def connect_postgress():
    try:
        postgres_host = os.getenv('POSTGRES_HOST', 'redis')
        postgres_user = os.getenv('POSTGRES_USER', 'user')
        postgres_password = os.getenv('POSTGRES_PASSWORD', 'password')
        postgres_db = os.getenv('POSTGRES_DB', 'mydatabase')

        return PostgressDB(postgres_db, postgres_user, postgres_password, postgres_host, port = 5432)
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")


def connect_redis():
    try:
        redis_host = os.getenv('REDIS_HOST', 'redis')

        return RedisDB(redis_host, 6379)
    except Exception as e:
        print(f"Erro ao conectar ao Redis: {e}")
    

def wait_migrations(redis: RedisDB, postgres: PostgressDB):
    messages = redis.list_messages()
    
    for msg in messages:
        
        role = msg["role"]
        message = msg["message"]
        key = f"message:{role}:{msg['timestamp']}"

        try:
            postgres.insert([(role, message)])
            redis.delete_message(key)
        except Exception as e:
            print(f"Erro ao processar mensagem '{key}': {e}")


if(__name__ == "__main__"):
    postgres = connect_postgress()
    redis = connect_redis()
    
    while True:
        wait_migrations(redis, postgres)