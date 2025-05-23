import random
import sys
# Johannes
class Dealer(): #für die spilerklasse das sie funktioniert, da die klasse spieler vor der klasse dealer defininiert worden ist 
    pass 

class Spieler():
    def __init__(self,guthaben,einsatz):
        self.__guthaben = guthaben
        self.spieler_deck = []
        self.einsatz = einsatz
        self.hand1 = []
        self.hand2 = []
        
        
    def spieler_karten(self,liste:list):
        self.spieler_deck = [liste[0],liste[2]] # spieler karten
        
        if self.spieler_deck[0].get_karten_wert() + self.spieler_deck[1].get_karten_wert() == 21:#schauen ob der Spieler 21 auf der Hand hat 
            print("Spieler hat gewonnen")
            sys.exit()
            
    def hit(self,liste:list):
        self.spieler_deck.append(liste[0])
        del liste[0]
        
        
    def double(self,liste:list):
        if self.einsatz >= self.__guthaben:
            print("Sie haben nicht genügend Geld")
        else:
            self.einsatz = self.einsatz * 2
            self.hit(liste)
            
            
    def split(self,liste:list):
        if self.spieler_deck[0].get_karten_wert() == self.spieler_deck[1].get_karten_wert(): # für assen muss noch anderer wert hinzugefüft werden 
            if self.einsatz * 2 > self.__guthaben:
                print("Nicht genügend Guthaben für Split")
                return
            self.__guthaben -= self.einsatz  # zweiter Einsatz

            self.hand1.append(self.spieler_deck[0])
            self.hand2.append(self.spieler_deck[1])
            
            self.hand1.append(liste[0])
            del liste[0]
            
            self.hand2.append(liste[0])
            del liste[0]
            # noch für jede hand den aktuellen kartenstand angeben 
            wert1 = 0
            wert2 = 0
            while True: 
                wert1 = sum([karte.get_karten_wert() for karte in self.hand1])
                print("Wert Hand1:", wert1)

                if wert1 > 21:
                    print("hand1 Verloren")
                    break 
                
                elif input("hitten?") == "hit": #muss als knopf in der Grafik angezeigt werden
    
                    self.split_hit(self.hand1,liste)
                    
                else:
                    break 
                    
                
            while True:
                wert2 = sum([karte.get_karten_wert() for karte in self.hand2])
                print("Wert Hand2:", wert2)
                if wert2 > 21:
                    print("hand2 Verloren")
                    break
  
                elif input("hitten?") == "hit": #muss als knopf in der Grafik angezeigt werden
                    self.split_hit(self.hand2,liste)
                    
                else:
                    break
                    
        else:
            print("Split nicht möglich")
            
    def split_hit(self,hand,liste:list):
        hand.append(liste[0])
        del liste[0]
    
               
    def stand(self):
        return self.spieler_deck

         
class Dealer():
    def __init__(self):
        self.__dealer_deck = []
    
    def dealer_karten(self,liste:list):
        self.__dealer_deck = [liste[1],liste[3]] # dealer karten
        
        #print(self.__dealer_deck[0].get_karten_wert()) # 1. karte des dealers aufdecken
        #print(self.__dealer_deck[1].get_karten_wert())
        
        if self.__dealer_deck[0].get_karten_wert() + self.__dealer_deck[1].get_karten_wert() == 21: #schauen ob der dealer 21 auf der Hand hat 
            print("dealer hat gewonnen") 

    def hitting_dealer(self,liste:list,spieler:Spieler):
        gesamtwert = sum([karte.get_karten_wert() for karte in self.__dealer_deck])
        if gesamtwert < 17:
            self.__dealer_deck.append(liste[0])
            del liste[0]
            self.hitting_dealer(liste,spieler)
            #print("Dealer Kartenwert:", )
        
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

for kartenwert in range(2,11): # Karten von 2 bis 11
    
        for karten in range(4): #von jeder Karte 4 
            if kartenwert == 10:
                karten_ls.extend([Zehn(), J(), Q(), K(), A()])     
                               
            else:  
                karte = Karte(kartenwert)
                karten_ls.append(karte)
                
                
random.shuffle(karten_ls) #mischeln

def run_me():
    # Objekte erstellen
    #einsatz = int(input())
    #guthabem = int(input())
    dealer1 = Dealer()
    spieler1 = Spieler(1000000, 100)

    dealer1.dealer_karten(karten_ls)
    spieler1.spieler_karten(karten_ls)

    print("Spielerhand:", [karte.get_karten_wert() for karte in spieler1.spieler_deck])
    eingabe = input("was möchten sie tun?")
    if eingabe == "split":
        spieler1.split(karten_ls)
        print("Finale Hände:")
        print("Hand1:", [karte.get_karten_wert() for karte in spieler1.hand1])
        print("Hand2:", [karte.get_karten_wert() for karte in spieler1.hand2])
        
    elif eingabe == "hit":
        spieler1.hit(karten_ls)
        print("Spieler Deck", [karte.get_karten_wert() for karte in spieler1.spieler_deck])
        
    elif eingabe == "double":
        spieler1.double(karten_ls)
        print("Spieler Deck", [karte.get_karten_wert() for karte in spieler1.spieler_deck])
        
    elif eingabe == "stand":
        spieler1.stand()
        print("Spieler Deck", [karte.get_karten_wert() for karte in spieler1.spieler_deck])
        
    else:
        print("die ausgewähle methode gibt es nicht")
        
    dealer1.hitting_dealer(karten_ls,spieler1)

    # Optional: show final hands
    


run_me()

#für nächstes mal dealer ausgabe, hit ausgabe, zusammenführung mit gui, geldwert, hit mehrmals ausfüherne 
