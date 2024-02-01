import pygame, random, pygame_menu
from tkinter import messagebox

pygame.init()
pygame.mixer.init()

# Screen Config
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

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
        self.ast_rect.y = random.choice([20, screen_height - 50])

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
        self.rect.x = (screen_width * 2 / 3) - 70
        self.rect.y = 10
        self.color_fg = 'blue'  # Define a cor da barra de progresso (cor do progresso)
        self.progress = progress  # Define o progresso atual da barra de progresso (0-100%)

    def update_progress(self, progress):
        self.progress = progress  # Atualiza o progresso
        self.image.fill('#022431')  # Preenche a imagem com a cor de fundo
        pygame.draw.rect(self.image, self.color_fg, (0, 0, self.rect.width * (progress / 100), self.rect.height))


# StageUp Sprite
class BlueRing(pygame.sprite.Sprite):
    def __init__(self, rkt_rect):
        pygame.sprite.Sprite.__init__(self)
        self.ring_sprite = []
        for i in range(1, 20):
            self.ring_sprite.append(pygame.image.load(f'imgs/blue-ring/Blue Ring Explosion{i}.png'))

        self.ring_current = 0
        self.image = self.ring_sprite[self.ring_current]
        self.rect = self.image.get_rect()
        self.rect.center = rkt_rect.center

    def update(self, anime_ring, rkt_rect):
        if anime_ring:
            self.ring_current += 0.5
            if self.ring_current >= len(self.ring_sprite):
                self.ring_current = 0
                anime_ring = False
            self.image = self.ring_sprite[int(self.ring_current)]
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.rect.center = rkt_rect.center
            self.rect.x += 70
            self.rect.y += 70


# Nitro Sprite
class Nitro(pygame.sprite.Sprite):
    def __init__(self, rkt_rect):
        pygame.sprite.Sprite.__init__(self)
        self.nitro_width = 15
        self.nitro_height = 25
        self.padding_right = 10
        self.padding_bottom = 10
        self.nitro_current = 0
        
        self.nitro_sprite = []
        for i in range(1, 5):
            self.nitro_sprite.append(pygame.image.load(f'imgs/blue-fire/bluefire{i}.png'))

        self.image = self.nitro_sprite[int(self.nitro_current)]
        self.image = pygame.transform.scale(self.image, (self.nitro_width, self.nitro_height))
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()

        self.rect.center = rkt_rect.center
        self.rect.y += 35

    def draw(self):
        root.blit(self.image, self.rect)

    def update(self, rkt_rect):
        self.nitro_current += 0.25
        if self.nitro_current >= len(self.nitro_sprite):
            self.nitro_current = 0
        self.image = self.nitro_sprite[int(self.nitro_current)]
        self.image = pygame.transform.scale(self.image, (self.nitro_width, self.nitro_height))
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()

        self.rect.center = rkt_rect.center
        self.rect.y += 35


# Menu
def show_menu():
    my_theme = pygame_menu.themes.Theme(background_color=bg_color, title_font=title_font, title_font_color=text_color,widget_font=widget_font, widget_font_color=text_color)

    menu = pygame_menu.Menu('SHIP GAME', screen_width, screen_height, theme=my_theme)
    menu.add.button('PLAY', menu_play)
    menu.add.button('EXIT', pygame_menu.events.EXIT)
    menu.mainloop(root)

def show_gameover():
    my_theme = pygame_menu.themes.Theme(background_color=bg_color, title_font=title_font, title_font_color=text_color,widget_font=widget_font, widget_font_color=text_color)

    gameover = pygame_menu.Menu('GAME OVER', screen_width, screen_height, theme=my_theme)
    gameover.add.button('RESTART', menu_play)
    gameover.add.button('EXIT', pygame_menu.events.EXIT)
    gameover.mainloop(root)
    
# Loop
def menu_play():
    global clock, dt, background, bg_rect, bg_speed, hud, hud_rect, hud2, hud2_rect, improve_clock, rkt_rect, rkt_mask, tool_cont, tool_cont_rect, all_sprites, font, asteroid_1, asteroid_2, asteroid_3, asteroid_4, asteroid_5, rkt_width, rkt_height, powerup_effect, ring_group, hit_effect, bubble_group, tool, score_effect, progress_bar, nitro, stage1, stage2, stage3, rkt_speed, update_time, score, start_time, progress_cont, progress_clock, anime_bubble, anime_ring, start_time, screen_width, screen_height

    # Ticks
    clock = pygame.time.Clock()
    dt = 0

    # Screen Config
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h

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
    asteroid_5 = Asteroid()

    update_time = 5000
    improve_clock = 10000


    # Tool preset
    tool = Tool()
    score = 0

    # Font preset
    font = pygame.font.SysFont('Arial', 50)

    # General preset
    start_time = pygame.time.get_ticks()
    run_time = pygame.time.get_ticks()

    # ProgressBar preset
    progress_bar = ProgressBar(100)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(progress_bar)
    progress_cont = 100
    progress_clock = pygame.time.get_ticks()

    # Blue Ring
    blue_ring = BlueRing(rkt_rect)
    ring_group = pygame.sprite.Group()
    ring_group.add(blue_ring)
    anime_ring = False

    # Nitro
    nitro = Nitro(rkt_rect)
    stage1 = True
    stage2 = False
    stage3 = False

    game_pause = False
    pause_time = 0
    pause_rect = pygame.Rect(0, 0, screen_width, screen_height)

    run = True
    while run:
        screen_width, screen_height = pygame.display.get_surface().get_size()
        current_time = pygame.time.get_ticks()
        clock_start = pygame.time.get_ticks() - int(run_time) - int(pause_time)
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_pause = not game_pause

        if not game_pause:
            # Text
            time_text = font.render(f"{clock_start / 1000:.2f}s", True, (0, 0, 255))
            time_rect = time_text.get_rect(topright = (screen_width - 25, 35))
            root.blit(time_text, time_rect)

            score_text = font.render(f'{score}', True, (0, 0, 255))
            score_rect = score_text.get_rect(topleft = (95, 25))
            root.blit(score_text, score_rect)

            speed_text_1 = font.render(f'1 => x: {asteroid_1.ast_speed_x} y: {asteroid_1.ast_speed_y}', True, (255, 255, 255))
            speed_rect_1 = speed_text_1.get_rect(topleft = (15, 120))

            speed_text_2 = font.render(f'2 => x: {asteroid_2.ast_speed_x} y: {asteroid_2.ast_speed_y}', True, (255, 255, 255))
            speed_rect_2 = speed_text_2.get_rect(topleft = (15, 170))

            speed_text_3 = font.render(f'3 => x: {asteroid_3.ast_speed_x} y: {asteroid_3.ast_speed_y}', True, (255, 255, 255))
            speed_rect_3 = speed_text_3.get_rect(topleft = (15, 220))

            speed_text_4 = font.render(f'4 => x: {asteroid_4.ast_speed_x} y: {asteroid_4.ast_speed_y}', True, (255, 255, 255))
            speed_rect_4 = speed_text_4.get_rect(topleft = (15, 270))

            if current_time > 125 * 1000:
                speed_text_5 = font.render(f'5 => x: {asteroid_5.ast_speed_x} y: {asteroid_5.ast_speed_y}', True, (255, 255, 255))
                speed_rect_5 = speed_text_5.get_rect(topleft = (15, 320))

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

            if key[pygame.K_TAB]:
                root.blit(speed_text_1, speed_rect_1)
                root.blit(speed_text_2, speed_rect_2)
                root.blit(speed_text_3, speed_rect_3)
                root.blit(speed_text_4, speed_rect_4)
                if clock_start > 125 * 1000:
                    root.blit(speed_text_5, speed_rect_5)

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
            if 65 * 1000 > clock_start > 60 * 1000:
                powerup_effect.play()
                anime_ring = True
                ring_group.draw(root)
                ring_group.update(anime_ring, rkt_rect)
            if clock_start > 60 * 1000:
                stage1 = False
                stage2 = True
                rocket = pygame.image.load("imgs/rocket-blue.png")
                rocket = pygame.transform.scale(rocket, (rkt_width, rkt_height))
                rkt_speed = 400
            if 125 * 1000 > clock_start > 120 * 1000:
                powerup_effect.play()
                anime_ring = True
                ring_group.draw(root)
                ring_group.update(anime_ring, rkt_rect)
            if clock_start > 120 * 1000:
                stage2 = False
                stage3 = True
                rocket = pygame.image.load("imgs/rocket-blue.png")
                rocket = pygame.transform.scale(rocket, (rkt_width, rkt_height))
                rkt_speed = 600

            # Ship-Asteroid Collision
            if asteroid_1.collision() or asteroid_2.collision() or asteroid_3.collision() or asteroid_4.collision() or  clock_start > 125 * 1000 and asteroid_5.collision():
                hit_effect.play()
                show_gameover()

            # Asteroid Moviment
            asteroid_1.draw()
            asteroid_1.update(improve_time)

            asteroid_2.draw()
            asteroid_2.update(improve_time)

            asteroid_3.draw()
            asteroid_3.update(improve_time)

            asteroid_4.draw()
            asteroid_4.update(improve_time)

            if clock_start > 120 * 1000:
                asteroid_5.draw()
                asteroid_5.update(improve_time)

            if improve_time > improve_clock:
                start_time = pygame.time.get_ticks()

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

            # ProgressBar
            if progress_cont == 0:
                anime_bubble = True
                bubble_group.draw(root)
                bubble_group.update(anime_bubble, rkt_rect)
                messagebox.showwarning("DERROTA", 'Sua nave quebrou!')
                rkt_rect.center = screen_width / 2, screen_height / 2
                show_gameover()

            if current_time - progress_clock > 500:
                progress_cont -= 1
                progress_bar.update_progress(progress_cont)
                progress_clock = pygame.time.get_ticks()

            # Nitro
            if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
                if stage1:
                    rkt_speed = 400
                elif stage2:
                    rkt_speed = 500
                elif stage3:
                    rkt_speed = 700
                progress_cont -= 0.5
                nitro.update(rkt_rect)
                nitro.draw()

            elif stage1:
                rkt_speed = 300
            elif stage2:
                rkt_speed = 400
            elif stage3:
                rkt_speed = 600

            pygame.display.flip()
            dt = clock.tick(60) / 1000

        elif game_pause == True:
            pause_time = pygame.time.get_ticks() - int(start_time)
            pygame.draw.rect(root, bg_color, pause_rect)

            pause_title = title_font.render("PAUSE", True, text_color)
            pause_title_rect = pause_title.get_rect()
            pause_title_rect.center = screen_width / 2, screen_height / 2

            obs_exit = widget_font.render("to exit press ALT+F4", True, text_color)
            obs_exit_rect = obs_exit.get_rect()
            obs_exit_rect.center = screen_width / 2, screen_height - pause_title_rect.y + 10

            root.blit(pause_title, pause_title_rect)
            root.blit(obs_exit, obs_exit_rect)

            pygame.display.flip()

    pygame.quit()

# Menu preset
bg_color = (10, 7, 26)
text_color = (255, 255, 255)
title_path = "font/blackops.ttf"
font_path = "font/workbench.ttf"

title_font = pygame.font.Font(title_path, 70)
widget_font = pygame.font.Font(font_path, 40)

root = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("SHIP GAME")

run = True
while run:
    show_menu()
    menu_play()

pygame.quit()