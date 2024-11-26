import socket
import threading
from variaveis import *


# Função para encaminhar as mensagens entre o funcionário e o cliente
def encaminhar_mensagem(usuarios: dict[str : socket.socket], conexao: socket.socket, nome: str) -> None:
    print(f"\n{nome} conectado.")

    if(nome != nome_admin):
        conexao.send("Olá, tudo bem? Bem vindo ao atendimento da DrogaLaugh.".encode())
        conexao.send("Qual a sua dúvida? Estou aqui para ajudar.".encode())

        if(nome_admin in usuarios.keys()):
            usuarios[nome_admin].send(f"{nome} se conectou".encode())

    try:
        while True:
            mensagem = conexao.recv(1024).decode()
            if(not mensagem):
                break
            
            destino = [user for user in usuarios.items() if user[0] != nome]

            if(len(destino) > 0):
                destino[0][1].send(mensagem.encode())
                print(f"\n{nome}: {mensagem}")

    finally:
        del usuarios[nome]
        conexao.close()
        print(f"\n{nome} desconectado.")
        if(nome != nome_admin and nome_admin in usuarios.keys()):
            usuarios[nome_admin].send(f"{nome} desconectou".encode())

# Função para iniciar o servidor
def iniciar_servidor(usuarios: dict[str : socket.socket] = {}) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(total_usuarios)
    print(f"Servidor rodando na porta {PORT}")

    while True:
        try:
            client_socket, _ = server_socket.accept()
            nome_usuario = client_socket.recv(1024).decode()
            usuarios[nome_usuario] = client_socket
            thread = threading.Thread(target=encaminhar_mensagem, args=(usuarios, client_socket, nome_usuario), daemon=True)
            thread.start()
        except KeyboardInterrupt:
            break
    
    print("\nFinalizando servidor...")
    server_socket.close()

if(__name__ == "__main__"):
    iniciar_servidor()