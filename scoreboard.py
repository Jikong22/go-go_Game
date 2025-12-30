import json
from settings import SCORES_FILE, SCREEN_W, SCREEN_H
import pygame
import os

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_score(nickname, score):
    scores = load_scores()
    scores.append({'nickname': nickname, 'score': score})
    # 점수(거리)가 높은 순서대로 정렬
    scores = sorted(scores, key=lambda x: -x['score'])[:10]
    try:
        with open(SCORES_FILE, 'w', encoding='utf-8') as f:
            json.dump(scores, f, ensure_ascii=False)
    except:
        pass

def reset_scores():
    try:
        with open(SCORES_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)
    except:
        pass

def draw_scores(screen, font):
    screen.fill((20, 20, 40))
    pygame.draw.rect(screen, (255, 255, 0), (100, 50, SCREEN_W - 200, SCREEN_H - 100), 2)
    
    title = font.render("명예의 전당", True, (255, 255, 255))
    screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 80))

    scores = load_scores()
    y = 130
    if not scores:
        no_data = font.render("기록이 없습니다.", True, (150, 150, 150))
        screen.blit(no_data, (SCREEN_W // 2 - no_data.get_width() // 2, y))
    else:
        for i, s in enumerate(scores):
            color = (200, 200, 200)
            if i == 0: color = (255, 215, 0) # 1등 금색
            elif i == 1: color = (192, 192, 192) # 2등 은색
            elif i == 2: color = (205, 127, 50) # 3등 동색
            
            # [수정] 저장된 점수를 km 단위로 변환하여 표시
            km = s['score'] / 1000.0
            text_str = f"{i+1}위  {s['nickname']}  :  {km:.2f} km"
            
            surf = font.render(text_str, True, color)
            screen.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2, y))
            y += 45

    guide = font.render("[ESC] 뒤로가기    [R] 초기화", True, (100, 255, 100))
    screen.blit(guide, (SCREEN_W // 2 - guide.get_width() // 2, 600))