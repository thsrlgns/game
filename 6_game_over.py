#모든공을 없애거나 
#캐릭터가 공에 닿으면 
#시간제한 

import random
import os
from turtle import Screen
import pygame
pygame.init() 
import os
import sys
import math
from tkinter import* 



 
default_offset_x_claw=40

angle_speed= 5
angle = 30
offset = pygame.math.Vector2(default_offset_x_claw,0)
goal_score=1500
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
BLACK= (0,0,0)



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



screen_width=1500
screen_height=750
screen=pygame.display.set_mode((screen_width,screen_height))




pygame.display.set_caption("핑크빈 잡기")
clock=pygame.time.Clock()

current_path=os.path.dirname(__file__) #파일의 위치 반환
image_path=os.path.join(current_path, "images") #images 폴더 위치 반환
background=pygame.image.load(os.path.join(image_path,"C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/핑크빈 배경.png"))

current_path=os.path.dirname(__file__) #파일의 위치 반환
image_path=os.path.join(current_path, "images") #images 폴더 위치 반환
stage=pygame.image.load(os.path.join(image_path,"C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/스테이지.png"))
stage_size=stage.get_rect().size 
stage_height=stage_size[1]  #스테이지의 높이 위에 캐릭터를 두기위해서 0=가로1=세로
#위치 지정해주기 세로 위치로 넣어야 좌표되니깐 ㅇㅇ 아니면 화면밖으로 나감


character = pygame.image.load(os.path.join(image_path,"C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/메이플캐릭터.png")).convert_alpha()
character_size = character.get_rect().size #이미지의 크기를 구해옴 
character_width = character_size[0] #캐릭터의 가로 위치
character_height = character_size[1] #캐릭터의 세로 위치
character_x_pos = (screen_width/2)-(character_width/2) #가로 위치
character_y_pos = screen_height-character_height-stage_height #세로 위치


character_to_x=0
character_to_y=0
character_speed=10

enemy = pygame.image.load("C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/이펙트2.png").convert_alpha()
enemy_size = enemy.get_rect().size #이미지의 크기를 구해옴 
enemy_width = enemy_size[0] #캐릭터의 가로 위치
enemy_height = enemy_size[1] #캐릭터의 세로 위치
enemy_x_pos = random.randint(0,1500)
enemy_y_pos = 0 #세로 위치
enemy_speed = 8

enemy1 = pygame.image.load("C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/이펙트.png").convert_alpha()
enemy1_size = enemy1.get_rect().size #이미지의 크기를 구해옴 
enemy1_width = enemy1_size[0] #캐릭터의 가로 위치
enemy1_height = enemy1_size[1] #캐릭터의 세로 위치
enemy1_x_pos = random.randint(0,1500)
enemy1_y_pos = 0 #세로 위치
enemy1_speed = 12


enemy2 = pygame.image.load("C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/이펙트2.png").convert_alpha()
enemy2_size = enemy2.get_rect().size #이미지의 크기를 구해옴 
enemy2_width = enemy2_size[0] #캐릭터의 가로 위치
enemy2_height = enemy2_size[1] #캐릭터의 세로 위치
enemy2_x_pos = random.randint(0,460)
enemy2_y_pos = 0 #세로 위치
enemy2_speed = 10

enemy3 = pygame.image.load("C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/이펙트.png").convert_alpha()
enemy3_size = enemy3.get_rect().size #이미지의 크기를 구해옴 
enemy3_width = enemy3_size[0] #캐릭터의 가로 위치
enemy3_height = enemy3_size[1] #캐릭터의 세로 위치
enemy3_x_pos = random.randint(0,1500)
enemy3_y_pos = 0 #세로 위치
enemy3_speed = 11




weapon = pygame.image.load(os.path.join(image_path,"C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/무기.png")).convert_alpha()
weapon_size = weapon.get_rect().size #이미지의 크기를 구해옴 
weapon_width = weapon_size[0] #캐릭터의 가로 위치

weapons=[]
weapon_speed=10

ball_images=[
    pygame.image.load(os.path.join(image_path,"C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/핑크빈.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path,"C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/핑크빈2.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path,"C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/공3.jpg")).convert_alpha(),
    pygame.image.load(os.path.join(image_path,"C:/Users/gary0/OneDrive/바탕 화면/python work space/새 폴더/공4.jpg"))]

ball_speed_y=[-23,-20,-16,-14]   #공 1234 속도  0123

balls=[] 
#공의 x,y 좌표 , 이미지 인덱스, 이동방향, 공의 최초속도 
balls.append({
    "pos_x":50,
    "pos_y":50,
    "img_idx":0,
    "to_x":3,
    "to_y":-6,
    "init_spe_y":ball_speed_y[0]})

#사라질 무기, 공 정보 저장 변수 
weapon_to_remove= -1
ball_to_remove= -1
game_font=pygame.font.Font(None,40)
total_time=100
start_ticks=pygame.time.get_ticks()
game_result="Game Over"
ball_hp=10

running=True 
while running:
    dt=clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False


        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                character_to_x-= character_speed
            elif event.key==pygame.K_RIGHT:
                character_to_x+= character_speed
            elif event.key==pygame.K_UP:
                character_to_y-= character_speed
            elif event.key==pygame.K_DOWN:
                character_to_y+= character_speed
            elif event.key==pygame.K_SPACE:
                weapon_x_pos = character_x_pos+(character_width/2)-(weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos]) #계속 쏠수있음
                
            elif event.type==pygame.K_KP0:
                weapon_x_pos = character_x_pos+(character_width/2)-(weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos]) 



    if event.type==pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            character_to_x=0
        if event.key == pygame.K_UP:
            character_to_y=0
        if event.key == pygame.K_DOWN:
            character_to_y=0



    character_x_pos+=character_to_x
    character_y_pos+=character_to_y

    enemy_y_pos+= enemy_speed
    if enemy_y_pos> screen_height-enemy_height:
        enemy_y_pos = 0 
        enemy_x_pos = random.randint(0,1500)

    enemy1_y_pos+= enemy1_speed
    if enemy1_y_pos> screen_height-enemy1_height:
        enemy1_y_pos = 0 
        enemy1_x_pos = random.randint(0,1500)

    enemy2_y_pos+= enemy2_speed
    if enemy2_y_pos> screen_height-enemy2_height:
        enemy2_y_pos = 0 
        enemy2_x_pos = random.randint(0,1500)    

    enemy3_y_pos+= enemy3_speed
    if enemy3_y_pos> screen_height-enemy3_height:
        enemy3_y_pos = 0 
        enemy3_x_pos = random.randint(0,1500)    
  


    enemy_rect=enemy.get_rect()
    enemy_rect.left=enemy_x_pos
    enemy_rect.top=enemy_y_pos    

    enemy1_rect=enemy.get_rect()
    enemy1_rect.left=enemy1_x_pos
    enemy1_rect.top=enemy1_y_pos    

    enemy2_rect=enemy.get_rect()
    enemy2_rect.left=enemy2_x_pos
    enemy2_rect.top=enemy2_y_pos    

    enemy3_rect=enemy.get_rect()
    enemy3_rect.left=enemy3_x_pos
    enemy3_rect.top=enemy3_y_pos    
   


#무기 위로올라감 
    weapons=[ [w[0],w[1]-weapon_speed] for w in weapons]
    weapons=[ [w[0],w[1]] for w in weapons if w[1] > 0]
#공 위치,몇번째 있는지+순환하면서 

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]

        ball_size=ball_images[ball_img_idx].get_rect().size
        ball_width =ball_size[0]
        ball_height =ball_size[1]

        if ball_pos_x<0 or ball_pos_x > (screen_width- ball_width): 
            ball_val["to_x"]=ball_val["to_x"]*-1

    # 4. 충돌 처리
        if ball_pos_y >= screen_height-stage_height-ball_height:
            ball_val["to_y"] = ball_val["init_spe_y"]
        else:
            ball_val["to_y"]+=0.5 #포물선 위해서 초기속도에서 점점 줄여나감   
        
        ball_val["pos_x"]+=ball_val["to_x"]
        ball_val["pos_y"]+=ball_val["to_y"]

    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos 

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]
        #공 rect 정보 업데이트 

        ball_rect=ball_images[ball_img_idx].get_rect()
        ball_rect.left= ball_pos_x
        ball_rect.top= ball_pos_y 

        #공 과 캐릭터의 충돌처리 
        if character_rect.colliderect(ball_rect):
            running = False
        if character_rect.colliderect(enemy_rect):
            running = False

            break 
        # 공과 무기들 충돌처리 
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x=weapon_val[0]
            weapon_pos_y=weapon_val[1]
    
            weapon_rect=weapon.get_rect()
            weapon_rect.left=weapon_pos_x
            weapon_rect.top=weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx #해당무기 없애기 위한 값 설정
                ball_to_remove = ball_idx
                ball_idx-=ball_hp
                
                

                if ball_img_idx<1:
                    ball_hp-=1
                    ball_width=ball_rect.size[0]
                    ball_height=ball_rect.size[1]
                    small_ball_rect=ball_images[ball_img_idx+1].get_rect()
                    small_ball_width=small_ball_rect.size[0]
                    small_ball_height=small_ball_rect.size[1]
                

                    #왼쪽으로 튕겨나가는 작은 공 
                    balls.append({
                        "pos_x":ball_pos_x+(ball_width/2)-(small_ball_width/2),
                        "pos_y":ball_pos_y+(ball_height/2)-(small_ball_height/2),
                        "img_idx":ball_img_idx+1,
                        "to_x":-3,
                        "to_y":-6,
                        "init_spe_y":ball_speed_y[ball_img_idx+1]})
                   
                    balls.append({
                        "pos_x":ball_pos_x+(ball_width/2)-(small_ball_width/2),
                        "pos_y":ball_pos_y+(ball_height/2)-(small_ball_height/2),
                        "img_idx":ball_img_idx+1,
                        "to_x":3,
                        "to_y":-6,
                        "init_spe_y":ball_speed_y[ball_img_idx+1]})
                   

                    break 



# 다시하자 

    if weapon_to_remove >-1:
        del weapons[weapon_to_remove]
        weapon_to_remove=-1
    if ball_hp==0:
        del balls[ball_to_remove]
        game_result="Clear"
        running= False



    screen.blit(background,(0,0))
    for weapon_X_pos, weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))



    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))
    screen.blit(enemy, (enemy_x_pos,enemy_y_pos)) 
    screen.blit(enemy1, (enemy1_x_pos,enemy1_y_pos)) 
    screen.blit(enemy2, (enemy2_x_pos,enemy2_y_pos))
    screen.blit(enemy3, (enemy3_x_pos,enemy3_y_pos))



    elasped_time=(pygame.time.get_ticks()-start_ticks)/1000
    timer=game_font.render("Time:{}".format(int(total_time- elasped_time)),True,(255,255,255))
    screen.blit(timer,(10,10))    
    if total_time-elasped_time<0:
        game_result="Time Over"
        running=False
    pygame.display.update()

msg= game_font.render(game_result,True,(255,255,0))
msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
screen.blit(msg,msg_rect)



pygame.display.update()


pygame.time.delay(2000)
pygame.quit()




















