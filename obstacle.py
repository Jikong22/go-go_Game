import pygame
import random
from settings import OBSTACLE_SPEED

class Obstacle:
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # 충돌 판정을 위한 Rect 미리 생성
        self.rect_obj = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def update(self, dt):
        self.y += OBSTACLE_SPEED * dt
        self.rect_obj.y = self.y # Rect 위치도 같이 업데이트

    def rect(self, offset_x):
        # 화면 그리기 및 차량 충돌 판정용 (offset 적용)
        return pygame.Rect(offset_x + self.x, self.y, self.WIDTH, self.HEIGHT)

class ObstacleManager:
    def __init__(self, center_rect):
        self.center_rect = center_rect
        self.obstacles = []
        self.spawn_timer = 0.0
        self.spawn_interval = 0.3 # 0.3초마다 생성 시도 (조절 가능)

    def update(self, dt):
        # 1. 기존 장애물 이동
        for obs in self.obstacles:
            obs.update(dt)
        
        # 화면 아래로 내려간 장애물 삭제
        self.obstacles = [o for o in self.obstacles if o.y < 720]

        # 2. 장애물 생성 로직 개선
        self.spawn_timer += dt
        
        # 일정 시간이 지나면 생성 시도
        if self.spawn_timer >= self.spawn_interval:
            # 생성 시도 (성공하면 타이머 리셋)
            if self.try_spawn_obstacle():
                self.spawn_timer = 0
                # 다음 생성 시간은 약간 랜덤하게 (0.3초 ~ 0.5초 사이)
                self.spawn_interval = random.uniform(0.3, 0.5)

    def try_spawn_obstacle(self):
        # 최대 5번 시도해서 빈 자리를 찾음
        for _ in range(5):
            # 랜덤 X 좌표 (도로 폭 안에서)
            x = random.randint(0, self.center_rect.width - Obstacle.WIDTH)
            y = -60 # 화면 살짝 위에서 생성
            
            # 새로 만들 장애물의 영역 (여유 공간 포함)
            # 가로/세로에 10px 정도 여유를 둬서 딱 붙지 않게 함
            new_rect = pygame.Rect(x - 10, y - 20, Obstacle.WIDTH + 20, Obstacle.HEIGHT + 40)
            
            # 기존 장애물들과 겹치는지 확인
            collided = False
            for obs in self.obstacles:
                # 화면 상단에 있는 장애물들만 검사하면 됨 (y < 200)
                if obs.y < 200:
                    # 기존 장애물 영역
                    existing_rect = pygame.Rect(obs.x, obs.y, Obstacle.WIDTH, Obstacle.HEIGHT)
                    if new_rect.colliderect(existing_rect):
                        collided = True
                        break
            
            # 겹치지 않는다면 생성 확정
            if not collided:
                self.obstacles.append(Obstacle(x, y))
                return True # 생성 성공
        
        return False # 자리 못 찾음 (생성 실패)

    def draw(self, screen, offset_x):
        for obs in self.obstacles:
            # 장애물 이미지 (빨간 네모 + 테두리)
            r = obs.rect(offset_x)
            pygame.draw.rect(screen, (200, 50, 50), r)
            pygame.draw.rect(screen, (100, 0, 0), r, 3) # 테두리

    def remove_collided(self, car, offset_x):
        car_rect = car.rect(offset_x)
        collided_obstacles = []
        for obs in self.obstacles:
            if car_rect.colliderect(obs.rect(offset_x)):
                collided_obstacles.append(obs)
        
        # 충돌한 장애물 리스트에서 제거
        for obs in collided_obstacles:
            if obs in self.obstacles:
                self.obstacles.remove(obs)
                return True # 충돌 발생 알림
        
        return False