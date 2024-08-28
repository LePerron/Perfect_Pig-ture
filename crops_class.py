import pygame
from farm_tile_class import FarmTiles


class Crops:
    list_surface_crops_animation = []
    crops_planted = []

    def __init__(self, crop_type=0, posx=None, posy=None, p_stage=0, growing=True, harvestable=False, state="normal", tile=None, crop_cooldown=1, last_update=None):
        self.crop_type = crop_type
        self.posx = posx
        self.posy = posy
        self._stage = p_stage
        self.growing = growing
        self.harvestable = harvestable
        self.state = state
        self._tile = tile
        self.crop_cooldown = crop_cooldown
        self.last_update = last_update

        if not self.posx:
            self.posx = 0

        if not self.posy:
            self.posy = 0

        self.surface = None
        self.get_surface()

    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, v_stage):
        if v_stage == "harvesting":
            self._stage += 1
            self.crop_cooldown = None
            self.state = "harvested"
        else:
            if v_stage >= len(Crops.list_surface_crops_animation[self.crop_type]) - 1:
                self.growing = False
                self.harvestable = True
            else:
                self._stage = v_stage
        self.get_surface()

    @property
    def tile(self):
        return self._tile

    @tile.setter
    def tile(self, v_tile):
        self._tile = v_tile
        self.tile.crop_planted = self

    def get_surface(self):
        self.surface = Crops.list_surface_crops_animation[self.crop_type][self._stage]

    def is_valid_placing(self):
        return not self.square.collideobjects(Crops.get_rects_crops()) and self.square.collideobjects(FarmTiles.get_rects_tiles())

    def update(self, sizebtwn):
        x, y = pygame.mouse.get_pos()
        ix = x // sizebtwn
        iy = y // sizebtwn
        self.posx, self.posy = ix * sizebtwn, iy * sizebtwn
        self.square = pygame.Rect(self.posx, self.posy, sizebtwn, sizebtwn)

    def draw(self, screen):
        temp_surface = Crops.list_surface_crops_animation[self.crop_type][-2]
        screen.blit(temp_surface, (self.square.x, self.square.y))
        if self.is_valid_placing():
            screen.blit(self.colorize(temp_surface, (0, 255, 0)), (self.square.x, self.square.y))
        else:
            screen.blit(self.colorize(temp_surface, (255, 0, 0)), (self.square.x, self.square.y))

    @staticmethod
    def colorize(image, new_color):
        image = image.copy()
        image.fill((0, 0, 0, 70), None, pygame.BLEND_RGBA_MULT)
        image.fill(new_color[0:3] + (0,), None, pygame.BLEND_ADD)
        return image

    @classmethod
    def create_crop(cls, crop):
        cls.crops_planted.append(crop)

    @classmethod
    def get_rects_crops(cls):
        return [c.square for c in cls.crops_planted]

    def remove_crop(self):
        Crops.crops_planted.remove(self)
        del self

