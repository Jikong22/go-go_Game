import pygame

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
    'basic': {'speed': 350, 'durability_per_sec': 3, 'max_durability': 100},
    'speed': {'speed': 450, 'durability_per_sec': 6, 'max_durability': 80},
    'durable': {'speed': 280, 'durability_per_sec': 1, 'max_durability': 150}
}

OBSTACLE_SPEED = 200

SCORES_FILE = 'scores.json'

# 피트레인 설정
PIT_INTERVAL = 15.0
PIT_BASE_CHANCE = 0.4
PIT_CHANCE_INC = 0.05
PIT_DURATION = 5.0

# === 폰트 자동 선택 로직 (수정됨) ===
def get_korean_font_name():
    fonts = ['malgungothic', 'apple sd gothic neo', 'applegothic', 'nanumgothic', 'gulim', 'arial']
    available = pygame.font.get_fonts()
    
    for name in fonts:
        if name in available:
            return name
            
    # 못 찾아도 윈도우 기본 폰트인 맑은 고딕을 강제로 리턴
    return 'malgungothic'

FONT_NAME = get_korean_font_name()