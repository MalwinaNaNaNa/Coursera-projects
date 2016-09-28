# implementation of card game - Memory

import simplegui
import random

im0 = simplegui.load_image('https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTMGX_0-aVfSBETdYZ2h543uL1L98YVZtkgBhsINK_7X9ZeA7qQtA')
im1 = simplegui.load_image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_ZZ8Gdeu4uvKvmvVgr66Dm5wcSD38vYjTTTtPnGQgs1wgs6S9')
im2 = simplegui.load_image('https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSex2R2Pxt2Do_c-qevzSVFSMnso7y8oYwtDz-NLAIZ6pLex-KU')
im3 = simplegui.load_image('https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRMLidlzNf9GyokkhIjII0GPcrerCdwzhz3Uc3-w6EmHunWxrMT6w')
im4 = simplegui.load_image('https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSf5csjyP3MQ11gsXzJxjukH2qdfs8bKnRArJVh3M6Js6RA0JiNVA')
im5 = simplegui.load_image('https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRvHNwzDyG72x8TBvh-eU1g4ANy6UHxEWoRuxuAEKLydIJp33Jt')
im6 = simplegui.load_image('https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRN12iMqDH6VkZVsH_yfddcf_sGVroiapya0SHxBJ6tbG3MGM0Vnw')
im7 = simplegui.load_image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxq4MADy7fZhGSdMujAdoscH8beMgp5NzHqhvAx8oX8XF61j78qA')

deck1 = [im0,im1,im2,im3,im4,im5,im6,im7]
deck2 = [im0,im1,im2,im3,im4,im5,im6,im7]
deck2
deck1.extend(deck2)
deck = deck1


            
#print deck
random.shuffle(deck)
#print deck

CARD_WIDTH = 800/16
CARD_HEIGHT = 100
card_center = [CARD_WIDTH/2, CARD_HEIGHT/2]
delta = 0

exposed = []
for i in range(0,16):
    exposed.append(False)
#print exposed
#print len(exposed)


state = 0
card1_index=[]
card2_index=[]

turns=0



# helper function to initialize globals
def new_game():
    global turns, state, exposed
    turns = 0
    state = 0
    card1_index=[]
    card2_index=[]
    random.shuffle(deck)
    exposed = []
    for i in range(0,16):
        exposed.append(False)
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global delta2, card_index, state, card_indexes, deck, turns
    click_pos = list(pos)
    
    for i in range(len(deck)):
        delta2 = CARD_WIDTH*i
        if delta2 < click_pos[0] < delta2+CARD_WIDTH:
            if exposed[i] == False:
                exposed[i] = True
                if state == 0:
                    state = 1
                    card1_index.append(i)                    
                    return i
                elif state == 1:
                    state = 2
                    turns += 1
                    label.set_text("Turns = " + str(turns))
                    card2_index.append(i)
                    return i
                else:                                                                   
                    if deck[card1_index[0]] is not deck[card2_index[0]]: 
                        exposed[card1_index[0]] = False
                        exposed[card2_index[0]] = False
                        state = 1
                        card1_index[0] = i
                        card2_index.pop()
                        return i
                    elif deck[card1_index[0]] == deck[card2_index[0]]:
                        state = 1
                        card1_index[0] = i
                        card2_index.pop()            
      

                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global delta
    global card_index
    
    for i in range(len(deck)):
        delta = CARD_WIDTH*i
        if exposed[i] == True:
#            canvas.draw_text(str(deck[i]), (card_center[1]+delta-CARD_WIDTH, CARD_HEIGHT/4*3),
#                            50, 'Black', 'monospace')
            canvas.draw_image(deck[i], (25,25), (50,50), (card_center[1]+delta-25, CARD_HEIGHT/2), (50,50))                            
        elif exposed[i] == False:
            canvas.draw_polygon([[delta,0],[delta+CARD_WIDTH,0], [delta+CARD_WIDTH, CARD_HEIGHT],
                                [delta,CARD_HEIGHT]], 1, "White", "Green")
            

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
frame.set_canvas_background('White')

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric