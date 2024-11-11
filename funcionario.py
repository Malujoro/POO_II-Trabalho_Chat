import socket
import threading
from variaveis import *


# Efetua a conexão com o servidor
socket_adm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_adm.connect(ADDR)

nome = nome_admin
socket_adm.send(nome.encode())

# Função para receber mensagens
def escutar_mensagens():
    while True:
        try:
            msg = socket_adm.recv(1024).decode()
            print(f"\n> {msg} \n")
        except:
            print("\nErro ao receber mensagem. ")
            break

thread_escuta = threading.Thread(target=escutar_mensagens, daemon=True)
thread_escuta.start()

def init_admin():
    while True:
        try:
            msg = input("\n")
            socket_adm.send(msg.encode())
        except KeyboardInterrupt:
            print("\nSaindo... ")
            break
    print("\nFinalizando conexão... ")
    socket_adm.close()

init_admin()