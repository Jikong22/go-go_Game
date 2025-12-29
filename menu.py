# menu.py
import pygame

class StartMenu:
    def __init__(self, fonts):
        self.nickname = ''
        self.active_input = False
        self.font_big, self.font_mid, self.font_small = fonts

        self.state = 'menu'  # 'menu' or 'car_select'

        # 입력창
        self.input_box = pygame.Rect(1280/2 - 200, 300, 400, 50)

        # 메뉴 버튼
        self.btn_start = pygame.Rect(1280/2 - 320, 420, 200, 60)
        self.btn_score = pygame.Rect(1280/2 - 100, 420, 200, 60)
        self.btn_help = pygame.Rect(1280/2 + 120, 420, 200, 60)

        # 차종 버튼 (처음에는 안보임)
        self.btn_basic = pygame.Rect(1280/2 - 300, 400, 150, 50)
        self.btn_speed = pygame.Rect(1280/2 - 75, 400, 150, 50)
        self.btn_durable = pygame.Rect(1280/2 + 150, 400, 150, 50)

    def draw(self, screen):
        screen.fill((30,30,40))
        title = self.font_big.render('목련제 레이싱', True, (255,255,255))
        screen.blit(title, (1280/2 - title.get_width()/2, 150))

        if self.state == 'menu':
            # 닉네임 입력
            pygame.draw.rect(screen, (255,255,255), self.input_box, 2)
            nm = self.nickname if self.nickname != '' else ''
            nickname_text = self.font_mid.render(nm, True, (255,255,255))
            screen.blit(nickname_text, (
                self.input_box.x + 10, 
                self.input_box.y + (self.input_box.height - nickname_text.get_height())/2
            ))

            # 메뉴 버튼
            buttons = [
                (self.btn_start, '게임 시작'), 
                (self.btn_score, '스코어보드'), 
                (self.btn_help, '게임 방법')
            ]
            colors = [(100,100,200),(100,200,100),(200,100,100)]
            for (rect,text),color in zip(buttons,colors):
                pygame.draw.rect(screen,color,rect)
                text_surf = self.font_small.render(text, True, (255,255,255))
                screen.blit(text_surf,(
                    rect.x + (rect.width - text_surf.get_width())/2,
                    rect.y + (rect.height - text_surf.get_height())/2
                ))
        elif self.state == 'car_select':
            car_buttons = [
                (self.btn_basic,'기본',(0,0,255)),
                (self.btn_speed,'속도형',(255,255,0)),
                (self.btn_durable,'내구형',(0,255,0))
            ]
            for rect,text,color in car_buttons:
                pygame.draw.rect(screen,color,rect)
                text_surf = self.font_small.render(text, True, (0,0,0))
                screen.blit(text_surf,(
                    rect.x + (rect.width - text_surf.get_width())/2,
                    rect.y + (rect.height - text_surf.get_height())/2
                ))

    def update(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.state == 'menu':
                    if self.input_box.collidepoint(e.pos):
                        self.active_input = True
                    else:
                        self.active_input = False

                    if self.btn_start.collidepoint(e.pos):
                        self.state = 'car_select'
                    if self.btn_score.collidepoint(e.pos):
                        return ('score', None)
                    if self.btn_help.collidepoint(e.pos):
                        return ('help', None)
                elif self.state == 'car_select':
                    if self.btn_basic.collidepoint(e.pos):
                        return ('start','basic')
                    if self.btn_speed.collidepoint(e.pos):
                        return ('start','speed')
                    if self.btn_durable.collidepoint(e.pos):
                        return ('start','durable')

            if e.type == pygame.KEYDOWN and self.active_input:
                if e.key == pygame.K_BACKSPACE:
                    self.nickname = self.nickname[:-1]
                elif e.key == pygame.K_RETURN:
                    self.active_input = False
                else:
                    if len(self.nickname) < 10:
                        self.nickname += e.unicode
        return None
