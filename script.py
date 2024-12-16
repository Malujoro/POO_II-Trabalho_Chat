# from bd.redis_bd import *
from worker.redis_bd import RedisDB
from random import randint
from chat.variaveis import *
from multiprocessing.pool import ThreadPool
"""
Importações:

1. Importa o módulo worker para interagir com o banco de dados Redis.
2. Importa a função randint para criar números aleatórios.
3. Importa as variáveis 'nome_cliente' e 'nome_admin'.
4. Importa a classe ThreadPool para executar as tarefas com Threads.
"""


def generate_data(i):
    """
    Método generate_data:

    -> Parâmetro:
    i (int): índice.

    Gera uma lista com o tipo do cliente - que será gerado aleatoriamente - e a mensagem.
    Gera uma mensagem padrão baseada no índice.
    Retorna a lista.
    """
    usuarios = [nome_cliente, nome_admin]
    return usuarios[randint(0, 1)], f"mensagem{i+1}"


def sender(data: tuple[str, str]):
    """
    Método sender:

    -> Parâmetro:
    data (tupla[str]): informações que serão salvos no Redis.

    Envia uma mensagem pro Redis com a tupla.
    """
    redisDB.create_message(data[0], data[1])


if __name__ == "__main__":
    """
    Bloco principal:

    Verifica se o script está sendo executado diretamente. 
    Se sim, cria-se uma instância do Redis que será usada para interagir com o banco de dados.
    Define o número de threads.
    Define o total de registros a serem criados.
    Define o tamanho de cada pacote.
    Calcula a quantidade de pacotes necessários.
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
        """
        For:

        Para cada pacote, calcula o seu tamnho.
        Utiliza threads para gerar dados com o método 'generate_data' e os armazena na 'list_objects'.
        Utiliza threads para enviar os dados gerados no 'sender' para o Redis.        
        """
        print(f"Batch {batch_num + 1}/{num_batches}")

        current_batch_size = min(
            batch_size, total_records - batch_num * batch_size)

        with ThreadPool(num_threads) as pool:
            list_objects = pool.map(generate_data, range(current_batch_size))

        print(f"{len(list_objects)} mensagens no batch {batch_num + 1}")

        with ThreadPool(num_threads) as pool:
            pool.map(sender, list_objects)

        print(f"Batch {batch_num + 1} finalizado\n")
