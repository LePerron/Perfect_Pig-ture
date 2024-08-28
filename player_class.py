from random import randint
import pygame


class Player:

    def __init__(self, tool_equiped=0, rect=None, surface=None, current_action=None, tile_facing=None, crop_facing=None,
                 is_plowing=False, animation_frame=0, player_last_update=pygame.time.get_ticks(),
                 animation_cooldown=randint(150, 240), player_animation_list=None, player_action_list=None,
                 player_animation_steps=None, player_action_steps=None, player_movement=None, player_facing=None,
                 player_action=None, player_width=0, player_height=0, player_scale=0, is_placing_tile=False, is_placing_crop=False):

        self.tool_equiped = tool_equiped
        self.rect = rect
        self.surface = surface
        self.current_action = current_action
        self.tile_facing = tile_facing
        self.crop_facing = crop_facing
        self.is_plowing = is_plowing
        self._animation_frame = animation_frame
        self.player_last_update = player_last_update
        self.animation_cooldown = animation_cooldown
        self.player_width = player_width
        self.player_height = player_height
        self.player_scale = player_scale
        self.is_placing_tile = is_placing_tile
        self.is_placing_crop = is_placing_crop




        if not player_animation_list:
            self.player_animation_list = []
        if not player_action_list:
            self.player_action_list = []
        if not player_animation_steps:
            self.player_animation_steps = []
        if not player_action_steps:
            self.player_action_steps = []
        if not player_movement:
            self.player_movement = 0
        if not player_facing:
            self.player_facing = 0
        if not player_action:
            self.player_action = 0


    @property
    def animation_frame(self):
        return self._animation_frame

    @animation_frame.setter
    def animation_frame(self, v_animation_frame):
        self._animation_frame = v_animation_frame
        self.animation_cooldown = randint(150, 240)

    def get_player_is_facing(self, crops_list, farmtiles_list, show_reach=False, screen=None):
        check_rect = pygame.Rect(
            self.rect.x + 8,
            self.rect.y + 8,
            self.rect.width - 16,
            self.rect.height - 16
        )

        if show_reach:
            pygame.draw.rect(screen, (255, 0, 0), check_rect, 2)  # reach of the player

        closest_crop = None
        min_distance = float('inf')

        for crop in crops_list:
            crop_rect = pygame.Rect(crop.posx, crop.posy, crop.surface.get_width(), crop.surface.get_height())
            if check_rect.colliderect(crop_rect):
                player_center = pygame.Vector2(self.rect.center)
                crop_center = pygame.Vector2(crop_rect.center)
                distance = player_center.distance_to(crop_center)
                if distance < min_distance:
                    min_distance = distance
                    closest_crop = crop


        closest_tile = None
        min_distance = float('inf')

        for tile in farmtiles_list:
            tile_rect = pygame.Rect(tile.posx, tile.posy, tile.surface.get_width(), tile.surface.get_height())
            if check_rect.colliderect(tile_rect):
                player_center = pygame.Vector2(self.rect.center)
                tile_center = pygame.Vector2(tile_rect.center)
                distance = player_center.distance_to(tile_center)
                if distance < min_distance:
                    min_distance = distance
                    closest_tile = tile

        self.crop_facing = closest_crop
        self.tile_facing = closest_tile


    def make_player_plow_farmtile(self):
        tile_rect = pygame.Rect(self.tile_facing.posx, self.tile_facing.posy,
                                self.tile_facing.surface.get_width(), self.tile_facing.surface.get_height())

        self.rect.x = tile_rect.centerx - self.rect.width // 2 - 32
        self.rect.y = tile_rect.centery - self.rect.height // 2 - 24
        self.is_plowing = True


    def make_player_face_crop(self):
        crop_rect = pygame.Rect(self.crop_facing.posx, self.crop_facing.posy,
                                self.crop_facing.surface.get_width(), self.crop_facing.surface.get_height())

        dx = crop_rect.centerx - self.rect.centerx
        dy = crop_rect.centery - self.rect.centery

        if abs(dx) > abs(dy):
            if dx > 0:
                self.player_facing = 1
            else:
                self.player_facing = 2
        else:
            if dy > 0:
                self.player_facing = 0
            else:
                self.player_facing = 3

    def get_current_player_frame(self, current_time):

        if current_time - self.player_last_update >= self.animation_cooldown:
            self.animation_frame += 1
            self.player_last_update = current_time

        if self.is_plowing:
            player_images_list = self.player_action_list[self.player_action]
            if self.animation_frame >= len(player_images_list):
                self.animation_frame = 0
                self.tile_facing.plowing_needed = False
                self.is_plowing = False
        else:
            player_images_list = self.player_animation_list[self.player_movement]
            if self.animation_frame >= len(player_images_list):
                self.animation_frame = 0

        self.surface = player_images_list[self.animation_frame]

