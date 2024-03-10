'''
CPSC 415 -- Homework #5 support file
Stephen Davies, University of Mary Washington, fall 2023
'''

from clue import CluePlayer, suspects, weapons, rooms, Card
from PropKB import KB
import random

# Throughout this file, you can refer to the global variables "suspects",
# "weapons", and "rooms", which are tuples of "Card" objects telling you what
# cards are in the game, period. You can even try this right now:
#
# >>> print(suspects)
# >>> print(weapons)
# >>> print(rooms)
#
# Each Card object has a name and a category, accessible with the dot (".")
# notation:
# >>> print(f"{suspects[0].name} is a {suspects[0].category}")
# mustard is a SUSPECT


class jcottrel_CluePlayer(CluePlayer):

    def __init__(self, hand, player_num):
        """
        Change 'starting' to your player name, and add anything else you want
        to this constructor. I've created an inst var "hand" since I think
        you'll want that. It's a list of the Cards you're dealt at the start
        of the game.
        """
        super().__init__(player_num, 'jcottrel')
        self.hand = hand
        self.kb = KB()
        self.accusation = []
        self.next_player_hand = []
        self.last_player_hand = []
        self.last_suggestion = ['Nothing', 'Nothing', 'Nothing']
        # Definitely could be better but I just wanted an easy fix lol
        if self.player_num == 1:
            self.next_player_num = 2
            self.last_player_num = 3
        elif self.player_num == 2:
            self.next_player_num = 3
            self.last_player_num = 1
        else:
            self.next_player_num = 1
            self.last_player_num = 2

        # Set up initial logic for the knowledge base
        for card in self.hand:
            # Cards I have in my hand are not the answer and are not in anyone else's hand
            self.kb.tell(f'{self.player_num}{card.name}{card.category}')
            self.kb.tell(f'-{self.next_player_num}{card.name}{card.category}')
            self.kb.tell(f'-{self.last_player_num}{card.name}{card.category}')
            # In the beginning of the game I have not shown anybody my cards
            self.kb.tell(f'-{self.player_num}shown{self.next_player_num}{card.name}{card.category}')
            self.kb.tell(f'-{self.player_num}shown{self.last_player_num}{card.name}{card.category}')
            # Also any card is "false" if it has been shown, and therefore is not the answer
            self.kb.tell(f'-{card.name}{card.category}')
        for card in suspects:
            if card not in self.hand:
                self.kb.tell(f'-{self.player_num}{card.name}{card.category}')  
        for card in weapons:
            if card not in self.hand:
                self.kb.tell(f'-{self.player_num}{card.name}{card.category}')  
        for card in rooms:
            if card not in self.hand:
                self.kb.tell(f'-{self.player_num}{card.name}{card.category}')


    def ready_to_accuse(self):
        """
        Return True if you know (or think you know) the answer, and are ready
        to risk all by declaring it.
        """
        # This comment is wrong now but I will not update it
        # All cards start as IDK and are made false if they are shown.
        # If there is only one card left that is IDK, then that card must be the answer
        # If we have the answer for all three categories, then we are ready to accuse
        num_idk = 0
        self.accusation = []

        for people in suspects:
            if self.kb.ask(f'{people.name}{people.category}') == True:
                num_idk += 1
                self.accusation.append(people)
        if num_idk != 1:
            return False
        if num_idk > 1:
            exit()
        
        for weapon in weapons:
            if self.kb.ask(f'{weapon.name}{weapon.category}') == True:
                num_idk += 1
                self.accusation.append(weapon)
        if num_idk != 2:
            return False
        
        for room in rooms:
            if self.kb.ask(f'{room.name}{room.category}') == True:
                num_idk += 1
                self.accusation.append(room)
        if num_idk != 3:
            return False
        
        return True

    def get_accusation(self):
        """
        Return a tuple of exactly three Cards: a SUSPECT, a WEAPON, and a ROOM,
        in that order. You will either win the game, or be DQ'd.
        """
        return tuple(self.accusation)

    def get_suggestion(self):
        """
        Return a tuple of exactly three Cards: a SUSPECT, a WEAPON, and a ROOM,
        in that order. This is what you want to "suggest" as the mystery answer
        to the next player in line. You will be told which card they show you,
        if any, in a future call to your .secretly_observe() method. If they do
        not have any of your named cards, your .secretly_observe() method will
        never be called; only your .publicly_observe() method will be.
        """
        suggSuspect = 'Nothing'
        suggWeapon = 'Nothing'
        suggRoom = 'Nothing'
        # Try to find suggestion that will give new information
        if len(self.next_player_hand) < 6:
            for suspect in suspects:
                if self.kb.ask(f'{suspect.name}{suspect.category}') == 'IDK' and suspect not in self.next_player_hand and suspect not in self.hand:
                    suggSuspect = suspect
            for weapon in weapons:
                if self.kb.ask(f'{weapon.name}{weapon.category}') == 'IDK' and weapon not in self.next_player_hand and suspect not in self.hand:
                    suggWeapon = weapon
            for room in rooms:
                if self.kb.ask(f'{room.name}{room.category}') == 'IDK' and room not in self.next_player_hand and suspect not in self.hand:
                    suggRoom = room
        
        # Otherwise make them random
        if suggSuspect == 'Nothing' or suggSuspect == self.last_suggestion[0]:
            suggSuspect = suspects[random.randint(0,len(suspects)-1)]
        if suggWeapon == 'Nothing' or suggWeapon == self.last_suggestion[1] :
            suggWeapon = weapons[random.randint(0,len(weapons)-1)]
        if suggRoom == 'Nothing' or suggRoom == self.last_suggestion[2]:
            suggRoom = rooms[random.randint(0,len(rooms)-1)]

        # Return suggestion
        self.last_suggestion = [suggSuspect, suggWeapon, suggRoom]
        return (suggSuspect, suggWeapon, suggRoom)

    def publicly_observe(self, suggesting_player_num, suggestion,
        responding_player_num, revealed_a_card):
        """
        This method will be called on your player whenever anyone makes a
        suggestion (including you). It tells you that a certain player made a
        suggestion (a tuple with three named cards, in suspect/weapon/room
        order) to another player, and whether or not that second player
        secretly showed them a card.
        """
        # If the responding player did not reveal a card, then we know that they do not have any of the suggested cards
        if not revealed_a_card:
            for card in suggestion:
                # print(self.kb.ask(f'{responding_player_num}{card.name}{card.category}'))
                self.kb.tell(f'-{responding_player_num}{card.name}{card.category}')
                
        # If the responding player did reveal a card, then we know that they have at least one of the suggested cards
        # (ignore if I was the suggesting player because that is handled in secretly observe)
        elif suggesting_player_num != self.player_num:
            self.kb.tell(f'{responding_player_num}{suggestion[0].name}{suggestion[0].category} + {responding_player_num}{suggestion[1].name}{suggestion[1].category} + {responding_player_num}{suggestion[2].name}{suggestion[2].category}')
        
        # If no player has the card that was suggested, then we know that the card is the answer
        for card in suggestion:
            if self.kb.ask(f'-{1}{card.name}{card.category} ^ -{(2)}{card.name}{card.category} ^ -{(3)}{card.name}{card.category}') == True:
                self.kb.tell(f'{card.name}{card.category}')


        return

    def secretly_observe(self, responding_player_num, card):
        """
        This method will be called on your player whenever you take your turn
        and make a suggestion, and one of your opponents does have one of the
        cards you named. The card passed will be the card that the responding
        player secretly showed you (one of the three you named). This method is
        *not* called if an opponent does not have any of your three cards; the
        way you'll know that is by paying attention to your .publicly_observe()
        method.
        """
        # If the responding player revealed a card, then we know that they have that card
        self.kb.tell(f'{responding_player_num}{card.name}{card.category}')
        if responding_player_num == (self.player_num+1)%3:
            self.next_player_hand.append(card)
        else:
            self.last_player_hand.append(card)
        # And that that card is not the answer
        self.kb.tell(f'-{card.name}{card.category}')
        return

    def handle_suggestion(self, suggesting_player_num, suggestion):
        """
        This method will be called on your player whenever the player before
        you suggests a murder solution (three named cards, in suspect/weapon/
        room order). You must return one of the three cards to secretly show
        them, or None if you don't have any of them.
        """
        # Find if I have any cards they suggested and add them to an array
        cards_I_have = []
        for card in suggestion:
            if card in self.hand:
                cards_I_have.append(card)
        
        # If I have no cards they suggested, return nothing
        if len(cards_I_have) == 0:
            return None
        # Otherwise, check if I have already shown them one of the cards they are suggesting
        else:
            for card in cards_I_have:
                # If I have, show them that one again so they get no new information
                if self.kb.ask(f'{self.player_num}shown{suggesting_player_num}{card.name}{card.category}') == True:
                    return card
            # Otherwise just choose a random card (the first one in the list)
            card = cards_I_have[random.randint(0,len(cards_I_have)-1)]
            # Update knowledge base to show that I have shown them this card
            self.kb.retract(f'-{self.player_num}shown{(suggesting_player_num)}{card.name}{card.category}')
            self.kb.tell(f'{self.player_num}shown{(suggesting_player_num)}{card.name}{card.category}')
            return card

