# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math
count = 0

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    secret_number = random.randrange(0, 100)
    global num_range
    global count
    count = 0
    print "New game! Choose range"
    print
        

# define event handlers for control panel
def range100():
    global secret_number
    secret_number = random.randrange(0, 100)
    global num_range
    num_range = 100
    print "New game. Range is from 0 to 100"
    print
    
    
def range1000():
    global secret_number
    secret_number = random.randrange(0, 1000)
    global num_range
    num_range = 1000
    print "New game. Range is from 0 to 1000"
    print
   
    
def input_guess(guess):
    # main game logic goes here	
    global count
    count += 1
           
    if num_range == 100:
        if count < 7:
            print "Guess was " + str(int(guess))
            print "Number of remaining guesses is " + str(7 - count)
        if int(guess) == secret_number and count < 7:
            print "Correct!"
            print 
        elif int(guess) > secret_number and count < 7:
            print "Lower!"
            print
        elif int(guess) < secret_number and count < 7:
            print "Higher!"
            print
        else:
            print "You run out of guesses. The number was " + str(secret_number)
            print
            new_game()
    
            
    if num_range == 1000:
        if count < 10:
            print "Guess was " + str(int(guess))
            print "Number of remaining guesses is " + str(10 - count)
        if int(guess) == secret_number and count < 10:
            print "Correct!"
            print
        elif int(guess) > secret_number and count < 10:
            print "Lower!"
            print
        elif int(guess) < secret_number and count < 10:
            print "Higher!"
            print
        else: 
            print "You run out of guesses. The number was " + str(secret_number)
            print
            new_game()  
   
    
   

    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range 0-100", range100, 200)
frame.add_button("Range 0-1000", range1000, 200)
frame.add_input("guess number", input_guess, 100)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
