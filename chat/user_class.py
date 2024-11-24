import socket
import threading
from variaveis import *

class User:

    __slots__ = ["_nome", "_timeout", "_endereco", "_socket_user"]

    def __init__(self, nome: str, timeout: int = 0, endereco: tuple[int, int] = ADDR):
        self._nome = nome
        self._timeout = timeout
        self._endereco = endereco
        self._socket_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket_user.connect(endereco)
        if(self._timeout > 0):
            self._socket_user.settimeout(timeout)

        self._socket_user.send(self._nome.encode())

    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, nome: str):
        self._nome = nome

    @property
    def timeout(self) -> int:
        return self._timeout
    
    @timeout.setter
    def timeout(self, timeout: int):
        self._timeout = timeout

    @property
    def endereco(self) -> tuple[int, int]:
        return self._endereco
    
    @endereco.setter
    def endereco(self, endereco: tuple[int, int]):
        self._endereco = endereco

    @property
    def socket_user(self) -> socket.socket:
        return self._socket_user
    
    @socket_user.setter
    def socket_user(self, socket_user: socket.socket):
        self._socket_user = socket_user

    def escutar_mensagens(self):
        while True:
            try:
                msg = self._socket_user.recv(1024).decode()
                print(f"\n> {msg} \n")
            except socket.timeout:
                print("\nTimeout de conexão")
                break
            except:
                print("\nErro ao receber mensagem.")
                break
        print("\nFinalizando conexão...")
        self._socket_user.close()


    def iniciar(self):
        thread_escuta = threading.Thread(target=self.escutar_mensagens, daemon=True)
        thread_escuta.start()
        while True:
            try:
                msg = input("\n")
                self._socket_user.send(msg.encode())
            except KeyboardInterrupt:
                print("\nSaindo...")
                break
            except socket.timeout:
                print("\nTimeout de conexão")
                break
        print("\nFinalizando conexão...")
        self._socket_user.close()