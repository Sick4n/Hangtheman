# Hangman Application
## Introduction

Welcome to the Hangman Application, a web-based game designed to provide a fun and interactive way to play the classic game of Hangman. This application is built using Flask, a Python web framework, and is deployed on Render for easy accessibility. The game allows players to guess letters or the word itself, with a visual representation of the hangman as the game progresses.

![New Game](/images/new.png)

## Contents

* Introduction
* Features
* Technologies Used
* How to Play
* Testing
* Deployment
* Future Enhancements
* Acknowledgements

## Features

* Interactive Hangman Display: Visual representation of the hangman that updates with each guess.
* Guess Tracking: Keeps track of guessed letters and words.
* Game Over Indication: Informs the player when the game is over, displaying a win or lose message.
* New Game Option: Allows players to easily start a new game.
![Game lost](/images/lose.png)
* Keyboard Accessibility: Supports keyboard input for guessing letters and words.

## Technologies Used

* Flask: A lightweight WSGI web application framework in Python.
* HTML/CSS: For structuring and styling the web page.
* JavaScript (jQuery): To make the game interactive and handle user input.
* Render: A cloud service used for deploying the application.
* Git and GitHub: For version control and repository hosting.

## How to Play

* Open the application in a web browser.
* Guess a letter or the entire word using the input field.
* The hangman and guessed letters/words will update based on your input.
* The game ends either when you guess the word correctly or run out of lives.
* Press any key or click the screen to start a new game.

![Game lost](/images/incorrect.png)

## Testing

The application has been rigorously tested for functionality and usability. Testing scenarios included:

* Guessing correct and incorrect letters.
* Guessing the complete word correctly and incorrectly.
* Testing on different browsers and devices.
* Ensuring the game restarts correctly.

## Deployment

The Hangman Application is deployed on Render, following these steps:

* Set up a Render account and link it to the GitHub repository.
* Configure the Render settings to match the application requirements.
* Deploy the application, making it accessible via a public URL.

## Future Enhancements

* Difficulty Levels: Introducing various difficulty levels to cater to a wider range of players.
* Leaderboard: Implementing a leaderboard to track high scores and encourage competition.
* Word Categories: Adding different categories of words for players to choose from.
* Multiplayer Mode: Enabling multiple players to play against each other.

## Dificulties/Bugs

### Transition from Hidden Inputs to Flask Session Variables:
Initially, the game's state was managed using hidden HTML inputs. This method posed security concerns and limited control over game state management. The transition to Flask session variables offered a more secure and robust solution, streamlining state management across different game stages.

### Input Validation Errors:
The game initially accepted non-alphabetic characters and multiple letters as valid guesses, leading to inconsistent gameplay. This was rectified by implementing stricter input validation checks in the Flask backend, ensuring that only single alphabetic characters were accepted as valid guesses.

### Incorrect Hangman Stage Rendering:
Initially, there was an issue where the hangman's visual stage wasn't updating correctly according to the number of incorrect guesses. This was due to a mismatch between the guess count and the corresponding hangman stage in the display_hangman function. The logic had to be carefully adjusted to ensure that each incorrect guess accurately reflected the correct stage of the hangman.

## Acknowledgements

Special thanks to the following:

* Code Institute: For providing resources and support in the development of this project.
* Community Support: Fellow developers and mentors who provided feedback and suggestions.
