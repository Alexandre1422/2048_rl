import pygame
import sys
import random

pygame.init()
font = pygame.font.SysFont(None, 36)
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
start = 0
fill = [[None for _ in range(4)] for _ in range(4)]
place = [[None for _ in range(4)] for _ in range(4)]

ball_speed = [5, 5]
i=0
for i in range(4):
    j=0
    for j in range(4):
        place[i][j] = pygame.Rect(35+i*110, 35+j*110, 100, 100)

def drawplace():
    win.fill((0, 0, 0))
    i=0
    for i in range(4):
        j=0
        for j in range(4):
            pygame.draw.rect(win, (255, 255, 255), place[i][j])
    pygame.display.flip()
    
def get_random_empty_cell():
    empty_cells = [(i, j) for i in range(4) for j in range(4) if fill[i][j] is None]
    if empty_cells:
        return random.choice(empty_cells)
    return None

def drawcase():
    cell = get_random_empty_cell()
    if cell is not None:
        i, j = cell
        text = "2"
        text_surf = font.render(text, True, (10, 10, 10))
        text_rect = text_surf.get_rect(center=place[i][j].center)
        pygame.draw.rect(win, (200, 200, 255), place[i][j])
        win.blit(text_surf, text_rect)
        fill[i][j] = 2
        pygame.display.flip()
    else:
        print("Perdu")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if start == 0:
        drawplace()
        start = 1

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        drawcase()
        wait = pygame.time.wait(400)
    if keys[pygame.K_DOWN]:
        drawcase()
        wait = pygame.time.wait(400)
    if keys[pygame.K_LEFT]:
        drawcase()
        wait = pygame.time.wait(400)
    if keys[pygame.K_RIGHT]:
        drawcase()
        wait = pygame.time.wait(400)
                
                

    

    
    clock.tick(60)
