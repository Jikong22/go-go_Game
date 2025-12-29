from settings import CAR_TYPES, CENTER_W
import pygame

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
        self.base_speed = CAR_TYPES[car_type]['speed']
        self.durability_per_sec = CAR_TYPES[car_type]['durability_per_sec']
        self.max_durability = CAR_TYPES[car_type]['max_durability']
        self.durability = float(self.max_durability)
        
        self.x = CENTER_W//2 - self.WIDTH//2
        self.y = 720 - self.HEIGHT - 10
        self.nickname = nickname

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

        # 내구도 절반 이하면 속도 감소
        current_speed = self.base_speed
        if self.durability <= (self.max_durability * 0.5):
            current_speed *= 0.7

        self.x += dx * current_speed * dt
        self.y += dy * current_speed * dt

        # 벽 충돌 방지
        self.x = max(0, min(self.x, CENTER_W - self.WIDTH))
        self.y = max(0, min(self.y, 720 - self.HEIGHT))

    def passive_damage(self, dt):
        self.durability -= self.durability_per_sec * dt

    def take_collision(self):
        self.durability -= 10

    def repair_full(self):
        self.durability = float(self.max_durability)

    def is_dead(self):
        return self.durability <= 0

    def rect(self, offset_x):
        return pygame.Rect(offset_x + self.x, self.y, self.WIDTH, self.HEIGHT)