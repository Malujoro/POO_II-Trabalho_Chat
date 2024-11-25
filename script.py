"""
Importações:

1. Incluir classes e funções para lidar com o banco de dados Redis.
2. Incluir a função randint para criar números aleatórios.
3. Importa as variáveis 'nome_cliente' e 'nome_admin'.
"""
from bd.redis_ex import *
from random import randint
from chat.variaveis import *

"""
Bloco principal:

Verifica se o script está sendo executado diretamente. 
Se sim, cria-se uma lista nomeada 'usuarios' contendo 'nome_cliente' e 'nome_admin' (são os nomes dos usuários).
Cria uma instância do Redis que será usada para interagir com o banco de dados.
"""
if __name__ == "__main__":
    usuarios = [nome_cliente, nome_admin]
    redis = RedisDB()

    """
    For:

    Inicia um loop de 1 milhão de vezes.
    Seleciona um usuário aleatório da lista de usuários, sendo 0 para cliente e 1 para funcionário.
    Chama a função do arquivo redis_ex.py.
    """
    for i in range(10000):
        redis.create_message(usuarios[randint(0, 1)], f"mensagem{i+1}")
