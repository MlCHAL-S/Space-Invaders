import pygame, sys
from settings import *
from game import Game, Player, Player2



class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
   # prints the button onto the screen
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)


    # check whether you hoover over a button
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            MUSIC[1].play()
            return True
        return False

    # changes the button's colour when hooverd over
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)



class Menu():
    def __init__(self):
        self.BG = pygame.image.load("assets/Background.png").convert_alpha()
        self.level = 0
        self.current_gameplay_mode = ''
        self.volume = 0
        self.is_music_on = False



    # returns font in the desired size
    def get_font(self, size): 
        return pygame.font.Font("assets/font.ttf", size)
    


    def save_options(self):
        with open('options.txt', 'w') as file:
            file.write('volume 'f'{self.volume}')



    # reads the options and plays the music
    def read_options(self):
        with open('options.txt', 'r+') as file:
            content = file.read().split()
            self.volume = int(content[1])

        

    def start_music(self):
        for sound in MUSIC:
            sound.set_volume(self.volume / 10)

        if not self.is_music_on:
            #MUSIC[2].play(loops = -1)
            self.is_music_on = True

        

    # starts a singleplayer mode
    def play_singleplayer(self):
         game = Game()

         game.level = self.level
         self.current_gameplay_mode = 'single'

         enemy_shoot_timer = pygame.USEREVENT + 1
         pygame.time.set_timer(enemy_shoot_timer, ENEMY_COOLDOWN)

         while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_BACKSPACE:
                        self.main_menu()
                if event.type == enemy_shoot_timer:
                    game.enemy_shoot()
                if not game.lives:
                     MUSIC[5].play()
                     self.dead_menu('UR DEAD')
                

            
            SCREEN.blit(BACKGROUNDS[self.level % 5], (0, 0))
            game.run()

            if len(game.aliens.sprites()) == 0:
                self.level +=1
                self.between_levels_menu()

            pygame.display.flip()
            CLOCK.tick(FPS)
    
    
    # starts a multiplayer mode
    def play_multiplayer(self):
         p_1 = Player((HALF_WIDTH, (3/4) * HEIGHT), PLAYER_START_LIVES, PLAYER_1_SKIN)
         p_2 = Player2((HALF_WIDTH, (1/4) * HEIGHT), PLAYER_START_LIVES, PLAYER_2_SKIN)

         player_1 = pygame.sprite.GroupSingle(p_1)
         player_2 = pygame.sprite.GroupSingle(p_2)
         self.current_gameplay_mode = 'multi'

         while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            
            SCREEN.blit(BACKGROUNDS[self.level % 5], (0, 0))
            player_1.update()
            player_2.update()

            # prints players and bullets
            player_1.sprite.lasers.draw(SCREEN)
            player_1.draw(SCREEN)
            player_2.sprite.lasers.draw(SCREEN)
            player_2.draw(SCREEN)

            # print lives onto the screen
            lives_1 = IN_GAME_FONT.render('P1 lives: 'f'{p_1.lives}', False, FONT_COLOUR)
            lives_1_rect = lives_1.get_rect(center = (HALF_WIDTH + 500, HALF_HEIGHT * 1.9))
            lives_2 = IN_GAME_FONT.render('P2 lives: 'f'{p_2.lives}', False, FONT_COLOUR)
            lives_2_rect = lives_2.get_rect(center = (HALF_WIDTH - 500, HALF_HEIGHT * 1.9))
            SCREEN.blit(lives_1, lives_1_rect)
            SCREEN.blit(lives_2, lives_2_rect)


            # check for player's 1 collisions
            if player_1.sprite.lasers:
                for laser in player_1.sprite.lasers:
                    if pygame.sprite.spritecollide(laser, player_2, False):
                        MUSIC[4].play()
                        laser.kill()
                        p_2.lives -= 1


            # check for player's 2 collisions
            if player_2.sprite.lasers:
                for laser in player_2.sprite.lasers:
                    if pygame.sprite.spritecollide(laser, player_1, False):
                        MUSIC[4].play()
                        laser.kill()
                        p_1.lives -= 1


            # check if any player is dead
            if not p_1.lives or not p_2.lives:
                 MUSIC[5].play()
                 if p_1.lives:
                      self.dead_menu('PLAYER 1 WINS')
                 else:
                      self.dead_menu('PLAYER 2 WINS')
                      

            pygame.display.flip()
            CLOCK.tick(FPS)


    # displays play menu
    def play_menu(self):
        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            SCREEN.blit(self.BG, (0, 0))

            MENU_TEXT = self.get_font(60).render("Choose gameplay mode", True, "White")
            MENU_RECT = MENU_TEXT.get_rect(center=(HALF_WIDTH, (1/6) * HEIGHT))
            SCREEN.blit(MENU_TEXT, MENU_RECT)

            SINGLEPLAYER_BUTTON = Button(image=pygame.image.load("assets/Single Rect.png"), pos=(HALF_WIDTH, (2/5) * HEIGHT), 
                                text_input="SINGLE", font=self.get_font(75), base_color="White", hovering_color="Green")
            
            MULTIPLAYER_BUTTON = Button(image=pygame.image.load("assets/Multi Rect.png"), pos=(HALF_WIDTH, (3/5) * HEIGHT), 
                                text_input="MULTI", font=self.get_font(75), base_color="White", hovering_color="Green")
            
            BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(HALF_WIDTH, (5/6 * HEIGHT)), 
                                text_input="BACK", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")


            for button in [SINGLEPLAYER_BUTTON, MULTIPLAYER_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SINGLEPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play_singleplayer()
                    if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                         self.play_multiplayer()
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                         self.main_menu()

            pygame.display.flip()
            CLOCK.tick(FPS)
       

    # allows the player to continue gameplay after a level is finished or exit
    def between_levels_menu(self):
         while True:
            SCREEN.fill('Black')
            SCREEN.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(90).render("YOU WIN", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(HALF_WIDTH, (1/5) * HEIGHT))
            SCREEN.blit(MENU_TEXT, MENU_RECT)

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(HALF_WIDTH, (4/6 * HEIGHT)), 
                                text_input="NEXT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(HALF_WIDTH, (5/6 * HEIGHT)), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")


    
            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play_singleplayer()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.play_singleplayer()

            pygame.display.flip()
            CLOCK.tick(FPS)


    # displays options menu
    def options_menu(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            SCREEN.blit(self.BG, (0, 0))

            OPTIONS_TEXT = self.get_font(105).render("OPTIONS", True, "white")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(HALF_WIDTH, 1/4 * HEIGHT))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            VOLUME_TEXT = self.get_font(40).render('VOLUME: 'f'{self.volume}', True, "white")
            VOLUME_RECT = OPTIONS_TEXT.get_rect(center=(HALF_WIDTH + 180, HALF_HEIGHT + 30))
            SCREEN.blit(VOLUME_TEXT, VOLUME_RECT)


            OPTIONS_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(HALF_WIDTH, 4/5 * HEIGHT), 
                                text_input="BACK", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            
            LEFT = Button(image=pygame.image.load("assets/Switch Rect.png"), pos=(1/4 * WIDTH, HALF_HEIGHT), 
                                text_input="<<", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            
            RIGHT = Button(image=pygame.image.load("assets/Switch Rect.png"), pos=(3/4 * WIDTH, HALF_HEIGHT), 
                                text_input=">>", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")

            
            for button in [OPTIONS_BACK, LEFT, RIGHT]:
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.save_options()
                        return
                    if LEFT.checkForInput(OPTIONS_MOUSE_POS) and self.volume >= 1:
                        self.volume -= 1
                        self.start_music()
                    if RIGHT.checkForInput(OPTIONS_MOUSE_POS) and self.volume <= 9:
                        self.volume += 1
                        self.start_music()

                    
                    

            pygame.display.flip()
            CLOCK.tick(FPS)


    # displays menu after death
    def dead_menu(self, message):
         while True:
            self.level = 0
            SCREEN.fill('Black')
            SCREEN.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(90).render(message, True, '#b68f40')
            MENU_RECT = MENU_TEXT.get_rect(center=(HALF_WIDTH, (1/5) * HEIGHT))
            SCREEN.blit(MENU_TEXT, MENU_RECT)


            PLAY_AGAIN_BUTTON = Button(image=pygame.image.load('assets/Playagain Rect.png'), pos=(HALF_WIDTH, (2/3 * HEIGHT)), 
                                text_input="PLAY AGAIN", font=self.get_font(75), base_color='#d7fcd4', hovering_color="White")

            QUIT_BUTTON = Button(image=pygame.image.load('assets/Quit Rect.png'), pos=(HALF_WIDTH, (5/6 * HEIGHT)), 
                                text_input="QUIT", font=self.get_font(75), base_color='#d7fcd4', hovering_color="White")


            for button in [PLAY_AGAIN_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play_menu()
                    if PLAY_AGAIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        if self.current_gameplay_mode == 'single':
                            self.play_singleplayer()
                        if self.current_gameplay_mode == 'multi':
                            self.play_multiplayer()
                        

            pygame.display.flip()
            CLOCK.tick(FPS)


    # displays main menu
    def main_menu(self):
        # making sure the level is set to 0
        self.level = 0
        self.read_options()
        self.start_music()

        while True:
            SCREEN.fill('Black')
            SCREEN.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(90).render("SPACE INVADERS", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(HALF_WIDTH, (1/5) * HEIGHT))
            SCREEN.blit(MENU_TEXT, MENU_RECT)

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(HALF_WIDTH, (1/2 * HEIGHT)), 
                                text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(HALF_WIDTH, (2/3 * HEIGHT)), 
                                text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(HALF_WIDTH, (5/6 * HEIGHT)), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")


            # cycle through all the buttons and check for events
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play_menu()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options_menu()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            CLOCK.tick(FPS)
