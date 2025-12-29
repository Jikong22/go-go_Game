import pygame
import random
from settings import PIT_INTERVAL, PIT_BASE_CHANCE, PIT_CHANCE_INC, PIT_DURATION

class PitStop:
    def __init__(self):
        self.active = False
        self.sequence = []
        self.index = 0
        self.can_enter = False
        
        self.spawn_timer = 0.0
        self.current_chance = PIT_BASE_CHANCE
        
        self.is_open = False
        self.open_timer = 0.0

    def update_spawn_logic(self, dt):
        if self.active:
            return

        if self.is_open:
            self.open_timer += dt
            if self.open_timer >= PIT_DURATION:
                self.is_open = False
                self.current_chance += PIT_CHANCE_INC
                self.spawn_timer = 0
            return

        self.spawn_timer += dt
        if self.spawn_timer >= PIT_INTERVAL:
            self.spawn_timer = 0
            if random.random() < self.current_chance:
                self.is_open = True
                self.open_timer = 0.0
                self.current_chance = PIT_BASE_CHANCE
            else:
                self.current_chance += PIT_CHANCE_INC

    def try_enter(self):
        if self.is_open and not self.active:
            self.start_minigame()
            self.is_open = False
            return True
        return False

    def start_minigame(self):
        self.active = True
        self.index = 0
        directions = ['위','아래','왼쪽','오른쪽']
        self.sequence = [random.choice(directions) for _ in range(8)]

    def handle_input(self, key):
        mapping = {
            pygame.K_UP: '위', pygame.K_DOWN: '아래',
            pygame.K_LEFT: '왼쪽', pygame.K_RIGHT: '오른쪽'
        }
        if key not in mapping:
            return 0, False
        
        if mapping[key] == self.sequence[self.index]:
            self.index += 1
            if self.index >= len(self.sequence):
                self.active = False
                return 0.2, True
            return 0, False
        else:
            return 0.5, False

    def draw_minigame(self, screen, font, left_w, center_w):
        overlay = pygame.Surface((center_w, 200))
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        screen.blit(overlay, (left_w, 260))

        text = " ".join(self.sequence[self.index:])
        surf = font.render(text, True, (255,255,0))
        rect = surf.get_rect(center=(left_w + center_w//2, 360))
        screen.blit(surf, rect)