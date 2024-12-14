# from bd.redis_bd import *
from worker.redis_bd import RedisDB
from random import randint
from chat.variaveis import *
"""
Importações:

1. Incluir classes e funções para lidar com o banco de dados Redis.
2. Incluir a função randint para criar números aleatórios.
3. Importa as variáveis 'nome_cliente' e 'nome_admin'.
"""

def generate_data(i):
    usuarios = [nome_cliente, nome_admin]
    return usuarios[randint(0, 1)], f"mensagem{i+1}"

if __name__ == "__main__":
    """
    Bloco principal:

    Verifica se o script está sendo executado diretamente. 
    Se sim, cria-se uma lista nomeada 'usuarios' contendo 'nome_cliente' e 'nome_admin' (são os nomes dos usuários).
    Cria uma instância do Redis que será usada para interagir com o banco de dados.
    """
    redisDB = RedisDB()

    # redisDB.clear_all_data()

    for i in range(1_000_000):
        """
        For:

        Inicia um loop de 1 milhão de vezes.
        Seleciona um usuário aleatório da lista de usuários, sendo 0 para cliente e 1 para funcionário.
        Chama a função do arquivo redisDB.py.
        """
        data = generate_data(i)
        redisDB.create_message(data[0], data[1])
