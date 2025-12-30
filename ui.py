import pygame
from settings import LEFT_W, CENTER_W, RIGHT_W

def draw_left_panel(screen, car, score, font):
    # 배경
    pygame.draw.rect(screen, (40,40,45), (0,0,LEFT_W,720))
    
    y_offset = 50
    line_h = 40
    
    # 거리를 km 단위로 변환
    km = score / 1000.0
    
    info_list = [
        f"주행 거리: {km:.2f} km",
        f"닉네임: {car.nickname}",
        f"차종: {car.car_type}",
        f"속도: {int(car.current_speed)} km/h",
        "", 
        f"내구도: {int(car.durability)}/{car.max_durability}"
    ]

    for info in info_list:
        text = font.render(info, True, (220,220,220))
        screen.blit(text, (20, y_offset))
        y_offset += line_h

    # 내구도 경고 (50% 미만)
    if car.durability < (car.max_durability * 0.5):
        warn = font.render("엔진 과열! 속도 저하", True, (255, 50, 50))
        screen.blit(warn, (20, y_offset + 20))

# [수정된 함수] finish_x 인자 제거
def draw_center_panel(screen, car, obstacles):
    # 1. 도로 배경
    road_rect = (LEFT_W, 0, CENTER_W, 720)
    pygame.draw.rect(screen, (60,60,60), road_rect)
    
    # 2. 피트레인 진입 구역 표시 (노란 점선)
    lane_x = LEFT_W + CENTER_W - 70
    pygame.draw.line(screen, (255,255,0), (lane_x, 0), (lane_x, 720), 2)
    
    # 바닥 글씨
    font = pygame.font.SysFont("arial", 20, bold=True)
    text = font.render("PIT ZONE", True, (100,100,100))
    screen.blit(text, (lane_x + 5, 600))

    # 3. 장애물 그리기
    obstacles.draw(screen, LEFT_W)

    # 4. 내 차 그리기 (이미지 적용)
    # 차 이미지가 있으면 이미지를 그리고, 없으면 네모를 그립니다.
    if hasattr(car, 'image') and car.image is not None:
        screen.blit(car.image, (car.x + LEFT_W, car.y))
    else:
        # 이미지가 없을 때
        car_rect = car.rect(LEFT_W)
        pygame.draw.rect(screen, car.color, car_rect)
        pygame.draw.rect(screen, (255,255,255), car_rect, 2)

def draw_right_panel(screen, pit, font):
    base_x = LEFT_W + CENTER_W
    pygame.draw.rect(screen, (30,30,30), (base_x, 0, RIGHT_W, 720))

    title = font.render("=== PIT LANE ===", True, (255,255,255))
    screen.blit(title, (base_x + 20, 50))

    status_color = (255, 0, 0) # Red (Closed)
    status_text = "Nope."
    
    if pit.is_open:
        status_color = (0, 255, 0) # Green (Open)
        status_text = "Box, Box!"
    
    pygame.draw.rect(screen, status_color, (base_x + 50, 150, 200, 100))
    text_surf = font.render(status_text, True, (0,0,0) if pit.is_open else (255,255,255))
    screen.blit(text_surf, (base_x + 150 - text_surf.get_width()//2, 185))

    y = 300
    if pit.is_open:
        msg = ["피트레인 진입 가능!", "오른쪽 차선에서", "[ F ] 키를 누르세요"]
        for m in msg:
            t = font.render(m, True, (255,255,0))
            screen.blit(t, (base_x + 20, y))
            y += 30
    else:
        next_prob = int(pit.current_chance * 100)
        remain = int(10 - pit.spawn_timer)
        msg = [f"다음 체크: {remain}초 후", f"현재 확률: {next_prob}%", "", "이곳이 초록색이 되면", "진입하세요."]
        for m in msg:
            t = font.render(m, True, (150,150,150))
            screen.blit(t, (base_x + 20, y))
            y += 30