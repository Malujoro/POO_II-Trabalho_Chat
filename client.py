import socket
import threading
from variaveis import *
from time import sleep


# Efetua a conexão com o servidor
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.settimeout(300)
socket_client.connect(ADDR)

nome = nome_cliente
socket_client.send(nome.encode())

# Função para receber mensagens
def escutar_mensagens():
    while True:
        try:
            msg = socket_client.recv(1024).decode()
            print(f"\n> {msg} \n")
        except socket.timeout:
            print("\nTimeout de conexão")
            break
        except:
            print("\nErro ao receber mensagem. ")
            break
    print("\nFinalizando conexão... ")
    socket_client.close()

thread_escuta = threading.Thread(target=escutar_mensagens, daemon=True)
thread_escuta.start()

def iniciar_cliente():
    sleep(1)
    while True:
        try:
            msg = input("\n")
            socket_client.send(msg.encode())
        except KeyboardInterrupt:
            print("\nSaindo... ")
            break
        except socket.timeout:
            print("\nTimeout de conexão")
            break
    print("\nFinalizando conexão... ")
    socket_client.close()

iniciar_cliente()