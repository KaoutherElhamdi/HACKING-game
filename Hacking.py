#Import
from uagame import Window
from time import sleep
from random import choice, choices, sample, randint

def create_window():
    window = Window("Hacking", 600, 500)
    
    #Format
    window.set_bg_color('black')
    window.set_font_name('couriernew')
    window.set_font_size(18)
    window.set_font_color('green')
    
    return window

def get_windiw_inf(window):
    return window.get_font_height(), window.get_height(), window.get_width()

def display_header(window, string_height, total_attempts, current_height):
    display_line(window, "DEBUG MODE", 0, current_height, 1)
    display_line(window, "{} ATTEMPT(S) LEFT".format(total_attempts), 0, string_height, 1)

def get_hint_msg(correct, guess):
    m = min(len(correct),len(guess))
    n = sum([1 for i in range(m) if correct[i]==guess[i]])
    return '{}/7 IN MATCHING POSITIONS   '.format(n)

def guesses(window, total_attempts, correct_password, current_height, string_height, width, height):
    #Verify guess
    correct_outcome = ["EXITING DEBUG MODE", "LOGIN SUCCESSFUL - WELCOME BACK", "PRESS ENTER TO CONTINUE"]
    incorrect_outcome = ["LOGIN FAILURE - TERMINAL LOCKED", "PLEASE CONTACT AN ADMINISTRATOR", "PRESS ENTER TO EXIT"]    
    outcome = incorrect_outcome
    
    #Prompt for guesses
    attemps = total_attempts
    guessed_word = ""
    incorrect_height = 0
    while attemps>0:
        
        current_height += string_height
        guessed_word = window.input_string('ENTER PASSWORD >', 0,current_height)
        window.update()
        
        if guessed_word==correct_password:
            outcome = correct_outcome
            break
        
        #Display "INCORRECT" msg and a hint
        hint_msg = get_hint_msg(correct_password, guessed_word)
        
        display_line(window, " INCORRECT", width-window.get_string_width(hint_msg) , incorrect_height)
        incorrect_height += string_height
        
        display_line(window, hint_msg, width-window.get_string_width(hint_msg) , incorrect_height)
        incorrect_height += string_height
        
        window.update()
        
        #Show attempts Left  
        attemps -= 1
        display_line(window, "{} ATTEMPT(S) LEFT".format(attemps), 0, string_height)
        
        if attemps == 1 :
            warning_msg = "*** LOCKOUT  WARNING ***"
            display_line(window, warning_msg, width-window.get_string_width(warning_msg), height-string_height)
    
    outcome = [guessed_word] + outcome
    window.clear()
    
    return outcome, current_height

def display_end_game_messages(window, outcome, height, width, string_height):
    y_space = ( height - 7 * string_height ) // 2
    current_height = y_space
    
    for s in outcome[:-1]:
        display_line(window, s, (width-window.get_string_width(s))//2, current_height, 0.5)
        current_height += string_height * 2
        
    window.input_string(outcome[-1], (width-window.get_string_width(outcome[-1]))//2 ,current_height)
    #Colse window
    window.close()
    
def display_line(window, msg, location_w, location_h, sleep_time=0):
    window.draw_string(msg, location_w, location_h)
    window.update()
    if sleep_time:
        sleep(sleep_time)    
    
def display_passwords_list(window, passwords, current_height, string_height):
    fill = '!@#$%^&*()-+=~[]{}'
    current_height += string_height * 2
    for password in passwords:
        
        r = randint(0,13)
        random_fill = ''.join(choices(fill, k=13))
        
        display_line(window, random_fill[:r]+password+random_fill[r:], 0, current_height, 0.5)

        current_height += string_height
    return current_height

def get_passwordlist_correct_password():
    
    with open('Passwords.txt','r') as f :
        passwords = sample(f.read().split(','), k=13)
           
    correct_password = choice(passwords)
    
    return passwords, correct_password

def display_mode_choice(window, width, heigth, string_height):
    mode_attemps = {'EASY': 10, 'NORMAL': 6, 'HARD': 4}
    current_height = 0
    for s in ['CHOOSE MODE :', 'EASY', 'NORMAL', 'HARD']:
        display_line(window, s, (width-window.get_string_width(s))//2, current_height, 0.5)
        current_height += 2 * string_height
        
    mode = ''
    while mode not in ['EASY', 'NORMAL', 'HARD']:
        mode = window.input_string('>>>   ', 0, current_height).upper()
        current_height += string_height
    
    window.clear()
    return mode_attemps[mode]

def main():    
    #Open a window
    window = create_window()
    
    #Height , width and string heigth
    string_height, height, width = get_windiw_inf(window)
    current_height = 0
    
    #Display Mode choice
    total_attempts = display_mode_choice(window, width, height, string_height)
    
    #Display header
    display_header(window, string_height, total_attempts, current_height)
    current_height += string_height
    
    #Passwords list
    passwords, correct_password = get_passwordlist_correct_password()
    
    #Display the list     
    current_height = display_passwords_list(window, passwords, current_height, string_height)
    
    #Prompt for guesses
    outcome, current_height = guesses(window, total_attempts, correct_password, current_height, string_height, width, height)
    
    #End game
    display_end_game_messages(window, outcome, height, width, string_height)
    
main()