
from bd.redis_ex import *
from random import randint
from chat.variaveis import *

if __name__ == "__main__":
    usuarios = [nome_cliente, nome_admin]
    redis = RedisDB()

    for i in range(10000):
        redis.create_message(usuarios[randint(0, 1)], f"mensagem02")