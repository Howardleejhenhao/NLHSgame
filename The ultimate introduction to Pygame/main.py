import pygame
from sys import exit, float_repr_style
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2] #走路圖片
        self.player_index = 0 #控制哪一個圖片
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3') # input sound
        self.jump_sound.set_volume(0.5) # 聲音大小

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play() # 播放

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        
        self.anumation_index = 0

        self.image = self.frames[self.anumation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.anumation_index += 0.1
        if self.anumation_index >= len(self.frames):
            self.anumation_index = 0
        self.image = self.frames[int(self.anumation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destory()

    def destory(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time#時間(毫秒)
    score_surf = test_font.render("Score : %.0f" % current_time, False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list): #此函是用來讓多的snail出現

    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)  

            # screen.blit(snail_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player, obstacles): #判斷是否碰到
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): # 前兩這撞擊，若第三個值為True會刪除
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        # jump
        player_surf = player_jump
    else:
        # walk
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

    # play walking animation if the player is on floor
    # display the jump surface when player is not on floor

pygame.init() #灌入pygame       

screen = pygame.display.set_mode((800, 400)) #設定視窗大小
pygame.display.set_caption('Runner') #視窗名稱
clock = pygame.time.Clock() #FPS設定

test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #pygame.font.Font(font type, font size)

game_active = False

start_time = 0

score = 0

bg_Music = pygame.mixer.Sound('audio/music.wav')
bg_Music.play(loops = -1) # play(播放幾次) if == -1持續撥放

# Group
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# score_surf = test_font.render('My game', False, (64, 64, 64)) #test_font.render(text, AA, color)
# score_rect = score_surf.get_rect(center = (400, 50))

sky_surface = pygame.image.load('graphics/Sky.png').convert() #匯入圖片
ground_surface = pygame.image.load('graphics/ground.png').convert()

"""
# obstacles
# snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
snail_rect = snail_surf.get_rect(bottomright = (600, 300))

# fly
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2] #走路圖片
player_index = 0 #控制哪一個圖片
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300)) #位置
player_gravity = 0
"""
# 初始畫面
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) #pygame.transform.rotozoom(圖像, 旋轉角度, 放大倍率) 
player_stand_rect = player_stand.get_rect(center = (400, 200))
# player_stand_scaled = pygame.transform.scale(player_stand, (200, 400)) # https://blog.csdn.net/Enderman_xiaohei/article/details/88282456

# 遊戲名稱
game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 320))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get(): #在視窗中所有的動作ex按下按鍵
        if event.type == pygame.QUIT: #關閉視窗鍵是否被按下
            pygame.quit()
            exit() #關閉視窗
        """if game_active:
            # if event.type == pygame.MOUSEMOTION:
                # if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: #滑鼠按下並且在player上
                #     player_gravity = -20

            # if event.type == pygame.KEYDOWN: #鍵盤被按下
            #     if event.key  == pygame.K_SPACE and player_rect.bottom >= 300: #空白鍵被按下  player_rect.bottom >= 300偵測是否在地面
            #         player_gravity = -20
            # 
        """
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                # if randint(0, 2): #隨機看是要放snail還是fly
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                # snail_rect.left = 800 # 將怪物設回原點，不會重疊
                # start_time = int(pygame.time.get_ticks() / 1000) # set up score
            """
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
            """
        #if event.type == pygame.MOUSEMOTION: #滑鼠移動
        #    print(event.pos) #滑鼠位置

        ##if event.type == pygame.MOUSEBUTTONDOWN: #按下滑鼠
        #   print('mouse down')

        #if event.type == pygame.MOUSEBUTTONUP: #抬起滑鼠鍵
        #    print('mouse up')

    if game_active:
        #draw all our elements
        screen.blit(sky_surface, (0, 0)) #show 物件
        screen.blit(ground_surface, (0, 300))

        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect) #pygame.draw.rect畫長方形(screen, color, pos)
        #pygame.draw.line(screen, 'Gold', (0, 0), pygame.mouse.get_pos(), 10) #pygame.draw.line畫直線(screen, color, 開始pos, 結束pos, 粗度)
        #pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50, 200, 100, 100))

        # screen.blit(score_surf, score_rect)

        score = display_score()

        # snail_rect.x -= 4   
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800 


        # screen.blit(snail_surf, snail_rect)

        # player
        # player_gravity += 1 #跳
        # player_rect.y += player_gravity

        # if player_rect.bottom >= 300: #讓player不跳出圖形之外
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rect)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision

        game_active = collision_sprite()
        # game_active = collisions(player_rect, obstacle_rect_list)
        # if snail_rect.colliderect(player_rect): #判斷player碰到障礙物結束遊戲
        #    game_active = False

        # if player_rect.colliderect(snail_rect): #碰撞 0 1
        #   print('collision')
        
        #mouse_pos = pygame.mouse.get_pos() #滑鼠位置 (x, y)
        #if player_rect.collidepoint(mouse_pos): #碰點 0 1
        #    print(pygame.mouse.get_pressed()) #三個bool(左鍵按下, 中鍵按下, 右鍵按下)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        # obstacle_rect_list.clear() #剛死亡會重疊，所以清除
        # player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render('Your score: %.0f' % score, False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        screen.blit(game_name, game_name_rect)
        # screen.blit(game_message, game_message_rect)
    
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    
    pygame.display.update() #update everying
    clock.tick(60) #FPS設定