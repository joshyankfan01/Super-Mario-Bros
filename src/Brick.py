import pygame
from abc import abstractmethod

class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    def shouldRender(self, game):
        return self.x + self.width - game.dx > 0 and self.x - game.dx < game.dim[0]

    @abstractmethod
    def update(self, game):
        pass

class Wall(Brick):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def update(self, game):
        if super().shouldRender(game):
            pygame.draw.rect(game.win, (160,82,45), (self.x - game.dx, self.y, self.width, self.height))
    
class Ground(Brick):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, game):
        if super().shouldRender(game):
            pygame.draw.rect(game.win, (0, 255, 0), (self.x - game.dx, self.y, self.width, self.height))