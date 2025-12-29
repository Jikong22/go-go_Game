import json
from settings import SCORES_FILE
import pygame

def load_scores():
    try:
        with open(SCORES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_score(nickname, score):
    scores = load_scores()
    scores.append({'nickname':nickname, 'score':score})
    scores = sorted(scores, key=lambda x: -x['score'])[:10]
    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False)

def draw_scores(screen, font):
    screen.fill((30,30,30))
    
    title = font.render("명예의 전당", True, (255,255,255))
    screen.blit(title, (1280//2 - title.get_width()//2, 50))
    
    scores = load_scores()
    
    y = 150
    if not scores:
        no_data = font.render("기록이 없습니다.", True, (150,150,150))
        screen.blit(no_data, (1280//2 - no_data.get_width()//2, y))
    
    for i, s in enumerate(scores):
        text = font.render(f"{i+1}. {s['nickname']} : {s['score']}점", True, (255,255,0))
        screen.blit(text, (1280//2 - 200, y))
        y += 50

    guide = font.render("[ESC] 뒤로가기", True, (200,200,200))
    screen.blit(guide, (1280//2 - guide.get_width()//2, 600))