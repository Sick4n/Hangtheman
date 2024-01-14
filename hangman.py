import random
from sys import stdin, stdout

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

def main():
    words = load_words()
    word = random.choice(words)
    guessed_letters = []
    guessed_words = []
    lives = 6

    print("Welcome to Hangman!")

    while lives > 0:
        # Display the current state of the game
        print(display_hangman(lives))
        print("Guessed Letters: ", " ".join(guessed_letters))
        print("Guessed Words: ", " ".join(guessed_words))
        print("Word: ", get_display_word(word, guessed_letters))
        stdout.flush()
        # Take the player's guess
        guess = stdin.readline().strip().upper()

        # Check if the guess has already been made
        if guess in guessed_letters or guess in guessed_words:
            print(f"You already guessed {guess}!")
            continue

        # Handle a single letter guess
        if len(guess) == 1 and guess.isalpha():
            guessed_letters.append(guess)
            if guess in word:
                print(f"{guess} is in the word!")
                if has_guessed_all_letters(word, guessed_letters):
                    print(f"Congratulations! You guessed the word: {word}")
                    break
            else:
                print(f"{guess} is not in the word!")
                lives -= 1

        # Handle a word guess
        elif len(guess) == len(word) and guess.isalpha():
            guessed_words.append(guess)
            if guess == word:
                print(f"Congratulations! You guessed the word: {word}")
                break
            else:
                print(f"{guess} is not the word!")
                lives -= 1

        # Handle invalid guesses
        else:
            print("Invalid guess. Please try again.")

        # Check if the player has run out of lives
        if lives == 0:
            print("\n" * 30)  # Clear the output again
            print(display_hangman(lives))
            print(f"You ran out of lives. The word was {word}.")
            print("press any key to play again")
            stdin.readline().strip().upper()
            main()

if __name__ == "__main__":
    main()

