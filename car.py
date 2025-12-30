from settings import CAR_TYPES, CENTER_W
import pygame
import os

class Car:
    WIDTH = 50
    HEIGHT = 80

    COLORS = {
        'basic': (0,0,255),   # 파랑
        'speed': (255,255,0), # 노랑
        'durable': (0,255,0)  # 초록
    }

    def __init__(self, car_type, nickname):
        self.car_type = car_type
        self.color = self.COLORS[car_type]
        
        # 설정 파일(settings.py)의 값을 그대로 가져옴
        self.base_speed = CAR_TYPES[car_type]['speed']
        self.durability_per_sec = CAR_TYPES[car_type]['durability_per_sec']
        self.max_durability = CAR_TYPES[car_type]['max_durability']
        self.durability = float(self.max_durability)
        
        # [추가] 점수 계산을 위해 현재 속도를 저장할 변수
        self.current_speed = self.base_speed
        
        self.x = CENTER_W//2 - self.WIDTH//2
        self.y = 720 - self.HEIGHT - 10
        self.nickname = nickname

        # === [추가된 부분] 이미지 로드 로직 ===
        # 이미지 파일 이름 매칭
        image_files = {
            'basic': 'basic.png',
            'speed': 'speed.png',
            'durable': 'durable.png'
        }
        
        file_name = image_files.get(car_type, 'basic.png') # 기본값 설정
        self.image = None
        
        # 이미지가 실제로 있는지 확인하고 로드
        if os.path.exists(file_name):
            try:
                img = pygame.image.load(file_name).convert_alpha() # 투명 배경 지원
                # 자동차 크기(WIDTH, HEIGHT)에 맞춰서 이미지 크기 조절
                self.image = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
            except:
                print(f"이미지 로드 실패: {file_name}")
                self.image = None
        else:
            print(f"이미지 파일 없음: {file_name}")

    def update(self, keys, dt):
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 1

        # [수정] 현재 속도를 self.current_speed에 저장 (외부에서 점수 계산용으로 씀)
        self.current_speed = self.base_speed
        
        # 내구도 절반 이하일 때 속도 감소 (기존 로직 0.7배 유지)
        if self.durability <= (self.max_durability * 0.5):
            self.current_speed *= 0.7

        self.x += dx * self.current_speed * dt
        self.y += dy * self.current_speed * dt

        # 벽 충돌 방지
        self.x = max(0, min(self.x, CENTER_W - self.WIDTH))
        self.y = max(0, min(self.y, 720 - self.HEIGHT))

    def passive_damage(self, dt):
        self.durability -= self.durability_per_sec * dt

    def take_collision(self):
        self.durability -= 20 # 충돌 시 내구도 감소

    def repair_full(self):
        self.durability = float(self.max_durability)

    def is_dead(self):
        return self.durability <= 0

    def rect(self, offset_x):
        return pygame.Rect(offset_x + self.x, self.y, self.WIDTH, self.HEIGHT)