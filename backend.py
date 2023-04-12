from random import randint, random
import pygame
import sys

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLATFORM_WIDTH = 50
PLATFORM_HEIGHT = 10
PLATFORM_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = (255, 0, 0)
PLAYER_INITIAL_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 64)
PLAYER_VELOCITY = 5
JUMP_VELOCITY = -12
GRAVITY = 0.5
FPS = 60
player_facing_right = True # Add a flag to keep track of player's direction

time = 0

timer = 60

player_image = pygame.image.load("characterSmol.png")
player_image = pygame.transform.scale(player_image, (64, 64)) # Scale image to desired size

bg_image = pygame.image.load("house.png")
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

bale_image = pygame.image.load("bale.png")
bale_image = pygame.transform.scale(bale_image, (64, 64))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platform Scrolling Game")
clock = pygame.time.Clock()

player_facing_right = True # Add a flag to keep track of player's direction

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image =  player_image # pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        # self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self):
        global player_facing_right # Use the global flag to update player's direction

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Apply gravity
        self.vel_y += GRAVITY

        # Limit player's vertical velocity
        if self.vel_y > 10:
            self.vel_y = 10

        # Check collision with platform
        if pygame.sprite.spritecollide(self, platforms, False):
            self.on_ground = True
            self.vel_y = 0
        else:
            self.on_ground = False

        # Update player's position based on velocity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.vel_x > 0:
            player_facing_right = False
        elif self.vel_x < 0:
            player_facing_right = True

        # Update player image based on direction
        if player_facing_right:
            self.image = player_image
        else:
            self.image = pygame.transform.flip(player_image, True, False)

# Platform Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(PLATFORM_COLOR)
        self.image = bale_image
        self.rect = self.image.get_rect()
        self.rect.x = x  - 32
        self.rect.y = y
        

# Create sprites
player = Player(*PLAYER_INITIAL_POS)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
platforms = pygame.sprite.Group()

# Create initial platforms
for i in range(5):
    platform = Platform(i * (PLATFORM_WIDTH + 50) + 100 + randint(-15,15), SCREEN_HEIGHT - PLATFORM_HEIGHT - 64)
    all_sprites.add(platform)
    platforms.add(platform)

def gameOver():
    font = pygame.font.SysFont(None, 25)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, [SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
    text = font.render("score: " + str(time), True, (255, 255, 255))
    screen.blit(text, [SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50])

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Game Loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Update player's velocity based on keyboard input
    if keys[pygame.K_LEFT]:
        player.vel_x = -PLAYER_VELOCITY
    elif keys[pygame.K_RIGHT]:
        player.vel_x = PLAYER_VELOCITY
    else:
        player.vel_x = 0

    # Jump if the player is on the ground and spacebar is pressed
    if keys[pygame.K_SPACE] and player.on_ground:
        player.vel_y = JUMP_VELOCITY

    # Update game state
    all_sprites.update()

    # Scroll platforms to the right
    if player.rect.right > SCREEN_WIDTH - (SCREEN_WIDTH / 3):
        player.rect.right = SCREEN_WIDTH - (SCREEN_WIDTH / 3)
        for platform in platforms:
            platform.rect.x -= player.vel_x

    if player.rect.x < 0:
        player.rect.x = 0
        
    # Add new platforms as old ones scroll off the screen
    while len(platforms) < 5:
        last_platform = platforms.sprites()[-1]
        for platform in platforms:
            if platform.rect.left > p.rect.left:
                p = platform
        new_platform = Platform(p.rect.x + 100 + randint(50,200) , SCREEN_HEIGHT - (PLATFORM_HEIGHT + randint(-10,200)))
        if(new_platform.rect.y < 100):
            new_platform.rect.y = SCREEN_HEIGHT - PLATFORM_HEIGHT
        if(new_platform.rect.y > SCREEN_HEIGHT - PLATFORM_HEIGHT - 64):
            new_platform.rect.y = SCREEN_HEIGHT - PLATFORM_HEIGHT - 64
        all_sprites.add(new_platform)
        platforms.add(new_platform)

    #remove off screen platforms
    for platform in platforms:
        if platform.rect.right < 0:
            platform.kill()

    if(player.rect.y > SCREEN_HEIGHT + 5):
        gameOver()

    # Draw background
    screen.fill(BG_COLOR)
    # draw the background image
    screen.blit(bg_image, [0, 0])
    #have the background image move with the character

    # Draw all sprites
    all_sprites.draw(screen)

    #add score based on distance right
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(time), True, (255, 255, 255))
    screen.blit(text, [0, 0])

    

    # Update screen
    pygame.display.flip()

    # Limit frames per second
    clock.tick(FPS)

    timer -= 1
    if(timer == 0):
        #get tail of list
        # last_platform = platforms.sprites()[-1]
        # last_platform.kill()
        timer = 60

    #find the left most platform and kill it    
        p = platform

        for platform in platforms:

            if platform.rect.left < p.rect.left:
                p = platform
        time += 1
        p.kill()
