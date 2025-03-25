import pygame
import socket
import json

pygame.init()

WIDTH, HEIGHT = 800, 600
GREEN = (34, 139, 34)
CARD_WIDTH, CARD_HEIGHT = 100, 150

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texas Hold'em Poker")

# Conectar ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 35001))

# Receber dados jogo (mão + cartas comunitárias)
data = client.recv(1024).decode()
game_data = json.loads(data)

player_hand = game_data["hand"]
community_cards = game_data["community_cards"]

# Carregar as imagens das cartas e meter no tamanho pretendido
card_images = {f"{rank}-{suit}": pygame.transform.scale(
    pygame.image.load(f"cards/{rank}-{suit}.png"), (CARD_WIDTH, CARD_HEIGHT))
    for rank in "23456789TJQKA" for suit in "CDHS"}

running = True
while running:
    screen.fill(GREEN)

    # Dar as cartas do jogador
    screen.blit(card_images[player_hand[0]], (100, 400))
    screen.blit(card_images[player_hand[1]], (200, 400))

    # Dar as cartas comunitárias
    for i, card in enumerate(community_cards):
        screen.blit(card_images[card], (250 + i * 110, 200))  # Meter as cartas no meio

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

client.send("quit".encode())  # Notifica o servidor antes de sair
pygame.quit()
client.close()
