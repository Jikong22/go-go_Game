import pygame
import os
from settings import SCREEN_W, SCREEN_H, FONT_NAME
from menu import StartMenu
from game import run_game
from scoreboard import draw_scores, save_score, reset_scores

pygame.init()
pygame.mixer.init() ### 2. 믹서 초기화 (소리 재생을 위해 필수) ###
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("피하go 달리go")

# 3. 배경음악 로드 및 무한 반복 재생
bgm_path = 'bgm.mp3'
if os.path.exists(bgm_path):
    try:
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.set_volume(0.3) # 볼륨 조절 (0.0 ~ 1.0)
        pygame.mixer.music.play(-1)        # -1은 무한 반복 의미
        print("BGM 재생 시작")
    except Exception as e:
        print(f"BGM 로드 실패: {e}")
else:
    print("bgm.wav 파일을 찾을 수 없습니다. create_bgm.py를 먼저 실행하세요.")

# 폰트 로드 (파일 경로인지 이름인지 확인)
if FONT_NAME and (os.path.exists(FONT_NAME) or FONT_NAME.endswith('.ttf')):
    # 파일 경로인 경우
    font_big = pygame.font.Font(FONT_NAME, 80)
    font_mid = pygame.font.Font(FONT_NAME, 40)
    font_small = pygame.font.Font(FONT_NAME, 24)
else:
    # 시스템 폰트 이름인 경우 (혹은 None)
    font_big = pygame.font.SysFont(FONT_NAME, 80)
    font_mid = pygame.font.SysFont(FONT_NAME, 40)
    font_small = pygame.font.SysFont(FONT_NAME, 24)

fonts = (font_big, font_mid, font_small)

menu = StartMenu(fonts)
nickname = '익명'
car_type = 'basic'
score = 0
state = 'menu'

# 비밀번호 입력 관련
input_pw = ""
pw_error_timer = 0

running = True
clock = pygame.time.Clock()

while running:
    # 1. 이벤트 처리 (모든 상태 공통)
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

    # 2. 상태별 로직 및 그리기
    if state == 'menu':
        menu.draw(screen)
        res = menu.update(events)
        if res:
            if res[0] == 'start':
                nickname = menu.nickname.strip() if menu.nickname.strip() != '' else '익명'
                car_type = res[1]
                state = 'game'
                menu.state = 'menu'
            elif res[0] == 'score':
                state = 'score'
            elif res[0] == 'help':
                state = 'help'

    elif state == 'game':
        score = run_game(screen, nickname, car_type)
        save_score(nickname, score)
        state = 'game_over'

    elif state == 'game_over':
        screen.fill((0, 0, 0))
        text_over = font_big.render("GAME OVER!", True, (255, 50, 50))
        screen.blit(text_over, (SCREEN_W//2 - text_over.get_width()//2, 200))

        info_text = f"{nickname} 님의 점수: {score}점"
        text_info = font_mid.render(info_text, True, (255, 255, 255))
        screen.blit(text_info, (SCREEN_W//2 - text_info.get_width()//2, 350))

        guide = font_small.render("스페이스바를 누르면 메뉴로 돌아갑니다.", True, (150, 150, 150))
        screen.blit(guide, (SCREEN_W//2 - guide.get_width()//2, 500))
        
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE or e.key == pygame.K_RETURN:
                    state = 'menu'

    elif state == 'score':
        # 스코어보드 그리기 함수 호출
        draw_scores(screen, font_mid)
        
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    state = 'menu'
                elif e.key == pygame.K_r:
                    state = 'password_input'
                    input_pw = ""
                    pw_error_timer = 0

    elif state == 'password_input':
        screen.fill((20, 20, 20))
        t = font_mid.render("관리자 비밀번호 입력", True, (255,255,255))
        screen.blit(t, (SCREEN_W//2 - t.get_width()//2, 200))

        masked = "*" * len(input_pw)
        pw_surf = font_big.render(masked, True, (255, 255, 0))
        screen.blit(pw_surf, (SCREEN_W//2 - pw_surf.get_width()//2, 300))

        info = font_small.render("엔터: 확인 / ESC: 취소", True, (150,150,150))
        screen.blit(info, (SCREEN_W//2 - info.get_width()//2, 450))

        if pw_error_timer > 0:
            err = font_small.render("비밀번호 불일치!", True, (255,0,0))
            screen.blit(err, (SCREEN_W//2 - err.get_width()//2, 380))
            pw_error_timer -= 1
        
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    state = 'score'
                elif e.key == pygame.K_BACKSPACE:
                    input_pw = input_pw[:-1]
                elif e.key == pygame.K_RETURN:
                    if input_pw == "1022":
                        reset_scores()
                        state = 'score'
                    else:
                        pw_error_timer = 60
                        input_pw = ""
                else:
                    if e.unicode.isnumeric() and len(input_pw) < 4:
                        input_pw += e.unicode

    elif state == 'help':
        screen.fill((30, 30, 30))
        lines = ["이동: WASD, 방향키", "피트레인: 피트레인 오픈 시 우측 차선에서 F키를 눌러 진입 가능", "장애물을 피해 달리세요!", "피트레인 진입 시 방향키를 사용해주세요."]
        y = 150
        for l in lines:
            t = font_mid.render(l, True, (255,255,255))
            screen.blit(t, (SCREEN_W//2 - t.get_width()//2, y))
            y += 60
            
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    state = 'menu'

    # 3. 화면 업데이트 (매우 중요: 루프 마지막에 한 번만 실행)
    pygame.display.flip()
    
    # 4. 프레임 제한
    clock.tick(60)

pygame.quit()