import pytest
from unittest.mock import patch
import socket
from user_class import User
from variaveis import *


class TestUser:

    @pytest.fixture
    def user_cliente(self):
        return User(nome_cliente, timeout=300, endereco=ADDR)

    @pytest.fixture
    def user_funcionario(self):
        return User(nome_admin)

    @pytest.fixture
    def mock_socket(self):
        # Cria um "substituto" para o socket.socket (utilizado na criação do objeto do socket)
        with patch("socket.socket") as mock_socket:
            yield mock_socket

    @pytest.fixture
    def mock_thread(self):
        # Cria um "substituto" para o threading.Thread (utilizado na criação do objeto de thread)
        with patch("threading.Thread") as mock_thread:
            yield mock_thread


    def test_client_init(self, mock_socket, user_cliente):
        """Teste para verificar a inicialização do User (cliente)"""
        # Cria uma instância do mock_socket
        test_socket = mock_socket.return_value
        # Define o retorno do método connect do objeto mockado (para que ele não tente se conectar)
        test_socket.connect.return_value = None

        user_cliente = User(nome_cliente, timeout=300, endereco=ADDR)

        # Verifica se os atributos do usuário foram inicializados corretamente
        assert user_cliente.nome == nome_cliente
        assert user_cliente.timeout == 300
        assert user_cliente.endereco == ADDR

        # Verifica se os métodos foram chamados com os parâmetros corretos (se o socket foi configurado corretamente)
        test_socket.connect.assert_called_with(ADDR)
        test_socket.settimeout.assert_called_with(300)
        test_socket.send.assert_called_with(nome_cliente.encode())
    
    def test_funcionario_init(self, mock_socket, user_funcionario):
        """Teste para verificar a inicialização do User (funcionario)"""
        # Cria uma instância do mock_socket
        test_socket = mock_socket.return_value
        # Define o retorno do método connect do objeto mockado (para que ele não tente se conectar)
        test_socket.connect.return_value = None

        user_funcionario = User(nome_admin)

        # Verifica se os atributos do usuário foram inicializados corretamente
        assert user_funcionario.nome == nome_admin
        assert user_funcionario.timeout == 0
        assert user_funcionario.endereco == ADDR

        # Verifica se os métodos foram chamados com os parâmetros corretos (se o socket foi configurado corretamente)
        test_socket.connect.assert_called_with(ADDR)
        test_socket.settimeout.assert_not_called()
        test_socket.send.assert_called_with(nome_admin.encode())

    def test_client_escutar_mensagens(self, mock_socket, user_cliente):
        """Teste para verificar a funcionalidade do método escutar_mensagens (Cliente)"""
        # Cria uma instância do mock_socket
        test_socket = mock_socket.return_value

        # Simula os valores que são "retornados" ao utilizar o método receive (recv)
        test_socket.recv.side_effect = [
            "Olá, tudo bem? Bem vindo ao atendimento da DrogaLaugh.".encode(),
            "Qual a sua dúvida? Estou aqui para ajudar.".encode(),
            "Mensagem de teste".encode(),
            socket.timeout,
        ]
        
        user_cliente = User(nome_cliente, 300, ADDR)
        user_cliente.socket_user = test_socket

        with patch("builtins.print") as mock_print:
            user_cliente.escutar_mensagens()
            # Verifica as mensagens recebidas
            mock_print.assert_any_call("\n> Olá, tudo bem? Bem vindo ao atendimento da DrogaLaugh. \n")
            mock_print.assert_any_call("\n> Qual a sua dúvida? Estou aqui para ajudar. \n")
            mock_print.assert_any_call("\n> Mensagem de teste \n")
            mock_print.assert_any_call("\nTimeout de conexão")
            mock_print.assert_any_call("\nFinalizando conexão...")

        # Verifica se o socket foi fechado
        test_socket.close.assert_called_once()

    def test_funcionario_escutar_mensagens(self, mock_socket, user_funcionario):
        """Teste para verificar a funcionalidade do método escutar_mensagens (Funcionario)"""
        # Cria uma instância do mock_socket
        test_socket = mock_socket.return_value

        # Simula os valores que são "retornados" ao utilizar o método receive (recv)
        test_socket.recv.side_effect = [
            "Mensagem de teste".encode(),
            Exception("Erro de teste"),
        ]

        user_funcionario = User(nome_admin)
        user_funcionario.socket_user = test_socket

        with patch("builtins.print") as mock_print:
            user_funcionario.escutar_mensagens()
            # Verifica as mensagens recebidas
            mock_print.assert_any_call("\n> Mensagem de teste \n")
            mock_print.assert_any_call("\nErro ao receber mensagem.")
            mock_print.assert_any_call("\nFinalizando conexão...")

        # Verifica se o socket foi fechado
        test_socket.close.assert_called_once()

    def test_iniciar(self, mock_socket, mock_thread, user_funcionario):
        """Teste para verificar o funcionamento do método iniciar"""
        test_socket = mock_socket.return_value
        test_socket.send.return_value = None

        user_funcionario = User(nome_admin)
        user_funcionario.socket_user = test_socket

        test_thread = mock_thread.return_value
        
        # Mock do input para simular entrada do usuário
        with patch("builtins.input", side_effect=["Mensagem de teste", KeyboardInterrupt]):
            with patch("builtins.print") as mock_print:
                user_funcionario.iniciar()

                test_thread.start.assert_called_once()

                # Verifica se as mensagens foram enviadas
                test_socket.send.assert_any_call("Mensagem de teste".encode())

                # Verifica mensagens de saída
                mock_print.assert_any_call("\nSaindo...")
                mock_print.assert_any_call("\nFinalizando conexão...")

        # Verifica se o socket foi fechado
        test_socket.close.assert_called_once()
