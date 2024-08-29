import pygame, sys
from paddle import Paddle
from ball import Ball
from pygame.locals import *
from random import randint

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
fps_clock = pygame.time.Clock()
FPS = 60
SCREENWIDTH = 854
SCREENHEIGHT = 480
GAMENAME = "Pong"

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption(GAMENAME)


class Scoreboard:
    def __init__(self):
        self.left_player_score = 0
        self.right_player_score = 0

scoreboard = Scoreboard()
left_paddle = Paddle(screen, positionY=(SCREENHEIGHT/2-25), positionX=20)
right_paddle = Paddle(screen, positionY=(SCREENHEIGHT/2-25), positionX=SCREENWIDTH-20)
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
            left_paddle.moveDown()
        if keys[pygame.K_w]:
            left_paddle.moveUp()
        if keys[pygame.K_o]:
            right_paddle.moveUp()
        if keys[pygame.K_l]:
            right_paddle.moveDown()
        ball.move([left_paddle.getRect(), right_paddle.getRect()])
        left_player_score = my_font.render(f"{scoreboard.left_player_score}", False, (255,255,255))
        right_player_score = my_font.render(f"{scoreboard.right_player_score}", False, (255,255,255))
        screen.fill(0)
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()
        screen.blit(left_player_score, (int(SCREENWIDTH/4), 40))
        screen.blit(right_player_score, (int(3*SCREENWIDTH/4), 40))
        pygame.display.update()
        fps_clock.tick(FPS)

if __name__ == "__main__":
    gameloop()

    