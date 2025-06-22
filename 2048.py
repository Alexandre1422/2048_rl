import pygame
import sys
import random
import time
import copy

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
    2048: (0, 0, 50),
    4096: (0, 50, 50),
    8192: (50, 50, 50),
    16384: (50, 50, 100),
    32768: (50, 100, 100)
}

# Initialisation des cases
for i in range(4):
    for j in range(4):
        place[i][j] = pygame.Rect(35+i*110, 45+j*110, 100, 100)

# Hyperparamètres Q-learning
alpha = 0.1
gamma = 0.9
epsilon = 0.99  # Commencer avec plus d'exploration
epsilon_decay = 0.995
epsilon_min = 0.001
max_steps = 5000
actions = ['up', 'down', 'left', 'right']
Q = {}

# Variables pour les métriques et l'évaluation
total_episodes = 0
best_episode_reward = float('-inf')
best_episode_steps = float('inf')
best_episode_time = float('inf')
episode_rewards = []
episode_steps = []
episode_times = []
current_episode_start_time = 0
current_episode_reward = 0
episode_step = 0
current_state = None
current_action = None

# Mode de jeu
HUMAN_MODE = 0
AI_MODE = 1
game_mode = AI_MODE

def drawplace():
    win.fill((0, 0, 0))
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(win, (255, 255, 255), place[i][j])
    pygame.display.flip()
    
def get_random_empty_cell():
    empty_cells = [(i, j) for i in range(4) for j in range(4) if fill[i][j] is None]
    if empty_cells:
        return random.choice(empty_cells)
    return None

def board_changed(old_board, new_board):
    """Vérifie si le plateau a changé après un mouvement"""
    for i in range(4):
        for j in range(4):
            if old_board[i][j] != new_board[i][j]:
                return True
    return False

def movecase(direction):
    old_fill = copy.deepcopy(fill)
    
    if direction == 3:  # Up
        for j in range(4):
            for i in range(1, 4):
                if fill[i][j] is not None:
                    k = i
                    while k > 0 and fill[k-1][j] is None:
                        fill[k-1][j] = fill[k][j]
                        fill[k][j] = None
                        k -= 1
                    if k > 0 and fill[k-1][j] == fill[k][j]:
                        fill[k-1][j] *= 2
                        fill[k][j] = None

    elif direction == 4:  # Down
        for j in range(4):
            for i in range(2, -1, -1):
                if fill[i][j] is not None:
                    k = i
                    while k < 3 and fill[k+1][j] is None:
                        fill[k+1][j] = fill[k][j]
                        fill[k][j] = None
                        k += 1
                    if k < 3 and fill[k+1][j] == fill[k][j]:
                        fill[k+1][j] *= 2
                        fill[k][j] = None

    elif direction == 1:  # Left
        for i in range(4):
            for j in range(1, 4):
                if fill[i][j] is not None:
                    k = j
                    while k > 0 and fill[i][k-1] is None:
                        fill[i][k-1] = fill[i][k]
                        fill[i][k] = None
                        k -= 1
                    if k > 0 and fill[i][k-1] == fill[i][k]:
                        fill[i][k-1] *= 2
                        fill[i][k] = None

    elif direction == 2:  # Right
        for i in range(4):
            for j in range(2, -1, -1):
                if fill[i][j] is not None:
                    k = j
                    while k < 3 and fill[i][k+1] is None:
                        fill[i][k+1] = fill[i][k]
                        fill[i][k] = None
                        k += 1
                    if k < 3 and fill[i][k+1] == fill[i][k]:
                        fill[i][k+1] *= 2
                        fill[i][k] = None
    
    return board_changed(old_fill, fill)

def redrawcase():
    win.fill((0, 0, 0))
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(win, (255, 255, 255), place[i][j])
            cell_value = fill[i][j]
            if cell_value is not None:
                text = str(cell_value)
                colortext = (245, 245, 245) if cell_value > 256 else (10, 10, 10)
                text_surf = font.render(text, True, colortext)
                text_rect = text_surf.get_rect(center=place[i][j].center)
                pygame.draw.rect(win, colors.get(cell_value, (100, 100, 100)), place[i][j])
                win.blit(text_surf, text_rect)
    pygame.display.flip()

def drawscore():
    score = sum(cell for row in fill for cell in row if cell is not None)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    mode_text = font.render(f"Mode: {'AI' if game_mode == AI_MODE else 'Human'}", True, (255, 255, 255))
    episode_text = font.render(f"Episode: {total_episodes}", True, (255, 255, 255))

    win.blit(score_text, (10, 10))
    #win.blit(mode_text, (100, 10))
    win.blit(episode_text, (300, 10))
    pygame.display.flip()

def drawcase():
    cell = get_random_empty_cell()
    if cell is not None:
        i, j = cell
        #if random.randint(1, 10) == 1:
        #    fill[i][j] = 4
        #else:
        fill[i][j] = 2
        redrawcase()
        drawscore()
        return True
    return False

def is_game_over():
    # Vérifie s'il reste une case vide
    for i in range(4):
        for j in range(4):
            if fill[i][j] is None:
                return False
            # Vérifie fusion possible à droite
            if j < 3 and fill[i][j] == fill[i][j+1]:
                return False
            # Vérifie fusion possible en bas
            if i < 3 and fill[i][j] == fill[i+1][j]:
                return False
    return True

def discretize_state():
    """Convertit l'état du plateau en tuple pour utilisation comme clé dans Q"""
    state = []
    for i in range(4):
        for j in range(4):
            state.append(fill[i][j] if fill[i][j] is not None else 0)
    return tuple(state)

def get_q(state):
    if state not in Q:
        Q[state] = [0.0 for _ in actions]
    return Q[state]

def choose_action(state):
    q_values = get_q(state)
    if random.random() < epsilon:
        return random.randint(0, len(actions) - 1)
    max_value = max(q_values)
    max_indices = [i for i, v in enumerate(q_values) if v == max_value]
    return random.choice(max_indices)

def get_reward(old_state, new_state, moved):
    """Calcule la récompense basée sur l'état du jeu"""
    if not moved:
        return -10  # Pénalité pour mouvement invalide
    
    # Récompense basée sur la fusion (score réel du jeu 2048)
    old_score = sum(cell for cell in old_state if cell != 0)
    new_score = sum(cell for cell in new_state if cell != 0)
    score_increase = new_score - old_score
    
    # Récompense supplémentaire pour les tuiles élevées (encourager la progression)
    max_tile_old = max(cell for cell in old_state if cell != 0)
    max_tile_new = max(cell for cell in new_state if cell != 0)
    max_tile_bonus = 0
    if max_tile_new > max_tile_old:
        max_tile_bonus = max_tile_new * 0.5  # Bonus proportionnel à la valeur de la tuile
    
    # Récompense pour atteindre 2048
    if max_tile_new >= 2048:
        return 1000
    
    # Récompense pour maintenir des espaces vides (stratégie importante)
    empty_cells = sum(1 for cell in new_state if cell == 0)
    empty_bonus = empty_cells * 2  # Valoriser les espaces vides
    
    # Combinaison des récompenses
    reward = score_increase * 0.1 + max_tile_bonus + empty_bonus
    
    # Pénalité si le jeu est terminé (proportionnelle au score final)
    if is_game_over():
        # Pénalité moins sévère pour les parties longues avec un bon score
        game_progress = sum(new_state) / 2048  # Mesure de progression
        reward -= max(20, 100 - game_progress)
    
    return reward

def reset_episode():
    global fill, current_episode_start_time, current_episode_reward, episode_step
    global total_episodes, epsilon
    
    # Enregistrer les métriques de l'épisode qui vient de se terminer
    if total_episodes > 0:
        episode_time = time.time() - current_episode_start_time
        episode_times.append(episode_time)
        episode_rewards.append(current_episode_reward)
        episode_steps.append(episode_step)
        
        # Mettre à jour les meilleures métriques si nécessaire
        update_best_metrics(current_episode_reward, episode_step, episode_time)
        
        # Afficher les progrès
        if total_episodes % 10 == 0:
            print(f"Episode {total_episodes}: Reward={current_episode_reward:.2f}, Steps={episode_step}, Epsilon={epsilon:.4f}")
    
    # Réinitialiser pour le nouvel épisode
    fill = [[None for _ in range(4)] for _ in range(4)]
    
    # Ajouter les deux premières tuiles
    drawcase()
    drawcase()
    
    redrawcase()
    drawscore()
    
    # Démarrer le chronomètre pour le nouvel épisode
    current_episode_start_time = time.time()
    current_episode_reward = 0
    episode_step = 0
    total_episodes += 1
    
    # Décroissance d'epsilon
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    
    return discretize_state()

def update_best_metrics(reward, steps, episode_time):
    global best_episode_reward, best_episode_steps, best_episode_time
    
    if reward > best_episode_reward:
        best_episode_reward = reward
        best_episode_steps = steps
        best_episode_time = episode_time
        
        print(f"NOUVEAU RECORD! Episode {total_episodes}")
        print(f"  Recompense: {best_episode_reward:.3f}")
        print(f"  Etapes: {best_episode_steps}")
        print(f"  Temps: {best_episode_time:.2f} sec")

def print_summary():
    """Affiche un résumé des performances d'apprentissage"""
    print("\n===== RESUME DE L'APPRENTISSAGE =====")
    print(f"Total des episodes: {total_episodes}")
    print(f"Epsilon final: {epsilon:.6f}")
    print("\nMEILLEURE PERFORMANCE:")
    print(f"  Recompense: {best_episode_reward:.3f}")
    print(f"  Etapes: {best_episode_steps}")
    print(f"  Temps: {best_episode_time:.2f} sec")
    
    window = min(50, len(episode_rewards))
    if window > 0:
        avg_reward = sum(episode_rewards[-window:]) / window
        avg_steps = sum(episode_steps[-window:]) / window
        
        print(f"\nMOYENNE (derniers {window} episodes):")
        print(f"  Recompense: {avg_reward:.3f}")
        print(f"  Etapes: {avg_steps:.1f}")
    
    print(f"\nEtats explores: {len(Q)}")

# Initialisation
drawplace()
drawcase()
drawcase()
redrawcase()
drawscore()
current_episode_start_time = time.time()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if game_mode == AI_MODE:
                print_summary()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # Changer de mode avec 'M'
                game_mode = AI_MODE if game_mode == HUMAN_MODE else HUMAN_MODE
                print(f"Mode changé vers: {'AI' if game_mode == AI_MODE else 'Human'}")
                if game_mode == AI_MODE:
                    current_state = reset_episode()
                drawscore()

    if game_mode == HUMAN_MODE:
        # Mode joueur humain
        keys = pygame.key.get_pressed()
        moved = False
        
        if keys[pygame.K_UP]:
            moved = movecase(1)
            if moved:
                drawcase()
                redrawcase()
                drawscore()
            pygame.time.wait(200)
        elif keys[pygame.K_DOWN]:
            moved = movecase(2)
            if moved:
                drawcase()
                redrawcase()
                drawscore()
            pygame.time.wait(200)
        elif keys[pygame.K_LEFT]:
            moved = movecase(3)
            if moved:
                drawcase()
                redrawcase()
                drawscore()
            pygame.time.wait(200)
        elif keys[pygame.K_RIGHT]:
            moved = movecase(4)
            if moved:
                drawcase()
                redrawcase()
                drawscore()
            pygame.time.wait(200)
        
        if moved and is_game_over():
            print("Game Over!")
            pygame.time.wait(2000)
            fill = [[None for _ in range(4)] for _ in range(4)]
            drawcase()
            drawcase()
            redrawcase()
            drawscore()
            
    else:
        # Mode IA (Q-learning)
        if current_state is None:
            current_state = reset_episode()
        
        # Choisir une action
        action_index = choose_action(current_state)
        old_state = current_state
        
        # Exécuter l'action
        moved = movecase(action_index + 1)  # +1 car movecase utilise 1-4
        
        if moved:
            drawcase()
        
        redrawcase()
        drawscore()
        
        # Obtenir le nouvel état
        new_state = discretize_state()
        
        # Calculer la récompense
        reward = get_reward(old_state, new_state, moved)
        current_episode_reward += reward
        episode_step += 1
        
        # Mise à jour Q-learning
        old_q_values = get_q(old_state)
        new_q_values = get_q(new_state)
        
        old_q_values[action_index] += alpha * (reward + gamma * max(new_q_values) - old_q_values[action_index])
        
        current_state = new_state
        
        # Vérifier si le jeu est terminé ou limite d'étapes atteinte
        if is_game_over() or episode_step >= max_steps:
            current_state = reset_episode()
        
        # Petit délai pour visualiser
        pygame.time.wait(50)
    
    clock.tick(60)