from user_class import *
""" 
Importação: 

1. Importa todas as definições do módulo 'user_class'.
"""

if (__name__ == "__main__"):
    """
    Bloco Principal:

    Verifica se o código está sendo executado diretamente.
    Se sim, cria uma instância de usuário com:
        - nome: nome_admin
    Utiliza o método iniciar do usuário
    """
    admin = User(nome_admin)
    admin.iniciar()
