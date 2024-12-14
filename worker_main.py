from worker import Worker
"""
Importações:

"""


if (__name__ == "__main__"):
    """
    Bloco principal:

    Verifica se o worker está sendo executado diretamente. 
    Se sim, cria-se uma instância dos bancos que serão utilizados para a transferência (Postgres e Redis)
    Utiliza a função wait_migrations para efetuar a migração
    """
    worker = Worker()
    while True:
        worker.wait_migrations(1_000_000, num_threads=4)