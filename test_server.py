import pytest
from unittest.mock import MagicMock, patch
import server
from variaveis import *


class TestServer:

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

    @pytest.mark.parametrize("usuarios", [
        ({nome_admin: MagicMock(), nome_cliente: MagicMock()}),
        ({nome_admin: MagicMock()}),
    ])
    def test_encaminhar_mensagem_funcionario(self, usuarios):
        """Teste para verificar o funcionamento do método encaminhar_mensagem (Funcionario)"""
        if(nome_admin in usuarios.keys()):
            mensagem = "Mensagem de teste"
            user_socket = usuarios[nome_admin]
            user_socket.recv.side_effect = [
                mensagem.encode(),
                "".encode(),
            ]
            
            with patch("builtins.print") as mock_print:
                server.encaminhar_mensagem(usuarios, user_socket, nome_admin)

                mock_print.assert_any_call(f"\n{nome_admin} conectado.")
                mock_print.assert_any_call(f"\n{nome_admin} desconectado.")

            if(nome_cliente in usuarios.keys()):
                usuarios[nome_cliente].send.assert_any_call(mensagem.encode())
                mock_print.assert_any_call(f"\n{nome_admin}: {mensagem}")

                
            user_socket.close.assert_called_once()
    

    @pytest.mark.parametrize("usuarios", [
        ({nome_admin: MagicMock(), nome_cliente: MagicMock()}),
        ({nome_cliente: MagicMock()}),
    ])
    def test_encaminhar_mensagem_cliente(self, usuarios):
        """Teste para verificar o funcionamento do método encaminhar_mensagem (Cliente)"""
        if(nome_cliente in usuarios.keys()):
            mensagem = "Mensagem de teste"
            user_socket = usuarios[nome_cliente]
            user_socket.recv.side_effect = [
                mensagem.encode(),
                "".encode(),
            ]

            user_socket.send.return_value = None
            
            with patch("builtins.print") as mock_print:
                server.encaminhar_mensagem(usuarios, user_socket, nome_cliente)

                mock_print.assert_any_call(f"\n{nome_cliente} conectado.")
                user_socket.send.assert_any_call("Olá, tudo bem? Bem vindo ao atendimento da DrogaLaugh.".encode())
                user_socket.send.assert_any_call("Qual a sua dúvida? Estou aqui para ajudar.".encode())

                mock_print.assert_any_call(f"\n{nome_cliente} desconectado.")

                if(nome_admin in usuarios.keys()):
                    usuarios[nome_admin].send.assert_any_call(f"{nome_cliente} se conectou".encode())
                    usuarios[nome_admin].send.assert_any_call(f"{nome_cliente} desconectou".encode())
                    usuarios[nome_admin].send.assert_any_call(mensagem.encode())
                    mock_print.assert_any_call(f"\n{nome_cliente}: {mensagem}")


    
    @pytest.mark.parametrize("nome_usuario", [
        (nome_admin),
        (nome_cliente),
    ])
    def test_iniciar_servidor(self, mock_socket, mock_thread, nome_usuario):
        """Teste para verificar o funcionamento do método iniciar_servidor"""
        usuarios = {}
        user_socket = MagicMock()
        user_socket.recv.return_value = nome_usuario.encode()

        server_socket = mock_socket.return_value
        server_socket.accept.side_effect = [
            (user_socket, None),
            KeyboardInterrupt,
        ]

        test_thread = mock_thread.return_value
        test_thread.start.return_value = None


        with patch("builtins.print") as mock_print:
            server.iniciar_servidor(usuarios)

            server_socket.bind.assert_called_with(ADDR)
            server_socket.listen.assert_called_with(total_usuarios)
            mock_print.assert_any_call(f"Servidor rodando na porta {PORT}")
            
            assert nome_usuario in usuarios.keys()
            test_thread.start.assert_called_once()

            mock_print.assert_any_call("\nFinalizando servidor...")

        # Verifica se o socket foi fechado
        server_socket.close.assert_called_once()