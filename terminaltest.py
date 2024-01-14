import random
from pyxtermjs import PyxtermJs

def load_words():
    with open("words.txt") as file:
        return [word.strip().upper() for word in file.readlines()]

def display_hangman(tries):
    stages = [  # final state: head, torso, both arms, and both legs
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


# Define the Hangman game logic as a function
def hangman_game():
    words = load_words()
    word = random.choice(words)
    guessed_letters = []
    guessed_words = []
    lives = 6

    output = []

    output.append("Welcome to Hangman!")

    while lives > 0:
        # Display the current state of the game
        output.append(display_hangman(lives))
        output.append("Guessed Letters: " + " ".join(guessed_letters))
        output.append("Guessed Words: " + " ".join(guessed_words))
        output.append("Word: " + get_display_word(word, guessed_letters))

        # Take the player's guess
        guess = input("Guess a letter or the word: ").upper().strip()

        # Check if the guess has already been made
        if guess in guessed_letters or guess in guessed_words:
            output.append(f"You already guessed {guess}!")
            continue

        # Handle a single letter guess
        if len(guess) == 1 and guess.isalpha():
            guessed_letters.append(guess)
            if guess in word:
                output.append(f"{guess} is in the word!")
                if has_guessed_all_letters(word, guessed_letters):
                    output.append(f"Congratulations! You guessed the word: {word}")
                    break
            else:
                output.append(f"{guess} is not in the word!")
                lives -= 1

        # Handle a word guess
        elif len(guess) == len(word) and guess.isalpha():
            guessed_words.append(guess)
            if guess == word:
                output.append(f"Congratulations! You guessed the word: {word}")
                break
            else:
                output.append(f"{guess} is not the word!")
                lives -= 1

        # Handle invalid guesses
        else:
            output.append("Invalid guess. Please try again.")

        # Check if the player has run out of lives
        if lives == 0:
            output.append("\n" * 30)  # Clear the output again
            output.append(display_hangman(lives))
            output.append(f"You ran out of lives. The word was {word}.")

    return "\n".join(output)

# Create a PyxtermJs instance
pyxterm = PyxtermJs()

# Define a function that will be called from the web page
def start_game():
    game_output = hangman_game()
    pyxterm.write(game_output)

# Embed the PyxtermJs instance in a web page
html_content = pyxterm.html(
    title="Hangman Game",
    on_ready="start_game()",
)

# Create an HTML file with the PyxtermJs content
with open("hangman_webapp.html", "w") as html_file:
    html_file.write(html_content)

