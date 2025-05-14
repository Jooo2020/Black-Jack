import pygame
import random
import sys

# Initialisierung
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# Farben & Schrift
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
FONT = pygame.font.SysFont('arial', 28)

# Kartendeck
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
CARDS = list(CARD_VALUES.keys()) * 4

# Karten ziehen
def draw_card(deck):
    return deck.pop(random.randint(0, len(deck)-1))

# Punkte zählen
def count_hand(hand):
    value = sum(CARD_VALUES[card] for card in hand)
    aces = hand.count('A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Anzeigen
def draw_text(text, x, y):
    render = FONT.render(text, True, WHITE)
    WIN.blit(render, (x, y))

def draw_game(player_hand, dealer_hand, status):
    WIN.fill(GREEN)
    draw_text("Dealer: " + " ".join(dealer_hand), 50, 50)
    draw_text("Spieler: " + " ".join(player_hand), 50, 150)
    draw_text("Status: " + status, 50, 300)
    pygame.display.flip()

# Hauptspiel
def main():
    deck = CARDS[:]
    random.shuffle(deck)

    player_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]
    status = ""

    running = True
    player_turn = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Tastensteuerung
            if event.type == pygame.KEYDOWN:
                if player_turn:
                    if event.key == pygame.K_h:  # Hit
                        player_hand.append(draw_card(deck))
                        if count_hand(player_hand) > 21:
                            status = "Bust! Dealer gewinnt."
                            player_turn = False
                    elif event.key == pygame.K_s:  # Stand
                        player_turn = False

        if not player_turn and not status:
            while count_hand(dealer_hand) < 17:
                dealer_hand.append(draw_card(deck))

            player_score = count_hand(player_hand)
            dealer_score = count_hand(dealer_hand)

            if dealer_score > 21 or player_score > dealer_score:
                status = "Spieler gewinnt!"
            elif dealer_score == player_score:
                status = "Unentschieden."
            else:
                status = "Dealer gewinnt."

        draw_game(player_hand, dealer_hand if not player_turn else [dealer_hand[0], '?'], status)

# Start
if __name__ == "__main__":
    main()
