from player_class import Player
from farm_tile_class import FarmTiles
from crops_class import Crops
from random import randint
import spritesheet_class
import pygame


pygame.init()
screen = pygame.display.set_mode((980, 720))
pygame.display.set_caption('Jeu farm ?')
clock = pygame.time.Clock()

BG = (50, 50, 50)
GREY = (60, 60, 60)
BLACK = (0, 0, 0)

player_animation_list, player_action_list = [], []
player_animation_steps, player_action_steps = [3, 3, 3, 3, 4, 4, 4, 4], [3]
player_mouvement, player_facing, player_action = 0, 0, 0

crop_animation_list = []
crop_animation_steps = [5, 5, 5, 5]

player_last_update = pygame.time.get_ticks()
player_animation_cooldown = randint(150, 240)

frame = 0
step_counter = 0

position_heigth = 0
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
PLAYER_SCALE = 4

placing_tile = False
placing_crop = False
showing = False

tool_equiped = "hands"

farm_tile = pygame.image.load("assets/pixil-frame-0.png")

# Player assets #
player_spritesheet_image = pygame.image.load("assets/hero2.png").convert_alpha()
player_spritesheet = spritesheet.SpriteSheet(player_spritesheet_image)

for player_animation in player_animation_steps:
    temp_img_list = []
    for _ in range(player_animation):
        temp_img_list.append(player_spritesheet.get_image(step_counter, position_heigth, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SCALE, BLACK))
        step_counter += 1
    player_animation_list.append(temp_img_list)
    position_heigth += 16
    step_counter = 0

# Player action assets #
player_action_spritesheet_image = pygame.image.load("assets/plowing.png").convert_alpha()
player_action_spritesheet = spritesheet.SpriteSheet(player_action_spritesheet_image)

PLAYER_ACTION_WIDTH = 24
PLAYER_ACTION_HEIGHT = 24
PLAYER_ACTION_SCALE = 4
position_heigth = 0
for player_animation_action in player_action_steps:
    temp_img_list = []
    for _ in range(player_animation_action):
        temp_img_list.append(player_action_spritesheet.get_image(step_counter, position_heigth, PLAYER_ACTION_WIDTH, PLAYER_ACTION_HEIGHT, PLAYER_ACTION_SCALE, BLACK))
        step_counter += 1
    player_action_list.append(temp_img_list)
    position_heigth += 24
    step_counter = 0


# Crops assets #
crops_spritesheet_image = pygame.image.load("assets/crops.png").convert_alpha()
crops_spritesheet = spritesheet.SpriteSheet(crops_spritesheet_image)

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

dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

rect_player = pygame.Rect(0, 0, (PLAYER_SCALE * 16), (PLAYER_SCALE * 16))
rect_player.topleft = (0, 0)


def draw_grid(w, rows, show=False):
    sizebtwn = w // rows
    if show:
        for i in range(0, screen.get_width(), sizebtwn):
            x, y = i, i
            pygame.draw.line(screen, GREY, (x, 0), (x, w))
            pygame.draw.line(screen, GREY, (0, y), (w, y))


def player_is_facing_crop(player_rect, crops_list):
    check_rect = pygame.Rect(
        player_rect.x + 8,
        player_rect.y + 8,
        player_rect.width - 16,
        player_rect.height - 16
    )

    # pygame.draw.rect(screen, (255, 0, 0), check_rect, 2)  # reach of the player

    closest_crop = None
    min_distance = float('inf')

    for crop in crops_list:
        crop_rect = pygame.Rect(crop.posx, crop.posy, crop.surface.get_width(), crop.surface.get_height())

        if check_rect.colliderect(crop_rect):
            player_center = pygame.Vector2(player_rect.center)
            crop_center = pygame.Vector2(crop_rect.center)
            distance = player_center.distance_to(crop_center)
            if distance < min_distance:
                min_distance = distance
                closest_crop = crop
    return closest_crop


def make_player_face_crop(player_rect, crop_facing):
    global player_facing
    crop_rect = pygame.Rect(crop_facing.posx, crop_facing.posy, crop_facing.surface.get_width(), crop_facing.surface.get_height())

    dx = crop_rect.centerx - player_rect.centerx
    dy = crop_rect.centery - player_rect.centery

    if abs(dx) > abs(dy):
        if dx > 0:
            player_facing = 1
        else:
            player_facing = 2
    else:
        if dy > 0:
            player_facing = 0
        else:
            player_facing = 3


def player_is_facing_farmtile(player_rect, farmtiles_list):
    check_rect = pygame.Rect(
        player_rect.x + 8,
        player_rect.y + 8,
        player_rect.width - 16,
        player_rect.height - 16
    )

    pygame.draw.rect(screen, (255, 0, 0), check_rect, 2)  # reach of the player

    closest_tile = None
    min_distance = float('inf')

    for tile in farmtiles_list:
        tile_rect = pygame.Rect(tile.posx, tile.posy, tile.surface.get_width(), tile.surface.get_height())

        if check_rect.colliderect(tile_rect):
            player_center = pygame.Vector2(player_rect.center)
            tile_center = pygame.Vector2(tile_rect.center)
            distance = player_center.distance_to(tile_center)
            if distance < min_distance:
                min_distance = distance
                closest_tile = tile
    return closest_tile


def make_player_plow_farmtile(player_rect, tile_facing):
    tile_rect = pygame.Rect(tile_facing.posx, tile_facing.posy, tile_facing.surface.get_width(), tile_facing.surface.get_height())

    dx = tile_rect.centerx - player_rect.centerx
    dy = tile_rect.centery - player_rect.centery

    if abs(dx) > abs(dy):
        if dx > 0:
            player_rect.x = tile_rect.x
            player_rect.y = tile_rect.y


def get_current_player_frame():
    global frame, current_time, player_last_update, player_animation_cooldown, \
        plowing, player_action_list, player_animation_list, player_action, player_mouvement

    if current_time - player_last_update >= player_animation_cooldown:
        frame += 1
        player_last_update = current_time
    if plowing:
        player_images_list = player_action_list[player_action]
        if frame >= len(player_images_list):
            tile_faced.plowing_needed = False
            crop_to_delete = tile_faced.crop_planted
            tile_faced.crop_planted = None
            Crops.crops_planted.remove(crop_to_delete)
            del crop_to_delete
            plowing = False
            frame = 0
    else:
        player_images_list = player_animation_list[player_mouvement]
        if frame >= len(player_images_list):
            frame = 0

    return player_images_list[frame]


running = True
while running:
    screen.fill(BG)
    pygame.mouse.set_visible(False)
    draw_grid(screen.get_width(), 18, showing)

    current_time = pygame.time.get_ticks()

    tile_faced = player_is_facing_farmtile(rect_player, FarmTiles.farm_tiles)
    crop_faced = player_is_facing_crop(rect_player, Crops.crops_planted)


    for tile in FarmTiles.farm_tiles:
        screen.blit(tile.surface, (tile.posx, tile.posy))

    for crop in Crops.crops_planted:
        screen.blit(crop.surface, (crop.posx, crop.posy))

        if crop.growing and not crop.harvestable and crop.crop_cooldown:
            if current_time - crop.last_update >= crop.crop_cooldown:
                crop.last_update = current_time
                growth_probability = randint(0, 3)
                if growth_probability == 1:
                    crop.stage += 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool_equiped = "hands"
            elif event.key == pygame.K_2:
                tool_equiped = "hoe"

            if event.key == pygame.K_b:
                if placing_tile:
                    placing_tile = False
                else:
                    placing_tile = True

            if event.key == pygame.K_e:
                if placing_crop:
                    placing_crop = False
                else:
                    placing_crop = True

            if event.key == pygame.K_SPACE:
                if tool_equiped == "hands":
                    if crop_faced and crop_faced.harvestable:
                        make_player_face_crop(rect_player, crop_faced)
                        crop_faced.stage = "harvesting"
                        crop_faced.tile.plowing_needed = True
                        crop_faced.harvestable = False

                elif tool_equiped == "hoe":
                    if tile_faced and tile_faced.plowing_needed:
                        plowing = True
                        make_player_plow_farmtile(rect_player, tile_faced)
                        frame = 0



    farmer = screen.blit(get_current_player_frame(), rect_player)

    if not plowing:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            rect_player.move_ip(0, -5)
            player_mouvement = 7
            player_facing = 3
        elif keys[pygame.K_s]:
            rect_player.move_ip(0, 5)
            player_mouvement = 4
            player_facing = 0
        elif keys[pygame.K_a]:
            rect_player.move_ip(-5, 0)
            player_mouvement = 6
            player_facing = 2
        elif keys[pygame.K_d]:
            rect_player.move_ip(5, 0)
            player_mouvement = 5
            player_facing = 1
        else:
            if player_mouvement != player_facing:
                frame = 0
            player_mouvement = player_facing

        if placing_tile:
            tile = FarmTiles()
            showing = True
            tile.update(screen.get_width() // 18)
            tile.draw(screen)
            if keys[pygame.K_SPACE] and tile.is_valid_placing():
                FarmTiles.create_tile(tile)
                placing_tile = False
        else:
            showing = False

        if placing_crop:
            crop = Crops()
            crop.last_update = current_time
            showing = True
            crop.update(screen.get_width() // 18)
            crop.draw(screen)
            if keys[pygame.K_SPACE] and crop.is_valid_placing():
                Crops.create_crop(crop)
                for tile in FarmTiles.farm_tiles:
                    tile_rect = pygame.Rect(tile.posx, tile.posy, tile.surface.get_width(), tile.surface.get_height())
                    if tile_rect.colliderect(crop.square):
                        crop.tile = tile
                placing_crop = False

    dt = clock.tick(60) / 2000
    pygame.display.flip()
pygame.quit()
