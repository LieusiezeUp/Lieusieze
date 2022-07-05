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


# 배경 이미지 불러오기 입니다
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 이미지 불러오기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 두기 위해 사용


# 캐릭터 이미지 불러오기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size # 사각형이미지의 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로 position의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height - stage_height # 화면 세로 크기 가장 아래에 해당하는 곳에 위치
# 캐릭터 이동할 좌표
character_to_x = 0
character_speed = 2

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
# 무기는 한 번에 여러 발 발사 가능
weapons = []
# 무기 이동 속도
weapon_speed = 10


# 적 캐릭터 만들기
enemy = pygame.image.load(os.path.join(image_path, "ballon1.png"))
enemy_size = enemy.get_rect().size # 사각형이미지의 크기를 구해옴
enemy_width = enemy_size[0] # 캐릭터의 가로 크기
enemy_height = enemy_size[1] # 캐릭터의 세로 크기
enemy_x_pos = random.randint(0, screen_width - enemy_width)
enemy_y_pos = 0 
enemy_speed = 0.5


# 폰트 정의
game_font = pygame.font.Font(None, 40) # game_font 변수만들고 디폴트폰트에 크기 40

# 총 시간
total_time = 10

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
    character_x_pos += character_to_x * dt
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
    
    
    
    # 3-2. 적 위치 정의            
    enemy_y_pos += enemy_speed * dt
       
    # 세로 경계값 처리
    if enemy_y_pos > screen_height:
          enemy_y_pos = 0
          enemy_x_pos = random.randint(0, screen_width - enemy_width)
          
        
        
    # 4. 충돌 처리
    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos
        
    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌했어요")
        running = False
        
    # 5. 화면에 그리기        
    screen.blit(background, (0, 0)) # 백그라운드 배경 그린다 그런다음 위치 지정함
    
    for weapon_x_pos, weapon_y_pos in weapons: # 무기 그린다 그런다음 위치지정
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos)) 
    
    screen.blit(stage, (0, screen_height - stage_height))
    
    screen.blit(character, (character_x_pos, character_y_pos)) # 캐릭터 그린다 그런다음 위치 지정함
    
    
    
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos)) # 적 그린다 그런다음 위치 지정함
    
    # 타이머 집어 넣기
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    # 경과 시간을 1000으로 나누어 (ms)을 (s)단위로 표시
    
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
    # 출력할 글자,True, 글자 색상
    screen.blit(timer, (10, 10))
    
    # 만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        print("Game Over")
        running = False
    
    
    pygame.display.update() # 파이썬은 디스플레이에 매번 업데이트 해줘야 한다(게임 화면을 다시 그리기)

# 잠시 대기
pygame.time.delay(500) # 0.5초대기

# pygame 종료
pygame.quit()