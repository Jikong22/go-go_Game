import pygame

# 폰트 모듈 초기화 (폰트 이름을 찾기 위해 필요)
pygame.init()

SCREEN_W = 1280
SCREEN_H = 720

FPS = 60

# 화면 레이아웃
LEFT_W = 280
CENTER_W = 700
RIGHT_W = 300

# 자동차 설정
# 기본형: 밸런스
# 속도형: 빠르지만 내구도가 빨리 닳음
# 내구형: 느리지만 튼튼함
CAR_TYPES = {
    'basic': {'speed': 350, 'durability_per_sec': 2, 'max_durability': 150},
    'speed': {'speed': 450, 'durability_per_sec': 4, 'max_durability': 150},
    'durable': {'speed': 250, 'durability_per_sec': 1, 'max_durability': 150}
}

OBSTACLE_SPEED = 200 # 장애물 속도

SCORES_FILE = 'scores.json'

# 피트레인 설정
PIT_INTERVAL = 15.0     # 15초마다 등장 체크
PIT_BASE_CHANCE = 0.4   # 기본 확률 40%
PIT_CHANCE_INC = 0.1   # 실패 시 증가 확률 10%
PIT_DURATION = 3.0      # 피트레인이 열려있는 시간 (3초 뒤 닫힘)

# === 폰트 자동 선택 로직 ===
def get_korean_font_name():
    # 운영체제별 한글 폰트 후보군
    fonts = ['malgungothic', 'apple sd gothic neo', 'applegothic', 'nanumgothic', 'gulim', 'arial']
    
    # 시스템에 설치된 폰트 목록 가져오기
    available = pygame.font.get_fonts()
    
    for name in fonts:
        if name in available:
            return name
    return None # 못 찾으면 기본 폰트 사용

# 이 변수(FONT_NAME)를 다른 파일에서 import 해서 사용합니다.
FONT_NAME = get_korean_font_name()