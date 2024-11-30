import socket
import threading
from .variaveis import *
from bd.postgresSQL import PostgressDB
"""
Importações:

1. Importa a biblioteca para criar e gerenciar conexões de rede.
2. Importa a biblioteca para gerenciar threads
3. Importa as variáveis 'IP' e 'Porta'.
4. Importa a classe PostgressDB para interagir com o banco de dados PostgreSQL.
"""


def encaminhar_mensagem(usuarios: dict[str: socket.socket], conexao: socket.socket, nome: str, banco: PostgressDB) -> None:
    """
    Método encaminhar_mensagem:

    -> Parâmetros:
    usuarios (dict[str: socket.socket]): um dicionário que armazena todas as conexões com os clientes ativas.
    conexao (socket.socket): objeto de conexão para enviar e receber mensagens.
    nome (str): o nome do usuário que está enviando a mensagem.
    banco (PostgressDB): uma instância da classe do banco de dados.

    Envia mensagens de boas-vindas se o cliente não for um administrador.
    Informa ao administrador quando um novo cliente se conecta.
    Entra em um loop para receber mensagens do cliente.
    Encaminha as mensagens para o destinatário adequado.
    Armazena as mensagens no banco de dados PostgreSQL.
    Remove o cliente da lista de usuários conectados e fecha a conexão quando o cliente se desconecta.
    """
    print(f"\n{nome} conectado.")

    if (nome != nome_admin):
        conexao.send(
            "Olá, tudo bem? Bem vindo ao atendimento da DrogaLaugh.".encode())
        conexao.send("Qual a sua dúvida? Estou aqui para ajudar.".encode())

        if (nome_admin in usuarios.keys()):
            usuarios[nome_admin].send(f"{nome} se conectou".encode())

    try:
        while True:
            mensagem = conexao.recv(1024).decode()
            if (not mensagem):
                break

            destino = [user for user in usuarios.items() if user[0] != nome]

            if (len(destino) > 0):
                destino[0][1].send(mensagem.encode())
                banco.insert([(nome, mensagem)])
                print(f"\n{nome}: {mensagem}")

    finally:
        del usuarios[nome]
        conexao.close()
        print(f"\n{nome} desconectado.")
        if (nome != nome_admin and nome_admin in usuarios.keys()):
            usuarios[nome_admin].send(f"{nome} desconectou".encode())


def iniciar_servidor(usuarios: dict[str: socket.socket] = {}) -> None:
    """
    Método iniciar_servidos:

    -> Parâmetros:
    usuarios (dict[str: socket.socket]): um dicionário que armazena todas as conexões com os clientes ativas.

    Cria uma instância de PostgressDB para interagir com o banco de dados.
    Cria um socket de servidor e o vincula ao endereço especificado.
    Coloca o socket em modo de escuta, aguardando conexões de clientes.
    Em um loop infinito, aceita novas conexões e cria uma nova thread para cada cliente conectado, chamando encaminhar_mensagem.
    Trata a interrupção do teclado (KeyboardInterrupt) para permitir o encerramento ordenado do servidor.
    """
    banco = PostgressDB()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(total_usuarios)
    print(f"Servidor rodando na porta {PORT}")

    while True:
        try:
            client_socket, _ = server_socket.accept()
            nome_usuario = client_socket.recv(1024).decode()
            usuarios[nome_usuario] = client_socket
            thread = threading.Thread(target=encaminhar_mensagem, args=(
                usuarios, client_socket, nome_usuario, banco), daemon=True)
            thread.start()
        except KeyboardInterrupt:
            break

    print("\nFinalizando servidor...")
    server_socket.close()


if (__name__ == "__main__"):
    """
    Bloco Principal:

    Executa a função iniciar_servidor se o script for executado diretamente.
    """
    iniciar_servidor()
