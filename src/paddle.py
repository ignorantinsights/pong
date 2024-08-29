import pygame

class Paddle:
    def __init__(self, screen, position_x=0, position_y=0, speed=10, width=10, height=100, color=pygame.Color(255,255,255)):
        self.position_x = position_x
        self.position_y = position_y
        self.speed = speed
        self.width = width
        self.height = height
        self.screen = screen
        self.color = color
        self.rect = pygame.Rect(self.position_x, self.position_y, self.width, self.height)
    def __str__(self):
        return f"{self.position_x},{self.position_y},{self.width},{self.height}"
    def moveUp(self):
        self.position_y -= self.speed
        if self.position_y <= 0:
            self.position_y = 0
        self.rect = pygame.Rect(self.position_x, self.position_y, self.width, self.height)
    def moveDown(self):
        self.position_y += self.speed
        if self.position_y >= self.screen.get_height() - self.height:
            self.position_y = self.screen.get_height() - self.height
        self.rect = pygame.Rect(self.position_x, self.position_y, self.width, self.height)
    def get_rect(self):
        return self.rect
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)