import random
from flask import Flask, render_template, request

app = Flask(__name__)

word_list = ["apple", "banana", "orange", "grape", "cherry"]

def get_word():
    word = random.choice(word_list)
    return word.upper()

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

@app.route('/')
def index():
    word = get_word()
    return render_template('index.html', word=word, hangman=display_hangman(6), word_completion="_" * len(word))

@app.route('/play', methods=['POST'])
def play():
    word = request.form['word'].upper()
    word_completion = request.form['word_completion']
    guessed_letters = request.form.getlist('guessed_letters[]')
    guessed_words = request.form.getlist('guessed_words[]')
    tries = int(request.form['tries'])
    guess = request.form['guess'].upper()

    if len(guess) == 1 and guess.isalpha():
        if guess in guessed_letters:
            message = f"You already guessed the letter {guess}"
        elif guess not in word:
            message = f"{guess} is not in the word."
            tries -= 1
            guessed_letters.append(guess)
        else:
            message = f"Good job, {guess} is in the word!"
            guessed_letters.append(guess)
            word_as_list = list(word_completion)
            indices = [i for i, letter in enumerate(word) if letter == guess]
            for index in indices:
                word_as_list[index] = guess
            word_completion = "".join(word_as_list)
            if "_" not in word_completion:
                return render_template('win.html', word=word)
    elif len(guess) == len(word) and guess.isalpha():
        if guess in guessed_words:
            message = f"You already guessed the word {guess}"
        elif guess != word:
            message = f"{guess} is not the word."
            tries -= 1
            guessed_words.append(guess)
        else:
            return render_template('win.html', word=word)
    else:
        message = "Not a valid guess."

    hangman = display_hangman(tries)

    if tries == 0:
        return render_template('lose.html', word=word)

    return render_template('play.html', word=word, hangman=hangman, word_completion=word_completion, message=message, tries=tries, guessed_letters=guessed_letters, guessed_words=guessed_words)

if __name__ == "__main__":
    app.run(debug=True)