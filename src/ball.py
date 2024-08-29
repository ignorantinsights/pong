import pygame
from random import randint


class Ball:
    def __init__(self, screen, scoreboard, position_x=0, position_y=0, velocity=pygame.Vector2(0.0,0.0), radius=10, color=pygame.Color(255,255,255)):
        self.position_x = position_x
        self.position_y = position_y
        self.velocity = velocity
        self.radius = radius
        self.screen = screen
        self.color = color
        self.rect = pygame.Rect(self.position_x-self.radius, self.position_y-self.radius, self.radius*2, self.radius*2)
        self.scoreboard = scoreboard
    def reset(self):
        self.velocity = pygame.Vector2(randint(1,10),randint(1,10))
        self.position_x = self.screen.get_width()/2
        self.position_y = self.screen.get_height()/2
        self.rect = pygame.Rect(self.position_x-self.radius, self.position_y-self.radius, self.radius*2, self.radius*2)
        print(f"{self.scoreboard.left_player_score}, {self.scoreboard.right_player_score}")
    def __str__(self):
        return f"{self.position_x},{self.position_y},{self.radius}"
    def move(self, paddles):
        self.position_x += self.velocity.x
        self.position_y += self.velocity.y
        if self.position_x <= self.radius:
            self.scoreboard.right_player_score += 1
            self.reset()
        if self.position_x >= self.screen.get_width()-self.radius:
            self.scoreboard.left_player_score += 1
            self.reset()
        if self.position_y <= self.radius:
            self.position_y = self.radius
            self.velocity.y *= -1
        if self.position_y >= self.screen.get_height()-self.radius:
            self.position_y = self.screen.get_height()-self.radius
            self.velocity.y *= -1
        self.rect = pygame.Rect(self.position_x-self.radius, self.position_y+self.radius, self.radius*2, self.radius*2)
        for paddle in paddles:
            if self.rect.colliderect(paddle):
                self.velocity.x *= -1.1
    def get_rect(self):
        return self.rect
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.position_x, self.position_y), self.radius)