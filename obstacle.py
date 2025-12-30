import pygame
import random
import os
from settings import OBSTACLE_SPEED

class Obstacle:
    WIDTH = 50
    HEIGHT = 100

    # [수정] 생성 시 이미지(image)를 인자로 받도록 변경
    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.image = image  # 전달받은 이미지를 저장
        
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
        self.spawn_interval = 0.5 # 0.5초마다 생성 시도
        
        # --- [추가] 장애물 이미지 3장 로드 ---
        self.obs_images = []
        filenames = ["obs1.png", "obs2.png", "obs3.png"]
        
        for name in filenames:
            if os.path.exists(name):
                try:
                    img = pygame.image.load(name)
                    # 장애물 크기(50x50)에 맞게 크기 조절
                    img = pygame.transform.scale(img, (Obstacle.WIDTH, Obstacle.HEIGHT))
                    self.obs_images.append(img)
                    print(f"{name} 로드 성공")
                except:
                    print(f"{name} 로드 실패")
            else:
                print(f"{name} 파일이 없습니다. (기본 도형 사용)")
        # -----------------------------------

    def update(self, dt):
        # 1. 기존 장애물 이동
        for obs in self.obstacles:
            obs.update(dt)
        
        # 화면 아래로 내려간 장애물 삭제
        self.obstacles = [o for o in self.obstacles if o.y < 720]

        # 2. 새 장애물 생성 로직
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            if self.try_spawn_obstacle():
                pass # 생성 성공

    def try_spawn_obstacle(self):
        # 도로 내에서 랜덤 X 좌표 (겹치지 않게 시도)
        attempts = 0
        max_attempts = 10
        
        while attempts < max_attempts:
            attempts += 1
            w = self.center_rect.width
            x = random.randint(0, w - Obstacle.WIDTH)
            y = -Obstacle.HEIGHT # 화면 위쪽 바깥에서 시작
            
            new_rect = pygame.Rect(x, y, Obstacle.WIDTH, Obstacle.HEIGHT)
            
            # 기존 장애물들과 겹치는지 확인
            collided = False
            for obs in self.obstacles:
                if obs.y < 200: # 화면 상단에 있는 장애물만 검사
                    existing_rect = pygame.Rect(obs.x, obs.y, Obstacle.WIDTH, Obstacle.HEIGHT)
                    if new_rect.colliderect(existing_rect):
                        collided = True
                        break
            
            # 겹치지 않는다면 생성 확정
            if not collided:
                # [수정] 이미지 리스트가 있으면 랜덤으로 하나 뽑음
                selected_img = None
                if self.obs_images:
                    selected_img = random.choice(self.obs_images)
                
                # 이미지를 가지고 장애물 생성
                self.obstacles.append(Obstacle(x, y, selected_img))
                return True 
        
        return False 

    def draw(self, screen, offset_x):
        for obs in self.obstacles:
            r = obs.rect(offset_x)
            
            # [수정] 이미지가 있으면 이미지를 그리고, 없으면 네모를 그림
            if obs.image:
                screen.blit(obs.image, (r.x, r.y))
            else:
                # 이미지 없을 때 (기존 빨간 네모)
                pygame.draw.rect(screen, (200, 50, 50), r)
                pygame.draw.rect(screen, (100, 0, 0), r, 3)

    def remove_collided(self, car, offset_x):
        car_rect = car.rect(offset_x)
        collided_list = []
        
        # 충돌한 장애물 찾기
        for obs in self.obstacles:
            if car_rect.colliderect(obs.rect(offset_x)):
                collided_list.append(obs)
        
        # 제거 및 결과 반환
        if collided_list:
            for obs in collided_list:
                self.obstacles.remove(obs)
            return True # 충돌 발생함
            
        return False