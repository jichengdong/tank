import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0) 
YELLOW = (255,255,0) 
BLACK = (0,0,0)
# 最新版 2023 10 19号 

# 游戏初始化
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('飞机大战')
clock = pygame.time.Clock()
backgroud_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img =  pygame.image.load( os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img,(25,20))
player_mini_img.set_colorkey(BLACK)  
rock_ing = pygame.image.load(os.path.join("img", "rock.png")).convert()
    
bullet_img = pygame.image.load( os.path.join("img","bullet.png")).convert()
rock_images = []
for i in range(7):
    rock_images.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()       
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img,(30,30)))
    player_expl_img = pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert() 
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
    
power_imgs = {} 
power_imgs['shield'] = pygame.image.load( os.path.join("img","shield.png")).convert()
power_imgs['gun'] = pygame.image.load( os.path.join("img","gun.png")).convert()

   
   
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
expl_souds = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]
die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))

pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.2)

font_name = pygame.font.match_font('arial')

def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)
    
def draw_health(surf,hp,x,y):
    if hp<0:
        hp=0
    BAR_LENGIH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGIH
    outline_rect = pygame.Rect(x,y,BAR_LENGIH,BAR_HEIGHT)    
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2) 
    
def draw_lives(surf,lives,img,x,y):
    for i in range(lives):  
        img_rect = img.get_rect()
        img_rect.x = x+30*i
        img_rect.y = y
        surf.blit(img,img_rect)
        
def new_rock():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)      

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,40))
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.radius = 23
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        
        self.rect.centerx = WIDTH/2.2
        self.rect.bottom =  HEIGHT - 10
         
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx 
            
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx 
        
        
        if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                
        if self.rect.left  < 0:
                self.rect.left = 0
        
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:      
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom =  HEIGHT - 20    
                
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)  
        shoot_sound.play()
        
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+500)
                
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speedy = -10
       
        
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
                       
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = random.choice(rock_images)
            
        self.image_origin.set_colorkey(BLACK)
        self.image = self.image_origin.copy()
        
        self.rect = self.image.get_rect()
        self.radius = self.rect.width/2
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-80)
        
        #self.speedy = random.randrange(2,10)
        self.speedy = 1
        self.speedx = random.randrange(-3,3)
        
        self.rot_degree = random.randrange(-3,3)
        self.total_degree = 0
        
    def rotate(self):  
        self.total_degree = self.total_degree + self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_origin,self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0: 
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y =random.randrange(-100,-40)
        
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)
 
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        
        
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
       
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.frame = self.frame + 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
                              
class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
            
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
                              
all_sprites = pygame.sprite.Group() 
rocks = pygame.sprite.Group() 
bullets = pygame.sprite.Group() 
player = Player() #实体化类
all_sprites.add(player)
score = 0
pygame.mixer.music.play(-1)
for i in range(8):
    new_rock()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE:   
                 player.shoot()
        #更新游戏    
        all_sprites.update()
        
        hits_rockandbullets =  pygame.sprite.groupcollide(rocks,bullets,True,True)
        for hit in  hits_rockandbullets:
            random.choice(expl_souds).play()
            expl = Explosion(hit.rect.center,'lg')
            all_sprites.add(expl)
            r = Rock()
            all_sprites.add(r)
            rocks.add(r)
            score = score + int(hit.radius)

            
            
        hits_playerandrock = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)
        for hit in hits_playerandrock:
            player.health = player.health - hit.radius
            new_rock()
            
            expl = Explosion(hit.rect.center,'sm')
            all_sprites.add(expl)
            if player.health<=0:
                death_expl = Explosion(player.rect.center,'player')
                all_sprites.add(death_expl)
                die_sound.play()
                player.lives = player.lives - 1
                player.health = 100
                player.hide()
            if player.lives == 0:     
                running = False
            
        #显示画面
        screen.fill(BLACK)
        screen.blit(backgroud_img,(0,0))
        all_sprites.draw(screen)
        draw_text(screen,str(score),18,WIDTH/2,0)
        draw_health(screen,player.health,10,30)
        draw_lives(screen,player.lives,player_mini_img,WIDTH-100,15)
        pygame.display.update()
pygame.quit()
# def ()new_rock:new_rock()def new_rock():
  #  def :def new_rock():  rock = Rock()
    