import pygame


class FarmTiles:
    farm_tiles = []

    def __init__(self, posx=None, posy=None, plowing_needed=False, surface=None, crop_planted=None):
        self.posx = posx
        self.posy = posy
        self._plowing_needed = plowing_needed
        self.crop_planted = crop_planted

        if not surface:
            self.surface = pygame.image.load("assets/pixil-frame-0.png")

    @property
    def plowing_needed(self):
        return self._plowing_needed

    @plowing_needed.setter
    def plowing_needed(self, v_plowing_needed):
        self._plowing_needed = v_plowing_needed
        if not v_plowing_needed and self.crop_planted and self.crop_planted.state == "harvested":
            self.crop_planted.remove_crop()
            self.crop_planted = None

    def update(self, sizebtwn):
        x, y = pygame.mouse.get_pos()
        ix = x // sizebtwn
        iy = y // sizebtwn
        self.posx, self.posy = ix * sizebtwn, iy * sizebtwn
        self.square = pygame.Rect(self.posx, self.posy, sizebtwn, sizebtwn)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.square, 1)  # DEBUGGING
        screen.blit(self.surface, (self.square.x, self.square.y))
        if self.is_valid_placing():
            screen.blit(self.colorize(self.surface, (0, 255, 0)), (self.square.x, self.square.y))
        else:
            screen.blit(self.colorize(self.surface, (255, 0, 0)), (self.square.x, self.square.y))

    def is_valid_placing(self):
        return not any(self.square.colliderect(rect) for rect in self.get_rects_tiles())

    @staticmethod
    def colorize(image, new_color):
        image = image.copy()
        image.fill((0, 0, 0, 70), None, pygame.BLEND_RGBA_MULT)
        image.fill(new_color[0:3] + (0,), None, pygame.BLEND_ADD)
        return image

    @classmethod
    def create_tile(cls, tile):
        cls.farm_tiles.append(tile)

    @classmethod
    def get_rects_tiles(cls):
        return [f.square for f in cls.farm_tiles]
