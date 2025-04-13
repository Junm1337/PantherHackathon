import pygame, random, sys

# Setup
pygame.init()

#Music
pygame.mixer.init()
#load music
pygame.mixer.music.load("jun.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Sound object
explosion_sound= pygame.mixer.Sound("explosion.mp3")
explosion_sound.set_volume(1.0)


# Player
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 60, 50, 50)
speed = 5

# Falling blocks
blocks = []
spawn_rate = 30
frame = 0
game_over = False
score = 0

def get_random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0, 255))


class Block:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Game loop
while True:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Player movement
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += speed

        if keys[pygame.K_UP] and player.top > 0:
            player.y-= speed
        if keys [pygame.K_DOWN] and player.bottom  < HEIGHT:
            player.y+= speed
        # Spawn new blocks
        if frame % spawn_rate == 0:
            w = random.randint(20, 50)
            h = random.randint (20,50)
            blocks.append(Block(random.randint(0, WIDTH - w), -50, w, h, get_random_color()))
        
            #blocks.append))((color
        if frame % 100 == 0:     
            score = score + 1

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Move and draw blocks
        for block in blocks:
            block.rect.y += 5
            block.draw(screen)
            
            # Collision
            if player.colliderect(block):
                game_over = True
                explosion_sound.play()

        # Draw player
        pygame.draw.rect(screen, BLUE, player)

        # Clean up blocks off screen
        blocks = [b for b in blocks if b.rect.y < HEIGHT]
        frame += 1

        # Increase difficulty
        if frame % 300 == 0 and spawn_rate > 10:
            spawn_rate -= 2
    else:
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 20))
        final_score = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2 + 80))
        retry = font.render("Press R to Retry", True, WHITE)
        screen.blit(retry, (WIDTH//2 - retry.get_width()//2, HEIGHT//2 + 30))
        if keys[pygame.K_r]:
            score = 0
            # Reset game
            player.x = WIDTH // 2 - 25
            blocks = []
            frame = 0
            spawn_rate = 30
            game_over = False
        
    pygame.display.flip()
    clock.tick(60)
