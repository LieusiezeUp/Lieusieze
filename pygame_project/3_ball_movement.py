import random
import os
import pygame
##############################################

# 기본 초기화(반드시 해야 하는 것들)

pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정 합니다
screen_width = 640 # 가로
screen_height = 480 # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("공튀기기") # 게임이름

#FPS 불러와서 변수로 지정
clock = pygame.time.Clock()

##############################################

# 1. 사용자 게임 초기화(배경화면, 게임 이미지, 좌표, 속도, 폰트등)

current_path = os.path.dirname(__file__) # 현재 파일의 위치를 반환함
image_path = os.path.join(current_path, "image") # image 폴더 위치 반환


# 1-1. 배경 이미지 불러오기 입니다
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 1-2. 스테이지 이미지 불러오기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 두기 위해 사용


# 1-3. 캐릭터 이미지 불러오기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size # 사각형이미지의 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로 position의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height - stage_height # 화면 세로 크기 가장 아래에 해당하는 곳에 위치
# 캐릭터 이동할 좌표
character_to_x = 0
character_speed = 2

# 1-4. 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
# 무기는 한 번에 여러 발 발사 가능
weapons = []
# 무기 이동 속도
weapon_speed = 10


# 1-5. 공 만들기(4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]
# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]
# 공들
balls = []
# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50, # 공의 x 좌표
    "pos_y" : 50, # 공의 y 좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x" : 3, # x축 이동방향, -3이면 왼쫏으로 , 3이면 오른쪽으로
    "to_y" : -6, # y축 이동방향
    "init_spe_y": ball_speed_y[0] # y 최초 속도
})


# 폰트 정의
game_font = pygame.font.Font(None, 40) # game_font 변수만들고 디폴트폰트에 크기 40

# 총 시간
total_time = 100

# 시작 시간
start_ticks = pygame.time.get_ticks() # 현재 tick을 받아옴

# 이벤트 루프
#파이썬에서는 이벤트 루프를 켜놔야 창이 안꺼진다
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # 변수 delta의 게임화면의 초당 프레임 수를 설정
    
    print(" fps : " + str(clock.get_fps()))
    
    # 2. 이벤트 처리(키보드, 마우스등)
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창의 X버튼을 누르면 이 이벤트가 발생
            running = False # 게임이 진행중이 아님
            
        if event.type == pygame.KEYDOWN: # 만약 키보드를 눌렀을 때
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
                
        if event.type == pygame.KEYUP: # 방향키를 떼일 때
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
                
    # 3. 게임 캐릭터 위치 정의            
    character_x_pos += character_to_x
    # 캐릭터 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width           
    # 캐릭터 세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height  
    
    # 3-1. 무기 위치 정의
    # ex) 100, 200 -> 180, 160, 140, .... 이런식으로 변함
    # ex) 500, 200 -> 180, 160, 140, .... 이런식으로 변함
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] 
    # weapons 에 있는 위치 값을 w라고 두고 w안에서 처리하고 weapons에 다시 집어 넣음
    # 그런다음 천장에 무기가 닿으면 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
    
    
    
    # 3-2. 공 위치 정의            
    for ball_idx, ball_val in enumerate(balls):
    # enumerate해서 balls리스트를 각각 하나하나씩 꺼내온다      
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        # 가로벽에 닿았을 때 공 튕기내기
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1
        # 세로 위치
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spe_y"] # 스테이지에 닿을 때 y최초속도로 튕겨 올라온다는 소리
        else:
            ball_val["to_y"] += 0.4 # 그 외는 상황일때는 0.5씩 줄어듬
        
        ball_val["pos_x"] += ball_val["to_x"] # 공 x방향 이동하기
        ball_val["pos_y"] += ball_val["to_y"] # 공 y방향 이동하기
        
    # 4. 충돌 처리
    # 충돌 처리를 위한 rect 정보 업데이트
    
        
    # 5. 화면에 그리기        
    screen.blit(background, (0, 0)) # 백그라운드 배경 그린다 그런다음 위치 지정함
    
    for weapon_x_pos, weapon_y_pos in weapons: # 무기 그린다 그런다음 위치지정
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos)) 
    
    for idx, val in enumerate(balls): # 공 그리고 위치지정
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    
    screen.blit(stage, (0, screen_height - stage_height))
    
    screen.blit(character, (character_x_pos, character_y_pos)) # 캐릭터 그린다 그런다음 위치 지정함
    
    

    pygame.display.update() # 파이썬은 디스플레이에 매번 업데이트 해줘야 한다(게임 화면을 다시 그리기)

# 잠시 대기
pygame.time.delay(500) # 0.5초대기

# pygame 종료
pygame.quit()