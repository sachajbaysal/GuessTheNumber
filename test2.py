from cmu_graphics import *
import random

# ============================
#  App setup
# ============================
app.width = 1200
app.height = 800

# ============================
#  Global variables
# ============================
min_num = 0
max_num = 0
num_range_list = []
correct_answer = None
guesses = []
guess_label = None
guess_button = None
incorrect_label = None
restart_button = None
answer = None
counts = None
out_of_range_label = None
ga = None
restart_text_label = None
hint_label = None

# ============================
#  Static UI elements
# ============================
number_range = Label("Please Select Your Number Range!", 600, 400, font='Arial', size=40, align='center')
button = Rect(500, 500, 200, 50, fill='blue', border='black')
start = Label("Start", 600, 525, size=30, fill='white', align='center')

congrats = Label("CONGRATS! You Won!", 600, 200, size=40, font='Arial', align='center', fill='green')
congrats.visible = False

warning = None

# ============================
# Restart Game
# ============================
def restart_game():
    global guesses, guess_label, incorrect_label, guess_button, restart_button, count, button2, question, question2, answer, counts, ga, restart_text_label, hint_label, out_of_range_label

    # Hide the main dynamic elements safely
    for item in [guess_button, ga, guess_label, incorrect_label, hint_label,
                 restart_button, restart_text_label, count, question, question2, answer, counts]:
        if item:
            item.visible = False

    guess_button = None
    ga = None
    guess_label = None
    incorrect_label = None
    hint_label = None
    restart_button = None
    restart_text_label = None
    count = None
    button2 = None
    question = None
    question2 = None
    answer = None
    counts = None

    # Reset guesses
    guesses.clear()

    # Reset static UI
    congrats.visible = False
    number_range.visible = True
    button.visible = True
    start.visible = True


    if restart_text_label:
        restart_text_label.visible = False
        restart_text_label = None
    if out_of_range_label:
        out_of_range_label.visible = False
        out_of_range_label = None
    if restart_button:
        restart_button.visible = False
        restart_button = None
    if guess_label:
        guess_label.visible = False
        guess_label = None
    if incorrect_label:
        incorrect_label.visible = False
        incorrect_label = None
    if guess_button:
        guess_button.visible = False
        guess_button = None
    if ga:
        ga.visible = False
        ga = None
    if hint_label:
        hint_label.visible = False
        hint_label = None
    if count:
        count.visible = False
        count = None
    if button2:
        button2.visible = False
        button2 = None
    if question:
        question.visible = False
        question = None
    if question2:
        question2.visible = False
        question2 = None
    if answer:
        answer.visible = False
        answer = None
    if counts:
        counts.visible = False
        counts = None
    congrats.visible = False
    guesses.clear()
    number_range.visible = True
    button.visible = True
    start.visible = True

# ============================
#  Start Game UI
# ============================ 
def start_game():
    global button2, question, question2, count
    guesses.clear()  # 
    number_range.visible = False
    button.visible = False
    start.visible = False

    count = Label(f"Your range is: {min_num} to {max_num}", 600, 500, font='Arial', size=30, align='center')
    question2 = Label("Guess a Number!", 600, 300, font='Arial', size=40, align='center')
    button2 = Rect(475, 600, 250, 50, fill='blue', border='black')
    question = Label("Guess a Number", 600, 625, size=30, fill='white', align='center')

# ============================
#  Get Number Range
# ============================
def start_questions():
    global min_num, max_num, num_range_list, correct_answer, warning

    min_num = int(app.getTextInput("What do you want the minimum number to be?").strip())
    max_num = int(app.getTextInput("What do you want the maximum number to be?").strip())

    if min_num > max_num:
        if warning:
            warning.visible = False
        warning = Label("Minimum number cannot be greater than maximum number!", 600, 200, size=30, font='Arial', align='center', fill='red')
        return

    if warning:
        warning.visible = False

    num_range_list = list(range(min_num, max_num + 1))
    correct_answer = random.choice(num_range_list)
    print(f"[Debug] Correct Answer: {correct_answer}")

    start_game()

# ============================
# Handle Wrong Guesses
# ============================
def guess_again(new_guess):
    global guesses, guess_button, guess_label, incorrect_label, ga, hint_label

    # Only allow if the guessing UI is active
    if not (count and count.visible):
        return

    # Defensive: Hide and remove any old guess_button and ga
    if guess_button:
        guess_button.visible = False
        guess_button = None
    if ga:
        ga.visible = False
        ga = None

    guesses.append(new_guess)

    if guess_label:
        guess_label.visible = False
        guess_label = None
    if incorrect_label:
        incorrect_label.visible = False
        incorrect_label = None
    if hint_label:
        hint_label.visible = False
        hint_label = None

    incorrect_label = Label("Incorrect guess. Keep trying!", 600, 200, size=30, font='Arial', align='center', fill='red')
    guess_label = Label(f"Previous Guesses: {guesses}", 600, 450, size=20, font='Arial', align='center')

    if new_guess < correct_answer:
        hint_label = Label("Try a higher number!", 600, 350, size=25, font='Arial', align='center', fill='green')
    elif new_guess > correct_answer:
        hint_label = Label("Try a lower number!", 600, 350, size=25, font='Arial', align='center', fill='red')

    guess_button = Rect(475, 600, 250, 50, fill='blue', border='black')
    ga = Label("Guess Again", 600, 625, size=30, fill='white', align='center')

# ============================
#  Main Mouse Handler
# ============================
def onMousePress(x, y):
    global guess, restart_button, out_of_range_label

    if button.hits(x, y):
        if out_of_range_label:
            out_of_range_label.visible = False
            out_of_range_label = None
        start_questions()

    elif 'button2' in globals() and button2 and button2.visible and button2.hits(x, y):
        if out_of_range_label:
            out_of_range_label.visible = False
            out_of_range_label = None
        guess = int(app.getTextInput("Guess a Number!").strip())
        if guess < min_num or guess > max_num:
            out_of_range_label = Label("Number not in range, guess again", 600, 400, size=30, font='Arial', align='center', fill='orange')
            return
        if guess == correct_answer:
            handle_correct_guess()
        else:
            hide_guess_ui()
            guess_again(guess)

    elif guess_button is not None and guess_button.visible and guess_button.hits(x, y):
        if out_of_range_label:
            out_of_range_label.visible = False
            out_of_range_label = None
        g = int(app.getTextInput("Guess Again").strip())
        if g < min_num or g > max_num:
            out_of_range_label = Label("Number not in range, guess again", 600, 400, size=30, font='Arial', align='center', fill='orange')
            return
        if g == correct_answer:
            handle_correct_guess()
        else:
            guess_again(g)

    elif restart_button and restart_button.visible and restart_button.hits(x, y):
        restart_game()

# ============================
# Correct Guess Handler
# ============================
def handle_correct_guess():
    global restart_button, counts, answer, ga, restart_text_label
    congrats.visible = True
    if answer:
        answer.visible = False
    answer = Label(f"The correct number was {correct_answer}", 600, 250, size=30, font='Arial', align='center', fill='black')
    hide_guess_ui()
    if restart_button:
        restart_button.visible = False
    if restart_text_label:
        restart_text_label.visible = False
    restart_button = Rect(475, 600, 250, 50, fill='orange', border='black')
    restart_text_label = Label("Restart Game", 600, 625, size=30, fill='white', align='center')
    if count:
        count.visible = False
    if counts:
        counts.visible = False
    counts = Label(f"Your range was: {min_num} to {max_num}", 600, 500, font='Arial', size=30, align='center')

def hide_guess_ui():
    global hint_label, guess_button, ga, guess_label, incorrect_label
    if 'button2' in globals() and button2:
        button2.visible = False
    if 'question' in globals() and question:
        question.visible = False
    if 'question2' in globals() and question2:
        question2.visible = False
    if guess_button:
        guess_button.visible = False
        guess_button = None
    if ga:
        ga.visible = False
        ga = None
    if guess_label:
        guess_label.visible = False
        guess_label = None
    if incorrect_label:
        incorrect_label.visible = False
        incorrect_label = None
    if hint_label:
        hint_label.visible = False
        hint_label = None

# ============================
#  Run the app
# ============================
cmu_graphics.run()