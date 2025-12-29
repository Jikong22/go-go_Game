# main.py
import pygame
from settings import SCREEN_W, SCREEN_H, FONT_NAME
from menu import StartMenu
from game import run_game
from scoreboard import draw_scores, save_score

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("목련제 레이싱")

# --- 폰트 설정 (settings.py의 FONT_NAME 사용) ---
# 시스템 폰트가 없으면 기본 폰트 사용
font_big = pygame.font.SysFont(FONT_NAME, 80) # Game Over용으로 조금 더 크게
font_mid = pygame.font.SysFont(FONT_NAME, 40)
font_small = pygame.font.SysFont(FONT_NAME, 24)

fonts = (font_big, font_mid, font_small)

menu = StartMenu(fonts)
nickname = '익명'
car_type = 'basic'
score = 0
state = 'menu' # 현재 게임 상태 (menu, game, game_over, score, help)

running = True
while running:
    # 1. 이벤트 처리
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

    # 2. 상태별 로직
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
        # 게임 실행 (게임이 끝나면 점수를 반환)
        score = run_game(screen, nickname, car_type)
        save_score(nickname, score)
        state = 'game_over' # 바로 메뉴로 가지 않고 게임오버 화면으로 이동

    elif state == 'game_over':
        # 배경 검은색
        screen.fill((0, 0, 0))

        # GAME OVER 텍스트
        text_over = font_big.render("GAME OVER!", True, (255, 50, 50)) # 빨간색
        rect_over = text_over.get_rect(center=(SCREEN_W/2, SCREEN_H/2 - 80))
        screen.blit(text_over, rect_over)

        # 점수 및 닉네임 표시
        info_text = f"{nickname} 님의 점수: {score}점"
        text_info = font_mid.render(info_text, True, (255, 255, 255))
        rect_info = text_info.get_rect(center=(SCREEN_W/2, SCREEN_H/2 + 20))
        screen.blit(text_info, rect_info)

        # 안내 문구
        guide_text = font_small.render("스페이스바를 누르면 메뉴로 돌아갑니다.", True, (150, 150, 150))
        rect_guide = guide_text.get_rect(center=(SCREEN_W/2, SCREEN_H/2 + 100))
        screen.blit(guide_text, rect_guide)

        pygame.display.flip()

        # 키 입력 확인 (스페이스바 또는 엔터)
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE or e.key == pygame.K_RETURN:
                    state = 'menu'

    elif state == 'score':
        draw_scores(screen, font_mid)
        # ESC 키로 뒤로가기
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            state = 'menu'

    elif state == 'help':
        screen.fill((30, 30, 30))
        lines = [
            "=== 조작법 ===",
            "이동: WASD 또는 방향키",
            "",
            "=== 피트레인 시스템 ===",
            "내구도가 50% 이하로 떨어지면 속도가 느려집니다.",
            "오른쪽 패널에 'OPEN' 신호가 뜨면",
            "가장 오른쪽 차선에 붙어서 [ F ] 키를 누르세요.",
            "화면에 나오는 방향키를 순서대로 입력하면 수리됩니다.",
            "",
            "ESC: 뒤로가기"
        ]
        
        y = 100
        for line in lines:
            color = (255, 255, 0) if "===" in line else (255, 255, 255)
            text = font_mid.render(line, True, color)
            screen.blit(text, (SCREEN_W//2 - text.get_width()//2, y))
            y += 45
        
        pygame.display.flip()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            state = 'menu'
            
    # 화면 업데이트는 각 상태 내부에서 처리하거나 여기서 공통 처리
    # (위 코드에서는 각 상태별로 flip을 하거나 그리기 함수 안에서 처리함)
    if state == 'menu': # 메뉴는 내부 루프가 없으므로 여기서 업데이트 필요
        pygame.display.flip()

pygame.quit()