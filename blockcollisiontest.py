import pygame

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Player (Cube) Rect and Physics
player_rect = pygame.Rect(100, 400, 40, 40)
player_vel_y = 0
gravity = 0.8
jump_strength = -14
on_ground = False

# Example Blocks List
blocks = [
    pygame.Rect(300, 500, 200, 40),
    pygame.Rect(550, 420, 100, 40),
]

running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_vel_y = jump_strength
                on_ground = False

    # 1. Apply Gravity
    player_vel_y += gravity
    player_rect.y += player_vel_y

    # 2. Check Y-Axis Collisions (Land on top or hit ceiling)
    on_ground = False
    for block in blocks:
        if player_rect.colliderect(block):
            # Falling down onto the top of a block
            if player_vel_y > 0 and player_rect.bottom >= block.top and player_rect.top < block.top:
                player_rect.bottom = block.top
                player_vel_y = 0
                on_ground = True
            # Hitting the bottom of a block
            elif player_vel_y < 0 and player_rect.top <= block.bottom:
                player_rect.top = block.bottom
                player_vel_y = 0

    # Optional: Floor collision (ground level at y = 500)
    if player_rect.bottom >= 500:
        player_rect.bottom = 500
        player_vel_y = 0
        on_ground = True

    # 3. Handle X-Axis / Side Collisions (Death / Obstacle check)
    # Move player forward or move blocks backward (auto-scroller)
    player_rect.x += 4

    for block in blocks:
        if player_rect.colliderect(block):
            # If hitting the side of a block, trigger Game Over
            if player_rect.right > block.left and player_rect.left < block.left:
                print("Game Over: Hit side of block")
                # Reset or close game

    # Drawing
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 255, 255), player_rect)
    for block in blocks:
        pygame.draw.rect(screen, (255, 255, 255), block)

    pygame.display.flip()

pygame.quit()
