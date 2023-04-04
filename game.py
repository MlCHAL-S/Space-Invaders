import pygame, random, sys
from settings import *
from random import choice


class Game:
    def __init__(self):
        # Players
        player_sprite = Player((HALF_WIDTH, HEIGHT * (4/5)), PLAYER_START_LIVES, PLAYER_1_SKIN)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.level = 0
        

        # health and score
        self.lives = PLAYER_START_LIVES


        # Enemies
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        

    # sets up the level and enemies
    def level_setup(self):
        if len(self.aliens.sprites()) == 0:
            self.level += 1
            self.lives = PLAYER_START_LIVES
            self.enemy_setup()


    # prints the number of player's lives
    def print_stats(self):
        lives = IN_GAME_FONT.render('Lives: 'f'{self.lives}', False, FONT_COLOUR)
        lives_rect = lives.get_rect(center = (HALF_WIDTH - 510, HALF_HEIGHT * 1.9))

        level = IN_GAME_FONT.render('Level: 'f'{self.level}', False, FONT_COLOUR)
        level_rect = level.get_rect(center = (HALF_WIDTH - 300, HALF_HEIGHT * 1.9))

        SCREEN.blit(lives, lives_rect)
        SCREEN.blit(level, level_rect)


    # detects all the collisions options and subtracts player's lives
    def collisions(self):
        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                
                # enemy collision
                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    MUSIC[5].play()
                    laser.kill()
                    
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    MUSIC[4].play()
                    laser.kill()
                    self.lives -= 1
    

    # spawns so many enemies as the level is
    def enemy_setup(self):
        for enemy in range(self.level):
            enemy = Enemy()
            self.aliens.add(enemy)


    # makes the enemy take a shot
    def enemy_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, ENEMY_BULLET_SPEED, -1, ENEMY_BULLET_IMG)
            self.alien_lasers.add(laser_sprite)


    # updates the screen
    def run(self):
        self.player.update()
        self.aliens.update()
        self.alien_lasers.update()
        self.level_setup()
        self.print_stats() 

        # 
        self.player.sprite.lasers.draw(SCREEN)
        self.player.draw(SCREEN)

        #
        self.aliens.draw(SCREEN)
        self.alien_lasers.draw(SCREEN)

        # collisions
        self.collisions()



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, lives, skin):
        super().__init__()
        self.image = skin
        self.rect = self.image.get_rect(midbottom = pos)
        self.ready = True
        self.laser_time = 0
        self.lives = lives
        self.live_surf = pygame.image.load

        self.lasers = pygame.sprite.Group()


    # creates an instance of Laser class
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, PLAYER_BULLET_SPEED, 1, PLAYER_BULLET_IMG))


    # gets player's input
    def get_input(self):
        keys = pygame.key.get_pressed()

        # movement controls
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

        # gameplay controls
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()


    # this function enforces the laser to cool down
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if (current_time - self.laser_time) >= PLAYER_BULLET_COOL_DOWN:
                self.ready = True


    # constraints the player to the resolution of the screen
    def constraint(self):
        temp = HEIGHT - 60

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom >= temp: 
            self.rect.bottom = temp
        if self.rect.top <= HALF_HEIGHT: 
            self.rect.top = HALF_HEIGHT


    # runs all the other methods simultaneously
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()



class Player2(Player):
    def __init__(self, pos, lives, skin):
        super().__init__(pos, lives, skin)


    # this class needs an upside-down bullet
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, PLAYER_BULLET_SPEED, -1, ENEMY_BULLET_IMG))


    # constraints the player to the resolution of the screen
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom >= HALF_HEIGHT: 
            self.rect.bottom = HALF_HEIGHT
        if self.rect.top <= 60: 
            self.rect.top = 60


    # gets player's input
    def get_input(self):
        keys = pygame.key.get_pressed()

        # movement controls
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

        # gameplay controls
        if keys[pygame.K_r] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()



class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, direction, skin):
        super().__init__()
        self.image = skin
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed * direction

        MUSIC[6].play()


    # destroys a bulles which has reached the very top or bottom of the screen
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= HEIGHT + 50:
            self.kill()


    # runs all the other methods simultaneously
    def update(self):
        self.rect.y -= self.speed
        self.destroy()



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ENEMY_SKINS[random.randint(0, 1)]
        self.rect = self.image.get_rect(center = (random.randint(0 + 100, WIDTH - 100), random.randint(0 + 100, HALF_HEIGHT - 100)))
        self.velocity_x = ENEMY_SPEED
        self.velocity_y = ENEMY_SPEED


    # moves the enemy
    def movement(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y


    # constraints the enemy to the screen border
    def constraint(self):
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.velocity_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT / 2:
            self.velocity_y *= -1


    # runs all the methods at the same time
    def update(self):
        self.movement()
        self.constraint()