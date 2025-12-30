import pygame
from car import Car
from obstacle import ObstacleManager
from pit import PitStop
from settings import LEFT_W, CENTER_W
import ui

# FONT_NAME이 없을 경우를 대비한 안전 장치
try:
    from settings import FONT_NAME
except ImportError:
    FONT_NAME = None

def run_game(screen, nickname, car_type):
    clock = pygame.time.Clock()
    car = Car(car_type, nickname)
    obstacles = ObstacleManager(pygame.Rect(0,0,CENTER_W,720))
    pit = PitStop()
    
    score = 0.0 # [수정] 거리는 소수점 계산이 필요하므로 실수형 사용
    running = True
    
    # 폰트 설정
    if FONT_NAME:
        # 파일 경로인 경우와 시스템 폰트 이름인 경우 구분
        if FONT_NAME.endswith('.ttf'):
            font_small = pygame.font.Font(FONT_NAME, 24)
            font_mid = pygame.font.Font(FONT_NAME, 36)
        else:
            font_small = pygame.font.SysFont(FONT_NAME, 24)
            font_mid = pygame.font.SysFont(FONT_NAME, 36)
    else:
        font_small = pygame.font.SysFont("malgungothic", 24)
        font_mid = pygame.font.SysFont("malgungothic", 36)

    while running:
        dt = clock.tick(60)/1000.0
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        for e in events:
            if e.type == pygame.QUIT:
                running = False
            
            if pit.active and e.type == pygame.KEYDOWN:
                delay, complete = pit.handle_input(e.key)
                if delay > 0:
                    pygame.time.delay(int(delay*1000))
                if complete:
                    car.repair_full()
            
            elif not pit.active and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    if car.x > (CENTER_W - 70): 
                        if pit.try_enter():
                            print("피트인 성공!")

        if not pit.active:
            car.update(keys, dt)
            car.passive_damage(dt)
            obstacles.update(dt)
            pit.update_spawn_logic(dt)

            if obstacles.remove_collided(car, LEFT_W):
                car.take_collision()

            # [핵심 수정] 점수 = 속도 * 시간 (거리 누적)
            # 예: 속도 300 * 0.1초 = 30만큼 이동
            score += car.current_speed * dt

            if car.durability < 0:
                running = False

        screen.fill((0,0,0))
        
        # ui에 score(거리) 전달
        ui.draw_left_panel(screen, car, score, font_small)
        ui.draw_center_panel(screen, car, obstacles)
        ui.draw_right_panel(screen, pit, font_small)

        if pit.active:
            pit.draw_minigame(screen, font_mid, LEFT_W, CENTER_W)

        pygame.display.flip()

        if car.is_dead():
            running = False

    return score # 누적된 총 거리 반환