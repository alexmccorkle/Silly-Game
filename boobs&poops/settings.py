import pygame

class Settings :
  def __init__(self) :  
    # Initializing the window
    self.win_height = 800
    self.win_width = 1000
    self.win = pygame.display.set_mode((self.win_width, self.win_height)) # Create a window

    spawn_x = 50 # Initial X position of the character
    spawn_y = 250 # Initial Y position of the character




