# Implementation of classic arcade game Pong by Malwina Strenkowska

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0,0]
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]
paddle1_vel = [0,0]
paddle2_vel = [0,0]
VEL = 5
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [int(WIDTH/2), int(HEIGHT/2)]
#    ball_vel = [5,0]
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 4),-random.randrange(1, 3)]
    elif direction == LEFT:
        ball_vel = [-random.randrange(2, 4),-random.randrange(1, 3)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(LEFT)
    score1 = 0
    score2 = 0
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_text(str(score1), (100,50), 50, "Yellow")
    canvas.draw_text(str(score2), (475,50), 50, "Yellow") 
        
    # update ball  
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
        
    if ball_pos[1] == HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    elif ball_pos[1] == BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if  paddle1_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT:
            ball_vel[0] = -(ball_vel[0] + 0.1*ball_vel[0])
            
                 
        else:
            spawn_ball(RIGHT)
            score2 += 1
            
                
    
    elif ball_pos[0] >= WIDTH - BALL_RADIUS:
        if  paddle2_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT:
            ball_vel[0] = -(ball_vel[0] + 0.1*ball_vel[0])
        
        else:
            spawn_ball(LEFT)
            score1 += 1
                
        
     
        
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Magenta", "Magenta")
    
    # update paddle's vertical position, keep paddle on the screen
    if HEIGHT - HALF_PAD_HEIGHT >= paddle1_pos[1] >= HALF_PAD_HEIGHT:   
        
        paddle1_pos[1] += paddle1_vel[1]
          
    else: 
        paddle1_vel[1] = 0
        if paddle1_pos[1] >= HALF_PAD_HEIGHT:
            paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        elif HEIGHT - HALF_PAD_HEIGHT >= paddle1_pos[1]:
            paddle1_pos[1] = HALF_PAD_HEIGHT
    
    if HEIGHT - HALF_PAD_HEIGHT >= paddle2_pos[1] >= HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel[1]
    else:
        paddle2_vel[1] = 0
        if paddle2_pos[1] >= HALF_PAD_HEIGHT:
            paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        elif HEIGHT - HALF_PAD_HEIGHT >= paddle2_pos[1]:
            paddle2_pos[1] = HALF_PAD_HEIGHT
        
    
    # draw paddles
    canvas.draw_polygon([(paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT), 
                        (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),
                        (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT),
                        (paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT)],
                        2, "Red", "Red")
    
    canvas.draw_polygon([(paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT), 
                        (paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                        (paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT),
                        (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)],
                        2, "Red", "Red")
    
    
    # determine whether paddle and ball collide    
    
    # draw scores
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = -VEL
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = +VEL
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= VEL
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += VEL
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] = 0
        
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] = 0
        
def reset():
    new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset, 100)



# start frame
new_game()
frame.start()
