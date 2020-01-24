import pygame
import random
import pygame.sprite as sprite

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_a,
    K_w,
    K_s,
    K_d,
    K_SPACE

)
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.init()



pygame.display.set_caption("Lost Wizard")
screen = pygame.display.set_mode([800, 600])
white = (255, 255, 255)
clock = pygame.time.Clock()
background = pygame.image.load('img/placeholder-bg.png')
background = pygame.transform.scale(background, (800, 600))
background_rect = background.get_rect()
bullets = pygame.sprite.Group()
shot_image = pygame.image.load('img/shot.png').convert_alpha()
blood1 = pygame.image.load('img/blood1.png').convert_alpha()
blood1 = pygame.transform.scale(blood1, (60, 60))
blood2 = pygame.image.load('img/blood2.png').convert_alpha()
blood2 = pygame.transform.scale(blood2, (70, 70))
shot_image = pygame.transform.scale(shot_image, (52, 52))
hero_image = pygame.image.load('img/hero.png').convert_alpha()
hero_image = pygame.transform.scale(hero_image, (90, 90))
skeleton_image = pygame.image.load('img/enemyskelly.png').convert_alpha()
skeleton_image = pygame.transform.scale(skeleton_image, (90, 90))
wizard_image = pygame.image.load('img/wizard.png').convert_alpha()
wizard_image = pygame.transform.scale(wizard_image, (90, 90))
ghost_image = pygame.image.load('img/ghost.gif').convert_alpha()
ghost_image = pygame.transform.scale(ghost_image, (120, 120))
dragon_image = pygame.image.load('img/Dragon.png').convert_alpha()
dragon_image = pygame.transform.scale(dragon_image, (120, 120))
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = shot_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            shots_out.pop()
            self.kill()



class Char(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 10
        self.x = 400
        self.y = 475
        self.last_shot = pygame.time.get_ticks()
        self.life = 5
        self.rect.center = [self.x, self.y]
        self.shoot_delay = 270
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullets.add(Bullet(self.rect.centerx, self.rect.top))
        # sprites.add(Bullet(self.rect.centerx, self.rect.top))
        # bullets.add(Bullet(self.rect.centerx, self.rect.top))
        shots_out.append("pew")
    def update(self, pressed_keys, pos):
            # self.rect.move_ip(pos)
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -(self.speed))
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-(self.speed), 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        if pressed_keys[K_SPACE]:
            self.shoot()
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Monster(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speedx = random.randint(-5, 7)
        self.speedy = random.randint(0,8)
        self.x = random.randint(1, 800)
        self.y = random.randint(5, 30)
        self.rect.center = [self.x, self.y]

    def update(self):
        self.rect.move_ip(self.speedx, self.speedy)
        if self.rect.left > 600:
            self.kill()
# class Monster(pygame.sprite.Sprite):
#     def __init__(self, image):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = image
#         self.rect = self.image.get_rect()
#         self.speed = random.randint(1, 7)
#         self.x = random.randint(1, 800)
#         self.y = random.randint(0, 30)
#         self.rect.center = [self.x, self.y]
#     def update(self):
#         self.rect.move_ip(0, self.speed)
#         if self.rect.left > 600:
#             self.kill()

class Blood(pygame.sprite.Sprite):
    def __init__(self, image, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 3:
                self.kill()
            else:
                center = self.rect.center
                self.image = blood2
                self.rect = self.image.get_rect()
                self.rect.center = center

def newMonster():
    roll = random.randint(1, 3)
    if roll == 1:
        a = Monster(skeleton_image)
    if roll == 2:
        a = Monster(wizard_image)
    if roll == 3:
        a = Monster(ghost_image)
    sprites.add(a)
    enemy_sprites.add(a)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "LOST WIZARD", 80, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_text(screen, "A and D to move left and right, SPACE to fire.", 50,
              SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, SCREEN_WIDTH/ 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


player = Char(hero_image)
enemy_sprites = pygame.sprite.Group()
sprites = pygame.sprite.Group()
shot = pygame.sprite.groupcollide(enemy_sprites, bullets, True, True)
blood_group = pygame.sprite.Group()
sprites.add(player)
shots_out = []
def redrawGameWindow():
    # screen.blit(bg, (0,0))
    sprites.draw(screen)
    bullets.draw(screen)
    bullets.update()
    blood_group.update()
    enemy_sprites.update()
    pygame.display.update()
    player.update(pressed_keys, pos)
    
level = 1
difficulty = 1
score = 0
counter = 0
running = True
start_screen = True
while running:
    pressed_keys = pygame.key.get_pressed()
    pos = pygame.mouse.get_pos()
    if start_screen:
        show_go_screen()
        start_screen = False
        sprites = pygame.sprite.Group()
        enemy_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Char(hero_image)
        sprites.add(player)
        for i in range(8):
            newMonster()
        score = 0
    
    clock.tick(60)
    for event in pygame.event.get():
        pressed_keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False

    hits = pygame.sprite.groupcollide(enemy_sprites, bullets, True, True)
    for hit in hits:
        score += 1
        random_roll = random.randint(1, 6)
        if random_roll > 3:
            blood = Blood(blood1, hit.rect.center, 3)
        elif random_roll <= 3:
            blood = Blood(blood2, hit.rect.center, 3)
        sprites.add(blood)
        blood_group.add (blood)
        if len(shots_out) > 0:
            shots_out.pop()

    hits = pygame.sprite.spritecollide(player, enemy_sprites, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.life -= 1
        if player.life == 0:
            start_screen = True

    random_roll = random.randint(1, 10)
    if random_roll <= difficulty:
        newMonster()      
    
    

    screen.fill((75, 22, 75))

    

    counter += 1
    redrawGameWindow()
    pygame.display.flip()
    

pygame.quit()