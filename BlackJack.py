import pygame
import sys
import random
import time

def zeichne_hand(screen, hand, pos_x, pos_y):
    abstand = 60  # Abstand zwischen Karten horizontal
    karte_breite, karte_hoehe = 80, 120
    for i, karte in enumerate(hand):
        karte_bild = karte.get_image()
        screen.blit(karte_bild, (pos_x + i * abstand, pos_y))

# Initialisierung
pygame.init()

# Bildschirm erstellen
screen = pygame.display.set_mode((1500, 750))
pygame.display.set_caption("Blackjack")

# Font
FONT = pygame.font.SysFont("Arial", 20)



# Uhr für Framerate
clock = pygame.time.Clock()

# Button-Funktion
class Button:
    def __init__(self, text, x, y, w, h, action=None, active=True):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action
        self.active = active

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        color = (70, 130, 180) if self.active else (120, 120, 120)
        if self.rect.collidepoint(mouse) and self.active:
            color = (100, 160, 210)
        pygame.draw.rect(screen, color, self.rect)
        text_surface = FONT.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.action:
                    self.action()







# Klassen
class Dealer():
    def __init__(self):
        self.__dealer_deck = []
        

    def dealer_karten(self):
        self.__dealer_deck = [karten_ls[1], karten_ls[3]]
        
        karten_ls.pop(1)
        karten_ls.pop(2)
        
        wert = berechne_hand_wert(self.__dealer_deck)
        if wert == 21:
            print("Dealer hat gewonnen")
            sys.exit()
            
    def hitting_dealer(self):
        wert = berechne_hand_wert(self.__dealer_deck)
        if wert < 17:
            self.__dealer_deck.append(karten_ls[0])
            del karten_ls[0]
            return self.hitting_dealer()
            
            
        elif wert > 21:
            print("Dealer verloren")
            return self.__dealer_deck
            
        else:
            return self.__dealer_deck
        
        time.sleep(1)

    def get_dealer_deck(self):
        return self.__dealer_deck


class Spieler():
    def __init__(self, guthaben, einsatz):
        self.__guthaben = guthaben
        self.hands = [[]]
        self.einsatz = einsatz
        self.active_hand_index = 0
        
        
    def spieler_karten(self):
        self.hands = [[karten_ls[0], karten_ls[2]]]
        karten_ls.pop(0)
        karten_ls.pop(1)
        
        wert = berechne_hand_wert(self.hands[0])
        if wert == 21: #visualisierung mit schriftzug 
            print("Spieler hat Blackjack")
            sys.exit()

    def hit(self):
        self.hands[self.active_hand_index].append(karten_ls.pop(0))
        

    def double(self):
        
        if self.einsatz >= self.__guthaben:
            print("Nicht genug Geld")
        else:
            self.__guthaben -= self.einsatz
            self.einsatz *= 2
            self.hit()
                
    def split(self):
        aktuelle_hand = self.hands[self.active_hand_index]
        if len(aktuelle_hand) == 2 and aktuelle_hand[0].get_karten_wert() == aktuelle_hand[1].get_karten_wert(): # ob nur 2 objekte in der hand sind und überprüft ob die beiden karten in gleichen wert 
            if self.einsatz * 2 > self.__guthaben:
                self.__guthaben -= self.einsatz  # zweiter Einsatz
                print("Nicht genügend Guthaben für Split")
                
            karte1 = aktuelle_hand[0]
            karte2 = aktuelle_hand[1]

            #auf beide gesplittene karten flogt eine neue karte
            self.hands[self.active_hand_index] = [karte1, karten_ls.pop(0)]

            # Neue Hand erstellen mit anderer Karte + neue vom Stapel
            neue_hand = [karte2, karten_ls.pop(0)]
            
            self.hands.append(neue_hand)
            
            
            
            
                   
            # noch für jede hand den aktuellen kartenstand angeben 
            for hand_index,hand in enumerate (self.hands):
                wert = berechne_hand_wert(hand)
                print(f"Wert Hand{hand_index}:", self.hands[hand_index][0].get_karten_wert(),self.hands[hand_index][1].get_karten_wert())
                
                if wert > 21:
                    print(f"hand{self.active_hand_index} Verloren")
                    break_loop[0] = True
                    
                elif wert ==21:
                    self.stand()
                    
                
        else:
            print("Split nicht möglich")
            
        
        
    def stand(self):
        if self.active_hand_index + 1 < len(self.hands):
            self.active_hand_index += 1
            print(f"Wechsel zu Hand {self.active_hand_index}")
            return False  # noch Hände offen
        
        else:
            print("Alle Hände gespielt")
           # alle Hände durch           
            dealer_deck = dealer1.hitting_dealer()
            dealer_wert = berechne_hand_wert(dealer_deck)
            
            print("Dealerhand:", [k.get_karten_wert() for k in dealer1.get_dealer_deck()])
            
            
            for hand in spieler1.hands:
                hand_wert = berechne_hand_wert(hand) 
                if hand_wert > dealer_wert and hand_wert <= 21 and dealer_wert <=21:
                    print(f"Hand{self.active_hand_index}: gewonnen")
                    self.__guthaben += 2*self.einsatz
                
                elif hand_wert < dealer_wert and dealer_wert <=21 and hand_wert <=21:
                    print(f"Hand{self.active_hand_index}: verloren")
                    
                elif hand_wert == dealer_wert and hand_wert <=21:
                    print(f"Draw")
                    self.__guthaben += self.einsatz
                    
            return True

class Karte():
    def __init__(self, wert, farbe):
        self.__wert = wert
        self.__farbe = farbe
        self.__image = pygame.transform.smoothscale(pygame.image.load(farbe).convert_alpha(), (80, 120))

    def get_karten_wert(self):
        return self.__wert

    def get_farbe(self):
        return self.__farbe
    
    def get_image(self):
        return self.__image


        
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
    for karten in range(0,4):
        if kartenwert == 10:
            karten_ls.extend([Zehn(Bild[8][karten]), J(Bild[10][karten]), Q(Bild[12][karten]), K(Bild[11][karten]), A(Bild[9][karten])])
        else:
            karte = Karte(kartenwert, Bild[karten_bild][karten])
            karten_ls.append(karte)
    karten_bild += 1

random.shuffle(karten_ls)


# Button-Aktionen


def berechne_hand_wert(hand):
    wert = sum([karte.get_karten_wert() for karte in hand])
    anzahl_asse = sum(1 for karte in hand if isinstance(karte, A))
    
    while wert > 21 and anzahl_asse > 0:
        wert -= 10
        anzahl_asse -= 1

    return wert

def deck_auswertung():
    for idx, hand in enumerate(spieler1.hands):
        wert = berechne_hand_wert(hand)
        print(f"Hand {idx}: {[k.get_karten_wert() for k in hand]}")
        
        if wert > 21:
            if spieler1.active_hand_index+1 == len(spieler1.hands):
                if spieler1.active_hand_index == 0:
                    print(f"Deck Verloren")
                
                else:
                    break_loop[0]
                    
            else:                    
                print(f"Hand{idx} Verloren")
                spieler1.stand()

def hit(): 
    spieler1.hit()
    deck_auswertung()

        
def stand():
    if spieler1.stand():  
        deck_auswertung()
    else:
        print(f"Hand{spieler1.active_hand_index} aktiv")

    


def double():
    if len(spieler1.hands[spieler1.active_hand_index]) == 2:
        spieler1.double()
        deck_auswertung()
        break_loop[0] = True
        
    else:
        print("Doubln nicht möglich")
    
    


def split(): 
    spieler1.split()

# Spielobjekte
dealer1 = Dealer()
spieler1 = Spieler(1000, 100)

dealer1.dealer_karten()
spieler1.spieler_karten()

break_loop = [False]
#auswertung muss auch visualisiert werden 
        
# Spiel-Schleife mit Buttons
buttons = [
    Button("Hit", 100, 500, 100, 40, hit),
    Button("Stand", 210, 500, 100, 40, stand),
    Button("Double", 320, 500, 100, 40, double),
    Button("Split", 430, 500, 100, 40, split)
]



deck_auswertung()
while not break_loop[0]: #Läuft, bis break_loop[0] True wird
    screen.fill((0, 120, 0))

    # Event-Handling zentral
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for btn in buttons:
            btn.handle_event(event)

    # Karten anzeigen
    zeichne_hand(screen, dealer1.get_dealer_deck(), 100, 50)
    for i, hand in enumerate(spieler1.hands):
        zeichne_hand(screen, hand, 100, 300 + i * 100)

    # Buttons zeichnen
    for btn in buttons:
        btn.draw(screen)

    pygame.display.flip()
    clock.tick(30)


# Pygame beenden
time.sleep(1)
pygame.quit()

