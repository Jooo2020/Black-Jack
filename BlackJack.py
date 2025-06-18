#Bibliothek importieren
import pygame
import sys
import random

"""
Blackjack-Spiel mit Pygame

Implementierung eines simplen Blackjack-Spiels mit folgenden Features:
- Kartendeck mit Bilddarstellung (inkl. Kartenwerte und -farben)
- Spieler- und Dealer-Klassen mit Spielmechanik (Hit, Stand, Double, Split)
- Button-Interface zur Steuerung (Hit, Stand, Double, Split, Restart)
- Spiel-Logik für Blackjack-Regeln, inklusive As-Wert-Anpassung
- Grafische Ausgabe der Karten und Statusmeldungen mit Pygame

Klassen:
- Button: GUI-Element zur Interaktion mit Maus
- Dealer: Repräsentiert den Dealer mit Kartenhand und Zieh-Logik
- Spieler: Repräsentiert den Spieler mit mehreren Händen, Einsatz und Spielaktionen
- Karte (+ Unterklassen Zehn, J, Q, K, A): Modelliert einzelne Spielkarten mit Bild und Wert

Wichtige Funktionen:
- berechne_hand_wert(hand): Ermittelt Wert einer Kartenhand mit Berücksichtigung von Assen
- deck_auswertung(): Wertauswertung und Statusupdate der aktuellen Hand
- run_me(): Hauptspielfunktion mit Pygame-Initialisierung, Spielstart und Hauptschleife

Benötigte Ressourcen:
- Kartenbilder im Ordner "cards" mit Benennung wie "2_of_clubs.png", "ace_of_spades.png" etc.
- Rückseite der Karte als "backside.png"

Startet das Spiel in einem Pygame-Fenster (1500x750 px).
"""


# Button Klasse (Johannes)
class Button:
    def __init__(self, text, x, y, w, h, action=None, active=True): #übergabe Parameter (text = Text,x,y = positionierung, w,h = Dimensionen,action = none falls ein Button keine funktion übergibt, active = ob button gedrükt werden kann oder nicht)
        self.text = text
        self.rect = pygame.Rect(x, y, w, h) #
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
        self.__dealer_deck = [karten_ls[1], karten_ls[3]] #gitb dem Dealer die 2te und 4te Karte 
        
        karten_ls.pop(1) 
        karten_ls.pop(2) 
        
        wert = berechne_hand_wert(self.__dealer_deck) # funktion welche den Wert der Hand zurückgibt
        
        if wert == 21: 
            set_status_message("Dealer hat gewonnen")
            spieler1.spieler_karten()
            stand()

    def hitting_dealer(self): #Wenn spieler alle seine Hände gespielt hat wird diese Methode aufgerufen um die Dealer hand zu vervolsständigen 
        wert = berechne_hand_wert(self.__dealer_deck) 
        restart_button.active = True
        if wert < 17:
            self.__dealer_deck.append(karten_ls.pop(0))
            return self.hitting_dealer() 

        elif wert > 21: #wenn wert >21 hat der Spieler gewonnen falls seine Hand auch nicht über 21 hat 
            set_status_message("Spieler hat gewonnen")
            return self.__dealer_deck

        else:
            
            return self.__dealer_deck
        
        
            

    def get_dealer_deck(self):
        return self.__dealer_deck

class Spieler():
    def __init__(self, guthaben, einsatz):
        self.__guthaben = guthaben #guthaben noch nicht eingebaut(keine funktion) für erweiterung 
        self.hands = []
        self.einsatz = einsatz #einsatz noch nicht eingebaut(keine funktion) für erweiterung
        self.active_hand_index = 0
        
        
    def spieler_karten(self):
        self.hands = [[karten_ls[0], karten_ls[2]]] #spieler bekommt 1. und 3. Karte
        karten_ls.pop(0)
        karten_ls.pop(1)
        
        wert = berechne_hand_wert(self.hands[0])
        if wert == 21: 
            stand()  # Ruft implizit stand() und deaktiviert Buttons



    def hit(self):
        self.hands[self.active_hand_index].append(karten_ls.pop(0)) #an der activen Hand(falls gesplittet) wird eine neue Karte hinzugefügt
        

    def double(self):
        if self.einsatz >= self.__guthaben: #falls einsatz hinzugefügt wird
            print("Nicht genug Geld")
        else:
            self.__guthaben -= self.einsatz #falls einsatz hinzugefügt wird
            self.einsatz *= 2 #falls einsatz hinzugefügt wird
            hit()
            stand()
            
        
            
        

    def split(self):
        aktuelle_hand = self.hands[self.active_hand_index]
        if len(aktuelle_hand) == 2 and aktuelle_hand[0].get_karten_wert() == aktuelle_hand[1].get_karten_wert():
            if self.einsatz * 2 > self.__guthaben:
                print("Nicht genügend Guthaben für Split")
            
            else: 
                karte1 = aktuelle_hand[0]
                karte2 = aktuelle_hand[1]

                # Auf beide gesplittene karten folgt eine neue karte
                self.hands[self.active_hand_index] = [karte1, karten_ls.pop(0)]

                # Neue Hand erstellen mit anderer Karte + neue vom Stapel
                neue_hand = [karte2, karten_ls.pop(0)]

                self.hands.append(neue_hand)
                self.active_hand_index = 0
                
                # noch für jede hand den aktuellen kartenstand angeben 
                for hand_index,hand in enumerate(self.hands):
                    wert = berechne_hand_wert(hand)
                    print(f"Wert Hand{hand_index}:", self.hands[hand_index][0].get_karten_wert(), self.hands[hand_index][1].get_karten_wert())

                    if wert > 21:
                        set_status_message(f"hand{self.active_hand_index} Verloren")
                        
                    elif wert == 21:
                        stand()
                        
        else:
            print("Split nicht möglich")

    def stand(self):
        global dealer_zeigt_zweite_karte,buttons

        if self.active_hand_index + 1 < len(self.hands): #der index ist kleiner als die länge der Hand 
            self.active_hand_index += 1
            print(f"Wechsel zu Hand {self.active_hand_index}")
            return False  # noch Hände offen
        
        else:
             
            dealer_zeigt_zweite_karte  =True 
            for btn in buttons:
                btn.active = False
            
            print("Alle Hände gespielt")
        # alle Hände durch
        
        #Ausführung der Auswertung 
        
            dealer_deck = dealer1.hitting_dealer()
            dealer_wert = berechne_hand_wert(dealer_deck)
            
            print("Dealerhand:", [k.get_karten_wert() for k in dealer1.get_dealer_deck()])#gibt die Karten des dealers aus
            
            #durchlauf jeder hand zum vergleich mit der Dealer Hand 
            for hand in self.hands:
                hand_wert = berechne_hand_wert(hand) 
                if hand_wert <21:
                    
                    if hand_wert > dealer_wert and dealer_wert>21:
                        set_status_message(f"Hand{self.active_hand_index}: Gewonnen")
                        self.__guthaben += 2*self.einsatz #noch keine funktion 
                    
                    elif hand_wert < dealer_wert and dealer_wert<= 21:
                        set_status_message(f"Hand{self.active_hand_index}: Verloren")
                        
                        
                    elif hand_wert == dealer_wert:
                        set_status_message(f"Hand{self.active_hand_index}: Draw")
                        self.__guthaben += self.einsatz #guthaben noch keine funktion 
                        
                elif hand_wert ==21 and len(self.hands) == 1:
                    set_status_message("Spieler hat Blackjack")
                        
                else:
                    deck_auswertung(False)    
                    
                                    
                    
                                        
            restart_button.active = True
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



# Button-Aktionen
def berechne_hand_wert(hand):
    wert = sum([karte.get_karten_wert() for karte in hand]) #listkomprehension für den Wert des decks
    anzahl_asse = sum(1 for karte in hand if isinstance(karte, A)) # Objektorientierte Typüberprüfung

    while wert > 21 and anzahl_asse > 0:
        wert -= 10
        anzahl_asse -= 1
    
    return wert


def deck_auswertung(active = True):
    global anzeige_wert

    print(f"Hand {spieler1.active_hand_index}: {[k.get_karten_wert() for k in spieler1.hands[spieler1.active_hand_index]]}") # zeigt kartenwert des Spielers an
        
    wert = berechne_hand_wert(spieler1.hands[spieler1.active_hand_index])
    anzeige_wert= f"Hand{spieler1.active_hand_index}: {wert}"

    if wert > 21:
        
        set_status_message(f"Hand{spieler1.active_hand_index} Verloren")
            
        if active == True:
            spieler1.stand()
        
                
                        
                

def hit(): 
    spieler1.hit()
    deck_auswertung()

        
def stand():
    global buttons
    if spieler1.stand():  
        deck_auswertung()
    else:
        print(f"Hand{spieler1.active_hand_index} aktiv")

def double():
    if len(spieler1.hands[spieler1.active_hand_index]) == 2:
        spieler1.double()
        deck_auswertung()

            
        
        
    else:
        print("Doubln nicht möglich")

def split(): 
    spieler1.split()
    deck_auswertung()

def set_status_message(text):
    global status_message
    status_message = text

def restart_game():
    global spieler1, dealer1, karten_ls, break_loop, dealer_zeigt_zweite_karte,status_message
    status_message = ""
    spieler1.active_hand_index =0
    break_loop[0] = True
    print("Spiel wurde neu gestartet")
    run_me()





#Darstellung für die Karten(Philip)
def zeichne_hand(screen, hand, pos_x, pos_y):
    abstand = 60  # Abstand zwischen Karten horizontal
    karte_breite, karte_hoehe = 80, 120
    for i, karte in enumerate(hand):
        karte_bild = karte.get_image()
        screen.blit(karte_bild, (pos_x + i * abstand, pos_y))

# Initialisierung




def karten_generierung():

# Karten erstelleng
    global karten_ls
    karten_ls = []
    Farben = ["clubs", "diamonds", "hearts", "spades"]
    Karten_Namen = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "ace", "jack", "king", "queen"]
    Bild = []

    for name in Karten_Namen:
        bildreihe = []
        for farbe in Farben:
            pfad = f"cards/{name}_of_{farbe}.png"
            bildreihe.append(pfad)
        Bild.append(bildreihe)


    for stelle_karten_bild,kartenwert in enumerate(range(2, 11)):
        for karten in range(0,4):
            if kartenwert == 10:
                karten_ls.extend([Zehn(Bild[8][karten]), J(Bild[10][karten]), Q(Bild[12][karten]), K(Bild[11][karten]), A(Bild[9][karten])])
            else:
                karte = Karte(kartenwert, Bild[stelle_karten_bild][karten])
                karten_ls.append(karte)

    for i in range(0,5):
        random.shuffle(karten_ls)
    


def run_me():
    global buttons,restart_button,break_loop,spieler1,dealer1,dealer_zeigt_zweite_karte,anzeige_wert
    anzeige_wert =""
    
    karten_generierung()
    
    dealer_zeigt_zweite_karte = False  # Flag, ob zweite Dealer-Karte gezeigt wird

    dealer1 = Dealer()
    spieler1 = Spieler(1000000000, 100)



    break_loop = [False]

    # Spiel-Schleife mit Buttons
    buttons = [
        Button("Hit", 500, 500, 100, 40, hit),
        Button("Stand", 610, 500, 100, 40, stand),
        Button("Double", 720, 500, 100, 40, double),
        Button("Split", 830, 500, 100, 40, split),
    ]
    restart_button = Button("Restart", 940, 500, 100, 40, restart_game,False)
    


    dealer1.dealer_karten()
    spieler1.spieler_karten()
    deck_auswertung()

    while not break_loop[0]: #Läuft, bis break_loop[0] True wird



        screen.fill((0, 120, 0))

        # Event-Handling zentral
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            restart_button.handle_event(event)
            for btn in buttons:
                btn.handle_event(event)

        # Dealer-Karten offen anzeigen
        if not dealer_zeigt_zweite_karte:
            # Erste Karte offen anzeigen
            screen.blit(dealer1.get_dealer_deck()[0].get_image(), (100, 50))

            # Zweite Karte verdeckt (blaues Rechteck)
            screen.blit(backside_image, (160, 50))

        else:
            # Alle Karten anzeigen
            zeichne_hand(screen, dealer1.get_dealer_deck(), 100, 50)

        # Spieler-Karten anzeigen (jede Hand untereinander)
        for i, hand in enumerate(spieler1.hands):
            zeichne_hand(screen, hand, 100, 300 + i * 100)

        # Buttons zeichnen
        for btn in buttons:
            btn.draw(screen)

        restart_button.draw(screen)
        if status_message != "":
            text_surf = FONT.render(status_message, True, (255, 255, 255))
            screen.blit(text_surf, (1000, 50))
        
        anzeig_wert = FONT.render(anzeige_wert, True, (255, 255, 255))
        screen.blit(anzeig_wert, (100, 250))


        pygame.display.flip()
        clock.tick(30)

    # Pygame beenden

pygame.init()
status_message = ""
screen = pygame.display.set_mode((1500, 750))
pygame.display.set_caption("Blackjack")

backside_image = pygame.transform.smoothscale(pygame.image.load("cards/backside.png").convert_alpha(), (80, 120))
# Font
FONT = pygame.font.SysFont("Arial", 20)

# Uhr für Framerate
clock = pygame.time.Clock()

run_me()
