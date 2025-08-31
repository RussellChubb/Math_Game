import pygame
import sys
import math
import os
import random

# --- To do ---
'''
1) Fix bug where the scores aren't correctly being written to the .txt file - Getting weird edge case where sometimes I get a completly different high-scores board. Weird behaviour, I just need it to save each completed attempt to the .txt file, and read the .txt file to the screen.
2) Get theming consistent on the different UI elements (buttons, backgrounds, etc.)
3) Move clock to somewhere where people can see the time remaining more easily? (Not sure how I'd go about this, open to ideas)
4) Implement hot streak (if you get 3 in a row, you get a custom sound and maybe some kind of fire effect?)
5) Add a back button to the high-scores screen.
6) Add two different background music tracks, one for the game-state, and one for the menu.
7) Add that Minecraft style random text in the top right hand corner of the menu
8) Add a settings menu where you can change music volume, SFX Volume, time limit, number range, etc.
9) Structure the folder (and the git repo, more appropriately)
10) Figure out how to run tests on the file (linting etc)
11) Create custom .ico file
12) Create logo for the game + Draw the logo on the main-screen.
13) Fix the fade effect, it currently doesn't work as intended. Also, I'd love more of a pixelated fade rather than a clean fade, as it's more in style with the game.
14) Make "Score" larger, (and maybe glow) on the finished game scene (so that people better understand what they achieved)
15) Add a line cursor to the text input field in the game state as well as the enter a name menu once the game has finished.
16) Add in the count-down beep, and then the final buzzer sound.
17) Add explosion sound to the donut explosion at the end of the game.
18) Add in a "Are you sure you want to quit?" prompt when you try and quit the game from the pause menu.
19) Duck Background music when transisioning between screens.
20) Add in a "New High Score!" prompt when you get a new high score.

'''

# --- Sound Setup ---
import os
import pygame

# --- Sound Setup ---
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Sound Folder Path
BASE_PATH = r"C:\Users\rc30\OneDrive - Meridian Energy Limited\Documents\Programming\Personal\Math_Game\Assets"

# Debugging Some Sound Stfuff

def load_sound(filename):
    path = os.path.join(BASE_PATH, filename)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    else:
        print(f"Sound file not found: {path}")
        return None

correct_sound = load_sound("correct.wav")
incorrect_sound = load_sound("incorrect.wav")
timesup_sound = load_sound("timesup.wav")
button_sound = load_sound("button.wav")

# Background music
bg_music_path = os.path.join(BASE_PATH, "background.wav")
if os.path.exists(bg_music_path):
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)
else:
    print(f"Background music not found: {bg_music_path}")

def play_sound(sound):
    if sound:
        sound.set_volume(1.0)
        sound.play()

# --- Smooth Fade Animation ---
def fade_transition(surface, duration=500):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)

    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        alpha = min(255, int((elapsed / duration) * 255))
        fade.set_alpha(alpha)
        surface.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        if elapsed >= duration:
            break

    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        alpha = max(0, 255 - int((elapsed / duration) * 255))
        fade.set_alpha(alpha)
        surface.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        if elapsed >= duration:
            break

# --- Constants ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (30, 30, 30)
WIDTH, HEIGHT = 1280, 720
FPS = 30
PASTEL_GREEN = (144, 238, 144)
PASTEL_RED = (255, 182, 193)

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_SCORES = "scores"

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Russell's Math Game")
clock = pygame.time.Clock()

# --- Fonts ---
def load_font(size):
    try:
        font_path = os.path.join(os.path.dirname(__file__), "VT323-Regular.ttf")
        return pygame.font.Font(font_path, size)
    except FileNotFoundError:
        return pygame.font.SysFont("Arial", size, bold=True)

MENU_TITLE_FONT = load_font(64)
MENU_BUTTON_FONT = load_font(36)
GAME_FONT = load_font(24)

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
A, B = 0, 0

def draw_ascii_globe(surface, capture=False):
    global A, B
    z = [0] * screen_size
    b = [' '] * screen_size
    captured = []

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
        if ch != ' ':
            text = GAME_FONT.render(ch, True, WHITE)
            surface.blit(text, (x_pos, y_pos))
            if capture:
                captured.append((x_pos, y_pos, ch))
        x_pos += x_sep
        if (idx + 1) % cols == 0:
            y_pos += y_sep
            x_pos = 0

    if capture:
        return captured

# --- Glow & Flash Effects ---
glow_color = None
glow_start_time = None
flash_color = None
flash_start_time = None
GLOW_DURATION = 1000
FLASH_DURATION = 500

def draw_glow(surface, rect, color, start_time):
    elapsed = pygame.time.get_ticks() - start_time
    if elapsed < GLOW_DURATION:
        progress = elapsed / GLOW_DURATION
        alpha = max(0, 255 - int(progress * 255))
        pulsate = 10 * math.sin(progress * math.pi * 4)
        glow_rect = rect.inflate(40 + pulsate, 40 + pulsate)
        glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*color, alpha), glow_surf.get_rect(), 10, border_radius=12)
        surface.blit(glow_surf, glow_rect.topleft)
        return True
    return False

def draw_flash(surface, rect, color, start_time):
    elapsed = pygame.time.get_ticks() - start_time
    if elapsed < FLASH_DURATION:
        progress = elapsed / FLASH_DURATION
        alpha = max(0, 100 - int(progress * 100))
        flash_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        flash_surf.fill((*color, alpha))
        surface.blit(flash_surf, rect.topleft)
        return True
    return False

# --- Button Class ---
class Button:
    def __init__(self, text, center, width, height, font, base_color=GREY, text_color=WHITE, hover_color=None, click_color=WHITE):
        self.text = text
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center
        self.font = font
        self.base_color = base_color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color else tuple(max(0, c-40) for c in base_color)
        self.click_color = click_color
        self.clicked = False

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        
        color = self.base_color
        txt_color = self.text_color

        if self.rect.collidepoint(mouse_pos):
            if pressed:
                color = self.click_color
                txt_color = BLACK
                self.clicked = True
            else:
                color = self.hover_color
                self.clicked = False
        else:
            self.clicked = False

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=10)

        txt_surf = self.font.render(self.text, True, txt_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                play_sound(button_sound)
                return True
        return False

# --- Countdown Function ---
def countdown(seconds=3):
    BIG_FONT = load_font(128)
    beep_sound = load_sound("countdown_beep.wav")
    clock = pygame.time.Clock()
    
    start_time = pygame.time.get_ticks()
    current_number = seconds
    
    while current_number > 0:
        elapsed_ms = pygame.time.get_ticks() - start_time
        new_number = seconds - elapsed_ms // 1000
        
        # Only play beep when number changes
        if new_number < current_number:
            current_number = new_number
            if beep_sound:
                beep_sound.play()
        
        screen.fill(BLACK)
        draw_ascii_globe(screen)
        
        # Draw countdown number with white border
        number_text = str(current_number)
        number_surf = BIG_FONT.render(number_text, True, WHITE)
        number_rect = number_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Draw border by blitting text offsets in white
        offsets = [(-4, 0), (4, 0), (0, -4), (0, 4), (-4, -4), (4, -4), (-4, 4), (4, 4)]
        for ox, oy in offsets:
            border_surf = BIG_FONT.render(number_text, True, BLACK)
            screen.blit(border_surf, number_rect.move(ox, oy))
        
        screen.blit(number_surf, number_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

# --- Menu ---

def draw_menu():
    title = MENU_TITLE_FONT.render("Russell's Really Cool Math Game", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    pygame.draw.rect(screen, GREY, title_rect.inflate(40, 20))
    screen.blit(title, title_rect)

    buttons = []
    BUTTON_WIDTH = 400
    BUTTON_HEIGHT = 70
    button_texts = ["Start Game", "View High Scores", "Quit Game"]

    for i, text in enumerate(button_texts):
        btn = Button(text=text, center=(WIDTH // 2, 250 + i * 100),
                     width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=MENU_BUTTON_FONT)
        buttons.append(btn)

    for btn in buttons:
        btn.draw(screen)

    return buttons

# --- Pause Menu ---
def pause_menu():
    BUTTON_WIDTH = 300
    BUTTON_HEIGHT = 60
    paused_A, paused_B = A, B

    buttons = [
        Button("Continue", (WIDTH // 2, HEIGHT // 2 - 30), BUTTON_WIDTH, BUTTON_HEIGHT, MENU_BUTTON_FONT),
        Button("Quit", (WIDTH // 2, HEIGHT // 2 + 60), BUTTON_WIDTH, BUTTON_HEIGHT, MENU_BUTTON_FONT)
    ]

    while True:
        screen.fill(BLACK)
        draw_ascii_globe(screen, capture=False)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(0, 0, 500, 400)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(screen, GREY, panel_rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, panel_rect, 3, border_radius=15)

        title = MENU_TITLE_FONT.render("PAUSED", True, WHITE)
        screen.blit(title, (panel_rect.centerx - title.get_width() // 2, panel_rect.top + 30))

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for btn in buttons:
                if btn.is_clicked(event):
                    if btn.text == "Continue":
                        return
                    elif btn.text == "Quit":
                        return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        clock.tick(FPS)

# --- Game functions ---
def generate_problem():
    return (random.randint(10, 99), random.randint(10, 99))

def donut_explosion(surface, chars_data, duration=1500):
    start_time = pygame.time.get_ticks()
    particles = []

    for (x, y, ch) in chars_data:
        angle = math.atan2(y - HEIGHT // 2, x - WIDTH // 2)
        speed = random.uniform(2, 6)
        vx = math.cos(angle) * speed + random.uniform(-1, 1)
        vy = math.sin(angle) * speed + random.uniform(-1, 1)
        particles.append([x, y, vx, vy, ch])

    while True:
        elapsed = pygame.time.get_ticks() - start_time
        if elapsed > duration:
            break

        surface.fill(BLACK)
        for p in particles:
            p[0] += p[2]
            p[1] += p[3]
            alpha = max(0, 255 - int((elapsed / duration) * 255))
            text = GAME_FONT.render(p[4], True, (255, 255, 255, alpha))
            surface.blit(text, (p[0], p[1]))

        pygame.display.flip()
        clock.tick(FPS)

def run_game():
    global glow_color, glow_start_time, flash_color, flash_start_time

    # Countdown before the game starts
    countdown(5)  # counts down from 5 seconds

    BIG_GAME_FONT = load_font(72)  # original was 24, now 72
    score = 0
    input_text = ""
    start_ticks = pygame.time.get_ticks()
    current_q = generate_problem()

    fade_transition(screen)

    while True:
        screen.fill(BLACK)
        draw_ascii_globe(screen)

        # Draw the main math question with bigger font
        q_surf = BIG_GAME_FONT.render(f"{current_q[0]} + {current_q[1]} = {input_text}", True, WHITE)
        q_rect = q_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Draw the rectangle behind the question
        pygame.draw.rect(screen, GREY, q_rect.inflate(60, 30))
        pygame.draw.rect(screen, WHITE, q_rect.inflate(60, 30), 5)

        # Draw the text
        screen.blit(q_surf, q_rect)

        # Flash effect if active
        if flash_color and flash_start_time:
            still_flashing = draw_flash(screen, q_rect.inflate(120, 60), flash_color, flash_start_time)
            if not still_flashing:
                flash_color, flash_start_time = None, None

        # Glow effect if active
        if glow_color and glow_start_time:
            still_active = draw_glow(screen, q_rect.inflate(0, 0), glow_color, glow_start_time)
            if not still_active:
                glow_color, glow_start_time = None, None

        # Timer and score display
        seconds = 60 - (pygame.time.get_ticks() - start_ticks) // 1000
        timer_surf = GAME_FONT.render(f"Time: {seconds}", True, WHITE)
        score_surf = GAME_FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(timer_surf, (50, 20))
        screen.blit(score_surf, (WIDTH - 150, 20))

        pygame.display.flip()

        # Time’s up
        if seconds <= 0:
            play_sound(timesup_sound)
            chars_data = draw_ascii_globe(screen, capture=True)
            donut_explosion(screen, chars_data)
            fade_transition(screen)
            name_entry_screen(score)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit():
                        if int(input_text) == sum(current_q):
                            score += 1
                            play_sound(correct_sound)
                            glow_color, glow_start_time = (0, 255, 0), pygame.time.get_ticks()
                            flash_color, flash_start_time = PASTEL_GREEN, pygame.time.get_ticks()
                        else:
                            score -= 1
                            play_sound(incorrect_sound)
                            glow_color, glow_start_time = (255, 0, 0), pygame.time.get_ticks()
                            flash_color, flash_start_time = PASTEL_RED, pygame.time.get_ticks()
                        current_q = generate_problem()
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    result = pause_menu()
                    if result == "quit":
                        return
                elif event.unicode.isdigit():
                    input_text += event.unicode

        clock.tick(FPS)

# --- High Scores ---
def save_score(name, score):
    with open(HS_FILE, "a") as f:
        f.write(f"{name},{score}\n")

def load_scores():
    scores = []
    with open(HS_FILE, "r") as f:
        for line in f:
            if "," in line:
                name, val = line.strip().split(",")
                scores.append((name, int(val)))
    return sorted(scores, key=lambda x: x[1], reverse=True)[:10]

def show_scores():
    fade_transition(screen)
    while True:
        screen.fill(BLACK)
        draw_ascii_globe(screen)
        scores = load_scores()
        panel_width, panel_height = 500, 500
        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(screen, GREY, panel_rect)

        title = MENU_TITLE_FONT.render("High Scores", True, WHITE)
        screen.blit(title, (panel_rect.centerx - title.get_width() // 2, panel_rect.top + 20))

        for i, (name, score) in enumerate(scores):
            line = GAME_FONT.render(f"{i+1}. {name} - {score}", True, WHITE)
            screen.blit(line, (panel_rect.left + 50, panel_rect.top + 80 + i * 40))

        back_txt = GAME_FONT.render("Press ESC to return", True, WHITE)
        screen.blit(back_txt, (panel_rect.centerx - back_txt.get_width() // 2, panel_rect.bottom - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                fade_transition(screen)
                return

        clock.tick(FPS)

# --- Name Entry ---
def name_entry_screen(score):
    name = ""
    BUTTON_WIDTH, BUTTON_HEIGHT = 300, 60
    while True:
        screen.fill(BLACK)
        draw_ascii_globe(screen)
        panel_width, panel_height = 500, 300
        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(screen, GREY, panel_rect)

        go_text = MENU_TITLE_FONT.render("GAME OVER", True, WHITE)
        screen.blit(go_text, (panel_rect.centerx - go_text.get_width() // 2, panel_rect.top + 20))
        score_text = GAME_FONT.render(f"Your Score: {score}", True, WHITE)
        screen.blit(score_text, (panel_rect.centerx - score_text.get_width() // 2, panel_rect.top + 80))
        input_text = GAME_FONT.render(f"Name (4 chars): {name}", True, WHITE)
        screen.blit(input_text, (panel_rect.left + 50, panel_rect.top + 160))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    save_score(name.upper(), score)
                    fade_transition(screen)
                    return
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 4 and event.unicode.isalpha():
                    name += event.unicode.upper()

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
                for btn in buttons:
                    if btn.is_clicked(event):
                        if btn.text == "Start Game":
                            run_game()
                        elif btn.text == "View High Scores":
                            show_scores()
                        elif btn.text == "Quit Game":
                            pygame.quit()
                            sys.exit()

        clock.tick(FPS)

if __name__ == "__main__":
    main()