import random

#generates 52 card deck
suits = ("Hearts","Clubs","Spades","Diamonds")
ranks = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King")
value = {"Ace":1, "Two": 2, "Three": 3, "Four": 4, "Five":5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10}

class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
    
class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank, value[rank])
                self.all_cards.append(created_card)
        random.shuffle(self.all_cards)
    def deal_card(self):
        return self.all_cards.pop()

class Human:
    def __init__(self):
        self.all_cards = []
        self.total_value = 0
        self.total_value_max = 0
        self.ranks = []
    def add_cards(self, card): 
        self.all_cards.append(card)
        if(card.rank == "Ace"):
            self.total_value_max = self.total_value_max + 11
        else:
            self.total_value_max = self.total_value_max + card.value
        self.total_value = self.total_value + card.value
        self.ranks.append(card.rank)

    def get_total_value(self):
        return (self.total_value, self.total_value_max)

class Dealer:
    def __init__(self):
        self.all_cards = []
        self.total_value = 0
        self.total_value_max = 0
        self.ranks =  []

    def add_cards(self, card): 
        self.all_cards.append(card)
        # only if greater than 1 because dealer has 1 card hidden until the end
        if(len(self.all_cards) > 1 ):
            if(card.rank == "Ace"):
                self.total_value_max = self.total_value_max + 11
            else:
                self.total_value_max = self.total_value_max + card.value
            self.total_value = self.total_value + card.value
            self.ranks.append(card.rank)
        
    def get_total_value(self):
        return (self.total_value, self.total_value_max)

new_game = True
lost = False
while(new_game):
    play = input("Start New Game? Please Enter Yes or No")
    while(play != "Yes" and play != "No"):
        play = input("Start New Game? Please Enter Yes or No")
    if(play == "No"):
        print("Thanks for playing! Refresh to play again")
        new_game = False
        continue
    new_deck = Deck()
    new_Player = Human()
    new_Dealer = Dealer()

    # starting condition. Both players start with 2 cards
    new_Player.add_cards(new_deck.deal_card())
    new_Player.add_cards(new_deck.deal_card())

    new_Dealer.add_cards(new_deck.deal_card())
    new_Dealer.add_cards(new_deck.deal_card())
    
    print(f"Your Starting Hand: \n Min value: {new_Player.get_total_value()[0]}, Max value: {new_Player.get_total_value()[1]} \n Cards: {new_Player.ranks}")
    print(f"Dealer Starting Visible Hand: \n Min value: {new_Dealer.get_total_value()[0]}, Max value: {new_Dealer.get_total_value()[1]} \n Cards: {new_Dealer.ranks}")
    
    #Human/Player 1 turn
    more_cards = True
    while more_cards:
        draw_card = input("Would you like to draw another card? Yes or No?")
        while(draw_card != "Yes" and draw_card != "No"):
            draw_card = input("Would you like to draw another card? Yes or No?")
        if(draw_card == "No"):
            more_cards = False
        else:
            new_Player.add_cards(new_deck.deal_card())

        #display hand
        print(f"Your Current Hand: \n Min value: {new_Player.get_total_value()[0]}, Max value: {new_Player.get_total_value()[1]} \n Cards: {new_Player.ranks}")
        
        #lose condition
        if new_Player.get_total_value()[0] > 21 and new_Player.get_total_value()[1] > 21 : 
            print("You've Lost!")
            more_cards = False
            lost = True
            break

    #start a new game, since you have already lost
    if(lost):
        continue
    
    #Dealer turn
    #restores invisible card
    new_Dealer.add_cards(new_Dealer.all_cards[0])
    print(f"Deal Invisible card: {new_Dealer.all_cards[0].rank}")

    # dealer will continue to draw until it is above player 1 hand, or at 21
    player1_win_21 = new_Player.get_total_value()[0] == 21 or new_Player.get_total_value()[1] == 21
    dealer_more = new_Dealer.get_total_value()[0] < new_Player.get_total_value()[1] and new_Dealer.get_total_value()[1] < new_Player.get_total_value()[1]
    dealer_win_21 = new_Dealer.get_total_value()[0] == 21 or new_Dealer.get_total_value()[1] == 21
    while(not dealer_win_21 and dealer_more):
        new_Dealer.add_cards(new_deck.deal_card())
        print(f"Dealer Visible Hand: \n Min value: {new_Dealer.get_total_value()[0]}, Max value: {new_Dealer.get_total_value()[1]} \n Cards: {new_Dealer.ranks}")
        dealer_more = new_Dealer.get_total_value()[0] < new_Player.get_total_value()[1] and new_Dealer.get_total_value()[1] < new_Player.get_total_value()[1]
        dealer_win_21 = new_Dealer.get_total_value()[0] == 21 or new_Dealer.get_total_value()[1] == 21
    
    print(f"Dealer Final Hand: \n Min value: {new_Dealer.get_total_value()[0]}, Max value: {new_Dealer.get_total_value()[1]} \n Cards: {new_Dealer.ranks}")
    
    # tie
    if player1_win_21 and dealer_win_21:
        print("You've tied!")
        more_cards = False

    # win condition : when you get 21, or dealer busts
    elif player1_win_21 or new_Dealer.get_total_value()[0]>21:
        print("You've Won!")

    #lose condition: when dealer has higher cards than you
    else:
        print("You've Lost!")