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
        self.hands = [[]]
        self.einsatz = einsatz
        self.active_hand_index = 0
        
    def spieler_karten(self, liste: list):
        self.hands = [[liste[0], liste[2]]]
        print(self.hands)
        
        for hand in self.hands:
            if sum([k.get_karten_wert() for k in hand]) == 21: #visualisierung mit schriftzug 
                print("Spieler hat Blackjack")

    def hit(self, liste: list):
        self.hands[self.active_hand_index].append(liste.pop(0))


    def double(self, liste: list):
        
        if self.einsatz >= self.__guthaben:
            print("Nicht genug Geld")
        else:
            self.__guthaben -= self.einsatz
            self.einsatz *= 2
            self.hit(liste)
                
    def split(self,liste:list):
        aktuelle_hand = self.hands[self.active_hand_index]
        if len(aktuelle_hand) == 2 and aktuelle_hand[0].get_karten_wert() == aktuelle_hand[1].get_karten_wert(): # ob nur 2 objekte in der hand sind und überprüft ob die beiden karten in gleichen wert 
            if self.einsatz * 2 > self.__guthaben:
                self.__guthaben -= self.einsatz  # zweiter Einsatz
                print("Nicht genügend Guthaben für Split")
                
            karte1 = aktuelle_hand[0]
            karte2 = aktuelle_hand[1]

            self.hands[self.active_hand_index] = [karte1, liste.pop(0)]

            # Neue Hand erstellen mit anderer Karte + neue vom Stapel
            neue_hand = [karte2, liste.pop(0)]
            self.hands.append(neue_hand)
            
            buttons = [["Hit", 100, 500, 100, 40, screen, self.split_hit(liste)],
                    ["Stand", 210, 500, 100, 40, screen, self.stand],
                    ["Double", 320, 500, 100, 40, screen, self.double(liste)],
                    ["Hit", 430, 500, 100, 40, lambda: self.split_hit(liste)]]
            
            for knopf in buttons:
                button( *knopf)
            
            # noch für jede hand den aktuellen kartenstand angeben 
            for hand in self.hands:
                wert = sum([karte.get_karten_wert() for karte in hand])
                print(f"Wert Hand{self.active_hand_index}:", wert)

                if wert > 21:
                    print(f"hand{self.active_hand_index} Verloren")
                    break_loop[0] = True
                    
                elif spieler1.stand():
                    break_loop[0] = True
                
        else:
            print("Split nicht möglich")
            
            
    def split_hit(self,liste:list):
        self.hands.append(liste[0])
        del liste[0]
        
        
    def stand(self):
        if self.active_hand_index + 1 < len(self.hands):
            self.active_hand_index += 1
            print(f"Wechsel zu Hand {self.active_hand_index}")
            return False  # noch Hände offen
        else:
            print("Alle Hände gespielt")
            return True  # alle Hände durch


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

for kartenwert in range(10, 11):
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

for hand in spieler1.hands:
    karte = [k.get_karten_wert() for k in hand]
print("Spielerhand:", karte)
    

# Button-Aktionen
break_loop = [False]
#Auswertung muss auch visualisiert werden 
def auswertung():
    for hand in spieler1.hands:
        karte = [k.get_karten_wert() for k in hand]
        print("Spielerhand: ", karte)
        
        if sum([k.get_karten_wert() for k in hand]) > 21:
            print("Verloren")
            break_loop[0] = True

def hit(): 
    spieler1.hit(karten_ls)
    deck =[]
    print(spieler1.hands)
    auswertung()

        
def stand(): 
    if spieler1.stand():
        auswertung()
        break_loop[0] = True
    else:
        print("Nächste Hand aktiv")

    


def double():
    if len(spieler1.hands[spieler1.active_hand_index]) == 2:
        spieler1.double(karten_ls)
        auswertung()
        break_loop[0] = True
        
    else:
        print("Doubln nicht möglich")
    
    


def split(): 
    spieler1.split(karten_ls)

        
        
# Spiel-Schleife mit Buttons
buttons = [["Hit", 100, 500, 100, 40, screen, hit],
        ["Stand", 210, 500, 100, 40, screen, stand],
        ["Double", 320, 500, 100, 40, screen, double],
        ["Split", 430, 500, 100, 40, screen, split]]

for knopf in buttons:
        button( *knopf)


while not break_loop[0]:
    screen.fill((0, 120, 0))  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Buttons zeichnen und Aktionen prüfen
    for knopf in buttons:
        button(*knopf)
    pygame.display.flip()
    clock.tick(30)


# Nach Stand oder Verlust → Dealer spielt
dealer1.hitting_dealer(karten_ls, spieler1)
print("Dealerhand:", [k.get_karten_wert() for k in dealer1.get_dealer_deck()])

# Pygame beenden

pygame.quit()
sys.exit()
