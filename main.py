import pygame
import os
# Initialize pygame fonts
pygame.font.init()
# Initialize sound effect library
pygame.mixer.init()

# Set window parameters
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Set window title
pygame.display.set_caption("Super Amazing, Awesome Game")

# Set constants
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Set codes for custom user events for ship hits
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Create a middle border to create a ship boundary
BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)

# Set bullet sound files
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# Define font and size for the text displays
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
# Import image, then resize and rotate it
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# Same with the red one
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Bring in and resize a background image
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    '''Function to draw the window display for each time through the loop'''
    # Fill the window with a background from the constants
    WIN.blit(SPACE, (0,0))

    # Draw the border divider
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Set the text for each ship's health, then draw it to the screen
    red_health_text = HEALTH_FONT.render(f"Health: {str(red_health)}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {str(yellow_health)}", 1, WHITE)
    # Pad the text by 10 so it is off the top and side of screen
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # Draw the spaceships at a set destination
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Draw red bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    # Draw yellow bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # Update the window with the newly drawn images
    pygame.display.update()

def handle_yellow_movement(keys_pressed, yellow):
    '''Handle yellow ship movements based on user input'''
    # Use WASD for the yellow ship (on the left)
    # Check if ship will move out of the boundaries
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: # Move left for key press 'a'
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x: # Move right for key press 'd'
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: # Move up for key press 'w'
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15 : # Move down for key press 's'
        yellow.y += VELOCITY

def handle_red_movement(keys_pressed, red):
    '''Handle red ship movements based on user input'''
    # Use WASD for the red ship (on the right)
    # Check if ship will move out of the boundaries
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: # Move left for key press 'left arrow'
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH: # Move right for key press 'right arrow'
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: # Move up for key press 'up arrow'
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15: # Move down for key press 'down arrow'
        red.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        # Move bullet to the right
        bullet.x += BULLET_VELOCITY
        # Check to see if the bullet collided with the ship
        if red.colliderect(bullet):
            # Make a new game event to use in the main function for the hit
            pygame.event.post(pygame.event.Event(RED_HIT))
            # Remove the bullet
            yellow_bullets.remove(bullet)
        # Check if bullet leaves the screen
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        # Move bullet to the left 
        bullet.x -= BULLET_VELOCITY
        # Check to see if the bullet collided with the ship
        if yellow.colliderect(bullet):
            # Make a new game event to use in the main function for the hit
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            # Remove the bullet
            red_bullets.remove(bullet)
        # Check if bullet leaves the screen
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    '''Shows text on the screen indicating a winner'''
    # Render text font
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    # Draw the text
    # NOTE - All calculations with division use // because pygame errors if a float is provided for a rect position
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    # Update the screen to draw the text
    pygame.display.update()
    # Restart the game after 5 seconds
    pygame.time.delay(5000)

def main():
    '''Main game function'''
    # Create the ship rectangles
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    # Set ship health
    yellow_health = 10
    red_health = 10

    # Initialize list to keep track of all the bullets on screen
    red_bullets = []
    yellow_bullets = []

    # Command 1 to set the clock speed to 60 FPS
    clock = pygame.time.Clock()

    # Set variable to True for an endless game loop
    run = True
    while run:

        # Command 2 to set the clock speed to 60 FPS
        clock.tick(FPS)
        
        # Loop through pygame events to see what actions should be taken
        for event in pygame.event.get():

            # If user closes window, exit the program
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            # Map key presses for bullet generation here to prevent spamming
            if event.type == pygame.KEYDOWN:

                # Set ship bullets checking to ensure max bullets hasn't been reached
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # Make the bullet come out of the middle of the ship as a 10x5 rectangle
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    # Add to bullet list
                    yellow_bullets.append(bullet)
                    # Play bullet fire sound
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    # Do the same for the red ship but start on the left side of the ship
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    # Add bullet to list
                    red_bullets.append(bullet)
                    # Play bullet fire sound
                    BULLET_FIRE_SOUND.play()

            # Take action for hit on red ship
            if event.type == RED_HIT:
                # Reduce health by one
                red_health -= 1
                # Play hit sound
                BULLET_HIT_SOUND.play()

            # Take action for hit on yellow ship
            if event.type == YELLOW_HIT:
                # Reduce health by one
                yellow_health -= 1
                # Play hit sound
                BULLET_HIT_SOUND.play()

        winner_text = ""

        # Check to see if either ship has lost all health
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            # Call function to display a winner, then reset
            draw_winner(winner_text)
            break

        # Check for key presses to know where to move the ships
        keys_pressed = pygame.key.get_pressed()
        
        # Move ships and bullets
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Call the function to redraw the window with updated coordinates/information
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # Exit the game/close the window
    main()

if __name__ == "__main__":
    '''Start the main function'''
    main()
