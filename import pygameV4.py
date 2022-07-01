import pygame
import random
import os

pygame.init() #遊戲初始化
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("pygame-太空生存戰","sound","background.ogg"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

Screen_color=(0,0,0)
width=800
hight=600
RESOLUTION=(width,hight)
screen = pygame.display.set_mode(RESOLUTION) #設定遊戲視窗，解析度
clock = pygame.time.Clock() #設定時間
pygame.display.set_caption("太空生存戰") #標題

FPS=60
hard=1

score=0

#仔入字體
#font_name=pygame.font.match_font('arial')#去找字體
font_name = os.path.join("pygame-太空生存戰","font.ttf")

#仔入音樂
shoot_sound=pygame.mixer.Sound(os.path.join("pygame-太空生存戰","sound","shoot.wav"))
die_sound=pygame.mixer.Sound(os.path.join("pygame-太空生存戰","sound","rumble.ogg"))
expl_sounds= [
    pygame.mixer.Sound(os.path.join("pygame-太空生存戰","sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("pygame-太空生存戰","sound","expl1.wav"))
    ]
gun_sound=pygame.mixer.Sound(os.path.join("pygame-太空生存戰","sound","pow1.wav"))
shield_sound=pygame.mixer.Sound(os.path.join("pygame-太空生存戰","sound","pow0.wav"))
#仔入圖片

background_img=pygame.image.load(os.path.join("pygame-太空生存戰","img","background.png")).convert()
player_img=pygame.image.load(os.path.join("pygame-太空生存戰","img","player.png")).convert()
player_mini_img=pygame.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey((0,0,0))
pygame.display.set_icon(player_mini_img)
#rock_img=pygame.image.load(os.path.join("pygame-太空生存戰","img","rock.png")).convert()
bullet_img=pygame.image.load(os.path.join("pygame-太空生存戰","img","bullet.png")).convert()
rock_imgs =[]
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("pygame-太空生存戰","img", f"rock{i}.png")).convert())
expl_animate ={}
expl_animate["big"]=[]
expl_animate["small"]=[]
expl_animate["player"]=[]
for i in range(9):
    expl_img=pygame.image.load(os.path.join("pygame-太空生存戰","img",f"expl{i}.png")).convert()
    expl_img.set_colorkey((0,0,0))
    expl_animate["big"].append(pygame.transform.scale(expl_img,(75,75)))
    expl_animate["small"].append(pygame.transform.scale(expl_img,(30,30)))
    player_expl_img=pygame.image.load(os.path.join("pygame-太空生存戰","img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey((0,0,0))
    expl_animate["player"].append(player_expl_img)
item_img = {}
item_img["shield"]=pygame.image.load(os.path.join("pygame-太空生存戰","img","shield.png"))
item_img["gun"]=pygame.image.load(os.path.join("pygame-太空生存戰","img","gun.png"))
class player(pygame.sprite.Sprite): #描述玩家用pygame中的sprite
    def __init__(self):                      #設定一個基礎參數
        pygame.sprite.Sprite.__init__(self)  
        self.image=pygame.transform.scale(player_img, (50,38)) #pygame.Surface((50,60))   #一個平面圖行當作玩家
        #self.image.fill((0,80,200))             #圖形用什麼顏色填滿
        self.rect=self.image.get_rect()          #獲取圖形的位置
        self.image.set_colorkey((0,0,0))         #設定什麼顏色為透明
        self.health = 100
        self.radius =20
        #pygame.draw.circle(self.image,(225,0,0),self.rect.center, self.radius)
        self.rect.centerx=width/2                      #設定圖形的位置
        self.rect.centery=hight-100
        self.speedx = 8
        self.life = 3
        self.hidden = False
        self.fide_time = 0
        self.gun = 1
        self.guntime = 0

    def update(self):
        if self.gun > 1 and pygame.time.get_ticks()- self.guntime > 5000:
                    self.gun -= 1
                    self.guntime = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx=width/2                      #設定圖形的位置
            self.rect.centery=hight-100
        if not(self.hidden):
            key_pressed= pygame.key.get_pressed() #接收按鍵(布林值)
            if key_pressed[pygame.K_RIGHT]:       #按下按鍵後做什麼
                self.rect.x+=self.speedx
            if key_pressed[pygame.K_LEFT]:
                self.rect.x-=self.speedx
            if key_pressed[pygame.K_UP]:
                    self.rect.y-=self.speedx
            if key_pressed[pygame.K_DOWN]:
                self.rect.y+=self.speedx
            if self.rect.left<1:
                self.rect.left=0
            if self.rect.right>width:
                self.rect.right=width
            if self.rect.top<0:
                self.rect.top=0
            if self.rect.bottom>hight:
                self.rect.bottom=hight
        

    def shoot(self):
        if not(self.hidden):
            if self.gun ==1: 
                Bullet = bullet(self.rect.centerx,self.rect.top,0)
                all_sprites.add(Bullet)
                Bullets.add(Bullet)
                shoot_sound.play(0,0,1)
            elif self.gun >=2:
                Multibullet = []
                if self.gun > 6:
                    self.gun = 6
                for b in range(1,self.gun):
                    Bullet_right = bullet(self.rect.centerx+(20*b),self.rect.top,2*b)
                    Bullet_left = bullet(self.rect.centerx-(20*b),self.rect.top,-2*b)                    
                    Multibullet.append(Bullet_left)
                    Multibullet.append(Bullet_right)
                Bullet = bullet(self.rect.centerx,self.rect.top,0)
                all_sprites.add(Bullet)
                Bullets.add(Bullet)
                all_sprites.add(Multibullet)
                Bullets.add(Multibullet)
                #Bullet = bullet(self.rect.centerx+10,self.rect.top)
                #Bullet2 = bullet(self.rect.centerx-10,self.rect.top)
                #all_sprites.add(Bullet)
                #Bullets.add(Bullet)
                #all_sprites.add(Bullet2)
                #Bullets.add(Bullet2)
                shoot_sound.play(0,0,1)

    
    
    def hide(self):
        self. hidden = True
        self. hide_time = pygame.time.get_ticks()
        self.rect.center = (width/2,hight+200)

    def gun_up(self):
        self.gun += 1
        self.guntime = pygame.time.get_ticks()

class player_god(pygame.sprite.Sprite): #描述玩家用pygame中的sprite
    def __init__(self):                      #設定一個基礎參數
        pygame.sprite.Sprite.__init__(self)  
        self.image=pygame.Surface((50,60))   #一個平面圖行當作玩家
        self.image.fill((0,80,200))             #圖形用什麼顏色填滿
        self.rect=self.image.get_rect()      #獲取圖形的位置   
        self.rect.centerx=width/2                      #設定圖形的位置
        self.rect.centery=hight-100
        self.speedx = 8
    def update(self):                         #設定變化
        key_pressed= pygame.key.get_pressed() #接收按鍵(布林值)
        if key_pressed[pygame.K_RIGHT]:       #按下按鍵後做什麼
            self.rect.x+=self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x-=self.speedx
        if key_pressed[pygame.K_UP]:
                self.rect.y-=self.speedx
        if key_pressed[pygame.K_DOWN]:
            self.rect.y+=self.speedx
        if self.rect.left>width:
            self.rect.right=0
        if self.rect.right<0:
            self.rect.left=width
        if self.rect.top>hight:
            self.rect.bottom=0
        if self.rect.bottom<0:
            self.rect.top=hight

class Rock(pygame.sprite.Sprite): #描述玩家用pygame中的sprite
    def __init__(self):                      #設定一個基礎參數
        pygame.sprite.Sprite.__init__(self)  
        self.image_origin = random.choice(rock_imgs)   #一個平面圖行當作玩家
        self.image = self.image_origin.copy()
        self.image_origin.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()      #獲取圖形的位置   
        self.radius = int(self.rect.width*0.85/2)
        #pygame.draw.circle(self.image, (225,0,0),self.rect.center, self.radius)
        self.rect.centerx = random.randrange(0,width-self.rect.width)                      #設定圖形的位置
        self.rect.centery = random.randrange(-200,-self.rect.height)        
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        self.tol_degree = 0
        self.rot_degree = random.randrange(-3,3)
 
    def rotate(self):
        self.tol_degree+=self.rot_degree
        self.tol_degree= self.tol_degree%360
        self.image = pygame.transform.rotate(self.image_origin, self.tol_degree)
        Center = self.rect.center
        self.rect = self.image.get_rect() 
        self.rect.center = Center
        
             
    def update(self):                         #設定變化
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top>hight or self.rect.left>width or self.rect.right<0:
            self.rect.centerx= random.randrange(0,width-self.rect.width)                      #設定圖形的位置
            self.rect.centery= random.randrange(-200,-self.rect.height)
            self.speedy = random.randrange(2,10)
            self.speedx= random.randrange(-3,3)
            
class bullet(pygame.sprite.Sprite): #描述玩家用pygame中的sprite
    def __init__(self,x,y,angle):                      #設定一個基礎參數
        pygame.sprite.Sprite.__init__(self)  
        self.image=bullet_img  #一個平面圖行當作玩家
        self.image.set_colorkey((0,0,0))              #圖形用什麼顏色填滿
        self.rect=self.image.get_rect()      #獲取圖形的位置   
        self.rect.centerx=x                      #設定圖形的位置
        self.rect.centery=y
        self.angle = angle
        self.speedy = -10
    def update(self):                         #設定變化
        self.rect.centery+=self.speedy
        self.rect.centerx+=self.angle
        if self.rect.bottom < 0:
            self.kill()

class explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):                      #設定一個基礎參數
        pygame.sprite.Sprite.__init__(self)
        self.size=size  
        self.image=expl_animate[self.size][0]  #一個平面圖行當作玩家
        self.rect=self.image.get_rect()      #獲取圖形的位置   
        self.rect.center=center
        self.frame=0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50                      #設定圖形的位置
    def update(self):                         #設定變化
        now =pygame.time.get_ticks()
        if now-self.last_update > self.frame_rate:
            self.last_update= now
            self.frame += 1
            if self.frame == len(expl_animate[self.size]):
                self.kill()
            else:
                self.image = expl_animate[self.size][self.frame] 
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class item(pygame.sprite.Sprite):
    def __init__(self,center):                      #設定一個基礎參數
        pygame.sprite.Sprite.__init__(self)
        self.type= random.choice(["shield", "gun"])  
        self.image=item_img[self.type]  #一個平面圖行當作玩家
        self.image.set_colorkey(((0,0,0)))
        self.rect=self.image.get_rect()      #獲取圖形的位置   
        self.rect.center=center
        self.speedy = 3
    def update(self):                         #設定變化
        self.rect.y += self.speedy
        if self.rect.top > hight:
            self.kill()


all_sprites = pygame.sprite.Group()
Rocks = pygame.sprite.Group()
Bullets = pygame.sprite.Group()
all_player = pygame.sprite.Group()
Items = pygame.sprite.Group()

Player1 = player()

all_sprites.add(Player1)
all_player.add(Player1)

def draw_text(surf, text,size,x,y):
    font = pygame.font.Font(font_name, size)#做字體跟大小
    text_surface = font.render(text,True,(225,225,225))#字體大小.渲染(文字,是否抗拒尺,顏色)
    text_rect = text_surface.get_rect()
    text_rect.centerx=x
    text_rect.centery=y
    surf.blit(text_surface,text_rect)#平面.填滿(渲染好的字體，字體位置)
def new_rock():
    rock = Rock() 
    all_sprites.add(rock)
    Rocks.add(rock)
def draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    bar_length = 100
    bar_hight = 10
    fill = hp/100*bar_length
    outline_rect= pygame.Rect(x,y,bar_length,bar_hight)
    fill_rect = pygame.Rect(x,y,fill,bar_hight)
    pygame.draw.rect(surf,(0,225,0),fill_rect)
    pygame.draw.rect(surf,(225,225,225),outline_rect,2)
def draw_life(surf,live,img,x,y):
    for i in range(live):
        img_rect = img.get_rect()
        img_rect.x = x+30*i
        img_rect.y = y
        surf.blit(img,img_rect)
def draw_init():
    screen.blit(background_img, (0,0))
    draw_text(screen,"太空生存戰",64,width/2,hight/4)
    draw_text(screen,"← → ↑ ↓ 移動飛船",22,width/2,hight/2)
    draw_text(screen,"按任意鍵開始遊戲",22,width/2,hight*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False



for i in range(hard):
    new_rock()
    
    

running=True
show_init = True
while running: #遊戲迴圈
    if show_init:# 初始畫面
        exit = draw_init()
        if exit :
            break
        show_init = False
        hard=1
        score=0
        all_sprites = pygame.sprite.Group()
        Rocks = pygame.sprite.Group()
        Bullets = pygame.sprite.Group()
        all_player = pygame.sprite.Group()
        Items = pygame.sprite.Group()

        Player1 = player()

        all_sprites.add(Player1)
        all_player.add(Player1)
        
        for i in range(hard):
            new_rock()

    clock.tick(FPS)
    #取得數據
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Player1.shoot()

    #更新遊戲
    all_sprites.update()
    Player1 = player_god()

    all_sprites.add(Player1)
    all_player.add(Player1)
     

    HIT=pygame.sprite.groupcollide(Rocks,Bullets,True,True)#groupcollide碰撞:要兩個都是sprite group
    for hit in HIT:
        expl=explosion(hit.rect.center,"big")
        score += hit.radius
        score_f = 0
        new_rock()
        if score-score_f > 500:
            new_rock()
            score_f = score
        all_sprites.add(expl)
        if random.random() > 0.9:
            Item = item(hit.rect.center)
            all_sprites.add(Item)
            Items.add(Item)
 
        random.choice(expl_sounds).play()
    HIT=pygame.sprite.spritecollide(Player1,Rocks,True, pygame.sprite.collide_circle)#spritecollide碰撞: 指操控一個sprite而不是群組
    for hit in HIT:
        expl=explosion(hit.rect.center,"small")
        all_sprites.add(expl)
        Player1.health -= hit.radius
        new_rock()
        if Player1.health<=0:
            die= explosion(Player1.rect.center, "player")
            die_sound.play()
            Player1.gun = 1
            all_sprites.add(die)
            Player1.life-=1
            Player1.health=100
            Player1.hide()
    if Player1.life == 0 and not(die.alive()):
        show_init = True
    HIT=pygame.sprite.spritecollide(Player1,Items,True)#spritecollide碰撞: 指操控一個sprite而不是群組   
    for hit in HIT:
        if hit.type == "shield":
            shield_sound.play()
            Player1.health += 20
            if Player1.health >100:
                Player1.health = 100
        
        if hit.type == "gun":
            Player1.gun_up()
            gun_sound.play()
            new_rock()
        
    
    #畫面顯示
    screen.fill(Screen_color)
    
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_text(screen,"Score: "+ str(score),18,width/2,10)
    draw_health(screen,Player1.health,10,5)
    draw_life(screen,Player1.life, player_mini_img, width-100,15)

    pygame.display.update()
pygame.quit() 