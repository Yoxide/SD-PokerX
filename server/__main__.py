import socket
import random
import json
import threading

PORT = 35001
SERVER_ADDRESS = "localhost"

# Baralho
ranks = "23456789TJQKA"
suits = "CDHS"
deck = [f"{rank}-{suit}" for rank in ranks for suit in suits]

# Guardar os jogadores conectados
players = []
community_cards = []

# Baralhar o baralho
def shuffle_deck():
    random.shuffle(deck)

# Dar a mão
def deal_hand():
    return [deck.pop(), deck.pop()]

# Dar as cartas comunitárias
def deal_community_cards():
    return [deck.pop() for _ in range(5)]  # 5 cartas comunitárias

# Coisas do client
def handle_client(connection, address):
    """Lida com uma conecção única
     :param connection: socket connection
     :param address: socket address
     """
    print(f"Player {address} joined!")

    shuffle_deck()
    player_hand = deal_hand()

    # Se for o primeiro jogador, dá as cartas comunitárias
    global community_cards
    if not community_cards:
        community_cards = deal_community_cards()

    # Envia a mão do jogador e as cartas comunitários em JSON
    game_data = {
        "hand": player_hand,
        "community_cards": community_cards
    }
    connection.send(json.dumps(game_data).encode())

    # Esperar pela ação do jogador (em progresso)
    while True:
        data = connection.recv(1024).decode()
        if data.lower() == "quit":
            print(f"Player {address} disconnected.")
            break

    connection.close()
    players.remove(connection)

def main():
    """Corre o servidor para vários jogadores"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(4)  # Até 4 jogadores
    print(f"Waiting for players on port {PORT}...")

    while True:
        connection, address = s.accept()
        players.append(connection)
        threading.Thread(target=handle_client, args=(connection, address), daemon=True).start()

if __name__ == "__main__":
    main()

