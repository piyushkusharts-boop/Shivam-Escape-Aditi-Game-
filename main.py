import pygame
import random
import sys

pygame.init()

# Android full screen support
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH = screen.get_width()
HEIGHT = screen.get_height()

pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# Fixed fonts for Android (Using default font instead of Arial system font)
font = pygame.font.Font(None, 45)
bigfont = pygame.font.Font(None, 65)

playerX = 120
playerY = HEIGHT // 2

vel = 0
gravity = 0.55
jump = -10

score = 0
game_over = False

# FIXED PIPES CONFIG
PIPE_WIDTH = 130
PIPE_GAP = 500
PIPE_SPEED = 8
PIPE_DISTANCE = 1000

pipes = []

for i in range(3):
    pipes.append({
        "x": WIDTH + (i * PIPE_DISTANCE),
        "gapY": random.randint(250, max(300, HEIGHT - 1150))
    })

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Phone tap / Touch handle
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            if not game_over:
                vel = jump
            else:
                # Game over hone par screen touch karne se game restart ho jayega
                playerY = HEIGHT // 2
                vel = 0
                score = 0
                game_over = False
                pipes = []
                for i in range(3):
                    pipes.append({
                        "x": WIDTH + (i * PIPE_DISTANCE),
                        "gapY": random.randint(250, max(300, HEIGHT - 1150))
                    })

    if not game_over:
        vel += gravity
        playerY += vel

    screen.fill((10, 10, 30))

    # Base platform
    pygame.draw.rect(screen, (30, 180, 50), (0, HEIGHT - 80, WIDTH, 80))

    # Player Rect
    player = pygame.Rect(playerX, int(playerY), 140, 45)
    pygame.draw.rect(screen, (0, 150, 255), player, border_radius=25)

    t = bigfont.render("SHIVAM", True, (255, 255, 255))
    screen.blit(t, (playerX + 5, playerY + 3))

    for p in pipes:
        if not game_over:
            p["x"] -= PIPE_SPEED

        top = pygame.Rect(p["x"], 0, PIPE_WIDTH, p["gapY"])
        bottom = pygame.Rect(p["x"], p["gapY"] + PIPE_GAP, PIPE_WIDTH, HEIGHT)

        pygame.draw.rect(screen, (255, 0, 0), top, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), bottom, border_radius=10)

        txt = font.render("ADITI MUNJAL", True, (255, 255, 255))
        screen.blit(txt, (p["x"] - 15, p["gapY"] - 40))
        screen.blit(txt, (p["x"] - 15, p["gapY"] + PIPE_GAP + 20))

        if player.colliderect(top) or player.colliderect(bottom):
            game_over = True

        if p["x"] < -200:
            maxX = max(pipe["x"] for pipe in pipes)
            p["x"] = maxX + PIPE_DISTANCE
            p["gapY"] = random.randint(250, max(300, HEIGHT - 1150))
            score += 1

    s = font.render("Score: " + str(score), True, (255, 255, 0))
    screen.blit(s, (20, 20))

    if playerY < 0 or playerY > HEIGHT - 80:
        game_over = True

    if game_over:
        over = bigfont.render("GAME OVER", True, (255, 0, 0))
        restart_txt = font.render("Tap to Restart", True, (255, 255, 255))
        screen.blit(over, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
        screen.blit(restart_txt, (WIDTH // 2 - 100, HEIGHT // 2 + 20))

    pygame.display.update()
    clock.tick(60)
