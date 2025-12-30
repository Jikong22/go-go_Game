import pygame
import os

# 폰트 모듈 초기화
pygame.init()

SCREEN_W = 1280
SCREEN_H = 720

FPS = 60

# 화면 레이아웃
LEFT_W = 280
CENTER_W = 700
RIGHT_W = 300

# 자동차 설정
CAR_TYPES = {
    'basic': {'speed': 300, 'durability_per_sec': 3, 'max_durability': 100},
    'speed': {'speed': 400, 'durability_per_sec': 4, 'max_durability': 100},
    'durable': {'speed': 200, 'durability_per_sec': 2, 'max_durability': 100}
}

OBSTACLE_SPEED = 400

SCORES_FILE = 'scores.json'

# 피트레인 설정
PIT_INTERVAL = 10.0
PIT_BASE_CHANCE = 0.5
PIT_CHANCE_INC = 0.2
PIT_DURATION = 3.0

# === 폰트 자동 선택 로직 (강화됨) ===
def get_korean_font_name():
    # 1. 시스템 폰트 이름으로 찾기
    fonts = ['malgungothic', 'apple sd gothic neo', 'applegothic', 'nanumgothic', 'gulim', 'arial']
    available = pygame.font.get_fonts()
    
    for name in fonts:
        if name in available:
            return name
            
    # 2. 폰트를 못 찾았을 경우, 윈도우 맑은고딕 경로 강제 지정
    # (폰트 파일이 있으면 무조건 나옵니다)
    font_path = 'C:/Windows/Fonts/malgun.ttf'
    if os.path.exists(font_path):
        return font_path

    # 3. 진짜 아무것도 없으면 None (영어만 나오지만 깨지진 않음)
    return None

FONT_NAME = get_korean_font_name()