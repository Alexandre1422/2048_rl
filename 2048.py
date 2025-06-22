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

colors = {
    2: (230, 230, 230),
    4: (255, 200, 200),
    8: (255, 150, 150),
    16: (255, 100, 100),
    32: (255, 50, 50),
    64: (255, 0, 0),
    128: (200, 200, 0),
    256: (150, 150, 0),
    512: (100, 100, 0),
    1024: (50, 50, 0),
    2048: (0, 0, 0)
}

ball_speed = [5, 5]
i=0
for i in range(4):
    j=0
    for j in range(4):
        place[i][j] = pygame.Rect(35+i*110, 45+j*110, 100, 100)

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



def movecase(direction):
    if direction == 3:  # Up
        for j in range(4):
            for i in range(1, 4):
                if fill[i][j] is not None:
                    k = i
                    while k > 0 and (fill[k-1][j] is None or fill[k-1][j] == fill[k][j]):
                        if fill[k-1][j] is None:
                            fill[k-1][j] = fill[k][j]
                        elif fill[k-1][j] == fill[k][j]:
                            fill[k-1][j] *= 2
                        fill[k][j] = None
                        k -= 1
                    redrawcase()

    elif direction == 4:  # Down
        for j in range(4):
            for i in range(2, -1, -1):
                if fill[i][j] is not None:
                    k = i
                    while k < 3 and (fill[k+1][j] is None or fill[k+1][j] == fill[k][j]):
                        if fill[k+1][j] is None:
                            fill[k+1][j] = fill[k][j]
                        elif fill[k+1][j] == fill[k][j]:
                            fill[k+1][j] *= 2
                        fill[k][j] = None
                        k += 1
                    redrawcase()

    elif direction == 1:  # Left
        for i in range(4):
            for j in range(1, 4):
                if fill[i][j] is not None:
                    k = j
                    while k > 0 and (fill[i][k-1] is None or fill[i][k-1] == fill[i][k]):
                        if fill[i][k-1] is None:
                            fill[i][k-1] = fill[i][k]
                        elif fill[i][k-1] == fill[i][k]:
                            fill[i][k-1] *= 2
                        fill[i][k] = None
                        k -= 1
                    redrawcase()

    elif direction == 2:  # Right
        for i in range(4):
            for j in range(2, -1, -1):
                if fill[i][j] is not None:
                    k = j
                    while k < 3 and (fill[i][k+1] is None or fill[i][k+1] == fill[i][k]):
                        if fill[i][k+1] is None:
                            fill[i][k+1] = fill[i][k]
                        elif fill[i][k+1] == fill[i][k]:
                            fill[i][k+1] *= 2
                        fill[i][k] = None
                        k += 1
                    redrawcase()


def redrawcase():
    for i in range(4):
        for j in range(4):
            cell_value = fill[i][j]
            if cell_value is not None:
                text = str(cell_value)
                text_surf = font.render(text, True, (10, 10, 10))
                text_rect = text_surf.get_rect(center=place[i][j].center)
                pygame.draw.rect(win, colors[cell_value], place[i][j])
                win.blit(text_surf, text_rect)
            else:
                pygame.draw.rect(win, (255, 255, 255), place[i][j])
    pygame.display.flip()

def drawscore():
    pygame.draw.rect(win, (0, 0, 0), (0, 0, 200, 40))
    score = sum(cell for row in fill for cell in row if cell is not None)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))
    pygame.display.flip()

def drawcase():
    cell = get_random_empty_cell()
    if cell is not None:
        i, j = cell
        if random.randint(1, 10) == 1:
            text = "4"
            fill[i][j] = 4
        else:
            text = "2"
            fill[i][j] = 2
        text_surf = font.render(text, True, (10, 10, 10))
        text_rect = text_surf.get_rect(center=place[i][j].center)
        pygame.draw.rect(win, colors[fill[i][j]], place[i][j])
        win.blit(text_surf, text_rect)
        
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
        movecase(1)
        drawcase()
        drawscore()
        wait = pygame.time.wait(300)
    if keys[pygame.K_DOWN]:
        movecase(2)
        drawcase()
        drawscore()
        wait = pygame.time.wait(300)
    if keys[pygame.K_LEFT]:
        movecase(3)
        drawcase()
        drawscore()
        wait = pygame.time.wait(300)
    if keys[pygame.K_RIGHT]:
        movecase(4)
        drawcase()
        drawscore()
        wait = pygame.time.wait(300)
                
                

    

    
    clock.tick(60)
