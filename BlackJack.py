import pygame
import sys
import random

# Initialisierung
pygame.init()

# Bildschirm erstellen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Blackjack")

# Font
FONT = pygame.font.SysFont("Arial", 20)

# Karte zum Testen anzeigen
card = pygame.image.load(r"cards/ace_of_spades.png")
card = pygame.transform.scale(card, (100, 150))  # Größe anpassen

# Uhr für Framerate
clock = pygame.time.Clock()

# Button-Funktion
def button(text, x, y, w, h, screen, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    color = (70, 130, 180)
    if rect.collidepoint(mouse):
        color = (100, 160, 210)
        if click[0] == 1 and action:
            pygame.time.delay(200)
            action()
    pygame.draw.rect(screen, color, rect)
    text_surface = FONT.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + 10, y + 10))


# Klassen
class Dealer():
    def __init__(self):
        self.__dealer_deck = []

    def dealer_karten(self, liste: list):
        self.__dealer_deck = [liste[1], liste[3]]
        print(self.__dealer_deck[0].get_karten_wert())
        if sum([k.get_karten_wert() for k in self.__dealer_deck]) == 21:
            print("Dealer hat gewonnen")

    def hitting_dealer(self, liste: list, spieler):
        gesamtwert = sum([karte.get_karten_wert() for karte in self.__dealer_deck])
        if gesamtwert < 17:
            self.__dealer_deck.append(liste[0])
            del liste[0]
            self.hitting_dealer(liste, spieler)
        elif gesamtwert > 21:
            print("Dealer verloren")
        return self.__dealer_deck

    def get_dealer_deck(self):
        return self.__dealer_deck


class Spieler():
    def __init__(self, guthaben, einsatz):
        self.__guthaben = guthaben
        self.spieler_deck = []
        self.einsatz = einsatz
        self.hand1 = []
        self.hand2 = []

    def spieler_karten(self, liste: list):
        self.spieler_deck = [liste[0], liste[2]]
        if sum([k.get_karten_wert() for k in self.spieler_deck]) == 21:
            print("Spieler hat Blackjack")
            sys.exit()

    def hit(self, liste: list):
        self.spieler_deck.append(liste[0])
        del liste[0]

    def double(self, liste: list):
        if self.einsatz >= self.__guthaben:
            print("Nicht genug Geld")
        else:
            self.einsatz *= 2
            self.hit(liste)

    def split(self, liste: list):
        if self.spieler_deck[0].get_karten_wert() == self.spieler_deck[1].get_karten_wert():
            if self.einsatz * 2 > self.__guthaben:
                print("Nicht genügend Guthaben für Split")
                return
            self.__guthaben -= self.einsatz
            self.hand1.append(self.spieler_deck[0])
            self.hand2.append(self.spieler_deck[1])
            print("Split durchgeführt")
        else:
            print("Split nicht möglich")

    def stand(self):
        return self.spieler_deck


class Karte():
    def __init__(self, wert, farbe):
        self.__wert = wert
        self.__farbe = farbe

    def get_karten_wert(self):
        return self.__wert

    def get_farbe(self):
        return self.__farbe
        
class Zehn(Karte):
    def __init__(self, farbe): 
        super().__init__(10, farbe)


class J(Karte):
    def __init__(self, farbe): 
        super().__init__(10, farbe)


class Q(Karte):
    def __init__(self, farbe): 
        super().__init__(10, farbe)


class K(Karte):
    def __init__(self, farbe): 
        super().__init__(10, farbe)


class A(Karte):
    def __init__(self, farbe): 
        super().__init__(11, farbe)


# Karten erstellen
karten_ls = []
Bild = [["cards/2_of_clubs.png","cards/2_of_diamonds.png","cards/2_of_hearts.png","cards/2_of_spades.png"],
        ["cards/3_of_clubs.png","cards/3_of_diamonds.png","cards/3_of_hearts.png","cards/3_of_spades.png"],
        ["cards/4_of_clubs.png","cards/4_of_diamonds.png","cards/4_of_hearts.png","cards/4_of_spades.png"],
        ["cards/5_of_clubs.png","cards/5_of_diamonds.png","cards/5_of_hearts.png","cards/5_of_spades.png"],
        ["cards/6_of_clubs.png","cards/6_of_diamonds.png","cards/6_of_hearts.png","cards/6_of_spades.png"],
        ["cards/7_of_clubs.png","cards/7_of_diamonds.png","cards/7_of_hearts.png","cards/7_of_spades.png"],
        ["cards/8_of_clubs.png","cards/8_of_diamonds.png","cards/8_of_hearts.png","cards/8_of_spades.png"],
        ["cards/9_of_clubs.png","cards/9_of_diamonds.png","cards/9_of_hearts.png","cards/9_of_spades.png"],
        ["cards/10_of_clubs.png","cards/10_of_diamonds.png","cards/10_of_hearts.png","cards/10_of_spades.png"],
        ["cards/ace_of_clubs.png","cards/ace_of_diamonds.png","cards/ace_of_hearts.png","cards/ace_of_spades.png"],
        ["cards/jack_of_clubs.png","cards/jack_of_diamonds.png","cards/jack_of_hearts.png","cards/jack_of_spades.png"],
        ["cards/king_of_clubs.png","cards/king_of_diamonds.png","cards/king_of_hearts.png","cards/king_of_spades.png"],
        ["cards/queen_of_clubs.png","cards/queen_of_diamonds.png","cards/queen_of_hearts.png","cards/queen_of_spades.png"]]

karten_bild = 0

for kartenwert in range(2, 11):
    for karten in range(4):
        if kartenwert == 10:
            karten_ls.extend([Zehn(Bild[8][karten]), J(Bild[10][karten]), Q(Bild[12][karten]), K(Bild[11][karten]), A(Bild[9][karten])])
        else:
            karte = Karte(kartenwert, Bild[karten_bild][karten])
            karten_ls.append(karte)
    karten_bild += 1

random.shuffle(karten_ls)

# Spielobjekte
dealer1 = Dealer()
spieler1 = Spieler(1000, 100)

dealer1.dealer_karten(karten_ls)
spieler1.spieler_karten(karten_ls)
print("Spielerhand:", [k.get_karten_wert() for k in spieler1.spieler_deck])

# Button-Aktionen
break_loop = [False]

def hit(): 
    spieler1.hit(karten_ls)
    print("Spielerhand:", [k.get_karten_wert() for k in spieler1.spieler_deck])
    if sum([k.get_karten_wert() for k in spieler1.spieler_deck]) > 21:
        print("Verloren")
        break_loop[0] = True

def stand(): 
    print("Spieler steht")
    break_loop[0] = True

def double(): 
    spieler1.double(karten_ls)
    print("Double ausgeführt")
    break_loop[0] = True

def split(): 
    spieler1.split(karten_ls)

# Spiel-Schleife mit Buttons
while not break_loop[0]:
    screen.fill((0, 120, 0))

    button("Hit", 100, 500, 100, 40, screen, hit)
    button("Stand", 210, 500, 100, 40, screen, stand)
    button("Double", 320, 500, 100, 40, screen, double)
    button("Split", 430, 500, 100, 40, screen, split)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(30)

# Nach Stand oder Verlust → Dealer spielt
dealer1.hitting_dealer(karten_ls, spieler1)
print("Dealerhand:", [k.get_karten_wert() for k in dealer1.get_dealer_deck()])

# Pygame beenden

pygame.quit()
sys.exit()
