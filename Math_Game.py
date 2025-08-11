# Russell's really cool math game 

# Imports
import random
import numpy as np
import pygame
import sys
from button import Button
from pygame.locals import *

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_LIGHT = (170, 170, 170)
COLOR_DARK = (100, 100, 100)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
FPS = 30

# Initialize the constructor
pygame.init()

# Setting the screen Properties
screen_resolution = (720, 720)
screen = pygame.display.set_mode(screen_resolution)
caption = pygame.display.set_caption("Russell's Math Game")
background_colour = pygame.display.set_background(BLACK)

# Actually start the game
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.quit:
            pygame.quit()

    pygame.display.update()

# Code for Generating Background
class Projection:
    def __init__(self, WIDTH, HEIGHT)
        self.WIDTH = WIDTH
        self.HEGIHT = HEIGHT
        self.SCREEN = SCREEN
            
clock = pygame.time.Clock()

# Main Menu Screen
# Start Game Text
text = smallfont.render("START GAME", true, WHITE)

# High Scores text
text = smallfont.render("VIEW HIGH SCORES", true, WHITE)

# Render Quit Text
text = smallfont.render("QUIT", true, WHITE)

if event.type == pygame.MOUSEBUTTONDOWN
    if WIDTH/2 <= mouse[0] <= WIDTH/2+140 and height/2 <= mouse[1] <= height/2+40:
    pygame.quit()

# Main Game Screen


# Initialize the two numbers we want to add together
integer1 = randint(10,99)
integer2 = randint(10,99)

# This is the target value we're after
target_value = integer1 + integer2

# Initialize score
score = 0

# TO do
# Need to create some kind of function that creates a 60 second timer
# Each game state consists of a 60 second interval where you need to try correctly solve math problems.
# Once you solve a question correctly, a score variable gets incremented by + 1
# At the end of the game, you're asked to input your name, and your score gets saved back to a "high-scores" text file.
# Pressing 2 will print the .txt file to the screen in a formatted fashion
# Create virtual environment
# Implement if name == main convention
# Add to GitHub, create .gitignore file
# Refactor to use .pygame

# Function to run a game
def start_game():
    # Need something in here to Initialize a 60 second timer - would be cool to see it countdown togetherer
    answer = input(printf("What's {integer1} + {integer2}"))
    if answer != target_value:
        print("Not quite right, try again")
    elif answer == target_value:
        print("Nice, have another one")
        Score += 100

# Function to print high-scores
def high_scores()
    file.open('high-scores')
    print('high-scores') # I don't really know how to open a file and then print it to terminal
    nav_input = input(print("Press 5 to navigate back"))
if nav_input = 5:
    Main_Menu()

# This controls user movement around the game
def Main_Menu()
    if control_input = 1:
        start_game()
    elif control_input = 2:
        high_scores()
    elif:
        control_input = 3
        exit() /# This just needs to break the program, not sure how to do that, but oh well.
