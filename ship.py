import pygame, random
from tkinter import messagebox


# Asteroid config
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

    def update(self, improve_time):
        self.ast_rect.x += self.ast_speed_x
        self.ast_rect.y += self.ast_speed_y
  
        if self.ast_rect.left < 0 or self.ast_rect.right > screen_width:
            self.ast_speed_x *= -1

        if self.ast_rect.top < 0 or self.ast_rect.bottom > screen_height:
            self.ast_speed_y *= -1

        if 0 < self.ast_speed_x < 15 or -15 < self.ast_speed_x < 0:
            if improve_time > improve_clock:
                if self.ast_speed_x > 0:
                    self.ast_speed_x += 1
                else:
                    self.ast_speed_x -= 1
        if 0 < self.ast_speed_y < 15 or -15 < self.ast_speed_y < 0:
            if improve_time > improve_clock:
                if self.ast_speed_y > 0:
                    self.ast_speed_y += 1
                else:
                    self.ast_speed_y -= 1

    def collision(self):
        ast_mask = pygame.mask.from_surface(self.asteroid)

        ast_x = int(self.ast_rect.x - rkt_rect.x)
        ast_y = int(self.ast_rect.y - rkt_rect.y)

        collision = rkt_mask.overlap(ast_mask, (ast_x, ast_y))
        if collision:
            return True


# Tool config
class Tool:
    def __init__(self):
        self.tool_width = 512 / 10
        self.tool_height = 512 / 10

        self.tool_img = pygame.image.load("imgs/tool.png")
        self.tool_img = pygame.transform.scale(self.tool_img, (self.tool_width, self.tool_height))
        
        self.tool_rect = self.tool_img.get_rect()
        self.tool_rect.x = random.randint(30, screen_width - 30)
        self.tool_rect.y = random.randint(30, screen_height - 50)

    def draw(self):
        root.blit(self.tool_img, self.tool_rect)


    def collision(self, hud_rect, hud2_rect):
        tool_mask = pygame.mask.from_surface(self.tool_img)

        tool_x = int(self.tool_rect.x - rkt_rect.x)
        tool_y = int(self.tool_rect.y - rkt_rect.y)

        collision = rkt_mask.overlap(tool_mask, (tool_x, tool_y))
        if collision:
            self.tool_rect.x = random.randint(30, screen_width - 30)
            self.tool_rect.y = random.randint(30, screen_height - 50)
            return True
        
        if self.tool_rect.colliderect(hud_rect) or self.tool_rect.colliderect(hud2_rect):
            self.tool_rect.x = random.randint(30, screen_width - 30)
            self.tool_rect.y = random.randint(30, screen_height - 50)


# ProgressBar config
class ProgressBar(pygame.sprite.Sprite):
    def __init__(self, progress):
        pygame.sprite.Sprite.__init__(self)
        self.progress_width = 325
        self.progress_height = 35
        self.image = pygame.Surface((self.progress_width, self.progress_height))
        self.image.fill('#022431')  # Define a cor de fundo da barra de progresso
        self.rect = self.image.get_rect()
        self.rect.x = screen_width * 2 / 3
        self.rect.y = 10
        self.color_fg = 'blue'  # Define a cor da barra de progresso (cor do progresso)
        self.progress = progress  # Define o progresso atual da barra de progresso (0-100%)

    def update_progress(self, progress):
        self.progress = progress  # Atualiza o progresso
        self.image.fill('#022431')  # Preenche a imagem com a cor de fundo
        pygame.draw.rect(self.image, self.color_fg, (0, 0, self.rect.width * (progress / 100), self.rect.height))
        

pygame.init()
pygame.mixer.init()

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
background = pygame.transform.scale(background, (screen_width * 2, screen_height * 2))

bg_rect = background.get_rect()
bg_rect.center = (screen_width / 2, screen_height / 2)
bg_speed = 100

# Hud
hud = pygame.image.load("imgs/hud_1.png")
hud = pygame.transform.scale(hud, (270, 120))

hud_rect = hud.get_rect()
hud_rect.x = 0
hud_rect.y = 0

hud2 = pygame.image.load("imgs/hud_2.png")
hud2 = pygame.transform.scale(hud2, (600, 140))

hud2_rect = hud2.get_rect()
hud2_rect.x = screen_width - hud2_rect.width
hud2_rect.y = 0

# Tool
tool_cont = pygame.image.load("imgs/tool.png")
tool_cont = pygame.transform.scale(tool_cont, (70, 70))

tool_cont_rect = tool_cont.get_rect()
tool_cont_rect.x = 15
tool_cont_rect.y = 15

# Sound
hit_effect = pygame.mixer.Sound("sound/hit-effect.wav")
powerup_effect = pygame.mixer.Sound("sound/power-up.wav")
score_effect = pygame.mixer.Sound("sound/score.wav")
space_music = pygame.mixer.Sound("sound/space-bass.ogg")

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
improve_clock = 10000
times_improved = 0

# Tool preset
tool = Tool()
score = 0

# Font preset
font = pygame.font.SysFont('Arial', 50)

# General preset
start_time = pygame.time.get_ticks()

# ProgressBar preset
progress_bar = ProgressBar(100)
all_sprites = pygame.sprite.Group()
all_sprites.add(progress_bar)
progress_cont = 100
progress_clock = pygame.time.get_ticks()
progress_max_clock = 0

# Loop
run = True
while run:
    screen_width, screen_height = pygame.display.get_surface().get_size()
    current_time = pygame.time.get_ticks()
    improve_time = int(current_time) - int(start_time)

    root.fill('#090619')
    root.blit(background, bg_rect)

    hud2_rect.x = screen_width - hud2_rect.width
    root.blit(hud, hud_rect)
    root.blit(hud2, hud2_rect)

    root.blit(tool_cont, tool_cont_rect)

    all_sprites.update()
    all_sprites.draw(root)

    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Text
    time_text = font.render(f"{current_time / 1000:.2f}s", True, (0, 0, 255))
    time_rect = time_text.get_rect(topright = (screen_width - 25, 35))
    root.blit(time_text, time_rect)

    score_text = font.render(f'{score}', True, (0, 0, 255))
    score_rect = score_text.get_rect(topleft = (95, 25))
    root.blit(score_text, score_rect)

    speed_text = font.render(f'Speed: {asteroid_1.ast_speed_x}', True, (255, 255, 255))
    speed_rect = speed_text.get_rect(center = (screen_width / 2, 35))
    root.blit(speed_text, speed_rect)

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

    # Ship config
    root.blit(rocket, rkt_rect)
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

        # Speed up
    if progress_max_clock > 60000:
        rocket = pygame.image.load("imgs/rocket-blue.png")
        rocket = pygame.transform.scale(rocket, (rkt_width, rkt_height))
        rkt_speed = 400
    if progress_max_clock > 120000:
        rkt_speed = 600

    # Ship-Asteroid Collision
    if asteroid_1.collision() or asteroid_2.collision() or asteroid_3.collision() or asteroid_4.collision():
        hit_effect.play()
        messagebox.showwarning("DERROTA", "você bateu no asteroid!")
        rkt_rect.center = screen_width / 2, screen_height / 2

    # Asteroid Moviment
    asteroid_1.draw()
    asteroid_1.update(improve_time)

    asteroid_2.draw()
    asteroid_2.update(improve_time)

    asteroid_3.draw()
    asteroid_3.update(improve_time)

    asteroid_4.draw()
    asteroid_4.update(improve_time)

    if improve_time > improve_clock:
        start_time = pygame.time.get_ticks()
        times_improved += 1

    # Tool
    tool.draw()
    if tool.collision(hud_rect, hud2_rect):
        score += 1
        score_effect.play()
        if progress_cont < 90:
            progress_cont += 10
            progress_bar.update_progress(progress_cont)
        else:
            progress_cont = 100
            progress_bar.update_progress(progress_cont)
            progress_max_clock = pygame.time.get_ticks()

    # ProgressBar
    if progress_cont == 0:
        messagebox.showwarning("DERROTA", 'Sua nave quebrou!')

    if current_time - progress_clock > 500:
        progress_cont -= 1
        progress_bar.update_progress(progress_cont)
        progress_clock = pygame.time.get_ticks()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()