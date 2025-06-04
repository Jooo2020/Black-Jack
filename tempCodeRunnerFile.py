def split(self,liste:list):
        aktuelle_hand = self.hands[self.active_hand_index]
        if len(aktuelle_hand) == 2 and aktuelle_hand[0].get_karten_wert() == aktuelle_hand[1].get_karten_wert(): # ob nur 2 objekte in der hand sind und überprüft ob die beiden karten in gleichen wert 
            if self.einsatz * 2 > self.__guthaben:
                self.__guthaben -= self.einsatz  # zweiter Ei