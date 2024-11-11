import socket
import threading
from variaveis import *


# Define um dicionário com o IP e Porta dos clientes
clientes = {}

# Função para gerenciar cada cliente em uma thread
def handle_client(conexao, nome):
    print(f"\n{nome} conectado.")

    if(nome != nome_admin):
        conexao.send("Olá, tudo bem? Bem vindo ao atendimento da DrogaLaugh.".encode())
        conexao.send("Qual a sua dúvida? Estou aqui para ajudar.".encode())

        if(nome_admin in clientes.keys()):
            clientes[nome_admin].send(f"{nome} se conectou".encode())

    try:
        while True:
            mensagem = conexao.recv(1024).decode()
            if(not mensagem):
                break
            
            destino = [user for user in clientes.items() if user[0] != nome]

            if(len(destino) > 0):
                destino[0][1].send(mensagem.encode())
                print(f"\n{nome} -> {destino[0][0]}: {mensagem}")

    finally:
        del clientes[nome]
        conexao.close()
        print(f"\n{nome} desconectado.")
        if(nome != nome_admin and nome_admin in clientes.keys()):
            clientes[nome_admin].send(f"{nome} desconectou".encode())

# Função para iniciar o servidor
def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(3)
    print(f"Servidor rodando na porta {PORT}")

    while True:
        client_socket, _ = server_socket.accept()
        nome_usuario = client_socket.recv(1024).decode()
        clientes[nome_usuario] = client_socket
        thread = threading.Thread(target=handle_client, args=(client_socket, nome_usuario))
        thread.start()

iniciar_servidor()