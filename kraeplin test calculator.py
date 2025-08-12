import pygame
import random
import sys
import time

pygame.init()

# Setup display
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tes Koran Pengurangan")

# Fonts
font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GRAY = (200, 200, 200)

# Random question number
def generate_question():
    a = random.randint(0, 9)
    b = random.randint(0, 9)
    result = abs(a - b)
    question = f"{a} - {b} = ?"
    return question, result

# Calculator
def draw_buttons():
    keys = [str(i) for i in range(1, 10)]
    buttons = []

    button_width = 80
    button_height = 60
    spacing_x = 20
    spacing_y = 20
    total_row_width = 3 * button_width + 2 * spacing_x  # total width of 3 buttons + spaces

    margin_left = (WIDTH - total_row_width) // 2
    top_start_y = 300

    # Buttons 1-9 in grid
    for i, key in enumerate(keys):
        col = i % 3
        row = i // 3
        x = margin_left + col * (button_width + spacing_x)
        y = top_start_y + row * (button_height + spacing_y)
        rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(screen, RED, rect)
        pygame.draw.rect(screen, BLACK, rect, 3)
        text = font.render(key, True, WHITE)
        screen.blit(text, (x + 30, y + 10))
        buttons.append((rect, int(key)))

    # 0 in center bottom 
    col = 1  # middle column
    row = 3
    x = margin_left + col * (button_width + spacing_x)
    y = top_start_y + row * (button_height + spacing_y)
    rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, BLACK, rect, 3)
    text = font.render("0", True, WHITE)
    screen.blit(text, (x + 30, y + 10))
    buttons.append((rect, 0))

    return buttons

# Timer input screen
def get_timer_input():
    input_minutes = ""
    active = True
    while active:
        screen.fill(WHITE)
        
        prompt = small_font.render("Set timer in minutes (press Enter):", True, BLACK)
        user_input = font.render(input_minutes, True, BLACK)

        prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        input_rect = user_input.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))

        screen.blit(prompt, prompt_rect)
        screen.blit(user_input, input_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_minutes.isdigit() and int(input_minutes) > 0:
                        return int(input_minutes) * 60
                elif event.key == pygame.K_BACKSPACE:
                    input_minutes = input_minutes[:-1]
                elif event.unicode.isdigit():
                    input_minutes += event.unicode

# Main game loop
def main():
    total_answered = 0
    question, correct_answer = generate_question()
    timer_duration = get_timer_input()
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, int(timer_duration - elapsed_time))

        if remaining_time <= 0:
            screen.fill(WHITE)
            done_text = font.render("Waktu Habis!", True, BLACK)
            score_text = font.render(f"Skor: {total_answered}", True, BLACK)

            done_rect = done_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

            screen.blit(done_text, done_rect)
            screen.blit(score_text, score_rect)

            pygame.display.flip()
            pygame.time.wait(4000)
            pygame.quit()
            sys.exit()

        screen.fill(WHITE)
        question_text = font.render(question, True, BLACK)
        timer_text = small_font.render(f"Sisa waktu: {remaining_time}s", True, RED)

        screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 100))
        screen.blit(timer_text, (10, 40))

        buttons = draw_buttons()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, value in buttons:
                    if rect.collidepoint(pos):
                        if value == correct_answer:
                            total_answered += 1
                            question, correct_answer = generate_question()

# Run the game
main()