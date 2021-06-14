import pygame
from random import randint
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
CENTER_X = int(WIDTH / 2)
CENTER_Y = int(HEIGHT / 2)
TITLE = "Evolve"
GAME_FONT = "fonts/larson.ttf"
TIMER = 300
IMMUNE = 180
HEALTH = 3
VELOCITY = 1.5
FOOD_VEL = (VELOCITY / 3)
BACKGROUND_VEL = 0.25
BACKGROUND_VEL2 = 0.1

game_mode = "intro"
level = 1

player_gen = 1
player_health = 3
evolve_count = (level * 3)
player_x = CENTER_X
player_y = CENTER_Y
last_direction = "up"
        
running = True
immune_timer = 0
reset_timer = TIMER
intro_scroll = HEIGHT
background_scroll = 0
background_scroll2 = 0

player_prey = []
enemy_prey = []
player_predator = []
enemy_predator = [1]

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
ICON = pygame.image.load("images/player-5.png").convert_alpha()
pygame.display.set_icon(ICON)
background = pygame.image.load("images/bubbles.png").convert_alpha()
background2 = pygame.image.load("images/bubbles2.png").convert_alpha()

def load_sprite(name):
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load("images/" + name + ".png").convert_alpha()
    sprite.mask = pygame.mask.from_surface(sprite.image)
    sprite.rect = sprite.image.get_rect()
    return sprite

def load_player(gen):
    global player_sprites, player_v, player, shield
    player_sprites = {}
    if gen in [1, 2, 4]:
        player_v = (VELOCITY / 3)
    elif gen in [3, 5]:
        player_v = (VELOCITY * 2 / 3)
    else:
        player_v = VELOCITY
    if gen in [3, 5, 6]:
        j = 0
        for i in ["left", "leftdown", "down", "rightdown", "right", "rightup", "up", "leftup"]:
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load("images/player-" + str(gen) + ".png").convert_alpha()
            if j > 0:
                sprite.image = pygame.transform.rotate(sprite.image, (j * 45))
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = [player_x, player_y]
            player_sprites[i] = sprite
            j += 1
        player = player_sprites["up"]
    else:
        player = load_sprite("player-" + str(gen))
        player.rect.center = [player_x, player_y]
    if gen == 1:
        shield = load_sprite("shield-small")
    elif gen in [2, 3, 5]:
        shield = load_sprite("shield-medium")
    elif gen in [4, 6]:
        shield = load_sprite("shield-large")
    shield.rect.center = [player_x, player_y]

def load_food():
    spritelist = []
    sprite = load_sprite("food")
    spritex = randint(0, (WIDTH - sprite.rect.width))
    spritey = -(randint(sprite.rect.height, HEIGHT))
    sprite.rect.topleft = [spritex, spritey]
    spritelist.append(sprite)
    spritelist.append(spritex)
    spritelist.append(spritey)
    food.append(spritelist)

def create_food(n):
    global food
    food = []
    for i in range(n):
        load_food()

def load_fish(name, gen):
    spritelist = []
    if name == "player":
        if gen in [1, 2, 4]:
            fish_v = (VELOCITY / 3)
        elif gen in [3, 5]:
            fish_v = (VELOCITY * 2 / 3)
        else:
            fish_v = VELOCITY
    else:
        fish_v = (VELOCITY * gen / 3)
    sprite = load_sprite(name + "-" + str(gen))
    if randint(0, 1) == 0:
        sprite.rect.centerx = -(randint(sprite.rect.width, CENTER_X))
        sprite.image = pygame.transform.flip(sprite.image, True, False)
        sprite.mask = pygame.mask.from_surface(sprite.image)
    else:
        sprite.rect.centerx = WIDTH + randint(0, CENTER_X)
        fish_v *= -1
    sprite.rect.centery = randint(int((sprite.rect.height / 2)), (HEIGHT - int((sprite.rect.height / 2))))
    spritelist.append(sprite)
    spritelist.append(sprite.rect.centerx)
    spritelist.append(sprite.rect.centery)
    spritelist.append(fish_v)
    spritelist.append(name)
    spritelist.append(gen)
    sprite2_type = 0
    if name == "player":
        if level == 1:
            if gen == 1:
                if randint(0, 2):
                    sprite2 = load_sprite("herb-small")
                    sprite2_type = 1
                else:
                    sprite2 = load_sprite("carn-small")
                    sprite2_type = 2
        elif level == 2:
            if gen == 2:
                sprite2 = load_sprite("herb-medium")
                sprite2_type = 1
            elif gen == 3:
                sprite2 = load_sprite("carn-medium")
                sprite2_type = 2
        else:
            if gen == 4:
                sprite2 = load_sprite("herb-large")
                sprite2_type = 1
            elif gen == 5:
                if randint(0, 2):
                    sprite2 = load_sprite("herb-medium")
                    sprite2_type = 1
                else:
                    sprite2 = load_sprite("carn-medium")
                    sprite2_type = 2
            elif gen == 6:
                sprite2 = load_sprite("carn-large")
                sprite2_type = 2
    if sprite2_type:
        sprite2.rect.center = sprite.rect.center
        spritelist.append(sprite2)
        spritelist.append(sprite2_type)
    else:
        spritelist.append(0)
        spritelist.append(0)
    fish.append(spritelist)

def create_fish(number):
    global fish
    fish = []
    if number == 1:
        for i in range(4):
            load_fish("enemy", 1)
            load_fish("player", 1)
    elif number == 2:
        for i in range(3):
            load_fish("enemy", 1)
            load_fish("enemy", 2)
            for j in range(2):
                load_fish("player", (i + 1))
    else:
        for i in range(2):
            load_fish("enemy", 1)
            load_fish("enemy", 2)
            load_fish("enemy", 3)
        for j in range(6):
            load_fish("player", (j + 1))

class Bubble_Text:
    def __init__(self, text, size, color, bcolor):
        self.text = text
        self.size = size
        self.color = color
        self.bcolor = bcolor
    
        font = pygame.font.Font(GAME_FONT, self.size)
        text = font.render(self.text, True, self.color)
        self.surface = pygame.Surface((text.get_width() + 20, text.get_height() + 20))
        self.surface = self.surface.convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        for index in range(-20, 20):
            x = ( math.cos(index * 9) * 10 ) + 10
            y = ( math.sin(index * 9) * 10 ) + 10
            self.surface.blit(text, (x, y))
        self.surface.blit(font.render(self.text, True, self.bcolor), (10, 10))
        self.x = ( self.surface.get_width() / 2)
        self.y = ( self.surface.get_height() / 2)
        self.bottom = self.surface.get_height()
        self.black = self.surface.copy()
        self.black.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)

class Text:
    def __init__(self, text, size, center, color):
        self.text = text
        self.size = size
        self.color = color
        self.center = center
        
        font = pygame.font.Font(GAME_FONT, self.size)
        self.text = font.render(self.text, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.center = self.center

def update():
    global running, background_scroll, background_scroll2, player_x, player_y, last_direction, player, player_sprites, intro_scroll
    global reset_timer, immune_timer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if game_mode == "play":
        direction_x = ""
        direction_y = ""
        move_x = 0
        move_y = 0
        if keys[pygame.K_LEFT]:
            move_x -= player_v
            direction_x = "left"
        if keys[pygame.K_RIGHT]:
            move_x += player_v
            if direction_x:
                direction_x = ""
            else:
                direction_x = "right"
        if keys[pygame.K_UP]:
            move_y -= player_v
            direction_y = "up"
        if keys[pygame.K_DOWN]:
            move_y += player_v
            if direction_y:
                direction_y = ""
            else:
                direction_y = "down"
        if direction_x and direction_y:
            move_x *= 0.71
            move_y *= 0.71
        player_x += move_x
        player_y += move_y
        if player_x < 0:
            player_x = 0
        if player_x > WIDTH:
            player_x = WIDTH
        if player_y < 0:
            player_y = 0
        if player_y > HEIGHT:
            player_y = HEIGHT
        if player_gen in [3, 5, 6]:
            direction = direction_x + direction_y
            if direction:
                if not direction == last_direction:
                    player = player_sprites[direction]
                last_direction = direction
        player.rect.center = player_x, player_y
        shield.rect.center = player_x, player_y
        if immune_timer:
            immune_timer -= 1
    elif game_mode == "intro":
        if intro_scroll:
            intro_scroll -= 1
        else:
            if reset_timer:
                reset_timer -= 1
            else:
                mode_select("level")
    elif game_mode == "level":
        if reset_timer:
            reset_timer -= 1
        else:
            mode_select("info")
    elif game_mode == "info":
        if reset_timer:
            reset_timer -= 1
        else:
            mode_select("play")
    elif game_mode == "over":
        if reset_timer:
            reset_timer -= 1
        else:
            mode_select("intro")
    if background_scroll > -HEIGHT:
        background_scroll -= BACKGROUND_VEL
    else:
        background_scroll = 0
    if background_scroll2 > -HEIGHT:
        background_scroll2 -= BACKGROUND_VEL2
    else:
        background_scroll2 = 0
    if game_mode in ["play", "intro"]:
        for i in food:
            if i[0].rect.y > HEIGHT:
                food.remove(i)
                load_food()
            else:
                i[2] += FOOD_VEL
                i[0].rect.top = i[2]
        for i in fish:
            if i[3] > 0:
                if i[0].rect.left > WIDTH:
                    load_fish(i[4], i[5])
                    fish.remove(i)
                else:
                    i[1] += i[3]
            else:
                if i[0].rect.right < 0:
                    load_fish(i[4], i[5])
                    fish.remove(i)
                else:
                    i[1] += i[3]
            i[0].rect.centerx = i[1]
            if not evolve_count:
                if i[7]:
                    i[6].rect.centerx = i[1]

def evolve(evolve_type):
    global player_gen, level, player_prey, enemy_prey, player_predator, enemy_predator
    if player_gen < 4:
        if player_gen == 1:
            if evolve_type == 1:
                player_gen = 2
                player_prey = [1]
                enemy_prey = []
                player_predator = [3]
                enemy_predator = [2]
            else:
                player_gen = 3
                player_prey = [1]
                enemy_prey = [2]
                player_predator = [2]
                enemy_predator = [1]
        elif player_gen == 2:
            if evolve_type == 1:
                player_gen = 4
                player_prey = [1]
                enemy_prey = []
                player_predator = [6]
                enemy_predator = [3]
            else:
                player_gen = 5
                player_prey = [1]
                enemy_prey = [2]
                player_predator = [6]
                enemy_predator = [1, 3]
        elif player_gen == 3:
            if evolve_type == 1:
                player_gen = 5
                player_prey = [1]
                enemy_prey = [2]
                player_predator = [6]
                enemy_predator = [1, 3]
            else:
                player_gen = 6
                player_prey = [1, 2]
                enemy_prey = [2]
                player_predator = [5]
                enemy_predator = [1, 3]
        level += 1
        mode_select("level")
    else:
        mode_select("win")
        

def check_collide(sprite):
    if pygame.Rect.colliderect(player.rect, sprite.rect):
        if pygame.sprite.collide_mask(player, sprite):
            return True
    return False

def check_collisions():
    global evolve_count, play_text1, player_health, play_text2, level, player_gen, immune_timer
    if player_gen in [1, 2, 4, 5]:
        for i in food:
            if check_collide(i[0]):
                food.remove(i)
                load_food()
                if evolve_count:
                    evolve_count -= 1
                    if evolve_count:
                        play_text1 = Text("Evolve " + str(evolve_count), 40, ((WIDTH / 4), 20), (255,255,255))
                    else:
                        play_text1 = Text("Evolve", 40, ((WIDTH / 4), 20), (255,255,255))
    for i in fish:
        if not evolve_count and i[7]:
            if check_collide(i[0]):
                evolve(i[7])
        elif i[4] == "player":
            if i[5] in player_predator:
                if not immune_timer:
                    if check_collide(i[0]):
                        player_health -= 1
                        if player_health:
                            immune_timer = IMMUNE
                            play_text2 = Text("Health " + str(player_health), 40, ((WIDTH * 3 / 4), 20), (255,255,255))
                        else:
                            mode_select("over")
            elif i[5] in player_prey:
                if check_collide(i[0]):
                    load_fish(i[4], i[5])
                    fish.remove(i)
                    if evolve_count:
                        evolve_count -= 1
                        if evolve_count:
                            play_text1 = Text("Evolve " + str(evolve_count), 40, ((WIDTH / 4), 20), (255,255,255))
                        else:
                            play_text1 = Text("Evolve", 40, ((WIDTH / 4), 20), (255,255,255))
        elif i[4] == "enemy":
            if i[5] in enemy_predator:
                if not immune_timer:
                    if check_collide(i[0]):
                        player_health -= 1
                        if player_health:
                            immune_timer = IMMUNE
                            play_text2 = Text("Health " + str(player_health), 40, ((WIDTH * 3 / 4), 20), (255,255,255))
                        else:
                            mode_select("over")
            elif i[5] in enemy_prey:
                if check_collide(i[0]):
                    load_fish(i[4], i[5])
                    fish.remove(i)
                    if evolve_count:
                        evolve_count -= 1
                        if evolve_count:
                            play_text1 = Text("Evolve " + str(evolve_count), 40, ((WIDTH / 4), 20), (255,255,255))
                        else:
                            play_text1 = Text("Evolve", 40, ((WIDTH / 4), 20), (255,255,255))

def draw():
    screen.fill('midnightblue')
    screen.blit(background2, (0, background_scroll2))
    screen.blit(background2, (0, background_scroll2 + 600))
    screen.blit(background, (0, background_scroll))
    screen.blit(background, (0, background_scroll + 600))
    if game_mode in ["intro", "play"]:
        for i in food:
            screen.blit(i[0].image, i[0].rect)
        for i in fish:
            screen.blit(i[0].image, i[0].rect)
            if not evolve_count:
                if i[7]:
                    screen.blit(i[6].image, i[6].rect)
    if game_mode == "play":
        screen.blit(player.image, player.rect)
        if immune_timer:
            screen.blit(shield.image, shield.rect)
        screen.blit(play_text1.text, play_text1.rect)
        screen.blit(play_text2.text, play_text2.rect)
    elif game_mode == "intro":
        screen.blit(intro_text6.surface, (CENTER_X - intro_text1.x + 295 - intro_scroll, CENTER_Y - intro_text1.y))
        screen.blit(intro_text5.surface, (CENTER_X - intro_text1.x + 170 - (intro_scroll * 0.7), CENTER_Y - intro_text1.y - (intro_scroll * 0.7)))
        screen.blit(intro_text4.surface, (CENTER_X - intro_text1.x + 85 - (intro_scroll * 0.7), CENTER_Y - intro_text1.y + (intro_scroll * 0.7)))
        screen.blit(intro_text3.surface, (CENTER_X - intro_text1.x - 34 + (intro_scroll * 0.7), CENTER_Y - intro_text1.y - (intro_scroll * 0.7)))
        screen.blit(intro_text2.surface, (CENTER_X - intro_text1.x - 155 + (intro_scroll * 0.7), CENTER_Y - intro_text1.y + (intro_scroll * 0.7)))
        screen.blit(intro_text1.surface, (CENTER_X - intro_text1.x - 274 + intro_scroll, CENTER_Y - intro_text1.y))
    elif game_mode == "level":
        screen.blit(level_text1.text, level_text1.rect)
        screen.blit(level_text2.text, level_text2.rect)
        screen.blit(player.image, player.rect)
    elif game_mode == "info":
        screen.blit(info_text1.text, info_text1.rect)
        screen.blit(info_text2.text, info_text2.rect)
        for i in prey_list:
            screen.blit(i.image, i.rect)
        for i in predator_list:
            screen.blit(i.image, i.rect)
    elif game_mode == "over":
        screen.blit(over_text1.text, over_text1.rect)
        screen.blit(over_text2.text, over_text2.rect)
        screen.blit(player.image, player.rect)
    pygame.display.flip()

def mode_select(mode):
    global game_mode, player, intro_scroll, reset_timer, level_text1, level_text2, play_text1, evolve_count, player_health, player_x, player_y
    global play_text2, over_text1, over_text2, player_gen, level, player_prey, enemy_prey, player_predator, enemy_predator, info_text1, info_text2
    global prey_list, predator_list, last_direction
    if mode == "intro":
        evolve_count = (level * 3)
        intro_scroll = HEIGHT
        reset_timer = TIMER
        player_gen = 1
        level = 1
        create_food(6)
        create_fish(3)
        player_prey = []
        enemy_prey = []
        player_predator = []
        enemy_predator = [1]
        game_mode = "intro"
    elif mode == "level":
        evolve_count = (level * 3)
        reset_timer = TIMER
        level_text1 = Text("Generation " + str(level), 80, (CENTER_X, (HEIGHT / 4)), (255,255,255))
        if player_gen == 1:
            player_type = "Proto-Life"
        elif player_gen == 2:
            player_type = "Early Herbivore"
        elif player_gen == 3:
            player_type = "Early Carnivore"
        elif player_gen == 4:
            player_type = "Late Herbivore"
        elif player_gen == 5:
            player_type = "Late Omnivore"
        else:
            player_type = "Late Carnivore"
        level_text2 = Text(player_type, 70, (CENTER_X, (HEIGHT / 2)), (255,255,255))
        load_player(player_gen)
        player.rect.center = CENTER_X, (HEIGHT * 0.75)
        game_mode = "level"
    elif mode == "info":
        reset_timer = TIMER
        prey_list = []
        info_text1 = Text("Food", 100, (CENTER_X, (HEIGHT / 5)), (255,255,255))
        if player_gen  in [1, 2, 4, 5]:
            prey = load_sprite("food")
            prey_list.append(prey)
        if player_prey:
            for i in player_prey:
                prey = load_sprite("player-" + str(i))
                prey_list.append(prey)
        if enemy_prey:
            for i in enemy_prey:
                prey = load_sprite("enemy-" + str(i))
                prey_list.append(prey)
        j = 1
        for i in prey_list:
            i.rect.center = (j / (len(prey_list) + 1) * WIDTH), (HEIGHT * 2 / 5)
            j += 1
        predator_list = []
        info_text2 = Text("Predators", 100, (CENTER_X, (HEIGHT * 3 / 5)), (255,255,255))
        if player_predator:
            for i in player_predator:
                predator = load_sprite("player-" + str(i))
                predator_list.append(predator)
        if enemy_predator:
            for i in enemy_predator:
                predator = load_sprite("enemy-" + str(i))
                predator_list.append(predator)
        j = 1
        for i in predator_list:
            i.rect.center = (j / (len(predator_list) + 1) * WIDTH), (HEIGHT * 4 / 5)
            j += 1
        game_mode = "info"
    elif mode == "play":
        player_health = HEALTH
        last_direction = "up"
        if evolve_count:
            play_text1 = Text("Evolve " + str(evolve_count), 40, ((WIDTH / 4), 20), (255,255,255))
        else:
            play_text1 = Text("Evolve", 40, ((WIDTH / 4), 20), (255,255,255))
        play_text2 = Text("Health " + str(player_health), 40, ((WIDTH * 3 / 4), 20), (255,255,255))
        create_food(6)
        create_fish(level)
        load_player(player_gen)
        player.rect.center = CENTER_X, CENTER_Y
        player_x = CENTER_X
        player_y = CENTER_Y
        game_mode = "play"
    elif mode == "over":
        reset_timer = TIMER
        over_text1 = Text("Game Over", 100, (CENTER_X, (HEIGHT / 4)), (255,255,255))
        over_text2 = Text("Reached Gen " + str(level), 70, (CENTER_X, (HEIGHT / 2)), (255,255,255))
        load_player(player_gen)
        player.rect.center = CENTER_X, (HEIGHT * 0.75)
        game_mode = "over"
    elif mode == "win":
        reset_timer = TIMER
        over_text1 = Text("Game Won", 100, (CENTER_X, (HEIGHT / 4)), (255,255,255))
        over_text2 = Text("Final Evolution", 70, (CENTER_X, (HEIGHT / 2)), (255,255,255))
        load_player(player_gen)
        player.rect.center = CENTER_X, (HEIGHT * 0.75)
        game_mode = "over"

intro_text1 = Bubble_Text("E", 180, (0,128,0), (0,64,0))
intro_text2 = Bubble_Text("v", 180, (178,63,0), (70,24,0))
intro_text3 = Bubble_Text("o", 180, (0,128,0), (0,64,0))
intro_text4 = Bubble_Text("l", 180, (137,22,136), (64,6,64))
intro_text5 = Bubble_Text("v", 180, (0,128,0), (0,64,0))
intro_text6 = Bubble_Text("e", 180, (111,135,255), (5,25,126))

mode_select(game_mode)

while running:
    clock.tick(60)
    update()
    if game_mode == "play":
        check_collisions()
    draw()

pygame.quit()
