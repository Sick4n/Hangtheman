from flask import Flask, render_template, request, session
import random
app = Flask(__name__)
app.secret_key = "super secret key"

words = open("words.txt").readlines()
words = [word.strip().upper() for word in words]

def display_hangman(tries):
    stages = [
     '''
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        ''',
        # head, torso, both arms, and one leg
        '''
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / 
           -
        ''',
        # head, torso, and both arms
        '''
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |      
           -
        ''',
        # head, torso, and one arm
        '''
           --------
           |      |
           |      O
           |     \\|
           |      |
           |     
           -
        ''',
        # head and torso
        '''
           --------
           |      |
           |      O
           |      |
           |      |
           |     
           -
        ''',
        # head
        '''
           --------
           |      |
           |      O
           |    
           |      
           |     
           -
        ''',
        # initial empty state
        '''
           --------
           |      |
           |      
           |    
           |      
           |     
           -
        '''
    ]
    return stages[tries]


def get_display_word(word, guessed_letters):
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    return display_word

def has_guessed_all_letters(word, guessed_letters):
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True

def render_play(message, additional_context):
    context = {
        "message": message,
        "guessed_letters": session["guessed_letters"],
        "guessed_words": session["guessed_words"],
        "display_word": session["display_word"],
        "hangman": display_hangman(session["lives"])
        }
    context.update(additional_context)
    return render_template("play.html", **context)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def internal_error(error):
    # Log the error
    app.logger.error('Server Error: %s', (error))
    # Return a generic error message
    return "An internal error occurred. Please try again later.", 500

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "POST":
        guess = request.form["guess"]
        guess = guess.upper()
        message = ""
        if guess in session["guessed_letters"] or guess in session["guessed_words"]:
            message = f"You already guessed {guess}!"
            return render_play(message, {})

        if len(guess) == 1 and guess.isalpha():
            session["guessed_letters"].append(guess)
            session["display_word"] = get_display_word(session["word"], session["guessed_letters"])
            if guess in session["word"]:
                if has_guessed_all_letters(session["word"], session["guessed_letters"]):
                    return render_template("win.html", word=session["word"])
                message = f"{guess} is in the word!"
            else:
                message= f"{guess} is not in the word!"
                session["lives"] -= 1

        elif len(guess) == len(session["word"]) and guess.isalpha():
            session["guessed_words"].append(guess)
            if guess == session["word"]:
                return render_template("win.html", word=session["word"])
            else:
                message = f"{guess} is not the word!"
                session["lives"] -= 1
                
        elif guess.isalpha() == False:
            message = "That is not a valid letter or word."
            
        elif len(guess) != 1 and len(guess) != len(session["word"]):
            message = "The guess must be one letter or the same length as the word."

        if session["lives"] == 0:
            return render_template("lose.html", word=session["word"])

        return render_play(message, {})


    elif request.method == "GET":
        session["word"] = random.choice(words)
        session["guessed_letters"] = []
        session["guessed_words"] = []
        session["lives"] = 6
        session["display_word"] = get_display_word(session["word"], session["guessed_letters"])
        return render_play("Welcome to Hangman! Guess a letter or the whole word.", {})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
