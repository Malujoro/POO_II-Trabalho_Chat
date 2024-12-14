# from bd.redis_bd import *
from worker.redis_bd import RedisDB
from random import randint
from chat.variaveis import *
from multiprocessing.pool import ThreadPool
"""
Importações:

1. Incluir classes e funções para lidar com o banco de dados Redis.
2. Incluir a função randint para criar números aleatórios.
3. Importa as variáveis 'nome_cliente' e 'nome_admin'.
"""

def generate_data(i):
    usuarios = [nome_cliente, nome_admin]
    return usuarios[randint(0, 1)], f"mensagem{i+1}"


def sender(data: tuple[str, str]):
    redisDB.create_message(data[0], data[1])


if __name__ == "__main__":
    """
    Bloco principal:

    Verifica se o script está sendo executado diretamente. 
    Se sim, cria-se uma lista nomeada 'usuarios' contendo 'nome_cliente' e 'nome_admin' (são os nomes dos usuários).
    Cria uma instância do Redis que será usada para interagir com o banco de dados.
    """
    redisDB = RedisDB()
    num_threads = 4
    total_records = 1_000_000
    batch_size = 100_000

    # redisDB.clear_all_data()

    # with ThreadPool(num_threads) as pool:
    #     batch_results = pool.map(generate_data, range(total_records))


    # for i in range(total_records):
    #     """
    #     For:

    #     Inicia um loop de 1 milhão de vezes.
    #     Seleciona um usuário aleatório da lista de usuários, sendo 0 para cliente e 1 para funcionário.
    #     Chama a função do arquivo redisDB.py.
    #     """
    #     data = generate_data(i)
    #     redisDB.create_message(data[0], data[1])

    num_batches = (total_records + batch_size - 1) // batch_size

    for batch_num in range(num_batches):
        print(f"Batch {batch_num + 1}/{num_batches}")

        current_batch_size = min(batch_size, total_records - batch_num * batch_size)

        with ThreadPool(num_threads) as pool:
            list_objects = pool.map(generate_data, range(current_batch_size))

        print(f"{len(list_objects)} mensagens no batch {batch_num + 1}")

        # Enviar dados do lote para o Redis
        with ThreadPool(num_threads) as pool:
            pool.map(sender, list_objects)

        print(f"Batch {batch_num + 1} finalizado\n")