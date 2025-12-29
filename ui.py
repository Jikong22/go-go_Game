# ui.py
import pygame
from settings import LEFT_W, CENTER_W, RIGHT_W

def draw_left_panel(screen, car, font):
    # 배경
    pygame.draw.rect(screen, (40,40,45), (0,0,LEFT_W,720))
    
    # 정보 표시
    y_offset = 50
    line_h = 40
    
    info_list = [
        f"닉네임: {car.nickname}",
        f"차종: {car.car_type}",
        f"속도: {int(car.base_speed)}",
        "", # 공백
        f"내구도: {int(car.durability)}/{car.max_durability}"
    ]

    for info in info_list:
        text = font.render(info, True, (220,220,220))
        screen.blit(text, (20, y_offset))
        y_offset += line_h

    # 내구도 경고 (50% 미만)
    if car.durability < (car.max_durability * 0.5):
        warn = font.render("⚠ 엔진 과열! 속도 저하 ⚠", True, (255, 50, 50))
        screen.blit(warn, (20, y_offset + 20))


def draw_center_panel(screen, car, obstacles):
    # 도로 배경
    road_rect = (LEFT_W, 0, CENTER_W, 720)
    pygame.draw.rect(screen, (60,60,60), road_rect)
    
    # 피트레인 진입 구역 표시 (오른쪽 끝 점선)
    lane_x = LEFT_W + CENTER_W - 70
    pygame.draw.line(screen, (255,255,0), (lane_x, 0), (lane_x, 720), 2)
    
    # 바닥에 'PIT ENTRY' 글씨 (장식)
    font = pygame.font.SysFont("arial", 20, bold=True)
    text = font.render("PIT ZONE", True, (100,100,100))
    screen.blit(text, (lane_x + 5, 600))

    # 장애물 및 차량
    obstacles.draw(screen, LEFT_W)
    
    # 내 차
    car_rect = car.rect(LEFT_W)
    pygame.draw.rect(screen, car.color, car_rect)
    # 차 테두리
    pygame.draw.rect(screen, (255,255,255), car_rect, 2)


def draw_right_panel(screen, pit, font):
    base_x = LEFT_W + CENTER_W
    pygame.draw.rect(screen, (30,30,30), (base_x, 0, RIGHT_W, 720))

    # 제목
    title = font.render("=== PIT LANE ===", True, (255,255,255))
    screen.blit(title, (base_x + 20, 50))

    # 상태 표시기 (신호등 느낌)
    status_color = (255, 0, 0) # Red (Closed)
    status_text = "CLOSED"
    
    if pit.is_open:
        status_color = (0, 255, 0) # Green (Open)
        status_text = "OPEN!"
    
    # 상태 박스
    pygame.draw.rect(screen, status_color, (base_x + 50, 150, 200, 100))
    text_surf = font.render(status_text, True, (0,0,0) if pit.is_open else (255,255,255))
    screen.blit(text_surf, (base_x + 150 - text_surf.get_width()//2, 185))

    # 설명 텍스트
    y = 300
    if pit.is_open:
        msg = [
            "피트레인 진입 가능!",
            "오른쪽 차선에서",
            "[ F ] 키를 누르세요"
        ]
        for m in msg:
            t = font.render(m, True, (255,255,0))
            screen.blit(t, (base_x + 20, y))
            y += 30
    else:
        # 다음 오픈 정보 (디버깅 겸 정보)
        next_prob = int(pit.current_chance * 100)
        remain = int(15 - pit.spawn_timer)
        msg = [
            f"다음 체크: {remain}초 후",
            f"현재 확률: {next_prob}%",
        ]
        for m in msg:
            t = font.render(m, True, (150,150,150))
            screen.blit(t, (base_x + 20, y))
            y += 30