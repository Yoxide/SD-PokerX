import pygame
from client.stub import interface as processar, INT_SIZE
from client.stub import OK_OP, CON_OP, HAND_OP, NAME_OP
from time import sleep

CARD_WIDTH, CARD_HEIGHT = 55, 80
WIDTH, HEIGHT = 1050, 590
GREEN = (34, 139, 34)

class User:
    def __init__(self, inter: processar):
        self.processar = inter
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Texas Hold'em Poker")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player_name = ""
        self.player_number = -1
        self.current_chips = 100

        self.opponent_name = "Oponente"
        self.opponent_chips = 100

        self.turn = 0

        self.load_assets()

    def resize_with_aspect_ratio(self, image, max_width, max_height):
        original_width, original_height = image.get_size()
        ratio = min(max_width / original_width, max_height / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        return pygame.transform.smoothscale(image, new_size)

    def load_assets(self):
        self.card_images = {
            f"{rank}-{suit}": pygame.transform.smoothscale(
                pygame.image.load(f"cards/{rank}-{suit}.png"),
                (CARD_WIDTH, CARD_HEIGHT))
            for rank in "23456789TJQKA" for suit in "CDHS"
        }

        def load_full(path):
            return pygame.image.load(path).convert_alpha()

        self.background = self.resize_with_aspect_ratio(load_full("UI/background.png"), WIDTH, HEIGHT)
        self.jogador1 = self.resize_with_aspect_ratio(load_full("UI/jogador1.png"), 975, 765)
        self.fichas = self.resize_with_aspect_ratio(load_full("UI/fichas.png"), 200, 200)
        self.caixa1 = self.resize_with_aspect_ratio(load_full("UI/caixinhas.png"), 900, 900)
        self.caixa2 = self.resize_with_aspect_ratio(load_full("UI/caixinhas.png"), 900, 900)

        self.btn_apostar = self.resize_with_aspect_ratio(load_full("UI/apostar.png"), 130, 60)
        self.btn_passar = self.resize_with_aspect_ratio(load_full("UI/passar.png"), 130, 60)
        self.btn_desistir = self.resize_with_aspect_ratio(load_full("UI/desistir.png"), 130, 60)

        self.font = pygame.font.SysFont("Arial", 20)

    def draw_cards(self, hand, community_cards):
        self.screen.blit(self.card_images[hand[0]], (340, 290))
        self.screen.blit(self.card_images[hand[1]], (410, 290))
        for i, card in enumerate(community_cards):
            self.screen.blit(self.card_images[card], (380 + i * 70, 130))

    def display_gui(self, hand, community_cards, message=""):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.jogador1, (-85, 180))
        self.screen.blit(self.fichas, (300, 335))
        self.screen.blit(self.caixa1, (-300, 150))
        self.screen.blit(self.caixa2, (500, 150))

        self.apostar_rect = self.screen.blit(self.btn_apostar, (350, 25))
        self.passar_rect = self.screen.blit(self.btn_passar, (500, 25))
        self.desistir_rect = self.screen.blit(self.btn_desistir, (650, 25))

        self.draw_cards(hand, community_cards)

        if message:
            text = self.font.render(message, True, (0, 0, 0))
            self.screen.blit(text, (WIDTH // 2 - 100, 220))

        # Player's name and chips
        if self.player_name:
            name_text = self.font.render(self.player_name, True, (255, 255, 255))
            chips_text = self.font.render(f"Fichas:{self.current_chips}", True, (255, 255, 255))
            if self.player_number == 0:
                self.screen.blit(name_text, (110, 375))
                self.screen.blit(chips_text, (110, 407))
            else:
                self.screen.blit(name_text, (911, 375))
                self.screen.blit(chips_text, (911, 407))

        # Opponent's name and chips
        opp_name_text = self.font.render(self.opponent_name, True, (255, 255, 255))
        opp_chips_text = self.font.render(f"Fichas:{self.opponent_chips}", True, (255, 255, 255))
        if self.player_number == 0:
            self.screen.blit(opp_name_text, (911, 375))
            self.screen.blit(opp_chips_text, (911, 407))
        else:
            self.screen.blit(opp_name_text, (110, 375))
            self.screen.blit(opp_chips_text, (110, 407))

        pygame.display.flip()

    def get_action_click(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.apostar_rect.collidepoint(x, y):
                        return 1
                    elif self.passar_rect.collidepoint(x, y):
                        return 3
                    elif self.desistir_rect.collidepoint(x, y):
                        return 2

            pygame.display.flip()
            self.clock.tick(30)

    def bet_value(self):
        return 20  # Can be made dynamic if needed

    def get_name_input(self):
        name = ""
        input_active = True
        input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
        input_color = pygame.Color('lightskyblue3')

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return ""
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 12:
                            name += event.unicode

            self.screen.blit(self.background, (0, 0))
            pygame.draw.rect(self.screen, input_color, input_box, 2)
            txt_surface = self.font.render("Nome: " + name, True, (255, 255, 255))
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.display.flip()
            self.clock.tick(30)

        return name

    def exec(self):
        self.processar.send_str(CON_OP)
        self.player_number = self.processar.receive_int(INT_SIZE)
        self.processar.send_str(HAND_OP)
        hand = self.processar.receive_object()

        pygame.mixer.music.load("sounds/cake.mp3")
        pygame.mixer.music.play()
        self.processar.send_str(NAME_OP)
        self.player_name = self.get_name_input()
        self.processar.send_str(self.player_name)

        pygame.mixer.music.unload()

        pygame.mixer.music.load("sounds/whirlwind.mp3")
        pygame.mixer.music.play(loops=-1)

        self.current_chips = self.processar.receive_int(INT_SIZE)

        community_cards = []
        while self.running:
            if self.turn > 0:
                #self.opponent_name = self.processar.get_opponent_name()
                self.opponent_chips = self.processar.get_opponent_chips()

            self.processar.send_str(OK_OP)
            res = self.processar.receive_int(INT_SIZE)

            if res == 1:
                community_cards = self.processar.receive_object()
                self.display_gui(hand, community_cards, "É a tua vez!")

                option = self.get_action_click()
                if option is None:
                    break

                match option:
                    case 1:
                        b_value = self.bet_value()
                        res = self.processar.bet(b_value)
                        self.current_chips = self.processar.receive_int(INT_SIZE)
                        if self.turn > 0:
                            self.opponent_chips = self.processar.get_opponent_chips()
                        self.display_gui(hand, community_cards, f"Apostaste {res} fichas!")
                        self.turn += 1
                        print(self.turn)
                    case 2:
                        self.processar.fold()
                        self.display_gui(hand, community_cards, "Desististe!")
                        self.turn += 1
                    case 3:
                        self.processar.pass_turn()
                        self.display_gui(hand, community_cards, "Passaste!")
                        self.turn += 1
            elif res == 2:
                result = self.processar.receive_str(100)
                self.display_gui(hand, community_cards, result)
                sleep(3)
                break
            else:
                sleep(1)

        pygame.mixer.music.stop()
        pygame.quit()