import pygame
from Player import Player
from Brick import Wall, Ground
from Enemy import BasicEnemy

init = pygame.init()
if init[1] != 0:
    print('Pygame failed to initialize')
    quit()

class Game:
    def __init__(self):
        self.dim = (800, 600)
        self.win = pygame.display.set_mode(self.dim)
        pygame.display.set_caption('Super Mario Bros')
        self.player = Player(50, 0, 50, 50)
        self.dx = 0

    def run(self):
        self.generateMap()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
            pygame.display.update()
            self.updateCamera()
            pygame.draw.rect(self.win, (0, 255, 255), (0, 0, self.dim[0], self.dim[1]))
            self.player.update(self)
            for brick in self.bricks:
                brick.update(self)
            for enemy in self.enemies:
                enemy.update(self)
            pygame.time.delay(int(1000/60))
        pygame.quit()

    def updateCamera(self):
        self.dx = max(self.player.x + self.player.width - (self.dim[0] / 2), 0)

    def generateMap(self):
        self.bricks = []
        self.enemies = []
        i = 0
        with open('Map.txt') as world:
            for line in world:
                j = 0
                for state in line:
                    if state == '1':
                        self.bricks.append(Wall(j * 50, i * 50))
                    elif state == '2':
                        self.bricks.append(Ground(j * 50, i * 50))
                    elif state == '3':
                        self.enemies.append(BasicEnemy(j * 50, i * 50))
                    j += 1
                i += 1

game = Game()
game.run()