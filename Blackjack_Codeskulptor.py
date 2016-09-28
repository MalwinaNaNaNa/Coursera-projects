# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

background_im = simplegui.load_image('https://s-media-cache-ak0.pinimg.com/736x/05/c8/ed/05c8ed7391615bdf0e253375fc08832d.jpg')

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
CARD_SPACE = 25
message = ''


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
 

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card = []

    def __str__(self):
        s = "Hands contains "
        for i in range(len(self.card)):           
            s += str(self.card[i]) + ' '
        return s
        
        pass	# return a string representation of a hand

    def add_card(self, card):
        self.card.append(card)
        

    def get_value(self):
            
               
        get_value = 0
        count = 0
        for i in self.card:
            card_rank = list(str(i))           
            value = VALUES.get(card_rank[1])
            get_value += value
            count += card_rank[1].count('A')
        
        if count == 1 and get_value + 10 <= 21:             
            get_value += 10
            return get_value
        elif count == 2 and get_value + 10 <=21:
            get_value += 10
            return get_value
        else:                
            return get_value
   
    def draw(self, canvas, pos):        
        for c in self.card:            
            c.draw(canvas, [pos[0] + self.card.index(c)*CARD_SIZE[0]+ self.card.index(c)*CARD_SPACE, pos[1]])
                                                                            
            
            
        
        
 
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck=[]
        for i in SUITS:                        
            for j in RANKS:               
                c = Card(i,j)
                self.deck.append(c)           
                                     
                                                      
    def shuffle(self):
        random.shuffle(self.deck)
        # shuffle the deck 
        

    def deal_card(self):
        return random.choice(self.deck)
    
    def __str__(self):
        s = "Deck contains "
        for i in self.deck:
            s += str(i) + ' '             
        return s



#define event handlers for buttons
def deal():    
    global outcome, in_play, deck, player_hand, dealer_hand, score
    if in_play == False:
        deck = Deck()
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        print "Player", player_hand
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        print "Dealer", dealer_hand
        outcome = ''
        in_play = True
    
    else:
        outcome = 'You lost!'
        score -= 1
        in_play = False
        
def hit():
    global in_play, score, outcome
    if in_play == True:
        print player_hand.get_value()
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            print "Player", player_hand
            print player_hand.get_value()
    
        if player_hand.get_value() > 21:
            outcome = 'You went bust and lose!'
            in_play = False
            score -= 1
            print "score", score   

       
def stand():
    global in_play, score, outcome
    if in_play == False: 
        return outcome
        
    elif in_play == True:
       
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            print "Dealer", dealer_hand
            print dealer_hand.get_value()
                
        print 'Dealer has busted!'
        if dealer_hand.get_value() >= 17:
            if dealer_hand.get_value() < player_hand.get_value():
                outcome = "You won!"
                score += 1
                in_play = False
                print "score", score   
            else: 
                outcome = "You lost!"
                score -= 1
                print "score", score
                in_play = False
            
            


# draw handler    
def draw(canvas):
    global message
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_image(background_im, [300,300], [600,600], [300,300], [600,600])
#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])
    
    player_hand.draw(canvas, [100,200])
    dealer_hand.draw(canvas, [100,400])
    canvas.draw_text('Blackjack', [10,50], 50, 'Black', 'monospace')
    canvas.draw_text("Score " + str(score), [320,50], 50, 'Yellow', 'monospace')
    canvas.draw_text("Player", [100,180], 20, 'Orange', 'sans-serif')
    canvas.draw_text("Dealer", [100,380], 20, 'Orange', 'sans-serif')
    canvas.draw_text(message, [300,180], 20, 'White', 'sans-serif')
    
    if in_play == True:
        message = "Hit or stand?"
        canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0],400 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    else:
        message = "New deal?"
        
    canvas.draw_text(outcome, [20,120], 50, 'White', 'sans-serif')
    
    
       
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)

frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric