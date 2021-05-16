

from pygame import *
from random import randint

font.init()
font1 = font.SysFont("Arial Black", 30)
font2 = font.SysFont("Arial Black", 30)
win = font1.render("Выиграл!", True, (87, 80, 80))
lose = font1.render("Ты проиграл!", True, (87, 80, 80))
 
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
lost = 0
img_back = "galaxy.jpg" 
img_hero = "rocket.png"
 

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
 
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
   def update(self):
    keys = key.get_pressed()
    if keys[K_LEFT] and self.rect.x > 5:
        self.rect.x -= self.speed
    if keys[K_RIGHT] and self.rect.x < win_width - 80:
        self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


win_width = 700

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("asteroid.png", randint(80, win_width - 80), 40, 80, 50, randint(1, 5))
    monsters.add(monster)


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
score = 0
ship = Player(img_hero, 5, win_height - 100, 90, 130, 10)
monster = Enemy("asteroid.png", 80, win_width - 80, 40, 80, 50)
finish = False
run = True

while run:
   for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
            if e.key == K_SPACE:
            #fire_sound.play()
                ship.fire()
 

   if not finish:
       window.blit(background,(0,0))
       ship.update()
       ship.reset()
       monsters.update()
       monsters.draw(window)
       collides = sprite.spritecollide(ship, monsters, True) 
       for c in collides:
           score = score + 1
           monster = Enemy("asteroid.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
       text = font2.render("Счет: " + str(score), 1, (0, 0, 0))
       window.blit(text, (10, 20))
       text_lose = font2.render("пропущено: " + str(lost), 1, (0, 0, 0))
       window.blit(text_lose, (10, 50))
       if score >= 5:
                finish = True
                draw.rect(window, (224, 224, 224), (210, 200, win_width-400, win_height-450))
                window.blit(win, (win_width/2-75, win_height/2-40))
       if lost >= 10:
                finish = True
                draw.rect(window, (224, 224, 224), (210, 200, win_width-400, win_height-450))
                window.blit(lose, (win_width/2-100, win_height/2-40))
       display.update()

       
   time.delay(50)