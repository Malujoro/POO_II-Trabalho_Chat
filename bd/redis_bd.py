"""
Importação:

1. Importa a biblioteca do Redis.
2. Importa o datetime para manipular datas e horas.
"""
import redis
from datetime import datetime


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

    def list_messages(self) -> list[dict[str: str]]:
        """
        Método list_messages:

        -> Variáveis:
        messages (lista): armazena todas as mensagens recuperadas do Redis.
        cursor (int): mantem o estado da iteração.
        pattern (str): define quais chaves o comando SCAN deve procurar.

        Procura chaves de 10 em 10 que correspondem ao pattern
        Adiciona na lista todos os valores armazenados no hash daquela chave.
        Retorna a lista com as mensagens encontradas.
        """
        messages = []
        cursor = 0
        pattern = "message:*"

        while True:
            cursor, keys = self._client.scan(
                cursor=cursor, match=pattern, count=10)
            for key in keys:
                messages.append(self._client.hgetall(key))
                print(messages[-1])
            if cursor == 0:
                break

        return messages

    def delete_message(self, keys: list[str]) -> None:
        """
        Método delete_message:

        -> Parâmetro:
        key (str): a chave da mensagem a ser excluída.

        Exclui uma mensagem mandando por parâmetro do Redis.
        """
        self._client.delete(*keys)

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
