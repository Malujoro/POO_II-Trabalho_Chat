import redis
from datetime import datetime

class RedisDB:

    """
    Classe para gerenciar a interação com um banco de dados Redis.
    Permite criar, listar e excluir mensagens, limpar o banco e fechar a conexão.
    """

    def __init__(self, host: str = 'localhost', port: int = 6380, decode_responses: bool = True) -> None:
        """
        Inicializa a instância do RedisDB e estabelece uma conexão com o Redis.

        host (str): Endereço do servidor Redis (padrão: 'localhost').
        port (str): Porta do servidor Redis (padrão: 6380).
        decode_responses (str): Define se as respostas do Redis devem ser decodificadas como strings (padrão: True).
        """
        self._host = host
        self._port = port
        self._decode_responses = decode_responses
        self._client = None 
        self.connect()


    def connect(self) -> None:
        """
        Estabelece uma conexão com o servidor Redis.
        """
        if(self._client is None):
            self._client = redis.Redis(
                host=self._host,
                port=self._port,
                decode_responses=self._decode_responses
            )


    def create_message(self, role: str, message: str) -> None:
        """
        Cria e armazena uma mensagem no Redis.

        role (str): Papel associado à mensagem (ex.: 'usuario', 'funcionario').
        message (str): Conteúdo da mensagem.
        """
        
        timestamp = datetime.now().isoformat()
        key = f"message:{role}:{timestamp}"
        self._client.hset(key, mapping={
            'role': role,
            'message': message,
            'timestamp': timestamp
        })
    

    def list_messages(self) -> list[dict[str : str]]:
        """
        Lista todas as mensagens armazenadas no Redis.

        Retorno: Lista de dicionários contendo as mensagens.
        """
        messages = []
        cursor = 0
        pattern = "message:*"

        while True:
            cursor, keys = self._client.scan(cursor=cursor, match=pattern, count=10)
            for key in keys:
                messages.append(self._client.hgetall(key))
                print(messages[-1])
            if cursor == 0:
                break

        return messages
    

    def delete_message(self, key: str) -> None:
        """
        Exclui uma mensagem específica do Redis.

        key (str): A chave da mensagem a ser excluída.
        """
        self._client.delete(key)


    def clear_all_data(self) -> None:
        """
        Remove todos os dados armazenados no Redis.
        """
        self._client.flushdb()


    def close(self) -> None:
        """
        Fecha a conexão com o servidor Redis.
        """
        self._client.close()


if(__name__ == "__main__"):
    """
    Teste de funcionalidades. 
    Exibe todas as mensagens do banco.
    """
    redis = RedisDB()

    # redis.create_message("usuario", "mensagem1")
    # redis.create_message("funcionario", "mensagem2")
    # redis.create_message("funcionario", "mensagem3")
    # redis.create_message("funcionario", "mensagem4")
    mensagens = redis.list_messages()
    for msg in mensagens:
        print(msg)

    redis.close()