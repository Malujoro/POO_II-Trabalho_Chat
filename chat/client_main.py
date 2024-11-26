""" 
Importa todas as definições do módulo 'user_class'.
Verifica se o código está sendo executado diretamente.
Se sim, cria uma instância de usuário com:
    - nome: nome_cliente
    - timeout: 300
Utiliza o método iniciar do usuário
"""
from user_class import *

if(__name__ == "__main__"):
    cliente = User(nome_cliente, 300)
    cliente.iniciar()