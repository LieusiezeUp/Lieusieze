import pygame

pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정 
screen_width = 480 # 가로
screen_height = 640 # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game") # 게임이름

# 배경 이미지 불러오기
background = pygame.image.load("C:/Users/Kim Family/Desktop/Python_ex/pygame_basic/background.png")

# 스프라이트 불러오기
character = pygame.image.load("C:/Users/Kim Family/Desktop/Python_ex/pygame_basic/Rion.jpg")
character_size = character.get_rect().size # 사각형이미지의 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로 position의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height # 화면 세로 크기 가장 아래에 해당하는 곳에 위치


# 이벤트 루프
#파이썬에서는 이벤트 루프를 켜놔야 창이 안꺼진다
running = True # 게임이 진행중인가?
while running:
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창의 X버튼을 누르면 이 이벤트가 발생
            running = False # 게임이 진행중이 아님
    screen.blit(background, (0, 0)) # 백그라운드 배경 그린다 그런다음 위치 지정함
    
    screen.blit(character, (character_x_pos, character_y_pos)) # 캐릭터 그린다 그런다음 위치 지정함
    
    pygame.display.update() # 파이썬은 디스플레이에 매번 업데이트 해줘야 한다(게임 화면을 다시 그리기)

# pygame 종료
pygame.quit()