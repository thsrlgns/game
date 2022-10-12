import pygame
import os 
import math





class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(default_offset_x_claw,0)
        self.position = position

        self.direction= LEFT
        self.angle_speed= 10
        self.angle = 30
     

    def update(self, to_x):
        if self.direction == LEFT:
            self.angle+=self.angle_speed 
        elif self.direction == RIGHT:
            self. angle-=self.angle_speed

        
        if self.angle>170:
            self.angle=170
            self.set_direction(RIGHT)
        elif self.angle< 10:
            self.angle=10
            self.set_direction(LEFT)
        
        self.offset.x+=to_x
        self.rotate()


    def rotate(self):
        self.image=pygame.transform.rotozoom(self.original_image, -self.angle, 1) 
        offset_rotated= self.offset.rotate(self.angle)
        self.rect= self.image.get_rect(center=self.position+offset_rotated)


    def set_direction(self,direction):
        self.direction=direction
 
    def draw(self,screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, YELLOW, self.position,3)
        pygame.draw.line(screen, YELLOW, self.position, self.rect.center,10)
    
    def set_init_state(self):
        self.offset.x=default_offset_x_claw
        self.angle=10
        self.direction=LEFT


class Coin(pygame.sprite.Sprite):
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.price= price
        self.speed= speed
    
    def set_position(self, position, angle):
        r=self.rect.size[0]//2
        rad_angle= math.radians(angle)
        to_x= r*math.cos(rad_angle)
        to_y= r*math.sin(rad_angle)

        self.rect.center=(position[0]+to_x, position[1]+to_y)



def setup_coin():
    btc_price, btc_speed= 10,40
    eth_price, eth_speed= 10,40
    ada_price, ada_speed= 10,40
    eos_price, eos_speed= 10,40
    sos_price, sos_speed= 10,40



    btc=Coin(coin_images[0],(100,380), btc_price, btc_speed)
    coin_group.add(btc)

    eth=Coin(coin_images[1],(300,500), eth_price, eth_speed)
    coin_group.add(eth)
    
    ada=Coin(coin_images[2],(400,380), ada_price, ada_speed)
    coin_group.add(ada)

    eos=Coin(coin_images[3],(900,420), eos_price, eos_speed)
    coin_group.add(eos)

    sos=Coin(coin_images[4],(1100,100), sos_price, sos_speed)
    coin_group.add(sos)

        

def update_score(score):
    global curr_score
    curr_score+=score 

def display_score():
    txt_curr_score=game_font.render(f"Curr score : {curr_score:,}",True, YELLOW )
    screen.blit(txt_curr_score,(50,20))


    txt_goal_score= game_font.render(f"Goal Score: {goal_score:,}",True, YELLOW)
    screen.blit(txt_goal_score,(50,80))


def display_time(time):
    txt_timer=game_font.render(f"Time: {time}", True, YELLOW)
    screen.blit(txt_timer,(1100,50))

def display_game_over():
    game_font=pygame.font.SysFont("arialrounded",60)
    txt_game_over = game_font.render(game_result, True, YELLOW)
    rect_game_over=txt_game_over.get_rect(center=(int(screen_width/2), int(screen_height/2)))
    screen.blit(txt_game_over, rect_game_over)
            
pygame.init()
screen_width=1280
screen_height=720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("블츠 그랩 연습게임")

clock = pygame.time.Clock()
game_font= pygame.font.SysFont("arialrounded",30)

goal_score=50
curr_score=0 
 
game_result= None
total_time=10
start_ticks= pygame.time.get_ticks()

default_offset_x_claw=40
to_x=0 
caught_coin = None


move_speed=40
return_speed=40
LEFT= -10
STOP=0
RIGHT=10

RED= (255,0,0)
YELLOW= (255,255,0)




current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "제목 없음.png"))

coin_images = [ 
    pygame.image.load(os.path.join(current_path, "볼리베어.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "아리.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "그레이브즈.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "애쉬.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "알리스타.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "블리츠.png")).convert_alpha()]

coin_group= pygame.sprite.Group()
setup_coin()

claw_image=pygame.image.load(os.path.join(current_path, "블츠.png"))
claw=Claw(claw_image, (screen_width//2, 110))

running = True 
while running: 
    clock.tick(30)

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running = False

        if event.type==pygame.MOUSEBUTTONDOWN:
            claw.set_direction(STOP)
            to_x=move_speed

    if claw.rect.left<0 or claw.rect.right>screen_width or claw.rect.bottom>screen_height:
        to_x=-return_speed
    if claw.offset.x < default_offset_x_claw:
        to_x=0
        claw.set_init_state()

        if caught_coin:
            update_score(caught_coin.price)
            coin_group.remove(caught_coin)
            caught_coin=None


    if not caught_coin:
        for coin in coin_group:
            # if claw.rect.colliderect(coin.rect):
            if pygame.sprite.collide_mask(claw,coin):
                caught_coin= coin  
                to_x=-coin.speed
                break 


    if caught_coin:
        caught_coin.set_position(claw.rect.center, claw.angle)
 
    screen.blit(background, (0,0))



    coin_group.draw(screen)
    claw.update(to_x)
    claw.draw(screen)

    display_score()
    elapsed_time=(pygame.time.get_ticks()-start_ticks)/1000
    display_time(total_time-int(elapsed_time))


    if total_time- int(elapsed_time)<=0:
        running=False
        if curr_score >=goal_score:
            game_result= "Mission Complete"
        else:
            game_result= "Game over"

        display_game_over() 

    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()
