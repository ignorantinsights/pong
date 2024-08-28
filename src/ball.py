import pygame
from random import randint


class Ball:
    def __init__(self, screen, scoreboard, positionX=0, positionY=0, velocity=pygame.Vector2(0.0,0.0), radius=10, color=pygame.Color(255,255,255)):
        self.positionX = positionX
        self.positionY = positionY
        self.velocity = velocity
        self.radius = radius
        self.screen = screen
        self.color = color
        self.rect = pygame.Rect(self.positionX-self.radius, self.positionY-self.radius, self.radius*2, self.radius*2)
        self.scoreboard = scoreboard
    def reset(self):
        self.velocity = pygame.Vector2(randint(1,10),randint(1,10))
        self.positionX = self.screen.get_width()/2
        self.positionY = self.screen.get_height()/2
        self.rect = pygame.Rect(self.positionX-self.radius, self.positionY-self.radius, self.radius*2, self.radius*2)
        print(f"{self.scoreboard.leftPlayerScore}, {self.scoreboard.rightPlayerScore}")
    def __str__(self):
        return f"{self.positionX},{self.positionY},{self.radius}"
    def move(self, paddles):
        self.positionX += self.velocity.x
        self.positionY += self.velocity.y
        if self.positionX <= self.radius:
            self.scoreboard.rightPlayerScore += 1
            self.reset()
        if self.positionX >= self.screen.get_width()-self.radius:
            self.scoreboard.leftPlayerScore += 1
            self.reset()
        if self.positionY <= self.radius:
            self.positionY = self.radius
            self.velocity.y *= -1
        if self.positionY >= self.screen.get_height()-self.radius:
            self.positionY = self.screen.get_height()-self.radius
            self.velocity.y *= -1
        self.rect = pygame.Rect(self.positionX-self.radius, self.positionY+self.radius, self.radius*2, self.radius*2)
        for paddle in paddles:
            if self.rect.colliderect(paddle):
                self.velocity.x *= -1.1
    def getRect(self):
        return self.rect
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.positionX, self.positionY), self.radius)