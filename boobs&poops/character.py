import pygame
from settings import Settings

class Character :
  def __init__(self, settings) :
    # Character Attributes
    self.x = settings.spawn_x # Initial x position
    self.y = settings.spawn_y # Initial y position
    self.width = 75 # Width of the character
    self.height = 75 # Height of the character
    self.vel = settings.win_width * 0.01 # Speed of the character

    # Movement Variables:
    self.gravity = 3
    self.jump_strength = 40
    self.vertical_speed = 0
    self.in_air = False
    self.movement_keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE]

    # State Variables: 
    self.sprite_facing = "right"
    self.sprite_state = "standing"

    # Load images: 
    # Right facing sprites
    self.sprite_standing_R = pygame.image.load("./images/sprite_standing_R.png")
    self.sprite_standing_R = pygame.transform.scale(self.sprite_standing_R, (self.width, self.height))
    self.sprite_jump_R = pygame.image.load("./images/sprite_jump_R.png")
    self.sprite_jump_R = pygame.transform.scale(self.sprite_jump_R, (self.width, self.height))
    self.sprite_landing_R = pygame.image.load("./images/sprite_landing_R.png")
    self.sprite_landing_R = pygame.transform.scale(self.sprite_landing_R, (self.width, self.height))
    self.sprite_move_R = pygame.image.load("./images/sprite_move_R.png")
    self.sprite_move_R = pygame.transform.scale(self.sprite_move_R, (self.width, self.height))

    # Left facing sprites
    self.sprite_standing_L = pygame.image.load("./images/sprite_standing_L.png")
    self.sprite_standing_L = pygame.transform.scale(self.sprite_standing_L, (self.width, self.height))
    self.sprite_jump_L = pygame.image.load("./images/sprite_jump_L.png")
    self.sprite_jump_L = pygame.transform.scale(self.sprite_jump_L, (self.width, self.height))
    self.sprite_landing_L = pygame.image.load("./images/sprite_landing_L.png")
    self.sprite_landing_L = pygame.transform.scale(self.sprite_landing_L, (self.width, self.height))
    self.sprite_move_L = pygame.image.load("./images/sprite_move_L.png")
    self.sprite_move_L = pygame.transform.scale(self.sprite_move_L, (self.width, self.height))

  def handle_movement(self,keys, settings) : 
    # Jumping: 
    if keys[pygame.K_w] and not self.in_air: # If the character is not in the air and the W key is pressed
      self.sprite_state = "jumping"
      self.vertical_speed = -self.jump_strength
      self.in_air = True
    elif not keys [pygame.K_w] :
      if self.vertical_speed < 0 : # If the character is moving upwards
        self.vertical_speed = 0 

      # Apply vertical speed and gravity
      self.y += self.vertical_speed
      self.vertical_speed += self.gravity 

      # Horizontal Movement:

      # Right Movement
    if keys[pygame.K_d] and self.x < settings.win_width - self.width :
      self.x += self.vel
      self.sprite_facing = "right"
      

    
