# template for "Stopwatch: The Game"

import simplegui

# define global variables
interval = 100
t = 0 
WIDTH = 400 
HEIGHT = 200 
y = 0 
x = 0 
first_click_stop = True 

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    d = t
    D = d%10
    c = d//10
    C = c%10
    b = c//10
    B = b%6
    a = b//6
    A = a
    format_t = str(A) + ":" + str(B) + str(C) +"." + str(D)  
    return format_t

    
     
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global first_click_stop
    timer.start()
    first_click_stop = True

def stop_handler():
    global y, x, t, first_click_stop
    """ y counts how many times stop button was pressed and x counts how many of those times were round secons"""
    """first_time_stop global is given to eliminate changing x and y by multiple pressing of stop when timer is not running"""
    timer.stop()
    if first_click_stop:
        y += 1
        if t%10 == 0:
            x += 1
        first_click_stop = False        
    return x, y
           
def reset_handler():
    global t, x, y
    timer.stop()
    t = 0
    x = 0
    y = 0
    

# define event handler for timer with 0.1 sec interval
def tick():
    """t counts how many tens of seconds have passed"""
    global t
    t += 1 
    print t


# define draw handler
def draw(canvas):
    canvas.draw_text(str(format(t)), (WIDTH/3, HEIGHT/2), 50, 'White')
    canvas.draw_text((str(x) + "/" + str(y)), (320, 40), 40, 'Aqua')
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", WIDTH, HEIGHT)
frame.add_button("start", start_handler, 200)
frame.add_button("stop", stop_handler, 200)
frame.add_button("reset", reset_handler, 200)


timer = simplegui.create_timer(interval, tick)

# register event handlers
frame.set_draw_handler(draw)

# start frame
frame.start()

# Please remember to review the grading rubric
