import pygame
import random
import math
import asyncio
import os

pygame.init()

# Auto-detect path: works both locally AND in pygbag web build
if os.path.exists("Space_Shooter/rocket.png"):
    PATH = "Space_Shooter/"   # running locally in VS Code
else:
    PATH = ""                  # running in pygbag web

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Shooter")

icon = pygame.image.load(PATH + "rocket.png")
pygame.display.set_icon(icon)

rocketimg = pygame.image.load(PATH + "rocket.png")
rocketx = 390
rockety = 500
x = rocketx
y = rockety
changex = 0

ufoimg = []
ufox = []
ufoy = []
prev_ufox = []
ufo_xchange = 1
ufo_ychange = 20
num = 7

for i in range(num):
    ufoimg.append(pygame.image.load(PATH + "ufo.png"))
    ufox.append(random.randint(0, 736))
    ufoy.append(random.randint(0, 100))
    prev_ufox.append(ufox[i] - 1)

space = pygame.image.load(PATH + "space.png")
bulletimg = pygame.image.load(PATH + "bullet.png")
fired = False
bulletx = x
bullety = y

def rocket(x, y):
    screen.blit(rocketimg, (x, y))

def ufo(x, y, i):
    screen.blit(ufoimg[i], (x, y))

def background():
    screen.blit(space, (0, 0))

def bulletfire(x, y):
    global fired
    fired = True
    screen.blit(bulletimg, (x, y))

def iscollision(bulletx, bullety, ufox, ufoy):
    distance = math.sqrt(math.pow(ufox - bulletx, 2) + math.pow(ufoy - bullety, 2))
    return distance < 29

value = 0
font = pygame.font.SysFont('freesansbold.ttf', 32)
big_font = pygame.font.SysFont('freesansbold.ttf', 64)
textx = 10
texty = 10

def showscore(x, y):
    score = font.render("SCORE : " + str(value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_game_over():
    end_game = big_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(end_game, (200, 250))


async def main():
    global x, y, changex, fired, bulletx, bullety, value

    running = True
    while running:
        screen.fill((0, 0, 0))
        background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    changex = -2
                if event.key == pygame.K_RIGHT:
                    changex = 2
                if event.key == pygame.K_SPACE:
                    if fired == False:
                        bulletx = x
                        bullety = y
                        bulletfire(x + 16, y - 10)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    changex = 0

        if changex < 0 and x + changex > 0:
            x += changex
        elif changex > 0 and x + changex < 736:
            x += changex

        rocket(x, y)

        for i in range(num):
            if ufoy[i] > 200:
                for j in range(num):
                    ufoy[j] = 2000
                show_game_over()
                break

            if prev_ufox[i] < ufox[i]:
                prev_ufox[i] = ufox[i]
                ufox[i] += ufo_xchange
                if ufox[i] >= 736:
                    prev_ufox[i] = ufox[i] + 1
                    ufoy[i] += ufo_ychange
            elif prev_ufox[i] > ufox[i]:
                prev_ufox[i] = ufox[i]
                ufox[i] -= ufo_xchange
                if ufox[i] <= 0:
                    prev_ufox[i] = ufox[i] - 1
                    ufoy[i] += ufo_ychange

            if iscollision(bulletx, bullety, ufox[i], ufoy[i]):
                fired = False
                bulletx = x
                bullety = y
                ufox[i] = random.randint(0, 736)
                ufoy[i] = random.randint(0, 100)
                prev_ufox[i] = ufox[i] - 1
                value += 1

            ufo(ufox[i], ufoy[i], i)

        if bullety <= 0:
            fired = False
            bulletx = x
            bullety = y

        if fired == True:
            bullety -= 3
            bulletfire(bulletx + 16, bullety - 10)

        showscore(textx, texty)
        pygame.display.update()
        await asyncio.sleep(0)  

asyncio.run(main())  