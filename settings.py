import pygame 

pygame.init()


# font initialisation
pygame.font.init()
IN_GAME_FONT = pygame.font.Font('fonts/font.otf', 50)


# game settings
RESOLUTION = WIDTH, HEIGHT = 1280, 720
FPS = 60
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FONT_COLOUR = (111, 196, 169)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
BACKGROUNDS = [pygame.image.load('backgrounds/b1.jpg').convert_alpha(), pygame.image.load('backgrounds/b2.jpg').convert_alpha(), pygame.image.load('backgrounds/b3.jpg').convert_alpha(), pygame.image.load('backgrounds/b4.jpg').convert_alpha(), pygame.image.load('backgrounds/b5.jpg').convert_alpha()]


# music                 0                                               1                                               2                                           3                                       4                                       5                                                   6                               
MUSIC = [pygame.mixer.Sound('music/button.wav'), pygame.mixer.Sound('music/button_pressed.wav'), pygame.mixer.Sound('music/main_theme.wav'), pygame.mixer.Sound('music/player_dead.wav'), pygame.mixer.Sound('music/player_hit.wav'), pygame.mixer.Sound('music/ship_destroyed.wav'), pygame.mixer.Sound('music/shoot.wav'), ]


# player settings
PLAYER_SPEED = 20
PLAYER_BULLET_SPEED = 20
PLAYER_BULLET_COOL_DOWN = 600
PLAYER_COOLDOWN = 600
PLAYER_START_LIVES = 3

PLAYER_1_SKIN = pygame.image.load('graphics/player1.png').convert_alpha()
PLAYER_2_SKIN = pygame.image.load('graphics/player2.png').convert_alpha()
PLAYER_BULLET_IMG = pygame.image.load('graphics/player_bullet.png').convert_alpha()


# enemy settings
ENEMY_SPEED = 5
ENEMY_BULLET_SPEED = 20
ENEMY_COOLDOWN = 500

ENEMY_BULLET_IMG = pygame.image.load('graphics/enemy_bullet.png').convert_alpha()
ENEMY_SKINS = [pygame.image.load('graphics/enemy1.png').convert_alpha(), pygame.image.load('graphics/enemy2.png').convert_alpha()]

        
        