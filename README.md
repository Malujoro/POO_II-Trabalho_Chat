# ChatMed: Comunicação Simples e Direta
Um módulo de chat eficiente para farmácias, integrando atendimento ao cliente em tempo real.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Docker](https://img.shields.io/badge/Docker-Compatible-blue)

## Descrição do Projeto
O chat é um módulo do sistema de gerenciamento de farmácias, projetado para facilitar a comunicação direta entre clientes e funcionários. Ele permite que os clientes tirem dúvidas sobre medicamentos, como contraindicações, formas de uso, formas de pagamento, informações de reserva e entrega, dentre outras. 

Através de uma interface amigável, o chat proporciona uma interação eficiente entre clientes e atendentes. O banco de dados do sistema armazena o histórico de mensagens trocadas entre as partes, garantindo que o atendimento seja registrado e possa ser consultado posteriormente, caso necessário. 

Com a integração em tempo real, os atendentes podem fornecer informações atualizadas sobre a disponibilidade de medicamentos e apoiar os clientes durante o processo de compra, incluindo a realização de reservas de medicamentos para retirada física.

## Funcionalidades principais
- Comunicação em tempo real entre clientes e atendentes.
- Suporte para dúvidas sobre medicamentos, como indicações, contraindicações e formas de uso.
- Ajuda na realização de reservas de medicamentos.
- Armazenamento do histórico de mensagens no banco de dados.
- Possibilidade de consultar a disponibilidade de produtos diretamente durante o chat.
- Horário de atendimento: das 6h às 22h.

## Instalação e configuração
### Pré-requisitos
* Python 3.12 ou superior
* Docker e Docker Compose instalados
* Acesso à internet para clonar o repositório e instalar dependências

### Passos para configurar
1. Clone o repositório:

```bash
git clone https://github.com/Malujoro/POO_II-Trabalho_Final.git
cd POO_II-Trabalho_Final
```
2. Crie o ambiente virtual e instale as dependencias:
```bash
python -m venv chatMed
source chatMed/bin/activate
pip install -r requirements.txt
```
3. Ative o docker compose
```bash
sudo docker compose up
```
4. Rode o script.py
```bash
python script.py
``` 

## Contribuidores
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/149737667?v=4" width=115><br><sub>Alef Cauan Sousa Rodrigues</sub>](https://github.com/alefCauan) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/157396271?v=4" width=115><br><sub>Áurea Letícia Carvalho Macedo</sub>](https://github.com/aureamcd) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/110724864?v=4" width=115><br><sub>Gabriel Alves de Freitas</sub>](https://github.com/gabreudev) |
| :---: | :---: | :---: |
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/157633101?v=4" width=115><br><sub>Márcio Roberto de Brito Rodrigues</sub>](https://github.com/MarcioRobt0) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/45736178?v=4" width=115><br><sub>Mateus da Rocha Sousa</sub>](https://github.com/Malujoro) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/77069795?v=4" width=115><br><sub>Viviany da Silva Araújo</sub>](https://github.com/VivySilva) |



