import pygame
from Enemy import BasicEnemy

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.landed = True
        self.speedY = 0
        self.isRunning = False
    
    def update(self, game):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.canMoveRight(game):
                if self.isRunning:
                    self.x += 4
                else:
                    self.x += 2
        if keys[pygame.K_LEFT]:
            if self.canMoveLeft(game):
                if self.isRunning:
                    self.x -= 4
                else:
                    self.x -= 2
        if keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_LSHIFT]:
            self.isRunning = True
        else:
            self.isRunning = False

        self.killEnemies(game)
        self.moveY()
        self.blockJump(game)
        self.land(game)
        self.drop(game)

        pygame.draw.ellipse(game.win, (255, 0, 0), pygame.Rect(self.x - game.dx, self.y, self.width, self.height))

    def jump(self):
        if self.landed:
            self.speedY = 20
            self.landed = False
    
    def moveY(self):
        if not self.landed:
            self.y -= self.speedY
            self.speedY -= 1

    def drop(self, game):
        if self.landed:
            shouldDrop = True
            for brick in game.bricks:
                if brick.x <= self.x + self.width and brick.x + brick.width >= self.x:
                    if self.y + self.height == brick.y:
                        shouldDrop = False
            if shouldDrop:
                self.landed = False
    
    def land(self, game):
        for brick in game.bricks:
            if brick.x < self.x + self.width and brick.x + brick.width > self.x:
                if self.y + self.height >= brick.y and self.y + self.height <= brick.y + brick.height and self.speedY < 0:
                    if self.checkAboveBricks(game, brick):
                        self.landed = True
                        self.y = brick.y - self.height
                        self.speedY = 0
                        break

    def checkAboveBricks(self, game, brick):
        for b in game.bricks:
            if b.x == brick.x and b.y + b.height == brick.y:
                return False
        return True

    def canMoveRight(self, game):
        for brick in game.bricks:
            if self.x + self.width >= brick.x and self.x + self.width <= brick.x + brick.width:
                if self.y == brick.y or brick.y > self.y and brick.y < self.y + self.height:
                    return False
        return True

    def canMoveLeft(self, game):
        if self.x <= 0:
            return False
        for brick in game.bricks:
            if self.x <= brick.x + brick.width and self.x >= brick.x:
                if self.y == brick.y or brick.y > self.y and brick.y < self.y + self.height:
                    return False
        return True

    def killEnemies(self, game):
        for enemy in game.enemies:
            if type(enemy) == BasicEnemy:
                if enemy.x <= self.x + self.width and enemy.x + enemy.width >= self.x:
                    if self.y + self.height >= enemy.y and self.y + self.height <= enemy.y + enemy.height / 2 and self.speedY < 0:
                        self.y = enemy.y - self.height
                        self.speedY = 15
                        game.enemies.remove(enemy)
                        break
                    elif self.y + self.height < enemy.y or self.y > enemy.y + enemy.height:
                        pass
                    else:
                        self.y = 0
        
    def blockJump(self, game):
        if self.speedY > 0:
            for brick in game.bricks:
                if self.x + self.width > brick.x + 5 and self.x < brick.x + brick.width - 5:
                    if self.y <= brick.y + brick.height and self.y + self.height >= brick.y:
                        self.speedY = 0
                        for enemy in game.enemies:
                            if type(enemy) == BasicEnemy:
                                if enemy.x <= brick.x + brick.width and enemy.x + enemy.width >= brick.x:
                                    if enemy.y + enemy.height == brick.y:
                                        game.enemies.remove(enemy)
                                        break
                        return