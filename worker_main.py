from worker import Worker
"""
Importações:
Biblioteca com as funções do Worker
"""


if (__name__ == "__main__"):
    """
    Bloco principal:

    Verifica se o worker está sendo executado diretamente. 
    Se sim, cria-se uma instância do worker que fará a migração
    """

    worker = Worker()

    while True:
        try:
            start = input("Inicializar worker? ")
            if(start != "0"):
                worker.wait_migrations(1_000_000, batch_size = 100_000, num_threads = 4)
            break
        except:
            print("Reinicializando worker")
            continue