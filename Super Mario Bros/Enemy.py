import pygame
from abc import abstractmethod

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    @abstractmethod
    def update(self, game):
        pass

    def shouldRender(self, game):
        return self.x + self.width - game.dx > 0 and self.x - game.dx < game.dim[0]

class BasicEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dir = 'RIGHT'

    def update(self, game):

        if self.dir == 'RIGHT':
            self.moveRight(game)
        else:
            self.moveLeft(game)

        if super().shouldRender(game):
            pygame.draw.ellipse(game.win, (255, 191, 0), pygame.Rect(self.x - game.dx, self.y, self.width, self.height))

    def moveRight(self, game):
        if self.canMoveRight(game):
            self.x += 1
        else:
            self.dir = 'LEFT'

    def moveLeft(self, game):
        if self.canMoveLeft(game):
            self.x -= 1
        else:
            self.dir = 'RIGHT'

    def canMoveRight(self, game):
        for brick in game.bricks:
            if self.x + self.width >= brick.x and self.x + self.width <= brick.x + brick.width:
                if self.y == brick.y or brick.y > self.y and brick.y < self.y + self.height:
                    return False
        return True

    def canMoveLeft(self, game):
        for brick in game.bricks:
            if self.x <= brick.x + brick.width and self.x >= brick.x:
                if self.y == brick.y or brick.y > self.y and brick.y < self.y + self.height:
                    return False
        return True