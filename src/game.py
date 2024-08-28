import pygame, sys
from paddle import Paddle
from ball import Ball
from pygame.locals import *
from random import randint

pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 30)
fpsClock = pygame.time.Clock()
FPS = 60
SCREENWIDTH = 854
SCREENHEIGHT = 480
GAMENAME = "Pong"

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption(GAMENAME)


class Scoreboard:
    def __init__(self):
        self.leftPlayerScore = 0
        self.rightPlayerScore = 0

scoreboard = Scoreboard()
leftPaddle = Paddle(screen, positionY=(SCREENHEIGHT/2-25), positionX=20)
rightPaddle = Paddle(screen, positionY=(SCREENHEIGHT/2-25), positionX=SCREENWIDTH-20)
ball = Ball(screen, scoreboard, SCREENWIDTH/2, SCREENHEIGHT/2,pygame.Vector2(randint(1,10),randint(1,10)))


def gameloop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            leftPaddle.moveDown()
        if keys[pygame.K_w]:
            leftPaddle.moveUp()
        if keys[pygame.K_o]:
            rightPaddle.moveUp()
        if keys[pygame.K_l]:
            rightPaddle.moveDown()
        ball.move([leftPaddle.getRect(), rightPaddle.getRect()])
        leftPlayerScore = myFont.render(f"{scoreboard.leftPlayerScore}", False, (255,255,255))
        rightPlayerScore = myFont.render(f"{scoreboard.rightPlayerScore}", False, (255,255,255))
        screen.fill(0)
        leftPaddle.draw()
        rightPaddle.draw()
        ball.draw()
        screen.blit(leftPlayerScore, (int(SCREENWIDTH/4), 40))
        screen.blit(rightPlayerScore, (int(3*SCREENWIDTH/4), 40))
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    gameloop()

    