from spritesheet_class import SpriteSheet
from farmtiles_class import FarmTiles
from player_class import Player
from crops_class import Crops

from random import randint
import pygame


pygame.init()
screen = pygame.display.set_mode((980, 720))
pygame.display.set_caption('Jeu farm ?')
clock = pygame.time.Clock()

BG = (50, 50, 50)
GREY = (60, 60, 60)
BLACK = (0, 0, 0)

player = Player()

player.width = 16
player.height = 16
player.scale = 4
player.rect = pygame.Rect(0, 0, (player.scale * 16), (player.scale * 16))
player.rect.topleft = (0, 0)

step_counter = 0
position_heigth = 0

show_placing_grid = False
farm_tile = pygame.image.load("assets/pixil-frame-0.png")


# Player movement assets #
player_spritesheet_image = pygame.image.load("assets/hero2.png").convert_alpha()
player_spritesheet = SpriteSheet(player_spritesheet_image)
player.player_animation_steps = [3, 3, 3, 3, 4, 4, 4, 4]

for player_animation in player.player_animation_steps:
    temp_img_list = []
    for _ in range(player_animation):
        temp_img_list.append(player_spritesheet.get_image(step_counter, position_heigth, player.width, player.height, player.scale, BLACK))
        step_counter += 1
    player.player_animation_list.append(temp_img_list)
    position_heigth += 16
    step_counter = 0

# Player action assets #
player_action_spritesheet_image = pygame.image.load("assets/plowing2.png").convert_alpha()
player_action_spritesheet = SpriteSheet(player_action_spritesheet_image)
player.player_action_steps = [6]

PLAYER_ACTION_WIDTH = 24
PLAYER_ACTION_HEIGHT = 24
PLAYER_ACTION_SCALE = 4
position_heigth = 0

for player_animation_action in player.player_action_steps:
    temp_img_list = []
    for _ in range(player_animation_action):
        temp_img_list.append(player_action_spritesheet.get_image(step_counter, position_heigth, PLAYER_ACTION_WIDTH, PLAYER_ACTION_HEIGHT, PLAYER_ACTION_SCALE, BLACK))
        step_counter += 1
    player.player_action_list.append(temp_img_list)
    position_heigth += 24
    step_counter = 0


# Crops assets #
crops_spritesheet_image = pygame.image.load("assets/crops.png").convert_alpha()
crops_spritesheet = SpriteSheet(crops_spritesheet_image)

crop_animation_list = []
crop_animation_steps = [5, 5, 5, 5]

CROPS_WIDTH = 32
CROPS_HEIGHT = 32
CROPS_SCALE = 1.5

for crop_animation in crop_animation_steps:
    temp_img_list = []
    position_heigth = 32
    for _ in range(crop_animation):
        temp_img_list.append(crops_spritesheet.get_image(step_counter, position_heigth, CROPS_WIDTH, CROPS_HEIGHT, CROPS_SCALE, BLACK))
        position_heigth += 64
    crop_animation_list.append(temp_img_list)
    step_counter += 1

Crops.list_surface_crops_animation = crop_animation_list


def draw_grid(w, rows, show=False):
    sizebtwn = w // rows
    if show:
        for i in range(0, screen.get_width(), sizebtwn):
            x, y = i, i
            pygame.draw.line(screen, GREY, (x, 0), (x, w))
            pygame.draw.line(screen, GREY, (0, y), (w, y))


running = True
while running:
    # initialisation #
    screen.fill(BG)
    pygame.mouse.set_visible(False)
    draw_grid(screen.get_width(), 18, show_placing_grid)

    current_time = pygame.time.get_ticks()

    # Affichage des farm tiles placés sur la map
    for tile in FarmTiles.farm_tiles:
        screen.blit(tile.surface, (tile.posx, tile.posy))

    # Affichage des crops plantés sur la map
    for crop in Crops.crops_planted:
        screen.blit(crop.surface, (crop.posx, crop.posy))
        if crop.growing and not crop.harvestable and crop.crop_cooldown:
            if current_time - crop.last_update >= crop.crop_cooldown:
                crop.last_update = current_time
                growth_probability = randint(0, 3)
                if growth_probability == 1:
                    crop.stage += 1

    player.get_player_is_facing(Crops.crops_planted, FarmTiles.farm_tiles, True, screen)
    player.get_current_player_frame(current_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.tool_equiped = 0
            elif event.key == pygame.K_2:
                player.tool_equiped = 1

            if event.key == pygame.K_b:
                if player.is_placing_tile:
                    player.is_placing_tile = False
                else:
                    player.is_placing_tile = True

            if event.key == pygame.K_e:
                if player.is_placing_crop:
                    player.is_placing_crop = False
                else:
                    player.is_placing_crop = True

            if event.key == pygame.K_SPACE:
                if player.tool_equiped == 0:
                    if player.crop_facing and player.crop_facing.harvestable:
                        player.make_player_face_crop()
                        player.crop_facing.stage = "harvesting"
                        player.crop_facing.tile.plowing_needed = True
                        player.crop_facing.harvestable = False

                elif player.tool_equiped == 1:
                    if player.tile_facing and player.tile_facing.plowing_needed:
                        player.make_player_plow_farmtile()
                        player.animation_frame = 0


    screen.blit(player.surface, player.rect)

    if not player.is_plowing:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.rect.move_ip(0, -5)
            player.player_movement = 7
            player.player_facing = 3
        elif keys[pygame.K_s]:
            player.rect.move_ip(0, 5)
            player.player_movement = 4
            player.player_facing = 0
        elif keys[pygame.K_a]:
            player.rect.move_ip(-5, 0)
            player.player_movement = 6
            player.player_facing = 2
        elif keys[pygame.K_d]:
            player.rect.move_ip(5, 0)
            player.player_movement = 5
            player.player_facing = 1
        else:
            if player.player_movement != player.player_facing:
                player.animation_frame = 0
            player.player_movement = player.player_facing

        if player.is_placing_tile:
            tile = FarmTiles()
            show_placing_grid = True
            tile.update(screen.get_width() // 18)
            tile.draw(screen)
            if keys[pygame.K_SPACE] and tile.is_valid_placing():
                FarmTiles.create_tile(tile)
                player.is_placing_tile = False
        else:
            show_placing_grid = False

        if player.is_placing_crop:
            crop = Crops()
            crop.last_update = current_time
            show_placing_grid = True
            crop.update(screen.get_width() // 18)
            crop.draw(screen)
            if keys[pygame.K_SPACE] and crop.is_valid_placing():
                Crops.create_crop(crop)
                for tile in FarmTiles.farm_tiles:
                    tile_rect = pygame.Rect(tile.posx, tile.posy, tile.surface.get_width(), tile.surface.get_height())
                    if tile_rect.colliderect(crop.square):
                        crop.tile = tile
                player.is_placing_crop = False

    clock.tick(60) / 2000
    pygame.display.flip()
pygame.quit()
