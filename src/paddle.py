import pygame

class Paddle:
    def __init__(self, screen, positionX=0, positionY=0, speed=10, width=10, height=100, color=pygame.Color(255,255,255)):
        self.positionX = positionX
        self.positionY = positionY
        self.speed = speed
        self.width = width
        self.height = height
        self.screen = screen
        self.color = color
        self.rect = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
    def __str__(self):
        return f"{self.positionX},{self.positionY},{self.width},{self.height}"
    def moveUp(self):
        self.positionY -= self.speed
        if self.positionY <= 0:
            self.positionY = 0
        self.rect = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
    def moveDown(self):
        self.positionY += self.speed
        if self.positionY >= self.screen.get_height() - self.height:
            self.positionY = self.screen.get_height() - self.height
        self.rect = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
    def getRect(self):
        return self.rect
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)