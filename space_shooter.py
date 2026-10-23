"""
PYGAME SPACE SHOOTER V1.0

Proyek Edukasi Gratis

Hanya untuk penggunaan edukasi pribadi dan non-komersial.
Disediakan "SEBAGAIMANA ADANYA" (AS IS), tanpa jaminan.
Lihat README untuk ketentuan penggunaan dan perizinan.

© 2026 Ikayama Education (PT IKAYAMA MANUSA SOLUSI)

"""
import pygame
import sys
import random

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Space Shooter V1.0")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Consolas", 18)
font_medium = pygame.font.SysFont("Consolas", 26)
font_large = pygame.font.SysFont(None, 64)

# Player Setup
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT - 50)
player_speed = 300
player_size = 40

# Player Health Setup
MAX_PLAYER_HEALTH = 3
player_health = MAX_PLAYER_HEALTH

# Bullet Setup
class Bullet:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.speed = 500
        self.radius = 5

    def update(self, dt):
        self.pos.y -= self.speed * dt

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            (255, 255, 0),
            (int(self.pos.x), int(self.pos.y)),
            self.radius
        )


bullets = []

# Obstacle Difficulty Setup
BASE_OBSTACLE_SPEED = 150
SPEED_INCREASE_PER_LEVEL = 25
SCORE_PER_LEVEL = 10

obstacle_speed = BASE_OBSTACLE_SPEED
level = 1

# Obstacle Spawn Setup
BASE_OBSTACLE_SPAWN_DURATION = 2.0
SPAWN_DECREASE_PER_LEVEL = 0.2
MIN_OBSTACLE_SPAWN_DURATION = 0.6

obstacle_spawn_duration = BASE_OBSTACLE_SPAWN_DURATION
obstacle_spawn_time = 0.0


class Obstacle:
    def __init__(self, x, y, speed):
        self.pos = pygame.Vector2(x, y)
        self.speed = speed
        self.radius = 30

    def update(self, dt):
        self.pos.y += self.speed * dt

    def draw_obstacle(self, surface):
        pygame.draw.circle(
            surface,
            (0, 0, 255),
            (int(self.pos.x), int(self.pos.y)),
            self.radius
        )


obstacle = []

# Game State
score = 0
game_started = False
game_over = False

# Game Loop
running = True

while running:
    dt = clock.tick(60) / 1000.0

    # ---------------------------------------------------------
    # 1. EVENT HANDLING
    # ---------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Start game or shoot a bullet
            if event.key == pygame.K_SPACE:

                if not game_started:
                    game_started = True

                elif not game_over:
                    bullet = Bullet(player_pos.x, HEIGHT - 55)
                    bullets.append(bullet)

            # Restart after Game Over
            elif event.key == pygame.K_r and game_over:
                player_pos = pygame.Vector2(
                    WIDTH // 2, HEIGHT - 50
                )
                player_health = MAX_PLAYER_HEALTH

                bullets.clear()
                obstacle.clear()

                score = 0
                level = 1
                obstacle_speed = BASE_OBSTACLE_SPEED

                obstacle_spawn_duration = (
                    BASE_OBSTACLE_SPAWN_DURATION
                )
                obstacle_spawn_time = 0.0

                game_over = False

    # ---------------------------------------------------------
    # 2. UPDATE GAME OBJECTS
    # Only update while the game is active
    # ---------------------------------------------------------
    if game_started and not game_over:

        # Player movement
        keys = pygame.key.get_pressed()
        move_dir = pygame.Vector2(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_dir.x -= 1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_dir.x += 1

        velocity = move_dir * player_speed
        player_pos += velocity * dt

        # Keep player inside the screen
        player_pos.x = max(
            player_size // 2,
            min(WIDTH - player_size // 2, player_pos.x)
        )

        # Spawn obstacles
        obstacle_spawn_time += dt

        if obstacle_spawn_time >= obstacle_spawn_duration:
            obs = Obstacle(
                random.randint(150, 650),
                -55,
                obstacle_speed
            )
            obstacle.append(obs)
            obstacle_spawn_time = 0.0

        # Update bullets
        for bullet in bullets[:]:
            bullet.update(dt)

            if bullet.pos.y < 0:
                bullets.remove(bullet)

        # Update obstacles and check collisions
        for game_obstacle in obstacle[:]:
            game_obstacle.update(dt)

            # Remove obstacles that leave the screen
            if game_obstacle.pos.y > HEIGHT + game_obstacle.radius:
                obstacle.remove(game_obstacle)
                continue

            # Check bullet collisions
            for bullet in bullets[:]:
                distance = game_obstacle.pos.distance_to(
                    bullet.pos
                )

                if distance <= (
                    game_obstacle.radius + bullet.radius
                ):
                    obstacle.remove(game_obstacle)
                    bullets.remove(bullet)

                    # Increase score
                    score += 1

                    # Calculate level
                    new_level = score // SCORE_PER_LEVEL + 1

                    if new_level > level:
                        level = new_level

                        # Increase obstacle speed
                        obstacle_speed = (
                            BASE_OBSTACLE_SPEED
                            + (level - 1)
                            * SPEED_INCREASE_PER_LEVEL
                        )

                        # Reduce spawn interval
                        obstacle_spawn_duration = max(
                            MIN_OBSTACLE_SPAWN_DURATION,
                            BASE_OBSTACLE_SPAWN_DURATION
                            - (level - 1)
                            * SPAWN_DECREASE_PER_LEVEL
                        )

                        # Update existing obstacles
                        for existing_obstacle in obstacle:
                            existing_obstacle.speed = (
                                obstacle_speed
                            )

                    break

            # Skip obstacles destroyed by bullets
            if game_obstacle not in obstacle:
                continue

            # Check player collision
            player_distance = player_pos.distance_to(
                game_obstacle.pos
            )

            if player_distance <= (
                player_size / 2 + game_obstacle.radius
            ):
                obstacle.remove(game_obstacle)
                player_health -= 1

                if player_health <= 0:
                    game_over = True
                    break

    # ---------------------------------------------------------
    # 3. RENDERING
    # ---------------------------------------------------------
    screen.fill((30, 30, 30))

    # Title Screen
    if not game_started:

        title_surface = font_large.render(
            "Pygame Space Shooter",
            True,
            (0, 200, 255)
        )
        title_rect = title_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 70)
        )
        screen.blit(title_surface, title_rect)

        instruction_surface = font_medium.render(
            "Press SPACE to start",
            True,
            (255, 255, 255)
        )
        instruction_rect = instruction_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 10)
        )
        screen.blit(instruction_surface, instruction_rect)

        controls_surface = font.render(
            "Move: LEFT / RIGHT or A / D",
            True,
            (180, 180, 180)
        )
        controls_rect = controls_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 55)
        )
        screen.blit(controls_surface, controls_rect)

        shooting_surface = font.render(
            "Shoot: SPACE",
            True,
            (180, 180, 180)
        )
        shooting_rect = shooting_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 85)
        )
        screen.blit(shooting_surface, shooting_rect)

    # Active Game Screen
    elif not game_over:

        # Draw player
        player_rect = pygame.Rect(
            player_pos.x - player_size // 2,
            player_pos.y - player_size // 2,
            player_size,
            player_size
        )
        pygame.draw.rect(
            screen, (0, 200, 255), player_rect
        )

        # Draw bullets
        for bullet in bullets:
            bullet.draw(screen)

        # Draw obstacles
        for game_obstacle in obstacle:
            game_obstacle.draw_obstacle(screen)

        # Score
        score_surface = font.render(
            f"SCORE: {score}",
            True,
            (255, 255, 255)
        )
        screen.blit(score_surface, (15, 15))

        # Level
        level_surface = font.render(
            f"LEVEL: {level}",
            True,
            (255, 255, 255)
        )
        screen.blit(level_surface, (15, 40))

        # Health
        health_surface = font.render(
            f"HEALTH: {player_health}/{MAX_PLAYER_HEALTH}",
            True,
            (255, 100, 100)
        )
        screen.blit(health_surface, (15, 65))

    # Game Over Screen
    else:
        game_over_surface = font_large.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )
        game_over_rect = game_over_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 50)
        )
        screen.blit(game_over_surface, game_over_rect)

        final_score_surface = font.render(
            f"FINAL SCORE: {score}",
            True,
            (255, 255, 255)
        )
        final_score_rect = final_score_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 5)
        )
        screen.blit(final_score_surface, final_score_rect)

        restart_surface = font_medium.render(
            "Press R to restart",
            True,
            (0, 200, 255)
        )
        restart_rect = restart_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 50)
        )
        screen.blit(restart_surface, restart_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
