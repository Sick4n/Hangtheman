from flask import Flask, render_template, jsonify, request, session
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
    return display_word.strip()


def has_guessed_all_letters(word, guessed_letters):
    return all(letter in guessed_letters for letter in word)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/guess", methods=["POST"])
def guess():
    session.setdefault('guessed_letters', [])
    session.setdefault('guessed_words', [])
    session.setdefault('lives', 6)
    session.setdefault('word', '')

    guess = request.json.get('guess', '').upper()
    message = ""

    if len(guess) == 1 and guess.isalpha():
        if guess in session['guessed_letters']:
            message = f"You already guessed the letter {guess}!"
        else:
            session['guessed_letters'].append(guess)
            if guess in session['word']:
                message = f"Good guess! {guess} is in the word!"
            else:
                message = f"Sorry, {guess} is not in the word."
                session['lives'] -= 1

    elif len(guess) == len(session['word']) and guess.isalpha():
        if guess in session['guessed_words']:
            message = f"You already guessed the word {guess}!"
        else:
            session['guessed_words'].append(guess)
            if guess == session['word']:
                return jsonify({"game_over": True, "win": True, "word":
                                session['word'], "message":
                                "Congratulations! You guessed the word!"})
            else:
                message = f"Sorry, {guess} is not the word."
                session['lives'] -= 1

    else:
        message = "Invalid guess. Try again."

    session['display_word'] = get_display_word(session['word'],
                                               session['guessed_letters'])
    if has_guessed_all_letters(session['word'], session['guessed_letters']):
        return jsonify({"game_over": True, "win": True,
                        "word": session['word'],
                        "message": "Congratulations! You guessed the word!",
                        "display_word": session['display_word']})

    if session['lives'] <= 0:
        hangman = display_hangman(session['lives'])
        return jsonify({"game_over": True, "win": False,
                        "word": session['word'],
                        "message": "You have run out of lives!",
                        "hangman": hangman})

    hangman = display_hangman(session['lives'])

    return jsonify({
        "message": message,
        "guessed_letters": session['guessed_letters'],
        "guessed_words": session['guessed_words'],
        "display_word": session['display_word'],
        "hangman": hangman,
        "game_over": False
    })


@app.route("/restart", methods=["POST"])
def restart():
    session['word'] = random.choice(words)
    session['guessed_letters'] = []
    session['guessed_words'] = []
    session['lives'] = 6
    session['display_word'] = get_display_word(session['word'],
                                               session['guessed_letters'])
    return jsonify({
        "message": "New game started! Guess a letter or the whole word.",
        "guessed_letters": session['guessed_letters'],
        "guessed_words": session["guessed_words"],
        "display_word": session['display_word'],
        "hangman": display_hangman(session['lives'])
        })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
