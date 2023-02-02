import pygame


class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, x_pos, value, color):
        super().__init__()
        self.x = x_pos
        self.y = 50
        self.width = 75
        self.height = value
        self.image = pygame.Surface([self.width, self.height])
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
