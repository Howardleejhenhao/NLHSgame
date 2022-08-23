from support import import_csv_layout, import_cut_graphics
import pygame
from settings import tile_size, screen_height, screen_width
from tile import Tile, StaticTile, Crate, Coin, Palm
from player import Player
#from enemy import Enemy

class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0

        # first
        #print("start to import csv")
        floor_layout = import_csv_layout(level_data['floor'])
        self.floor_sprites = self.create_tile_group(floor_layout, 'floor')
        #print("correct import")

        # player
        player_layout = import_csv_layout(level_data['player'])
        print(player_layout)
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        """
        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # creates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coin_layout, 'coins')

        # foreground palms
        fg_plam_layout = import_csv_layout(level_data['fg palms'])
        self.fg_plam_sprites = self.create_tile_group(fg_plam_layout, 'fg palms')

        # background palms
        bg_plam_layout = import_csv_layout(level_data['bg palms'])
        self.bg_plam_sprites = self.create_tile_group(bg_plam_layout, 'bg palms')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprite = self.create_tile_group(constraint_layout, 'constraint')"""


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type == 'floor':
                        floor_tile_list = import_cut_graphics('../graphics/Background/floor_pix.png')
                        tile_surface = floor_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    sprite_group.add(sprite)
        return sprite_group            

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface) # , self.create_jump_particles
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('../graphics/character/white_stand/1.png').convert_alpha()
                    print("YYYYY")
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)    

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprite, False):
                enemy.reverse()


    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        # collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_plam_sprites.sprites()
        """
        for sprite in collidable_sprites: # 處理貼牆壁的問題
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: # 右或左
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False
            """

    def vertical_movement_collision(self):
        player = self.player.sprite
        print("catc")
        player.apply_gravity()
        # collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_plam_sprites.sprites()
        """
        for sprite in collidable_sprites: # 處理貼牆壁的問題
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: # 上下
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    """
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def scroll_x(self): # 處理會超出視窗
            player = self.player.sprite
            player_x = player.rect.centerx
            direction_x = player.direction.x

            if player_x < screen_width / 4 and direction_x < 0: #要讓他可以回來
                self.world_shift = 8
                player.speed = 0
            elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
                self.world_shift = -8
                player.speed = 0
            else:
                self.world_shift = 0
                player.speed = 8

    def get_player_on_ground(self): # 在不再地板上
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
            """

    def create_landing_dust(self): # 烙下的灰塵
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites(): # 裡面沒東西
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)
            """
    def run(self):
        """
        # run the entire game / level
        # background palms
        self.bg_plam_sprites.update(self.world_shift)
        self.bg_plam_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        
        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)
        
        # enemy
        self.enemy_sprites.update(self.world_shift)
        
        self.constraint_sprite.update(self.world_shift)
        self.enemy_collision_reverse()

        self.enemy_sprites.draw(self.display_surface)
        
        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        
        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # forground palms
        self.fg_plam_sprites.update(self.world_shift)
        self.fg_plam_sprites.draw(self.display_surface)"""

        #floor
        self.floor_sprites.update(self.world_shift)
        self.floor_sprites.draw(self.display_surface)

        #player sprite
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        # self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)


