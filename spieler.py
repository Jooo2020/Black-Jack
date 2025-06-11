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
        if len(aktuelle_hand) == 2 and aktuelle_hand[0].get_karten_wert() == aktuelle_hand[1].get_karten_wert():
            if self.einsatz * 2 > self.__guthaben:
                self.__guthaben -= self.einsatz  # zweiter Einsatz
                print("Nicht genügend Guthaben für Split")

            karte1 = aktuelle_hand[0]
            karte2 = aktuelle_hand[1]

            # Auf beide gesplittene karten folgt eine neue karte
            self.hands[self.active_hand_index] = [karte1, karten_ls.pop(0)]

            # Neue Hand erstellen mit anderer Karte + neue vom Stapel
            neue_hand = [karte2, karten_ls.pop(0)]

            self.hands.append(neue_hand)

            # noch für jede hand den aktuellen kartenstand angeben 
            for hand_index,hand in enumerate(self.hands):
                wert = berechne_hand_wert(hand)
                print(f"Wert Hand{hand_index}:", self.hands[hand_index][0].get_karten_wert(), self.hands[hand_index][1].get_karten_wert())

                if wert > 21:
                    print(f"hand{self.active_hand_index} Verloren")
                    break_loop[0] = True

                elif wert == 21:
                    self.stand()
                    
                
        else:
            print("Split nicht möglich")

    def stand(self):
        global dealer_zeigt_zweite_karte

        if self.active_hand_index + 1 < len(self.hands):
            self.active_hand_index += 1
            print(f"Wechsel zu Hand {self.active_hand_index}")
            return False  # noch Hände offen
        else:
            dealer_zeigt_zweite_karte  =True
            deck_auswertung()
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