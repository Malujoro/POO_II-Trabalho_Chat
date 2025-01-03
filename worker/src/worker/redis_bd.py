"""
Importação:

1. Importa a biblioteca do Redis.
2. Importa o datetime para manipular datas e horas.
"""
import redis
from datetime import datetime
from multiprocessing.pool import ThreadPool


class RedisDB:
    """
    Classe RedisDB:

    Gerenciar a interação com um banco de dados Redis.
    Permite criar, listar e excluir mensagens, limpar o banco e fechar a conexão.
    """

    def __init__(self, host: str = 'localhost', port: int = 6380, decode_responses: bool = True) -> None:
        """
        Construção da classe:

        Inicializa a instância do RedisDB e estabelece uma conexão com o banco.

        -> Atributos (privados):

        Inicializa a classe com os parâmetros de conexão do banco de dados, com dados pré definidos caso não seja informado:
        host (str): endereço do servidor Redis (padrão: 'localhost').
        port (str): porta do servidor Redis (padrão: 6380).
        decode_responses (str): define se as respostas do Redis devem ser decodificadas como strings (padrão: True).

        client (objeto): a conexão com o Redis
        connect: a conexão com o banco de dados é estabelecida.
        """
        self._host = host
        self._port = port
        self._decode_responses = decode_responses
        self._client = None
        self.connect()

    def connect(self) -> None:
        """
        Método connect:

        Verifica de a variável conn é None.
        Se sim, cria uma nova instância do cliente Redis.
        """
        if (self._client is None):
            self._client = redis.Redis(
                host=self._host,
                port=self._port,
                decode_responses=self._decode_responses
            )

    def create_message(self, role: str, message: str) -> None:
        """
        Método create_message:

        -> Parâmetros:
        role (str): papel associado à mensagem.
        message (str): conteúdo da mensagem.

        Gera um timestamp atual no formato ISO 8601.
        Cria uma chave única para a mensagem.
        Armazena dados na forma de um hash (estrutura de dados similar a um dicionário) em Redis.
        """
        timestamp = datetime.now().isoformat()
        key = f"message:{role}:{timestamp}"
        self._client.hset(key, mapping={
            'role': role,
            'message': message,
            'timestamp': timestamp
        })


    def fetch_data(self, key: list[str]):
        """
        Método fetch_data:

        -> Parâmetros:
        key (lista): armazena todas as chaves.

        Retorna a lista com as mensagens referentes a chave enviada.
        """
        return self._client.hgetall(key)
    

    def list_messages(self, quant: int = 100_000, num_threads: int = 1) -> list[dict[str, str]]:
        """
        Método list_messages:

        -> Variáveis:
        messages (lista): armazena todas as mensagens recuperadas do Redis.
        cursor (int): mantém o estado da iteração.
        pattern (str): define o "molde" das chaves que o comando SCAN deve procurar.
        remaining (int): define quantas mensagens ainda faltam ser buscadas.
        keys (lista): define as chaves que serão buscadas pelo fetch_data.

        Procura chaves de 100.000 em 100.000 que correspondem ao pattern
        Adiciona na lista todos os valores armazenados no hash daquela chave.
        Retorna a lista com as mensagens encontradas.
        """
        messages = []
        cursor = 0
        pattern = "message:*"

        while len(messages) < quant:
            cursor, keys = self._client.scan(cursor=cursor, match=pattern, count=quant)

            if(not keys):
                break

            remaining = quant - len(messages)
            keys = keys[:remaining]

            with ThreadPool(num_threads) as pool:
                batch_results = pool.map(self.fetch_data, keys)

            messages.extend(batch_results)

            if(cursor == 0):
                break

        return messages

    def delete_message(self, keys: list[str]) -> None:
        """
        Método delete_message:

        -> Parâmetro:
        key (list[str]): as chaves das mensagems a serem excluídas.

        Exclui a lista de mensagems desempacotadas mandando por parâmetro do Redis.
        """
        self._client.delete(*keys)

    def count_records(self) -> int:
        """
        Método count_records:

        Retorna o número total de registros armazenados no Redis.
        """
        return self._client.dbsize()


    def clear_all_data(self) -> None:
        """
        Método clear_all_data:

        Remove todos os dados armazenados no Redis.
        """
        self._client.flushdb()

    def close(self) -> None:
        """
        Método close:

        Fecha a conexão com o servidor Redis.
        """
        self._client.close()


if (__name__ == "__main__"):
    """
    Bloco Principal:

    Cria uma instância da classe RedisDB
    Retorna todas as mensagens armazenadas do Redis
    Chama o método close para desconectar do banco de dados.
    """
    redisDb = RedisDB()

    # redisDb.create_message("usuario", "mensagem1")
    # redisDb.create_message("funcionario", "mensagem2")
    # redisDb.create_message("funcionario", "mensagem3")
    # redisDb.create_message("funcionario", "mensagem4")

    # redisDb.clear_all_data()
    mensagens = redisDb.list_messages()
    # for msg in mensagens:
    #     print(msg)

    redisDb.close()
