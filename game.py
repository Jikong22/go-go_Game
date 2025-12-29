# game.py
import pygame
from car import Car
from obstacle import ObstacleManager
from pit import PitStop
from settings import LEFT_W, CENTER_W

def run_game(screen, nickname, car_type):
    clock = pygame.time.Clock()
    car = Car(car_type, nickname)
    obstacles = ObstacleManager(pygame.Rect(0,0,CENTER_W,720))
    pit = PitStop()
    
    score = 0
    running = True
    
    font_small = pygame.font.SysFont("malgungothic", 24)
    font_mid = pygame.font.SysFont("malgungothic", 36)

    while running:
        dt = clock.tick(60)/1000.0
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        for e in events:
            if e.type == pygame.QUIT:
                running = False
            
            # 피트레인 미니게임 중일 때 입력 처리
            if pit.active and e.type == pygame.KEYDOWN:
                delay, complete = pit.handle_input(e.key)
                if delay > 0:
                    pygame.time.delay(int(delay*1000))
                if complete:
                    car.repair_full()
            
            # 게임 중 피트레인 진입 시도 (F키)
            elif not pit.active and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    # 차가 오른쪽 끝 차선에 있어야 함 (너비 700 기준 630 이상)
                    if car.x > (CENTER_W - 70): 
                        if pit.try_enter():
                            print("피트인 성공!")

        # 미니게임 중이 아닐 때만 게임 업데이트
        if not pit.active:
            car.update(keys, dt)
            car.passive_damage(dt)
            obstacles.update(dt)
            pit.update_spawn_logic(dt) # 피트레인 등장 확률 계산

            if obstacles.remove_collided(car, LEFT_W):
                car.take_collision()

            # 점수 증가 (생존 시간에 비례 + 속도 보너스)
            score += int(10 * dt)
            if car.durability < 0:
                running = False

        # --- 그리기 ---
        screen.fill((0,0,0))
        
        import ui
        ui.draw_left_panel(screen, car, font_small)
        ui.draw_center_panel(screen, car, obstacles)
        ui.draw_right_panel(screen, pit, font_small)

        # 미니게임 오버레이
        if pit.active:
            pit.draw_minigame(screen, font_mid, LEFT_W, CENTER_W)

        pygame.display.flip()

        if car.is_dead():
            running = False

    return score