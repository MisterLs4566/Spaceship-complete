from tkinter import *
from tkinter import font as tkFont
import pygame, sys
from pygame.locals import *
import keyboard
from random import randint
import time as t
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
window = None
width = 600
height = 600
score = 0
all_sprites = pygame.sprite.Group()
first_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 60
player = None
ufo = None
volume = 0.3
laser_sound = pygame.mixer.Sound("sounds/Laser_Shoot28.wav")
laser_sound.set_volume(volume)
laser_sound2 = pygame.mixer.Sound("sounds/Laser_Shoot64.wav")
laser_sound2.set_volume(volume)
explosion_sound1 = pygame.mixer.Sound("sounds/Explosion32.wav")
explosion_sound1.set_volume(volume)
explosion_sound2 = pygame.mixer.Sound("sounds/Explosion38.wav")
explosion_sound2.set_volume(volume)
pickup_sound = pygame.mixer.Sound("sounds/Pickup_Coin70.wav")
pickup_sound.set_volume(volume)
explosion_sound3 = pygame.mixer.Sound("sounds/Explosion42.wav")
explosion_sound3.set_volume(volume)
randomize_sound = pygame.mixer.Sound("sounds/Randomize35.wav")
randomize_sound.set_volume(volume)
sounds = [laser_sound, explosion_sound1, explosion_sound2]
enemies = []
old_time = 0
time = 0
timer = 0
ufo_timer = 0
direction="right"
velocity = 1
positions = []
enemies = []
positions_x = []
points = 0
level = 1
fontobj = pygame.font.Font("freesansbold.ttf", 10)
fontobj2 = pygame.font.Font("freesansbold.ttf", 20)
fontsurfobj2 = fontobj2.render("PAUSE", True, (255, 255, 255))
fontsurfobj4 = fontobj2.render("PRESS R TO TRY AGAIN", True, (255, 255, 255))
fontsurfobj6 = fontobj2.render("LEVEL " + str(level), True, (255, 255, 255))
plane = 10
stars = 0
stop = False
dif = 1
necessary = 100
class Ufo (pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed, scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.image = pygame.image.load("sprites/ufo.PNG").convert()
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
        self.instantiate = False
        self.spawnrate = 3
        self.spawn = True
    def update(self):
        if self.instantiate == True:
            if self.rect.x < 550:
                self.rect.x += self.speed
            else:
                self.instantiate = False
                self.rect.x = self.pos_x
        if self.rect.colliderect(player.rect):
            explosion_sound1.play()
            player.hearts -= 1
            backup = player.speed
            player.speed = 0
            player.rect.x = player.pos_x
            player.rect.y = player.pos_y
            if player.hearts == 0:
                player.laser.instantiate = False
                game.game_over()
            self.play = True
            player.speed = backup
class Star(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, time, scale):
        pygame.sprite.Sprite.__init__(self)
        self.stars = ["sprites/star_yellow.png", "sprites/star_red.png", "sprites/star_green.png", "sprites/star_blue.png"]
        self.random = randint(0, 3)
        self.image = pygame.image.load(self.stars[self.random])
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.scale = 33
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.time = time
        self.old_time = 0
        self.counter = 0
        self.timer = 0
    def update(self):
        global time
        global first_sprites
        global points
        global timer
        global stars
        if self.counter == 0:
            self.counter = 1
            self.old_time = pygame.time.get_ticks()
        if time-self.old_time > self.time:
            first_sprites.remove(self)
        if self.rect.colliderect(player.rect):
            points += 1
            player.color = (255, 255, 0)
            timer = pygame.time.get_ticks()
            first_sprites.remove(self)
            stars += 1
            pickup_sound.play()
        if self.rect.colliderect(player.laser.rect):
            points += 1
            player.color = (255, 255, 0)
            timer = pygame.time.get_ticks()
            first_sprites.remove(self)
            stars += 1
            pickup_sound.play()
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/laser3.PNG").convert()
        self.picture = pygame.image.load("sprites/laser3.PNG").convert()
        self.picture2 = pygame.image.load("sprites/invisible.PNG").convert()
        self.image_counter = 1
        self.image = pygame.transform.scale(self.image, (10, 15))
        self.scalex = 10
        self.scaley = 10
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect()
        #self.rect = self.rect.move(500, 0)
        #self.rect.inflate_ip(-65, -60)
        self.rect.x = pos_y
        self.rect.y = pos_y
        self.speed = speed
        self.velocity = direction
        self.instantiate = False
        self.play = True
        self.play2 = True
    def update(self):
        global enemies
        global all_sprites
        global timer
        global points
        global level
        global stars
        if self.velocity == 1:
            for enemy in enemies:
                if self.instantiate == True:
                    if self.rect.colliderect(enemy.rect):
                        if self.play == True:
                            self.play = False
                            explosion_sound2.play()
                        game.create_star(enemy.rect.x, enemy.rect.y, 2000)
                        self.instantiate = False
                        all_sprites.remove(enemy)
                        all_sprites.remove(enemy.laser)
                        enemy.removed = True
                        enemies.remove(enemy)
                        if len(enemies) == 0:
                            randomize_sound.play()
                            lives = player.hearts
                            level += 1
                            game.button = False
                            game.manager()
                            player.hearts = lives
                        self.rect.x = player.rect.x + 2
                        self.rect.y = player.rect.y + 28
                        self.play = True
                    if self.rect.colliderect(ufo.rect):
                        self.instantiate = False
                        all_sprites.remove(ufo)
                        explosion_sound3.play()
                        points += 3
                        stars  += 3
                        timer = pygame.time.get_ticks()
                        ufo.rect.x = 600
                        all_sprites.add(ufo)
        elif self.velocity == -1:
            if self.rect.colliderect(player.rect):
                player.laser.instantiate = False
                if self.play2 == True:
                    self.play2 = False
                    explosion_sound1.play()
                player.hearts -= 1
                player.rect.x = player.pos_x
                player.rect.y = player.pos_y
                self.rect.x = self.pos_x
                self.rect.y = self.pos_y
                self.play2 = True
                if player.hearts == 0:
                    self.instantiate = False
                    game.game_over()
class Player(pygame.sprite.Sprite):
    def __init__(self, speed, hearts, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.scale = 60
        self.pos_x = game.width/2-self.scale/2
        self.pos_y = game.height-self.scale*1.25
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.speed = speed
        self.laser = Laser(self.pos_x, self.pos_y, 10, 1)
        self.play = True
        self.hearts = hearts
        self.color = (255, 255, 255)
        self.fontsurfobj = fontobj.render("stars: " + str(points), True, self.color)
        self.joystick = False
        self.joystick_d = ""
        self.pressed = [0, 0]
    def update(self):
        global timer
        global plane
        global stars
        if self.rect.y < plane:
            player.laser.instantiate = False
            explosion_sound1.play()
            player.hearts -= 1
            player.rect.x = player.pos_x
            player.rect.y = player.pos_y
            self.rect.x = self.pos_x
            self.rect.y = self.pos_y
            self.play2 = True
            if player.hearts == 0:
                self.instantiate = False
                game.game_over()
        self.fontsurfobj = fontobj.render("stars: " + str(stars), True, self.color)
        if self.joystick == True:
            if self.joystick_d == "right":
                if self.rect.x <= game.width - 70:
                    self.rect.x += self.speed
            if self.joystick_d == "left":
                if self.rect.x >= 10:
                    self.rect.x -= self.speed
            if self.joystick_d == "up":
                if self.rect.y >= 10:
                    self.rect.y -= self.speed
            if self.joystick_d == "down":
                if self.rect.y <= game.height - 70:
                    self.rect.y += self.speed
        if keyboard.is_pressed("w"):
            if self.rect.y >= 10:
                self.rect.y -= self.speed
        if keyboard.is_pressed("a"):
            if self.rect.x >= 10:
                self.rect.x -= self.speed
        if keyboard.is_pressed("s"):
            if self.rect.y <= game.height - 70:
                self.rect.y += self.speed
        if keyboard.is_pressed("d"):
            if self.rect.x <= game.width - 70:
                self.rect.x += self.speed
        if self.laser.instantiate == False:
            self.play = True
            self.laser.rect.x = self.rect.x+25
            self.laser.rect.y = self.rect.y+20
        if self.laser.instantiate == True:
            self.play = False
            if self.laser.rect.y > 10:
                self.laser.rect.y -= self.laser.speed * self.laser.velocity
            else:
                self.laser.instantiate = False
        if timer != 0:
            if time-timer > 1000:
                self.color = (255, 255, 255)
                timer = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed, image):
        pygame.sprite.Sprite.__init__(self)
        global dif
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.scale = 50
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 50, 50)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
        self.velocity = 1
        self.steps = 10
        self.direction = "right"
        self.laser = Laser(self.pos_x, self.pos_y, 7, -1)
        self.movement = True
        if dif == 1:
            self.spawnrate = 1500
        elif dif == 2:
            self.spawnrate = 1000
        elif dif == 3:
            self.spawnrate = 750
        self.play = True
        self.x = 0
        self.removed = False
    def shoot(self):
        self.x = randint(0, self.spawnrate)
        if self.x == self.spawnrate:
            if self.laser.instantiate == False:
                return True
            else:
                return False
        else:
            return False
    def ufo(self):
        global ufo
        global plane
        plane += self.steps
        if plane > 40:
            x = randint(0, ufo.spawnrate)
            if x == ufo.spawnrate:
                ufo.spawn = False
                if ufo.instantiate == False:
                    ufo.instantiate = True
    def update(self):
        global enemies
        global old_time
        global time
        global direction
        global velocity
        global positions
        global positions_x
        global plane
        global points
        global dif
        if self.movement == True:
            self.rect.x += self.speed * velocity
            old_time = pygame.time.get_ticks()
            self.movement = False
        if time-old_time > 10:
            self.movement = True
        if self.rect.y > 450:
            if self.play == True:
                self.play = False
                explosion_sound1.play()
            player.hearts -= 1
            backup = player.speed
            player.speed = 0
            player.rect.x = player.pos_x
            player.rect.y = player.pos_y
            if player.hearts == 0:
                points = 0
                player.laser.instantiate = False
                game.game_over()
            self.play = True
            player.speed = backup
        if self.rect.x > game.width-50:
            velocity = 0
            velocity = 0
            self.rect.x = game.width-50
            if direction == "right":
                direction = "left"
                for enemy in enemies:
                    enemy.rect.y += enemy.steps
                    enemy.laser.rect.y += enemy.steps
                    if dif > 1:
                        if enemy.rect.y > 200:
                            enemy.speed +=1
                if ufo.spawn == True:
                    self.ufo()
                for enemy in enemies:
                    for position in positions_x:
                        if enemy.rect.x > position:
                            if (enemy.rect.x - position) < 5:
                                enemy.rect.x = position
                        elif position > enemy.rect.x:
                            if (position - enemy.rect.x) < 5:
                                enemy.rect.x = position
                velocity = -1
        if self.rect.x < 0:
            velocity = 0
            self.rect.x = 0
            if direction == "left":
                direction = "right"
                for enemy in enemies:
                    enemy.rect.y += enemy.steps
                    enemy.laser.rect.y += enemy.steps
                    if dif > 1:
                        if enemy.rect.y > 200:
                            enemy.speed +=1
                if ufo.spawn == True:
                    self.ufo()
                for enemy in enemies:
                    for position in positions_x:
                        if enemy.rect.x > position:
                            if (enemy.rect.x - position) < 5:
                                enemy.rect.x = position
                        elif position > enemy.rect.x:
                            if (position - enemy.rect.x) < 5:
                                enemy.rect.x = position
                velocity = 1
        if self.rect.colliderect(player.rect):
            if self.play == True:
                self.play = False
                explosion_sound1.play()
            player.hearts -= 1
            backup = player.speed
            player.speed = 0
            player.rect.x = player.pos_x
            player.rect.y = player.pos_y
            if player.hearts == 0:
                points = 0
                player.laser.instantiate = False
                game.game_over()
            self.play = True
            player.speed = backup
        if self.laser.instantiate == False:
            self.play = True
            self.laser.rect.x = self.rect.x+20
            self.laser.rect.y = self.rect.y+25
        if self.laser.instantiate == True:
            self.play = False
            if self.laser.rect.y < 600:
                self.laser.rect.y -= self.laser.speed * self.laser.velocity
            else:
                self.laser.instantiate = False
        if self.shoot():
            pygame.mixer.Sound.play(laser_sound2)
            self.laser.instantiate = True
class Game():
    def __init__(self, width, height):
        self.status = 1
        self.menu = None
        self.canvas = None
        self.canvas2 = None
        self.options = None
        self.option_possible = True
        self.counter = 0
        self.button = True
        self.width = width
        self.height = height
        self.create_window = False
    def quit(self):
        sys.exit()
    def create_enemies(self, number, speed):
        global enemies
        global positions_x
        positions_x = [0, 100, 200, 300, 400]
        positions_y = [10, 100, 190, 280, 370]
        numbers = [1, 2, 3, 4]
        counter = 0
        quantity = 0
        pos_x = 0
        pos_y = positions_y[counter]
        enemies = []
        for x in range(0, number):
            enemies.append(x)
        for x in range(0, number):
            quantity += 1
            if pos_y < 200:
                enemies[x] = Enemy(positions_x[pos_x], pos_y, speed, "sprites/enemy.png")
            else:
                enemies[x] = Enemy(positions_x[pos_x], pos_y, speed, "sprites/enemy2.png")
            pos_x+=1
            if quantity/4 in numbers:
                counter+=1
                pos_y = positions_y[counter]
                pos_x = 0
        for enemy in enemies:
            all_sprites.add(enemy.laser, enemy)
    def create_star(self, x, y, t):
        star = Star(x, y, t, 33)
        first_sprites.add(star)
    def start_easy(self):
        global window
        global player
        global enemies
        global positions
        global ufo
        global plane
        global points
        global stars
        global necessary
        plane = 10
        self.status = 3
        self.counter += 1
        enemies.clear()
        if self.counter > 1:
            all_sprites.empty()
            first_sprites.empty()
        if self.option_possible == True:
            if self.button == True:
                points = 0
                self.menu.destroy()
                window = pygame.display.set_mode((self.width, self.height))
                pygame.display.set_caption("Spaceship - main")
            else:
                self.button = True
            pygame.display.update()
            if stars > necessary-1:
                player = Player(9, 3, "sprites/spaceship3.png")
            else:
                player = Player(7, 3, "sprites/spaceship2.png")
            ufo = Ufo(-50, 0, 3, 50)
            all_sprites.add(ufo, player.laser, player)
            self.create_enemies(16, 5)
    def start_normal(self):
        global window
        global player
        global enemies
        global positions
        global ufo
        global plane
        global points
        global necessary
        plane = 10
        self.status = 3
        self.counter += 1
        enemies.clear()
        if self.counter > 1:
            all_sprites.empty()
            first_sprites.empty()
        if self.option_possible == True:
            if self.button == True:
                points = 0
                self.menu.destroy()
                window = pygame.display.set_mode((self.width, self.height))
                pygame.display.set_caption("Spaceship - main")
            else:
                self.button = True
            pygame.display.update()
            if stars > necessary-1:
                player = Player(9, 3, "sprites/spaceship3.png")
            else:
                player = Player(7, 3, "sprites/spaceship2.png")
            ufo = Ufo(-50, 0, 3, 50)
            all_sprites.add(ufo, player.laser, player)
            self.create_enemies(16, 5)
    def start_hard(self):
        global window
        global player
        global enemies
        global positions
        global ufo
        global plane
        global points
        global necessary
        plane = 10
        self.status = 3
        self.counter += 1
        enemies.clear()
        if self.counter > 1:
            all_sprites.empty()
            first_sprites.empty()
        if self.option_possible == True:
            if self.button == True:
                points = 0
                self.menu.destroy()
                window = pygame.display.set_mode((self.width, self.height))
                pygame.display.set_caption("Spaceship - main")
            else:
                self.button = True
            pygame.display.update()
            if stars > necessary-1:
                player = Player(7, 4, "sprites/spaceship3.png")
            else:
                player = Player(7, 3, "sprites/spaceship2.png")
            ufo = Ufo(-50, 0, 3, 50)
            all_sprites.add(ufo, player.laser, player)
            self.create_enemies(20, 5)
    def game_over(self):
        self.status = 4
        all_sprites.empty()
        first_sprites.empty()
    def on_closing(self):
        self.options.destroy()
        self.option_possible = True
    def easy(self):
        global dif
        dif = 1
        self.options.destroy()
        self.option_possible = True
    def normal(self):
        global dif
        dif = 2
        self.options.destroy()
        self.option_possible = True
    def hard(self):
        global dif
        dif = 3
        self.options.destroy()
        self.option_possible = True
    def difficulty(self):
        global dif
        global stars
        global necessary
        new_font = tkFont.Font(family='Comic Sans MS', size=10)
        if self.option_possible == True:
            self.option_possible = False
            self.options = Tk()
            self.options.geometry("300x350")
            self.options.resizable(0, 0)
            self.options.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.options.title("Spaceship - difficulty")
            self.options.update()
            self.canvas2 = Canvas(self.options, bg="black", width=310, height=350)
            self.canvas2.update()
            self.canvas2.place(x=-10, y=0)
            easy = Button(self.options, text="Easy", width=20, height=1, bg="black", fg="white",
                       activebackground="white", font=new_font, command=self.easy)
            normal = Button(self.options, text="Normal", width=20, height=1, bg="black", fg="white",
                            activebackground="white", font=new_font, command=self.normal)
            hard = Button(self.options, text="Hard", width=20, height=1, bg="black", fg="white",
                          activebackground="white", font=new_font, command=self.hard)
            stars_l = Label(self.options, bg = "black",fg="white", text="stars: "+str(stars)+"/"+str(necessary), font=new_font)
            self.options.update()
            easy.place(x=35, y=75)
            normal.place(x=35, y=150)
            hard.place(x=35, y=225)
            stars_l.place(x=95, y=290)
            self.options.mainloop()
    def manager(self):
        global dif
        if dif == 1:
            self.start_easy()
        if dif == 2:
            self.start_normal()
        if dif == 3:
            self.start_hard()
    def open_menu(self):
        if self.create_window == True:
            self.menu = Tk()
            self.menu.geometry("300x350")
            self.menu.resizable(0, 0)
            self.canvas = Canvas(self.menu, bg="black", width=310, height=350)
            self.enemy_img = PhotoImage(file='sprites/enemy.png')
            self.enemy_img = self.enemy_img.subsample(6, 6)
            self.canvas.create_image(159, 100, image=self.enemy_img)
            self.canvas.update()
            self.canvas.place(x=-10, y=0)
        else:
            self.canvas = Canvas(self.menu, bg="black", width=310, height=350)
            self.enemy_img = PhotoImage(file='sprites/enemy.PNG')
            self.enemy_img = self.enemy_img.subsample(6, 6)
            self.canvas.create_image(159, 100, image=self.enemy_img)
            self.canvas.update()
            self.canvas.place(x=-10, y=0)
        self.menu.title("Spaceship - menu")
        font = tkFont.Font(family='Comic Sans MS', size=10)
        start = Button(text="Start", width=25, height=2, command=self.manager, bg="black", fg="white",
                       activebackground="white", font=font)
        exit = Button(text="Quit", width=25, height=2, command=self.quit, bg="black", fg="white",
                      activebackground="white", font=font)
        settings = Button(text="Difficulty", width=25, height=2, command=self.difficulty, bg="black", fg="white",
                          activebackground="white", font=font)
        start.place(x=45, y=150)
        exit.place(x=45, y=225)
        settings.place(x=45, y=75)
        self.menu.update()
        self.menu.mainloop()
    def intro(self):
        self.menu = Tk()
        self.menu.geometry("300x350")
        self.menu.resizable(0, 0)
        self.menu.title("Spaceship - intro")
        self.canvas = Canvas(self.menu, bg="black", width=310, height=350)
        self.background = PhotoImage(file='sprites/logo.PNG')
        self.background = self.background.subsample(7, 7)
        self.star = PhotoImage(file='sprites/star_blue.PNG')
        self.star = self.star.subsample(6, 6)
        #self.canvas.create_image(160, 200, image=self.background)
        self.canvas.create_image(160, 170, image=self.star)
        self.canvas.place(x=-10, y=0)
        self.menu.update()
        self.canvas.update()
        t.sleep(0.7)
        self.canvas.delete("all")
        self.open_menu()
    def update(self):
        if self.status == 1:
            self.status = 2
            if self.counter < 1:
                self.intro()
            else:
                self.create_window = True
                self.open_menu()
game = Game(width, height)
if __name__ == "__main__":
    game.update()
timer_set = False
game_over_color = (255, 255, 255)
while True:
    if stop == True:
        window.blit(fontsurfobj2, (10, game.height/2))
    if game.status == 3:
        if stop == False:
            first_sprites.update()
            all_sprites.update()
        #pygame.draw.rect(window, (20, 25, 25), player.rect)
        #for enemy in enemies:
            #pygame.draw.rect(window, (255, 255, 255), enemy.rect)
        #pygame.draw.rect(window, (255, 255, 255), player.laser.rect)
        window.blit(player.fontsurfobj, (width-60, height-15))
        fontsurfobj5 = fontobj.render("LEVEL " + str(level), True, (255, 255, 255))
        window.blit(fontsurfobj5, (10, height-15))
        fontsurfobj7 = fontobj.render("lives: "+str(player.hearts), True, (255, 255, 255))
        window.blit(fontsurfobj7, (width-60, height-30))
        first_sprites.draw(window)
        all_sprites.draw(window)
        pygame.display.update()
        if stop == False:
            clock.tick(fps)
        time = pygame.time.get_ticks()
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == 32:
                    if stop == False:
                        if player.laser.instantiate == False:
                            if player.play == True:
                                laser_sound.set_volume(volume)
                                laser_sound.play()
                            player.laser.instantiate = True
                if event.key == 27:
                    if stop == False:
                        stop = True
                    else:
                        stop = False
                if event.key == 114:
                    level = 0
                    points = 0
                    game.button = False
                    game.manager()
            if event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    if stop == False:
                        if player.laser.instantiate == False:
                            if player.play == True:
                                laser_sound.set_volume(volume)
                                laser_sound.play()
                            player.laser.instantiate = True
                if event.button == 5:
                    level = 0
                    points = 0
                    game.button = False
                    game.manager()
                if event.button == 7:
                    stop = False
                    pygame.display.quit()
                    game.status = 1
                    game.update()
            if event.type == JOYHATMOTION:
                if event.value[0] == 0:
                    if event.value[1] == 0:
                        if player.joystick == True:
                            player.joystick = False
                if event.value[1] == 1:
                    player.joystick = True
                    player.joystick_d = "up"
                if event.value[1] == -1:
                    player.joystick = True
                    player.joystick_d = "down"
                if event.value[0] == 1:
                    player.joystick = True
                    player.joystick_d = "right"
                if event.value[0] == -1:
                    player.joystick = True
                    player.joystick_d = "left"
            if event.type == QUIT:
                stop = False
                pygame.display.quit()
                game.status = 1
                game.update()
    if game.status == 4:
        fontsurfobj3 = fontobj2.render("GAME OVER", True, game_over_color)
        fontsurfobj6 = fontobj2.render("LEVEL " + str(level), True, (255, 255, 255))
        if timer_set == False:
            timer_set = True
            game_over_timer = pygame.time.get_ticks()
        time = pygame.time.get_ticks()
        if time-game_over_timer > 1000:
            if game_over_color == (255, 255, 255):
                game_over_color = (0, 0, 0)
            elif game_over_color == (0, 0, 0):
                game_over_color = (255, 255, 255)
            timer_set = False
        pygame.display.update()
        window.fill((0, 0, 0))
        if game.button == True:
            window.blit(fontsurfobj3, (width/2-75, 200))
            window.blit(fontsurfobj6, (width/2-52, 300))
            window.blit(fontsurfobj4, (width/2-131, 400))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == 114:
                    level = 1
                    points = 0
                    game.button = False
                    window.fill((0, 0, 0))
                    game.manager()
            if event.type == MOUSEBUTTONDOWN:
                level = 1
                points = 0
                game.button = False
                window.fill((0, 0, 0))
                game.manager()
            if event.type == JOYBUTTONDOWN:
                if event.button == 5:
                    level = 0
                    points = 0
                    game.button = False
                    window.fill((0, 0, 0))
                    game.manager()
                if event.button == 7:
                    stop = False
                    pygame.display.quit()
                    game.status = 1
                    game.update()
            if event.type == QUIT:
                stop = False
                pygame.display.quit()
                game.status = 1
                game.update()
