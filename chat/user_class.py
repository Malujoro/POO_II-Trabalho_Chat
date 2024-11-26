"""
Importação:

Importa a biblioteca de socket (para se conectar utilizando sockets).
Importa a biblioteca threading (para utilizar múltiplas threads)
Importa informações importantes do arquivo variáveis (como o endereço ip, porta e nomes padronizados do usuário e cliente)
"""
import socket
import threading
from variaveis import *

class User:
    """
    Construção da classe:

    Atributos (privados):

    Inicializa a classe com os parâmetros necessários do usuário, com dados pré definidos caso não seja informado:
    nome (str): nome do usuário;
    timeout (int): tempo limite do timeout (padrão: 0);
    endereco tuple[int, int]: tupla contendo o endereço e porta do servidor a ser acessado (padrão: ADDR, originado do arquivo "variáveis.py");
    socket_user (socket.socket): atributo que irá guardar a instância do socket;

    O socket efetuará uma conexão ao servidor.
    Caso timeout seja maior que 0, ele será definido
    Por fim, o cliente irá enviar seu nome como primeira mensagem no servidor
    """

    __slots__ = ["_nome", "_timeout", "_endereco", "_socket_user"]

    def __init__(self, nome: str, timeout: int = 0, endereco: tuple[int, int] = ADDR) -> None:
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
    def nome(self, nome: str) -> None:
        self._nome = nome

    @property
    def timeout(self) -> int:
        return self._timeout
    
    @timeout.setter
    def timeout(self, timeout: int) -> None:
        self._timeout = timeout

    @property
    def endereco(self) -> tuple[int, int]:
        return self._endereco
    
    @endereco.setter
    def endereco(self, endereco: tuple[int, int]) -> None:
        self._endereco = endereco

    @property
    def socket_user(self) -> socket.socket:
        return self._socket_user
    
    @socket_user.setter
    def socket_user(self, socket_user: socket.socket) -> None:
        self._socket_user = socket_user

    """
    Método escutar_mensagens:

    Utilizado para escutar mensagens de maneira contínua
    Exibe na tela a mensagem recebida, ou então um feedback de erro
    """
    def escutar_mensagens(self) -> None:
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

    """
    Método iniciar:

    Utilizado para inicializar a troca de mensagens com o servidor
    Atribui a uma thread a função de escutar_mensagens
    Espera uma entrada do usuário (msg), que será enviada ao servidor
    Caso ocorra uma exceção KeyboardInterrupt, a conexão será finalizada
    """
    def iniciar(self) -> None:
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