import pygame
import sys
import math
import os
import random

# --- Constants ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 1280, 720
FPS = 30

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_SCORES = "scores"

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Russell's Math Game")
font = pygame.font.SysFont("Arial", 24, bold=True)
clock = pygame.time.Clock()

# --- High Scores ---
HS_FILE = "high-scores.txt"
if not os.path.exists(HS_FILE):
    open(HS_FILE, "w").close()

# --- ASCII Globe Setup ---
x_sep, y_sep = 10, 20
rows = HEIGHT // y_sep
cols = WIDTH // x_sep
screen_size = rows * cols
x_offset, y_offset = cols / 2, rows / 2
theta_spacing = 10
phi_spacing = 1
chars = ".,-~:;=!*#$@"
A, B = 0, 0  # rotation angles

def draw_ascii_globe(surface):
    global A, B
    z = [0] * screen_size
    b = [' '] * screen_size

    for j in range(0, 628, theta_spacing):
        for i in range(0, 628, phi_spacing):
            c = math.sin(i)
            d = math.cos(j)
            e = math.sin(A)
            f = math.sin(j)
            g = math.cos(A)
            h = d + 2
            D = 1 / (c * h * e + f * g + 5)
            l = math.cos(i)
            m = math.cos(B)
            n = math.sin(B)
            t = c * h * g - f * e
            x = int(x_offset + 40 * D * (l * h * m - t * n))
            y = int(y_offset + 20 * D * (l * h * n + t * m))
            o = x + cols * y
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
            if 0 <= y < rows and 0 <= x < cols and D > z[o]:
                z[o] = D
                b[o] = chars[max(N, 0)]

    A += 0.04
    B += 0.0002

    y_pos = 0
    x_pos = 0
    for idx, ch in enumerate(b):
        text = font.render(ch, True, WHITE)
        surface.blit(text, (x_pos, y_pos))
        x_pos += x_sep
        if (idx + 1) % cols == 0:
            y_pos += y_sep
            x_pos = 0

# --- Menu ---
def draw_menu():
    title = font.render("Russell's Really Cool Math Game", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    buttons = ["Start Game", "View High Scores", "Quit Game"]
    button_rects = []
    for i, text in enumerate(buttons):
        txt_surf = font.render(text, True, WHITE)
        rect = txt_surf.get_rect(center=(WIDTH // 2, 250 + i * 60))
        pygame.draw.rect(screen, (50, 50, 50), rect.inflate(20, 10))
        screen.blit(txt_surf, rect)
        button_rects.append((rect, text))
    return button_rects

# --- Game ---
def run_game():
    score = 0
    problems = []
    input_text = ""
    start_ticks = pygame.time.get_ticks()
    current_q = generate_problem()

    while True:
        screen.fill(BLACK)
        draw_ascii_globe(screen)

        # Timer
        seconds = 60 - (pygame.time.get_ticks() - start_ticks) // 1000
        if seconds <= 0:
            save_score(score)
            return  # Exit to menu

        # Draw
        timer_surf = font.render(f"Time: {seconds}", True, WHITE)
        score_surf = font.render(f"Score: {score}", True, WHITE)
        q_surf = font.render(f"{current_q[0]} + {current_q[1]} = {input_text}", True, WHITE)
        screen.blit(timer_surf, (50, 20))
        screen.blit(score_surf, (WIDTH - 150, 20))
        screen.blit(q_surf, (WIDTH // 2 - q_surf.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit():
                        if int(input_text) == sum(current_q):
                            score += 1
                        else:
                            score -= 1
                        current_q = generate_problem()
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode

        clock.tick(FPS)

def generate_problem():
    return (random.randint(10, 99), random.randint(10, 99))

# --- High Scores ---
# TO DO:
# - Add a text entry for player name

def save_score(score):
    name = "Player"
    with open(HS_FILE, "a") as f:
        f.write(f"{name},{score}\n")

def load_scores():
    scores = []
    with open(HS_FILE, "r") as f:
        for line in f:
            name, val = line.strip().split(",")
            scores.append((name, int(val)))
    return sorted(scores, key=lambda x: x[1], reverse=True)[:10]

def show_scores():
    while True:
        screen.fill(BLACK)
        draw_ascii_globe(screen)
        scores = load_scores()
        title = font.render("High Scores", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        for i, (name, score) in enumerate(scores):
            line = font.render(f"{i+1}. {name} - {score}", True, WHITE)
            screen.blit(line, (WIDTH // 2 - 100, 150 + i * 40))

        back_txt = font.render("Press ESC to return", True, WHITE)
        screen.blit(back_txt, (WIDTH // 2 - back_txt.get_width() // 2, HEIGHT - 60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        clock.tick(FPS)

# --- Main Loop ---
def main():
    state = STATE_MENU
    while True:
        screen.fill(BLACK)
        draw_ascii_globe(screen)

        if state == STATE_MENU:
            buttons = draw_menu()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, label in buttons:
                        if rect.collidepoint(event.pos):
                            if label == "Start Game":
                                run_game()
                            elif label == "View High Scores":
                                show_scores()
                            elif label == "Quit Game":
                                pygame.quit()
                                sys.exit()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
