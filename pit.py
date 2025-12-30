import pygame
import random
import os
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

        # === [추가] 효과음 로드 ===
        self.open_sound = None
        sound_file = "box.MP3"  # 파일 이름 정확히 일치해야 함
        
        if os.path.exists(sound_file):
            try:
                # 효과음(Sound) 객체 생성
                self.open_sound = pygame.mixer.Sound(sound_file)
                self.open_sound.set_volume(0.5) # 볼륨 조절 (0.0 ~ 1.0)
            except Exception as e:
                print(f"효과음 로드 실패: {e}")
        else:
            print(f"효과음 파일 없음: {sound_file}")

    def update_spawn_logic(self, dt):
        if self.active:
            return

        # 열려있는 상태라면 시간 체크해서 닫기
        if self.is_open:
            self.open_timer += dt
            if self.open_timer >= PIT_DURATION:
                self.is_open = False
                self.current_chance += PIT_CHANCE_INC
                self.spawn_timer = 0
            return

        # 닫혀있는 상태라면 열릴지 말지 결정
        self.spawn_timer += dt
        if self.spawn_timer >= PIT_INTERVAL:
            self.spawn_timer = 0
            # 확률 체크
            if random.random() < self.current_chance:
                # === 피트레인 오픈! ===
                self.is_open = True
                self.open_timer = 0.0
                self.current_chance = PIT_BASE_CHANCE
                
                # [추가] 소리가 로드되어 있다면 재생
                if self.open_sound:
                    self.open_sound.play()
                    print("효과음 재생!")
            else:
                # 실패하면 다음 확률 증가
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