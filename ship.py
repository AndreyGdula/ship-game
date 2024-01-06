import pygame, random
from tkinter import messagebox


# Asteroid preset
class Asteroid:
    def __init__(self):
        self.ast_width = 50
        self.ast_height = 50
        self.asteroid = pygame.image.load("imgs/asteroid.png")
        self.asteroid = pygame.transform.scale(self.asteroid, (self.ast_width, self.ast_height))

        self.ast_rect = self.asteroid.get_rect()
        self.ast_mask = pygame.mask.from_surface(self.asteroid)
        self.ast_rect.x = random.randint(1, screen_width - 20)
        self.ast_rect.y = random.choice([20, screen_height - 35])

        self.ast_speed_x = random.randint(-4, 4)
        self.ast_speed_y = random.randint(-4, 4)
        self.ast_interval = 3000
        self.ast_improve = 1

    def draw(self):
        root.blit(self.asteroid, self.ast_rect)

    def update(self):
        self.ast_rect.x += self.ast_speed_x
        self.ast_rect.y += self.ast_speed_y
  
        if self.ast_rect.left < 0 or self.ast_rect.right > screen_width:
            self.ast_speed_x *= -1

        if self.ast_rect.top < 0 or self.ast_rect.bottom > screen_height:
            self.ast_speed_y *= -1
    
    def collision(self):
        ast_mask = pygame.mask.from_surface(self.asteroid)

        ast_x = int(self.ast_rect.x - rkt_rect.x)
        ast_y = int(self.ast_rect.y - rkt_rect.y)

        collision = rkt_mask.overlap(ast_mask, (ast_x, ast_y))
        if collision:
            return True


pygame.init()

# Screen config
screen_width = pygame.display.Info().current_w - 100
screen_height = pygame.display.Info().current_h - 100

root = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("SHIP GAME")

# Ticks
clock = pygame.time.Clock()
dt = 0

    # Files config
# Background preset
background = pygame.image.load("imgs/bg_space.png")
background = pygame.transform.scale(background, (1920, 1280))

bg_rect = background.get_rect()
bg_rect.center = (screen_width / 2, screen_height / 2)
bg_speed = 100

# Ship preset
rkt_width = 30
rkt_height = 60

rocket = pygame.image.load("imgs/rocket.png")
rocket = pygame.transform.scale(rocket, (rkt_width, rkt_height))

rkt_rect = rocket.get_rect()
rkt_mask = pygame.mask.from_surface(rocket)
rkt_rect.x = screen_width / 2
rkt_rect.y = screen_height / 2
rkt_speed = 300

# Asteroid preset
asteroid_1 = Asteroid()
asteroid_2 = Asteroid()
asteroid_3 = Asteroid()
asteroid_4 = Asteroid()
update_time = 5000

# Font preset
font = pygame.font.SysFont('Arial', 50)

# Loop
run = True
while run:
    screen_width, screen_height = pygame.display.get_surface().get_size()
    current_time = pygame.time.get_ticks()

    root.fill('#333637')
    root.blit(background, bg_rect)
    root.blit(rocket, rkt_rect)

    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    text_time = font.render(f"{current_time}", True, (255, 255, 255))
    time_rect = text_time.get_rect(topright = (screen_width - 30, 15))
    root.blit(text_time, time_rect)

    # Key mapping
    key = pygame.key.get_pressed()
    if key[pygame.K_w] or key[pygame.K_UP]:
        bg_rect.y += bg_speed * dt
        rkt_rect.y -= rkt_speed * dt
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        bg_rect.x += bg_speed * dt
        rkt_rect.x -= rkt_speed * dt
    if key[pygame.K_s] or key[pygame.K_DOWN]:
        bg_rect.y -= bg_speed * dt
        rkt_rect.y += rkt_speed * dt
    if key[pygame.K_d] or key[pygame.K_RIGHT]:
        bg_rect.x -= bg_speed * dt
        rkt_rect.x += rkt_speed * dt
    if key[pygame.K_ESCAPE]:
        run = False

    # Ship Collision
    if rkt_rect.x < 0:
        rkt_rect.x = 0
        bg_speed = 0
    elif rkt_rect.x + rkt_width >  screen_width:
        rkt_rect.x = screen_width - rkt_width
        bg_speed = 0
    elif rkt_rect.y < 0:
        rkt_rect.y = 0
        bg_speed = 0
    elif rkt_rect.y + rkt_height > screen_height:
        rkt_rect.y = screen_height - rkt_height
        bg_speed = 0
    else:
        bg_speed = 100

    # Ship-Asteroid Collision
    if asteroid_1.collision() or asteroid_2.collision() or asteroid_3.collision() or asteroid_4.collision():
        messagebox.showwarning("DERROTA", "você bateu no asteroid!")
        rkt_rect.center = screen_width / 2, screen_height / 2

    # Asteroid Moviment
    asteroid_1.draw()
    asteroid_1.update()

    if current_time > update_time:
        asteroid_2.draw()
        asteroid_2.update()

    if current_time > update_time * 2:
        asteroid_3.draw()
        asteroid_3.update()

    if current_time > update_time * 3:
        asteroid_4.draw()
        asteroid_4.update()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()