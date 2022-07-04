import pygame

pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정 합니다
screen_width = 480 # 가로
screen_height = 640 # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game") # 게임이름

#FPS 블러와서 변수로 지정
clock = pygame.time.Clock()


# 배경 이미지 불러오기 입니다
background = pygame.image.load("C:/Users/Kim Family/Desktop/Python_ex/pygame_basic/background.png")

# 스프라이트 불러오기
character = pygame.image.load("C:/Users/Kim Family/Desktop/Python_ex/pygame_basic/Rion.jpg")
character_size = character.get_rect().size # 사각형이미지의 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로 position의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height # 화면 세로 크기 가장 아래에 해당하는 곳에 위치

# 이동할 좌표
to_x = 0
to_y = 0

# 이동 속도
character_speed = 2

# 적 캐릭터 만들기
enemy = pygame.image.load("C:/Users/Kim Family/Desktop/Python_ex/pygame_basic/enemy.jpg")
enemy_size = enemy.get_rect().size # 사각형이미지의 크기를 구해옴
enemy_width = enemy_size[0] # 캐릭터의 가로 크기
enemy_height = enemy_size[1] # 캐릭터의 세로 크기
enemy_x_pos = (screen_width / 2) - (enemy_width / 2) # 화면 가로 position의 절반 크기에 해당하는 곳에 위치
enemy_y_pos = (screen_height / 2) - (enemy_height / 2) # 화면 세로 크기 가장 아래에 해당하는 곳에 위치


# 이벤트 루프
#파이썬에서는 이벤트 루프를 켜놔야 창이 안꺼진다
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # 변수 delta의 게임화면의 초당 프레임 수를 설정
    
    print(" fps : " + str(clock.get_fps()))
    
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창의 X버튼을 누르면 이 이벤트가 발생
            running = False # 게임이 진행중이 아님
            
        if event.type == pygame.KEYDOWN: # 만약 키보드를 눌렀을 때
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                to_x += character_speed
            elif event.key == pygame.K_UP: # 캐릭터를 위쪽으로
                to_y -= character_speed
            elif event.key == pygame.K_DOWN: # 캐릭터를 아래쪽으로
                to_y += character_speed
                
        if event.type == pygame.KEYUP: # 방향키를 떼일 때
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
                
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt
    
    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width  
                
    
    # 세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height  
        
    
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
        
            
    screen.blit(background, (0, 0)) # 백그라운드 배경 그린다 그런다음 위치 지정함
    
    screen.blit(character, (character_x_pos, character_y_pos)) # 캐릭터 그린다 그런다음 위치 지정함
    
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos)) # 적 그린다 그런다음 위치 지정함
    
    pygame.display.update() # 파이썬은 디스플레이에 매번 업데이트 해줘야 한다(게임 화면을 다시 그리기)

# pygame 종료
pygame.quit()