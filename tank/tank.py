import pygame

FPS = 60
WIDTH = 500
HEIGHT = 600
WHITE = (255,255,255)
GREEN = (0,255,0)

# 游戏初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('飞机大战')
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom =  HEIGHT - 10
        self.speedx = 8
    
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx 
            
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx 
        
        
        if self.rect.left > WIDTH:
                self.rect.x = 0
        
 
all_sprites = pygame.sprite.Group()      
player = Player() #实体化类
all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #更新游戏    
        all_sprites.update()
        #显示画面
        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.update()
pygame.quit()