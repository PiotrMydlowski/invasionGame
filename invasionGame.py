import pygame
import random
import os
import math

pygame.init()

screenWidth = 600
screenHeight = 400

class Actor():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.shape = pygame.Rect(self.x, self. y, self. width, self.height)
        self.graphics = pygame.image.load(os.path.join('actorInvasion.gif'))
    def draw(self):
        screen.blit(self.graphics, (self.x, self.y))
    def move(self, vX, vY):
        if self.y < (screenHeight - self.height) or vY < 0:
            if vY > 0 or self.y > 0:
                self.y = self.y + vY
        if self.x < (screenWidth - self.width) or vX < 0:
            if vX > 0 or self.x > 0:
                self.x = self.x + vX
                
        self.shape = pygame.Rect(self.x, self. y, self. width, self.height)

class Obstacle():
    def __init__(self, playerActor):
        self.x = playerActor.x
        self.y = playerActor.y
        while math.fabs(self.x - playerActor.x) < playerActor.width + 10:
            self.x = random.randint(0, screenWidth)
        while math.fabs(self.y - playerActor.y) < playerActor.height + 10:
            self.y = random.randint(0, screenHeight)
        self.dX = 0
        self.dY = 0
        while self.dX == 0:
            self.dX = random.randint(-10, 10)/10
        while self.dY == 0:
            self.dY = random.randint(-10, 10)/10
        self.obstacleWidth = 20
        self.obstacleHeight = 20
        self.color = (0,255,0)
        self.shape = pygame.Rect(self.x, self.y, self.obstacleWidth, self.obstacleHeight)
    def draw(self):
        pygame.draw.rect(screen, self.color, self.shape, 0)
    def move(self, v):
        self.x = self.x + v*self.dX
        self.y = self.y + v*self.dY
        self.shape = pygame.Rect(self.x, self.y, self.obstacleWidth, self.obstacleHeight)
    def crash(self, playerRect):
        if self.shape.colliderect(playerRect):
            return True
        else:
            return False
       
screen = pygame.display.set_mode((screenWidth,screenHeight))

def write(text, x, y, size):
    writingFont = pygame.font.SysFont("Arial", size)
    rend = writingFont.render(text, 1, (255, 100, 100))
    screen.blit(rend, (x, y))

def writeInMiddle(text, size):
    writingFont = pygame.font.SysFont("Arial", size)
    rend = writingFont.render(text, 1, (255, 100, 100))
    x = (screenWidth - rend.get_rect().width) /2
    y = (screenHeight - rend.get_rect().height) /2
    screen.blit(rend, (x, y))

activeScreen = "menu"
dx = 0
dy = 0
obstacles = []
obstacleAmount = 7
obstacleSpeed = 0.1
player = Actor(screenWidth/2, screenHeight/2)

while True:
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if dy == 0:
                    dy = - 0.2
                else:
                    dy = 0
            if event.key == pygame.K_DOWN:
                if dy == 0:
                    dy = 0.2
                else:
                    dy = 0
            if event.key == pygame.K_LEFT:
                if dx == 0:
                    dx = - 0.2
                else:
                    dx = 0
            if event.key == pygame.K_RIGHT:
                if dx == 0:
                    dx = 0.2
                else:
                    dx = 0
            if event.key == pygame.K_SPACE:
                if activeScreen != "play":
                    obstacles.clear()
                    player = Actor(screenWidth/2, screenHeight/2)
                    for i in range (obstacleAmount):
                        obstacles.append(Obstacle(player))
                    dy = 0
                    dx = 0
                    activeScreen = "play"
                    points = 0
                        
    if activeScreen == "menu":
        write ("INVASION", 20, 20, 50)
        writeInMiddle ("Press space bar to start...", 25)
        logo = pygame.image.load(os.path.join('actorInvasion.gif'))
        screen.blit(logo, (400, 40))

    elif activeScreen == "end":
        write ("INVASION", 20, 20, 50)
        write ("You have been caught! Your result: " + str(points), 20, 100, 25)
        writeInMiddle ("Press space bar to start again...", 25)
        logo = pygame.image.load(os.path.join('actorInvasion.gif'))
        screen.blit(logo, (400, 40))

    elif activeScreen == "play":
        for p in obstacles:
            p.move(obstacleSpeed)
            p.draw()
            if p.crash(player.shape):
                activeScreen = "end"
        for p in obstacles:
            if p.x <= -p.obstacleWidth:
                obstacles.remove(p)
                obstacles.append(Obstacle(player))
                points = points + 1
            elif p.x > screenWidth:
                obstacles.remove(p)
                obstacles.append(Obstacle(player))
                points = points + 1
            elif p.y <= -p.obstacleHeight:
                obstacles.remove(p)
                obstacles.append(Obstacle(player))
                points = points + 1
            elif p.y > screenHeight:
                obstacles.remove(p)
                obstacles.append(Obstacle(player))
                points = points + 1
        player.draw()
        player.move(dx, dy)
        write ("P: "+str(points), screenWidth - 100, screenHeight - 30, 20)
        
    pygame.display.update()
