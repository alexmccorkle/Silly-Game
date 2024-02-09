import pygame
import random

import os 

os.chdir("/Users/alexmccorkle/Desktop/boobs&poops") # Change the current working directory to the directory where the file is located
print(os.getcwd())


pygame.init()
pygame.font.init() # Initialize the font module
pygame.mixer.init() # Initialize the mixer module
font = pygame.font.SysFont('arial', 30) # Create a font object


def reset_game_state():
    global health, score, poops_avoided, boobs_avoided, level, total_time
    global falling_objects, falling_hearts, rolling_objects, vel, jump_strength
    global x, y, sprite_state, sprite_facing, current_sprite, character_rect
    global platform_rect, world_objects, frame_counter, damage_cooldown, heal_cooldown
    global run, dead

    health = 100
    score = 0
    poops_avoided = 0
    boobs_avoided = 0
    level = 1
    total_time = 0
    falling_objects = []
    falling_hearts = []
    rolling_objects = []
    vel = win_width * 0.01
    jump_strength = 25
    x = 50
    y = 250
    sprite_state = 'standing'
    sprite_facing = 'right'
    current_sprite = sprite_standing_R
    character_rect = pygame.Rect(x, y, (width-5), (height-5))
    platform_rect = pygame.Rect(0, platform_y, platform_soil.get_width(), platform_soil.get_height())
    world_objects = [platform_rect,]
    frame_counter = 0
    damage_cooldown = 0
    heal_cooldown = 0
    pygame.time.set_timer(DROP_EVENT, 2000)
    pygame.time.set_timer(DROP_EVENT2, drop_interval)
    run = True
    dead = False
    print("Game Reset")

class FallingObject : 
  def __init__(self, x, y, width, height, speed, poop):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.speed = speed
    self.poop = poop
    self.rect = self.poop.get_rect(topleft=(x, y))

  def update(self) :
    self.y += self.speed
    self.rect.y = self.y - 10

  def draw (self, win) :
    win.blit(self.poop, (self.x, self.y))

class FallingHealth : 
  def __init__(self, width, height, heart):
    self.x = random.randint(0, win_width - 100)
    self.y = 0
    self.width = width
    self.height = height
    self.speed = 4
    self.heart = heart
    self.rect = self.heart.get_rect(topleft=(self.x, self.y))

  def update(self) :
    self.y += self.speed
    self.rect.y = self.y

  def draw (self, win) :
    win.blit(self.heart, (self.x, self.y))

class RollingObject :
  def __init__(self, x, y, width, height, speed, boob):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.speed = speed
    self.boob = boob
    self.rect = self.boob.get_rect(topleft=(x, y))

  def update(self) :
    self.x -= self.speed
    self.rect.x = self.x - 5

  def draw (self, win) :
    win.blit(self.boob, (self.x, self.y))

def get_high_score() :
  try:
    with open("high_score.txt", "r") as file:
      high_score = file.read()
      return int(high_score) if high_score else 0
  except FileNotFoundError:
    return 0
  
def update_high_score(score) :
  with open("high_score.txt", "w") as file:
    file.write(str(score))
    print("High Score Updated")
  
high_score = get_high_score()


# Initializing the window and the character: 
win_height = 800
win_width = 1000
win = pygame.display.set_mode((win_width, win_height)) # Create a window


x = 50 # Initial X position of the character
y = 250 # Initial Y position of the character
width = 75 # Width of the character
height = 75 # Height of the character
vel = win_width * 0.01 # Speed of the character
health = 100 # Health of the character

# Game Variables:
total_time = 0 # Total time the character has survived
level = 1 # Level of the game
poops_avoided = 0 # Number of poops avoided
boobs_avoided = 0 # Number of boobs avoided
score = 0


# Movement Variables:
gravity = 2 # Gravity of the character
jump_strength = 25 # Jump strength of the character
in_air = False # Variable to check if the character is in the air
vertical_speed = 0 # The vertical speed of the character
movement_keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d] # Keys that can be used to move the character
frame_counter = 0 # Counter to keep track of the frames
damage_cooldown = 0 # Cooldown for the damage animation
heal_cooldown = 0 # Cooldown for the heal animation


# Sounds:
# Music:
background_music = pygame.mixer.music.load("./sounds/music.mp3")
pygame.mixer.music.play(-1) # Play the music on loop

# Sound Effects:
splat1 = pygame.mixer.Sound("./sounds/splat1.mp3")
splat2 = pygame.mixer.Sound("./sounds/splat2.mp3")
crunch1 = pygame.mixer.Sound("./sounds/crunch1.mp3")
fart_sound = pygame.mixer.Sound("./sounds/fart.mp3")
squish1 = pygame.mixer.Sound("./sounds/squish1.mp3")
grunt1 = pygame.mixer.Sound("./sounds/grunt1.mp3")
grunt2 = pygame.mixer.Sound("./sounds/grunt2.mp3")
grunt1.set_volume(0.3)
grunt2.set_volume(0.3)

splat_sounds = [splat1, splat2]
squish_sounds = [squish1]
consumable_sounds = [crunch1]
character_sounds = [grunt1, grunt2]




#Images/Models:

# Background:
bg = pygame.image.load("./images/background.jpg")
bg = pygame.transform.scale(bg, (win_width, win_height))



# Falling/Moving Objects and Events:
DROP_EVENT = pygame.USEREVENT + 1
DROP_EVENT2 = pygame.USEREVENT + 2
drop_interval = random.randint(10000,20000) # Time interval between falling objects

pygame.time.set_timer(DROP_EVENT, 2000) # Drop an object every 2s
pygame.time.set_timer(DROP_EVENT2, drop_interval) # Drop an object every 20-30s
falling_objects = [] # List of falling objects
rolling_objects = [] # List of rolling objects
falling_hearts = [] # List of falling hearts

# Poop:
poop_x, poop_y = 75, 75

poop1 = pygame.image.load("./images/poop.png")
poop1 = pygame.transform.scale(poop1, (poop_x, poop_y))
poop2 = pygame.image.load("./images/poop2.png")
poop2 = pygame.transform.scale(poop2, (poop_x, poop_y))
poop3 = pygame.image.load("./images/poop3.png")
poop3 = pygame.transform.scale(poop3, (poop_x, poop_y))

# Boob:
boob_x, boob_y = 75, 75

boob1 = pygame.image.load("./images/boob1.png")
boob1 = pygame.transform.scale(boob1, (boob_x, boob_y))
boob2 = pygame.image.load("./images/boob2.png")
boob2 = pygame.transform.scale(boob2, (boob_x, boob_y))
boob3 = pygame.image.load("./images/boob3.png")
boob3 = pygame.transform.scale(boob3, (45, 45))

# Health:
heart_width, heart_height = 75, 75
heart_sprite = pygame.image.load("./images/heart.png")
heart_sprite = pygame.transform.scale(heart_sprite, (heart_width, heart_height))

# TEXT/OVERLAYS:

# Health Bar:
health_bar_length = 300  # The maximum length of the health bar
health_bar_height = 35  # The height of the health bar
health_bar_color = (255, 0, 0)  # The color of the health bar
health_bar_color2 = (50,205,50)  # The color of the health bar
health_bar_bg_color = (192, 192, 192)  # The color of the health bar background
margin_right = 350  # The margin from the right side of the window
health_bar_position = (win_width-health_bar_length - margin_right, 50)  # The position of the health bar

# Game Over:
game_text = font.render("Game ", True, (255, 0, 0))
over_text = font.render("ver", True, (255, 0, 0))

shift_amount = 50 # Amount to shift the text to the right
scale_factor = 2 # Scale factor for the text

# Game Title:
# Render the words and the "&" sign
top_word = font.render("boobs", True, (255, 255, 255))
bottom_word = font.render("poops", True, (255, 255, 255))
and_sign = font.render("&", True, (255, 255, 255))

# Scaling:
game_text = pygame.transform.scale(game_text, (game_text.get_width() * scale_factor, game_text.get_height() * scale_factor))
boob3 = pygame.transform.scale(boob3, (boob3.get_width() * scale_factor, boob3.get_height() * scale_factor))
over_text = pygame.transform.scale(over_text, (over_text.get_width() * scale_factor, over_text.get_height() * scale_factor))

top_word = pygame.transform.scale(top_word, (top_word.get_width() * scale_factor, top_word.get_height() * scale_factor))
bottom_word = pygame.transform.scale(bottom_word, (bottom_word.get_width() * scale_factor, bottom_word.get_height() * scale_factor))
and_sign = pygame.transform.scale(and_sign, (and_sign.get_width() * scale_factor, and_sign.get_height() * scale_factor))  




# Platform: 
platform_soil = pygame.image.load("./images/platform_soil.png")
platform_height = 75
platform_soil = pygame.transform.scale(platform_soil, (win_width, platform_height))
platform_y = win_height - platform_height


# Character Sprites :
  # Right facing sprites
sprite_standing_R = pygame.image.load("./images/sprite_standing_R.png")
sprite_standing_R = pygame.transform.scale(sprite_standing_R, (width, height))
sprite_jump_R = pygame.image.load("./images/sprite_jump_R.png")
sprite_jump_R = pygame.transform.scale(sprite_jump_R, (width, height))
sprite_landing_R = pygame.image.load("./images/sprite_landing_R.png")
sprite_landing_R = pygame.transform.scale(sprite_landing_R, (width, height))
sprite_move_R = pygame.image.load("./images/sprite_move_R.png")
sprite_move_R = pygame.transform.scale(sprite_move_R, (width, height))
sprite_move_R2 = pygame.image.load("./images/sprite_move_R2.png")
sprite_move_R2 = pygame.transform.scale(sprite_move_R2, (width, height))


  # Left facing sprites
sprite_standing_L = pygame.image.load("./images/sprite_standing_L.png")
sprite_standing_L = pygame.transform.scale(sprite_standing_L, (width, height))
sprite_jump_L = pygame.image.load("./images/sprite_jump_L.png")
sprite_jump_L = pygame.transform.scale(sprite_jump_L, (width, height))
sprite_landing_L = pygame.image.load("./images/sprite_landing_L.png")
sprite_landing_L = pygame.transform.scale(sprite_landing_L, (width, height))
sprite_move_L = pygame.image.load("./images/sprite_move_L.png")
sprite_move_L = pygame.transform.scale(sprite_move_L, (width, height))
sprite_move_L2 = pygame.image.load("./images/sprite_move_L2.png")
sprite_move_L2 = pygame.transform.scale(sprite_move_L2, (width, height))

  # Sprite Effects : 
sprite_damage = pygame.image.load("./images/sprite_damage.png")
sprite_damage = pygame.transform.scale(sprite_damage, (width, height))
sprite_damage_L = pygame.image.load("./images/sprite_damage_L.png")
sprite_damage_L = pygame.transform.scale(sprite_damage_L, (width, height))
sprite_dead = pygame.image.load("./images/sprite_dead.png")
sprite_dead = pygame.transform.scale(sprite_dead, (width, height))
sprite_heal = pygame.image.load("./images/sprite_heal.png")
sprite_heal = pygame.transform.scale(sprite_heal, (width, height))
sprite_heal_L = pygame.image.load("./images/sprite_heal_L.png")
sprite_heal_L = pygame.transform.scale(sprite_heal_L, (width, height))


#State Variables:
clock = pygame.time.Clock() # Create a clock to manage FPS/Time
sprite_state = 'standing' # The default sprite of the character
sprite_facing = 'right' # The default direction the character is facing
current_sprite = sprite_standing_R # The default sprite of the character

# Collision:
character_rect = pygame.Rect(x, y, (width-5), (height-5)) # Create a rectangle to represent the character
platform_rect = pygame.Rect(0, platform_y, platform_soil.get_width(), platform_soil.get_height()) # Create a rectangle to represent the platform

world_objects = [platform_rect,]



def show_start_menu():
  menu_run = True
  keys = pygame.key.get_pressed()

  while menu_run :


    for event in pygame.event.get() :
      if event.type == pygame.QUIT :
        pygame.quit()
      
      if event.type == pygame.KEYDOWN :
        if event.key == pygame.K_SPACE :
          menu_run = False
        if event.key == pygame.K_ESCAPE :
          pygame.quit()
      if event.type == pygame.MOUSEBUTTONDOWN :
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if play_button.collidepoint(mouse_x, mouse_y) :
          menu_run = False

    # Draw the start menu
    win.fill((0, 0, 0)) # Fill the window with black




    # Calculate the positions
    top_word_x = win_width / 2 - top_word.get_width() / 2 - 20
    top_word_y = win_height / 2 - top_word.get_height() + 38  # Adjust the "- 12" as needed
    bottom_word_x = win_width / 2 - bottom_word.get_width() / 2  - 20 # Adjust the "+ 1" as needed
    bottom_word_y = win_height / 2
    and_sign_x = win_width / 2 + max(top_word.get_width(), bottom_word.get_width()) / 2 - 25  # Adjust the "+ 10" as needed
    and_sign_y = win_height / 2 - and_sign.get_height() / 2 + 20  # Adjust the "+ 20" as needed

    # Blit the words and the "&" sign onto the screen
    win.blit(top_word, (top_word_x, top_word_y))
    win.blit(bottom_word, (bottom_word_x, bottom_word_y))
    win.blit(and_sign, (and_sign_x, and_sign_y))
    # Play Button: 
    button_width = 200
    button_height = 50
    button_x = win_width / 2 - button_width / 2
    button_y = win_height / 2 + 150
    button_color = (0, 255, 0)
    play_button = pygame.draw.rect(win, button_color, (button_x, button_y, button_width, button_height))

    # Draw the button text
    button_text = font.render("Play", True, (255, 255, 255))
    win.blit(button_text, (button_x + button_width / 2 - button_text.get_width() / 2, button_y + button_height / 2 - button_text.get_height() / 2))

    # Show Highscore:
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    win.blit(high_score_text, (10, 10))

    pygame.display.update()

show_start_menu()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

run = True # Variable to keep our main loop running
dead = False # Variable to check if the character is dead

while run : # Our main loop
  restart = False # Variable to check if the game is restarted

  while dead : # If the character is dead
    if score > high_score:
      high_score = score
      update_high_score(high_score)

    for event in pygame.event.get() :
      if event.type == pygame.KEYDOWN :
        if event.key == pygame.K_SPACE :
          reset_game_state()
          restart = True
        elif event.key == pygame.K_ESCAPE :
          pygame.quit()

      elif event.type == pygame.MOUSEBUTTONDOWN :
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if play_again.collidepoint(mouse_x, mouse_y) :
          reset_game_state()
          restart = True
      if event.type == pygame.QUIT :
        pygame.quit()
    if restart :
      break # Ends the 'while dead' loop when pressing R
    
    pygame.display.update()

    # GAME OVER SCREEN START:
    # ________________________________________________________________________________________________________________
    # ________________________________________________________________________________________________________________

    # Fill the window with black
    win.fill((0, 0, 0))

    # Game Over Text:
    game_text_x = win_width / 2 - game_text.get_width() / 2 - boob3.get_width() / 2 - shift_amount
    game_text_y = win_height / 2 - game_text.get_height() / 2
    over_text_x = game_text_x + game_text.get_width() + boob3.get_width()
    over_text_y = win_height / 2 - over_text.get_height() / 2
    o_image_x = game_text_x + game_text.get_width()
    o_image_y = win_height / 2 - boob3.get_height() / 2

    win.blit(game_text, (game_text_x, game_text_y))
    win.blit(boob3, (o_image_x, o_image_y))
    win.blit(over_text, (over_text_x, over_text_y))

    # Final Score:
    final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))
    win.blit(final_score, (win_width / 2 - final_score.get_width() / 2, win_height / 2 + final_score.get_height() + 50 / 2))

    # High Scores:
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    win.blit(high_score_text, (10, 10))


  
    # Button :
    button_width = 200
    button_height = 50
    button_x = win_width / 2 - button_width / 2
    button_y = win_height / 2 + 150
    button_color = (0, 255, 0)
    play_again = pygame.draw.rect(win, button_color, (button_x, button_y, button_width, button_height))

    # Draw the button text
    button_text = font.render("Play Again", True, (255, 255, 255))
    win.blit(button_text, (button_x + button_width / 2 - button_text.get_width() / 2, button_y + button_height / 2 - button_text.get_height() / 2))
    
    # GAME OVER SCREEN END
  # ________________________________________________________________________________________________________________
  # ________________________________________________________________________________________________________________
    

  if not run : 
    break # Ends the main loop when run is False

  # MAIN GAME LOOP:
  # ________________________________________________________________________________________________________________
  # ________________________________________________________________________________________________________________
  # ________________________________________________________________________________________________________________


  frame_counter += 1 # Increment the frame counter
  # win.fill((0, 0, 0)) # Fill the window with black
  win.blit(bg, (0, 0)) # Background
  clock.tick(60) # FPS of our game = 60
  elapsed_time = clock.get_time() # Get the time elapsed since the last frame
  total_time += elapsed_time # Increment the total time


  if total_time > level * 20000 :
    level += 1
    print("Level: ", level)



  # Event Handling:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False # Stop the loop

    if event.type == DROP_EVENT: # FALLING POOP!
      for _ in range(level) :
        fall_position = random.randint(0, win_width - 100)
        fall_speed = random.randint(3, level + 4)
        poop_sprite = random.choice([poop1, poop2, poop3])
        falling_objects.append(FallingObject(fall_position, 0, 100, 100, fall_speed, poop_sprite))

      if level >= 5 :
        rolling_object_x = win_width
        rolling_object_vel = random.randint(4, 6)
        rolling_object_sprite = random.choice([boob1, boob2])
        rolling_objects.append(RollingObject(rolling_object_x, (platform_y-height), 100, 100, rolling_object_vel, rolling_object_sprite))

    if event.type == DROP_EVENT2 : # Health Drop
      heart = heart_sprite
      falling_hearts.append(FallingHealth(heart_width, heart_height, heart))





  # Movement rules:
  keys = pygame.key.get_pressed() # Get the keys pressed by the user

  # Jumping
  if keys[pygame.K_w] and in_air == False : # If the user presses the jump key
    sprite_state = 'jump'
    vertical_speed = -jump_strength # The character goes up
    in_air = True
    random.choice(character_sounds).play()
  elif not keys[pygame.K_w]:
    if vertical_speed < 0:  
      vertical_speed = 0

  # Apply vertical speed and gravity
  y += vertical_speed
  vertical_speed += gravity   

  # Check if the character is falling
  if in_air and vertical_speed > 0 :    
    sprite_state = 'land' 


  # Gravity
  if character_rect.colliderect(platform_rect):
    in_air = False
    if vertical_speed > 0: # If the character is falling
      y = platform_rect.top - character_rect.height + 8 # The character is on the platform
      vertical_speed = 0

  # Left
  if keys[pygame.K_a] and x > 0 :  
    x-=vel
    sprite_facing = 'left'
    if character_rect.colliderect(platform_rect) :
      sprite_state = 'moving'
  # Right
  if keys[pygame.K_d] and x < win_width - width:
    x+=vel
    sprite_facing = 'right'
    if character_rect.colliderect(platform_rect) :
      sprite_state = 'moving'

  # Standing
  elif not any(keys[key] for key in movement_keys) and character_rect.colliderect(platform_rect):
    sprite_state = 'standing'

  # Update Character Rectangle: 
  character_rect.x = x
  character_rect.y = y

  # Collision Rules:
  
  # Platform:
  for object in world_objects : 
    if character_rect.colliderect(object) : # If the character is colliding with the object
      y = object.y - (height - 8) # The character is on the platform

  # Falling Objects:
  # Poops:
  for obj in falling_objects[:] : # A copy of the list to avoid errors
    if character_rect.colliderect(obj.rect) and dead == False and damage_cooldown <= 0:
      health -= 10
      damage_cooldown = 25
      sprite_state = 'damaged'
      falling_objects.remove(obj) # Remove the object from the list after it hits the character
      random.choice(splat_sounds).play()
    if character_rect.colliderect(obj.rect) and health <= 0 :
      sprite_state = 'dead'
      dead = True # The character is dead
      vel = 0
      jump_strength = 0
      fart_sound.play()
    if obj.y > win_height : # If the object is out of the window
      falling_objects.remove(obj) # Remove the object from the list
      poops_avoided += 1 # Increment the number of poops avoided
      score += 1

  # Hearts:
  for obj in falling_hearts[:] :
    if character_rect.colliderect(obj.rect) and not dead and damage_cooldown <= 0:
        health += 20
        heal_cooldown = 25
        sprite_state = 'heal'
        print("Healed!")
        if health > 100 :
          health = 100
        falling_hearts.remove(obj)
        random.choice(consumable_sounds).play()
    if obj.y > win_height :
      falling_hearts.remove(obj)

  # Rolling Objects:
  # Boobs:
  for obj in rolling_objects[:] :
    if character_rect.colliderect(obj.rect) and dead == False:
      health -= 20
      heal_cooldown = 50
      sprite_state = 'heal'
      if health <= 0 :
        sprite_state = 'dead'
        dead = True
        vel = 0
        jump_strength = 0 
      else:
        sprite_state = 'heal'
      rolling_objects.remove(obj) # Remove the object from the list after it hits the character
      random.choice(squish_sounds).play()
    if obj.x < 0 :
      rolling_objects.remove(obj) # Remove the object from the list when it is out of the window
      boobs_avoided += 1 # Increment the number of boobs avoided
      score += 1

      


  
  # Active Sprites:
  

  if heal_cooldown > 0: # If I've been healed
    if sprite_facing == 'right' : # and I'm facing right
      current_sprite = sprite_heal # then I show the right facing sprite
    else :
      current_sprite = sprite_heal_L
    heal_cooldown -= 1

  elif damage_cooldown > 0:
    if sprite_facing == 'right' :
      current_sprite = sprite_damage
    else :
      current_sprite = sprite_damage_L
    damage_cooldown -= 1

  elif health <= 0 :
    current_sprite = sprite_dead

  elif sprite_state == 'land' :
    if sprite_facing == 'right' :
      current_sprite = sprite_landing_R
    else :
      current_sprite = sprite_landing_L

  elif sprite_state == 'jump' :
    if sprite_facing == 'right' :
      current_sprite = sprite_jump_R
    else :
      current_sprite = sprite_jump_L

  elif sprite_state == 'moving' :
    if sprite_facing == 'right' :
      if frame_counter % 15 < 5 :
        current_sprite = sprite_move_R
      else :
        current_sprite = sprite_standing_R
    else :
      if frame_counter % 15 < 5 :
        current_sprite = sprite_move_L
      else :
        current_sprite = sprite_standing_L    

  else :
      if sprite_facing == 'right' :
        current_sprite = sprite_standing_R
      else :
        current_sprite = sprite_standing_L








  #Draw the images
  win.blit(current_sprite, (x, y)) # Character
  win.blit(platform_soil, (0, platform_y)) # Platform - Soil

  for obj in falling_objects : 
    obj.update()
    obj.draw(win)

  for obj in rolling_objects :
    obj.update()
    obj.draw(win)

  for obj in falling_hearts :
    obj.update()
    obj.draw(win)


# Text on the screen:
  
  # Left Side:
  score_text = font.render(f"Score: {score}", True, (255, 255, 255)) # Create a text object
  win.blit(score_text, (10, 10)) # Draw the text on the screen
  poop_text = font.render(f"Poops Avoided: {poops_avoided}", True, (255, 255, 255)) # Create a text object
  win.blit(poop_text, (10, 40)) # Draw the text on the screen
  if level >= 5 :
    boob_text = font.render(f"Boobs Avoided: {boobs_avoided}", True, (255, 255, 255)) # Create a text object
    win.blit(boob_text, (10, 70)) # Draw the text on the screen
  level_text = font.render(f"Level: {level}", True, (255, 255, 255)) # Create a text object
  win.blit(level_text, (10, 100)) # Draw the text on the screen



  # Draw the health bar background
  pygame.draw.rect(win, health_bar_bg_color, (*health_bar_position, health_bar_length, health_bar_height))

  # Draw the health bar
  current_health = health  # This should be updated based on the actual health
  pygame.draw.rect(win, health_bar_color, (*health_bar_position, health_bar_length * (current_health / 100), health_bar_height))
  if current_health > 30 :
    pygame.draw.rect(win, health_bar_color2, (*health_bar_position, health_bar_length * (current_health / 100), health_bar_height))

  # Render the health text
  health_text = font.render(f"{health}", True, (0, 0, 0)) # Create a text object
  if health <= 30 :
    health_text = font.render(f"{health}", True, (255, 0, 0))

  # Calculate the position of the health text
  health_text_x =  win_width/2 #(health_bar_position[0] + health_bar_length - health_text.get_width() / 2) - 150
  health_text_y = health_bar_position[1] + health_bar_height / 2 - health_text.get_height() / 2

  # Draw the health text
  win.blit(health_text, (health_text_x, health_text_y))



  # # Right Side:
  # health_text = font.render(f"{health}", True, (255, 255, 255)) # Create a text object
  # if health <= 30 :
  #   health_text = font.render(f"{health}", True, (255, 0, 0))
  # win.blit(health_text, (health_bar_position[0], health_bar_position[1])) # Draw the text on the screen

  pygame.display.update() # Update the window

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pygame.quit() # Close the window

# TODO






