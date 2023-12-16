# Name:Cheran Selvarajah and Bilal Malik
# Date: June 9th 2021
# Program: CLI Hangman
# Description: This is a command line based game called hangman.
#              You are initally given the option to choose a difficulty or themed version.
#              The instructions for the game are simple just like traditional hangman.
#              You are given a random word for which you must try and guess the word.
#              You can do so by either guesing single letters or words.
#              You have 6 wrong attempts until you loose the game.
#              Once you win or loose you are given a play again option.
#              This will either close the game or allow you to replay the game.

############################# IMPORTING LIBARIES, INITALIZING VARIABLES, INITIALIZING MUSIC AND SOUND EFFECTS ###############################################
import random
import pygame
import os
import time
from pygame import mixer
pygame.mixer.init()

#Initialize Variables and constants :
attempts = 0 #Initizalize number of attempts that user can try to guess word
mixer.music.load("background_music.mp3") # Importing the background music 
select_sound = pygame.mixer.Sound("select_sound.mp3") # Importing select, error, correct, incorrect, defeat, and victory sound effects
error_sound = pygame.mixer.Sound("error_sound.mp3")
correct_sound = pygame.mixer.Sound("correct_sound.mp3")
incorrect_sound = pygame.mixer.Sound("incorrect_sound.mp3")
defeat_sound = pygame.mixer.Sound("defeat_sound.mp3")
victory_sound = pygame.mixer.Sound("victory_sound.mp3")

# Background Music
mixer.music.set_volume(0.01) # Turning the volume of the background sounds to a set amount 
mixer.music.play(-1) # Making the background music play an infinite amount

# Setting the volume of the sound effects
select_sound.set_volume(0.02)
error_sound.set_volume(0.02)
correct_sound.set_volume(0.02)
incorrect_sound.set_volume(0.02)
defeat_sound.set_volume(0.02)
victory_sound.set_volume(0.02)

################################################### Instructions and welcoming ##########################################################

print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("Welcome to Hangman!")
print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")


# Prompting the user for their name at the start of the game
name = input("\nTell us about yourself, what is your name? ")
select_sound.play() # Select sound effect is played throughout the user's inputs for the setting

print("\nTake a few seconds to make sure this screen is in fullscreen mode.")
time.sleep(6)

#Initial welcoming message and instructions 
print("\nHello,", name + "!", "Welcome to Hangman!")
print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("The instructions to play hangman are fairly simple. \nYou will be given a random word and have to try to guess that word. You can do so by guessing letters or if you are confident, guessing the word itself.\
      \nYou only have a limited number of guesses so choose wisely! If the full body of the man is complete, he dies and you will lose.")
print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

######################################################### MODE SELECTION #############################################
def get_gamemodes():
  mode_validated = False #Variable used to ensure that the input for regular/themed version is validated
# While loop continuously asks user for input until valid input is entered
  while not mode_validated:
    get_mode = input("\nWould you like to play our regular game or play a themed version? Type REGULAR or THEMED to choose: ") # Prompting the user if they would like to play the regular or themed version
    
    if get_mode.upper() == "REGULAR": # If the user chose the regular version
      mode_validated = True # Becomes True when mode is validated, so while loop can exit
      difficulty_validated = False # States that the difficulty is not set
      select_sound.play()
      
# While loop continuously asks user for input until valid input is entered
      while not difficulty_validated: 
        get_version = input("\nWhat difficulty would you like? Type EASY, MEDIUM or HARD to choose: ") # Prompt the user for the difficulty
        # Validates the difficulty_validated variable to True once the user picks their choice of difficulty
        
        if get_version.upper() == "EASY": 
          select_sound.play()
          difficulty_validated = True
          
        elif get_version.upper() == "MEDIUM":
          select_sound.play()
          difficulty_validated = True
          
        elif get_version.upper() == "HARD":
          select_sound.play()
          difficulty_validated = True
          
        #Occurs if the user did not type either Easy, Medium, or Hard (invalid inputs)
        else:
          print("\nPlease input a valid input. Enter EASY, MEDIUM or HARD")
          error_sound.play()
          
    elif get_mode.upper() == "THEMED": #If the user chose the Themed version
      mode_validated = True #Becomes True when mode is validated, so while loop can exit
      theme_validated = False # States that the theme is not set
      select_sound.play()
      
# While loop continuously asks user for input until valid input is entered
      while not theme_validated: 
        get_version = input("\nWhat theme would you like? Type ANIME or POKEMON to choose: ") #Prompts the user if they would like to play with anime or pokemon names
      
        #Validates the theme_validated variable to True once the user decides their theme
        if get_version.upper() == "ANIME": 
          select_sound.play()
          theme_validated = True
          
        elif get_version.upper() == "POKEMON":
          select_sound.play()
          theme_validated = True
        # Occurs if the user did not type either Anime or Pokemon
        
        else:
            print("\nThat was an invalid input, please enter ANIME or POKEMON")
            error_sound.play()
    # Occurs if the user did not enter either Regular or Themed (invalid input)
    
    else:
      print("\nYour input was invalid, please enter REGULAR or THEMED")
      error_sound.play()
      
  return get_version # Returns the variable get_version for use in other functions
        
  
##################################### OBTAIN THE FILES ###############################################
def get_words(game_mode):
  if game_mode.upper() == "EASY": # If user inputted easy, input the easy_words file
    version = "easy_words.txt"

  elif game_mode.upper() == "MEDIUM": # If user inputted medium, input the medium_words file
    version = "medium_words.txt"

  elif game_mode.upper() == "HARD": # If user inputted hard, input the hard_words file
    version = "hard_words.txt"
  
  elif game_mode.upper() == "POKEMON": # If user inputted Pokemon, input the pokemon_words file
    version = "pokemon_words.txt"

  elif game_mode.upper() == "ANIME": # If user inputted easy, input the anime_words file
    version = "anime_words.txt"
    
#RANDOMIZE A WORD FROM THE FILE OF CHOICE    
  input_file = open(version, "r") 
  random_number = random.randint(1,90) # Choose a random number from 1-90
  
  # Number is specifically 1-90 as there are 90 words in the file
  # Picks a random word corresponding to the number chosen above and strips the spaces
  
  for  i in range (random_number):
    word = input_file.readline()
  word = word.strip("\n")
  return word # Returns the variable word for use in later code
  

##################################### APPEARANCE OF HANGMAN #############################################
def hangman_visual(attempts):
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[attempts]

############################################ FULL GAME CODE #########################################################
  
def main(word, get_version):
# Importing variables and arrays to be used
  os.system("cls") # Clears the python shell for all previous inputs
  alphabet = "abcdefghijklmnopqrstuvwxyz" 
  letters_guessed = []
  word_completion = []
  
  # Loops for the length of word and adds a "_" to represent each letter of the word
  for i in range (len(word)):
    word_completion.append("_")
    
  attempts = 6 # Amount of lives
  guessed = False 
  print("\n=-=-=-=-=-=-=-=-=-=-=-=- Let's Start! :) =-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
  
  while guessed == False and attempts > 0:
    guess = input("\nPlease enter one letter or the full word: ").lower()
    # If the user inputted a letter, the if statement below will run
    
    if len(guess) == 1:
      if guess not in alphabet: # Checks if the user has typed a letter
        print("\nYou have not entered a letter.")
        error_sound.play()
        
      elif guess in letters_guessed: # Checks if the user has already guessed that letter
        print("\nYou have already guessed that letter before")
        error_sound.play()
        
      elif guess not in word: # Checks if the user's guess is not in the word
        print("\nSorry, that letter is not part of the word :(")
        letters_guessed.append(guess)
        attempts -=1
        incorrect_sound.play()
        
      elif guess in word: # Checks if the user's guess is in the word
        print("\nWell done, that letter is in the word!")
        correct_sound.play()
        
        # For the length of the word, check which letter the input matches
        for i in range (len(word)):         
          if guess == word[i]:
            word_completion[i] = guess
            
        letters_guessed.append(guess) # Fills in the "_" with each guessed letter
        if word_completion.count("_") == 0: 
          guessed = True
        
    elif len(guess) !=1: # If the user's input is more than one letter
      guess_not_word = False #Variable used to check if the inputted word is valid
      
      # For the length of the word, check if each letter is in the alphabet
      for i in range(len(guess)):
        
        if guess[i] not in alphabet:
          guess_not_word = True # Set guess_not_word to True, as the word has invalid characters (characters other than letters)
          
      if guess_not_word == True: 
        print("\nYour input was invalid, please enter a WORD (only letters)") 
        error_sound.play()

      elif guess == word: #If the user's guess was the word they had to find
        
        for i in range (len(word)):
          word_completion[i] = word[i]          
          guessed = True
          
      else: # If all conditions are not met, execute the following code
        print("Sorry, that was not the correct word") 
        attempts -=1 # Remove one attempt
        incorrect_sound.play()
        
    time.sleep(2) # Delay the code for 2 seconds
    os.system("cls") # Clears pthon shell used for hangman_visuals

    # Print the model of the hangman from the function hangman_visual and print how many lives are left
    print(hangman_visual(attempts)) 
    print("You have", str(attempts), "lives left!")
    
    print_word = ""
    for i in range (len(word)):
      print_word += str(word_completion[i]) + " "
    print(print_word)

  # If all attempts are done, print the defeat screen and print the actual word
  if attempts == 0:
    print("\n=============================================================")
    print("                           DEFEAT!                              ")
    print("=============================================================")
    print("\nYou have lost, the actual word is", word)
    defeat_sound.play()
    
  # If the word is complete and there are more than 0 attempts, print the victory screen   
  else:
    print("\n=============================================================")
    print("                          VICTORY!                              ")
    print("=============================================================")
    print("\nCongratulations, you have guessed the word!")
    victory_sound.play()
    guessed = True # Guessed turns True once the word is complete
    
  play_again(get_version) # Play the function play_again

############################################ PLAY AGAIN ##################################################
def play_again(get_version):
  # Initialize Variables
  play_again = ""
  change_settings = ""
  # While loop continuously asks user for input until valid input is entered
  
  while play_again.lower() != "y" and play_again.lower() != "n":
    play_again = input("\nWould you like to play again? Y/N: ")
    
    if play_again.lower() == "y":
      select_sound.play()
      change_settings = input("\nWould you like to change the settings? Y/N: ")
      
      # While loop continuously asks user for input until valid input is entered
      while change_settings.lower() != "y" and change_settings.lower() != "n": 
        change_settings = input("\nWould you like to change the settings? Y/N: ") # Prompt for settings

      # If user entered y to change settings, restart the code from the function get_gamemodes
      if change_settings.lower() == "y":
        get_version = get_gamemodes()
        word = get_words(get_version)
        main(word, get_version)

      # If user entered n to change settings, restart the game from the function main  
      elif change_settings.lower() == "n":
        select_sound.play()
        word = get_words(get_version)
        main(word, get_version)
        
      else: # If user did not input either y or n, print an error message
        print("\n Your input is invalid, please type either Y or N") 
        error_sound.play()
      get_version = get_version
      
     # If user entered the letter n, exit the game and end the code 
    elif play_again.lower() == "n":
      select_sound.play()
      print("\nThank you for playing!") # Print an output message
      time.sleep(2) # Delay for 2 seconds before exiting the game
      
      # In the file hangman_ending, write a thank you for playing message
      output_message = "hangman_ending.txt"
      output_file = open(output_message, "w")
      output_file.write("Thank you for playing " + name + "!")
      exit() # Exit the game
      
    else: # If user did not input either y or n, print an error message
      print("\n Your input is invalid, please type either Y or N") 
      error_sound.play()


############################################################################################
# Calls for main functions
get_version = get_gamemodes()
word = get_words(get_version)
main(word, get_version)
############################################################################################

# DISCLAIMER: Pygames 2.0.X was used to create this code
              
