#Philip
import pygame
import sys
#für pygame

import random



# Initialisierung
pygame.init()

# Bildschirm erstellen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mein erstes Pygame-Spiel")

# Farben
card = pygame.image.load(r"cards/ace_of_spades.png")
card = pygame.transform.scale(card, (100, 150))  # Größe anpassen

# Uhr für Framerate
clock = pygame.time.Clock()


# Johannes

class Dealer():
    pass 

class Spieler():
    def __init__(self,guthaben,einsatz):
        self.__guthaben = guthaben
        self.__spieler_deck = []
        self.einsatz = einsatz
        
        
    def spieler_karten(self,liste:list):
        self.__spieler_deck = [liste[0],liste[2]] # spieler karten
        
        if self.__spieler_deck[0].get_karten_wert() + self.__spieler_deck[1].get_karten_wert() == 21:#schauen ob der Spieler 21 auf der Hand hat 
            print("Spieler hat gewonnen") 
            
    def get_spieler_deck(self):
        return self.__spieler_deck
            
    def hit(self,liste:list):
        self.__spieler_deck.append(liste[0])
        del liste[0]
        
    def double(self,liste:list):
        if self.einsatz >= self.__guthaben:
            print("Sie haben nicht genügend Geld")
        else:
            self.einsatz = self.einsatz * 2
            self.hit(liste)
            
            
    def split(self,liste:list):
        if self.__spieler_deck[0].get_karten_wert() == self.__spieler_deck[1].get_karten_wert():
            hand1 = self.__spieler_deck[0]
            hand2 = self.__spieler_deck[1]
            
            hand1.append[liste]
            del liste[0]
            
            hand2.append[liste]
            del liste[0]
            for i in range(0,100):
                wert1 = sum([karte.get_karten_wert() for karte in hand1])
                wert2 = sum([karte.get_karten_wert() for karte in hand2])
                if wert1 > 21:
                    print("Hand1 Verloren")
                    
                if wert2 > 21:
                    print("Hand2 Verloren")
        else:
            print("Split nicht möglich")
        
        
    def stand(self):
        return self.__spieler_deck

    

        
           
            
class Dealer():
    def __init__(self):
        self.__dealer_deck = []
    
    def dealer_karten(self,liste:list):
        self.__dealer_deck = [liste[1],liste[3]] # dealer karten
        
        print(self.__dealer_deck[0]) # 1. karte des dealers aufdecken


        if self.__dealer_deck[0].get_karten_wert() + self.__dealer_deck[1].get_karten_wert() == 21: #schauen ob der dealer 21 auf der Hand hat 
            print("dealer hat gewonnen") 

    def hitting_dealer(self,liste:list,spieler:Spieler):
        gesamtwert = sum([karte.get_karten_wert() for karte in self.__dealer_deck])
        if gesamtwert < 17:
            self.__dealer_deck.append(liste[0])
            del liste[0]
            self.hitting_dealer(liste,spieler)
        
        elif gesamtwert > 21:
            print("verloren")
            return self.__dealer_deck
        
        else:
            return self.__dealer_deck
        
    def get_dealer_deck(self):  
        return self.__dealer_deck

        
    
class Jetons():
    pass

class Karte():
    def __init__(self,wert):
        self.__wert = wert
        
    def get_karten_wert(self):
        return self.__wert
    
        
    
class Zehner(Karte):
    def __init__(self):
        super().__init__(10)
        

class Zehn(Zehner):
    def __init__(self):
        super().__init__()

class J(Zehner):
    def __init__(self):
        super().__init__()

class Q(Zehner):
    def __init__(self):
        super().__init__()

class K(Zehner):
    def __init__(self):
        super().__init__()
        
class A(Karte):
    def __init__(self):
        super().__init__(11)
        
        
# Karten erstellen und mischen
karten_ls = []

for kartenwert in range(2,11,1): # Karten von 2 bis 11
    
        for karten in range(0,4,1): #von jeder Karte 4 
            if kartenwert == 10:
                karte = Zehn()
                karten_ls.append(karte)
                
                karte = J()
                karten_ls.append(karte)
                
                karte = Q()
                karten_ls.append(karte)
                
                karte = K()
                karten_ls.append(karte)
                
                karte = A()
                karten_ls.append(karte)
                    
            else:  
                karte = Karte(kartenwert)
                karten_ls.append(karte)
                
random.shuffle(karten_ls) #mischeln
def run_me():
    # Objekte erstellen
    #einsatz = int(input())
    #guthabem = int(input())
    dealer1 = Dealer()
    spieler1 = Spieler(1000000,100)
    for i in range (0,5):
        del karten_ls[0]
    
    dealer1.dealer_karten(karten_ls)
    spieler1.spieler_karten(karten_ls)
    spieler1.hit(karten_ls)

run_me()

# Spiel läuft
running = True
while running:
    clock.tick(30)  # 30 FPS

    # Events abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Bildschirm füllen
    screen.fill((0, 120, 0))  # grüner Tisch
    screen.blit(card, (100, 100))  # Karte anzeigen

    # Bildschirm aktualisieren
    pygame.display.flip()

# Pygame beenden
pygame.quit()
sys.exit()

