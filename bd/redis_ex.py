import redis
from datetime import datetime
class RedisDB:

    def __init__(self, host='localhost', port=6380, decode_responses=True):
        self._host = host
        self._port = port
        self._decode_responses = decode_responses
        self._client = None
        self.connect()

    def connect(self):
        if(self._client is None):
            self._client = redis.Redis(
                host=self._host,
                port=self._port,
                decode_responses=self._decode_responses
            )

    def create_message(self, role: str, message: str):
        timestamp = datetime.now().isoformat()
        key = f"message:{role}:{timestamp}"
        self._client.hset(key, mapping={
            'role': role,
            'message': message,
            'timestamp': timestamp
        })
    
    def list_messages(self):
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
    
    def delete_message(self, key: str):
        self._client.delete(key)

    def clear_all_data(self):
        self._client.flushdb()

    def close(self):
        self._client.close()


if(__name__ == "__main__"):
    redis = RedisDB()

    # redis.create_message("usuario", "mensagem1")
    # redis.create_message("funcionario", "mensagem2")
    # redis.create_message("funcionario", "mensagem3")
    # redis.create_message("funcionario", "mensagem4")
    mensagens = redis.list_messages()
    for msg in mensagens:
        print(msg)

    redis.close()