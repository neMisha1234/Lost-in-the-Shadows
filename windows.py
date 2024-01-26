import pygame
from load_image import load_image
from Button import Button, Scroll_btns
from Field import generate_level, load_level
from Enemy import Enemy
from BaseCharacter import BaseCharacter
from HpBar import HpBar
from Items import Inventory, Item_dialog, Current_inventory, items_function


class Pause:
    def __init__(self, cntrl, mn, game):
        self.controller = cntrl
        self.game = game
        self.menu = mn
        self.btns = []
        self.btn_names = ["Продолжить игру", "  Настройки  ", "Главное меню"]

    def create_button(self, x, y, text, screen):
        btn = Button(x, y, 250, 90)
        background = btn.check_position(*pygame.mouse.get_pos())
        btn.draw_btn_and_txt(text, screen, background)
        self.btns.append(btn)

    def check_event(self, event, keys=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.btns:
                if btn.check_position(*pygame.mouse.get_pos()):
                    if btn.get_text().strip() == "Главное меню":
                        self.controller.set_current_window(self.menu)
                    if btn.get_text().strip() == "Настройки":
                        pass
                    if btn.get_text().strip() == "Продолжить игру":
                        items_function["standart"](self.game.hero)
                        self.game.hero.load_items_from_db()
                        self.controller.set_current_window(self.game)
        if keys[pygame.K_ESCAPE]:
            self.game.hero.load_items_from_db()
            items_function["standart"](self.game.hero)
            self.game.hero.load_items_from_db()
            self.controller.set_current_window(self.game)

    def start(self, screen):
        screen.fill((0, 0, 0))
        self.btns = []
        x1, y1 = pygame.mouse.get_pos()
        cnt = 0
        for i in range(3):
            self.create_button(100, 50 + 150 * i, self.btn_names[i], screen)
            if self.btns[i].check_position(x1, y1):
                cnt += 1
        if cnt > 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class Invent_window:
    def __init__(self, cntrl, game):
        self.inventory = Inventory(500, 5, 100, 500, 300)
        self.controller = cntrl
        self.mouse_pos_1, self.mouse_pos_2 = None, None
        self.dialog = None
        self.game = game
        self.hero = self.game.hero
        self.player_im = load_image("Player.png", colorkey=(255, 255, 255))
        self.player_im = pygame.transform.scale(self.player_im, (200, 300))
        self.it_des = None
        self.current_inv = Current_inventory(650, 390, 100, game.hero)
        self.on_click = None
        self.attributes = [f"Текущее здоровье: {self.hero.hp}", f"Сопротивление урону: {self.hero.damage_resist}",
                           f"Скорость бега: {self.hero.vx}", f"Максимальная энергия: {self.hero.MAX_ENERGY}",
                           f"Высота прыжка: {self.hero.vy}"]

    def check_event(self, event, keys=None):
        if self.dialog:
            if self.dialog.check_event(event):
                self.dialog = None
                self.mouse_pos_1 = None
                self.mouse_pos_2 = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.it_des:
                if self.it_des.check_event(event):
                    self.it_des = None
                elif not self.it_des.check_coords(pygame.mouse.get_pos()):
                    self.it_des = None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            temp = self.inventory.check_coords(pygame.mouse.get_pos())
            temp2 = self.current_inv.check_coords(pygame.mouse.get_pos())
            if temp:
                t_x, t_y = temp
                self.mouse_pos_2 = None
                if t_y * 5 + t_x < len(self.inventory.get_invent()):
                    self.mouse_pos_1 = pygame.mouse.get_pos()
                    self.on_click = t_y * 5 + t_x
                else:
                    self.on_click = None
                    self.mouse_pos_1 = None

            elif temp2:
                tx, ty = temp2
                self.mouse_pos_1 = None
                if tx < len(self.current_inv.items):
                    self.mouse_pos_2 = pygame.mouse.get_pos()
                    self.on_click = tx
                else:
                    self.mouse_pos_2 = None
                    self.on_click = None
            else:
                self.mouse_pos_1 = None
                self.mouse_pos_2 = None
                self.on_click = None

        if keys[pygame.K_e]:
            self.game.hero.load_items_from_db()
            items_function["standart"](self.game.hero)
            self.game.hero.load_items_from_db()
            self.controller.set_current_window(self.game)

    def start(self, screen):
        screen.fill((0, 0, 0))
        if self.dialog:
            if self.dialog.it_desc:
                self.it_des = self.dialog.it_desc
        self.inventory.draw_on_screen(screen)
        self.current_inv.draw_on_screen(screen)
        if self.mouse_pos_1:
            x, y = self.mouse_pos_1
            it_nd_im = self.inventory.get_invent()[self.on_click]
            self.dialog = Item_dialog(x, y, self.current_inv, it_nd_im, "Надеть", "Читать", 0)
            self.dialog.draw(screen)
        if self.mouse_pos_2:
            x, y = self.mouse_pos_2
            if self.on_click < len(self.current_inv.items):
                it_nd_im = self.current_inv.items[self.on_click]
                self.dialog = Item_dialog(x, y, self.current_inv, it_nd_im, " Снять   ", "Читать", 1)
                self.dialog.draw(screen)
        if self.it_des:
            self.it_des.draw_on_screen(screen)
        screen.blit(self.player_im, (150, 100))
        for i in range(len(self.attributes)):
            font = pygame.font.Font(None, 30)
            text = font.render(self.attributes[i], True, (159, 131, 3))
            screen.blit(text, (100, 50 * i + 150))


class Game:
    def __init__(self, cont, menu, go):
        self.controller = cont
        self.menu = menu

        self.hero_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.size = w, h = 2000, 500
        self.game_over = go
        self.background = load_image("background.jpg")
        self.background = pygame.transform.scale(self.background, (w, h))

        self.map = pygame.surface.Surface(self.size)
        self.map.fill((255, 255, 255))
        self.fps = 60
        self.btns = []
        self.btn_names = ["Pause.png"]

        def generate_location():
            generate_level(load_level("small_lvl"), self.objects, self.all_sprites)

        generate_location()
        self.enemy = Enemy(self.enemy_sprites, 400, 200, self.fps, w, h, self.all_sprites)
        self.hero = BaseCharacter(self.hero_sprites, 100, 200, self.fps, w, h, self.all_sprites)
        self.hpbar = HpBar(750, h - 50, self.hero.hp)

    def create_button(self, x, y, image, screen):
        btn = Button(x, y, 50, 50)
        background = btn.check_position(*pygame.mouse.get_pos())
        btn.draw_btn_with_image(screen, image)
        self.btns.append(btn)

    def check_event(self, event, keys=None):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.btns:
                if btn.check_position(*pygame.mouse.get_pos()):
                    if btn.get_text().strip() == "Pause.png":
                        self.controller.set_current_window(Pause(self.controller, self.menu, self))
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.hero.climb = True
        else:
            self.hero.climb = False
        if keys[pygame.K_e]:
            self.controller.set_current_window(Invent_window(self.controller, self))
        if keys[pygame.K_ESCAPE]:
            self.controller.set_current_window(Pause(self.controller, self.menu, self))

    def start(self, screen):
        self.map.fill((255, 255, 255))
        self.btns = []
        x, y = pygame.mouse.get_pos()
        cnt = 0

        self.create_button(0, 0, self.btn_names[0], self.map)
        for i in range(len(self.btns)):
            if self.btns[i].check_position(x, y):
                cnt += 1

        if cnt > 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.hero_sprites.update(self.objects, self.enemy_sprites)
        self.hero_sprites.draw(self.map)
        if not self.hero_sprites:
            print("GAME_OVER")
            self.controller.set_current_window(self.game_over)

        self.hpbar.draw(self.map)

        self.enemy_sprites.update(self.objects, self.hero)
        self.enemy_sprites.draw(self.map)
        self.enemy.set_player(self.hero.rect.x)

        self.objects.draw(self.map)
        self.hpbar.update(self.hero.hp)
        self.hpbar.draw(self.map)

        screen.blit(self.map, (0, 0))
        screen.blit(pygame.transform.scale(load_image("scelet.jpg", "white"), (50, 50)), (40, 0))
        screen.blit(pygame.transform.scale(load_image("equal.png", "white"), (30, 30)), (90, 10))
        f = pygame.font.Font(None, 50)
        text = f.render(f"{self.hero.kills}", 1, (0, 0, 0))
        screen.blit(text, (130, 5))


class Dialog_window:
    def __init__(self, w, h, cntrl, mn):
        pygame.init()
        self.start_image = load_image("are_you_sure.png")
        self.w = w
        self.h = h
        self.controller = cntrl
        self.btns = []
        self.btn_names = ["     Да     ", "    Нет     "]
        self.menu = mn

    def create_button(self, x, y, text, screen):
        btn = Button(x, y, 200, 50)
        background = btn.check_position(*pygame.mouse.get_pos())
        btn.draw_btn_and_txt(text, screen, background)
        self.btns.append(btn)

    def check_event(self, event, keys=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.btns:
                if btn.check_position(*pygame.mouse.get_pos()):
                    if btn.get_text().strip() == "Да":
                        return True
                    if btn.get_text().strip() == "Нет":
                        self.controller.set_current_window(self.menu)

    def start(self, screen):
        screen.fill((0, 0, 0))
        self.btns = []
        x, y = pygame.mouse.get_pos()
        cnt = 0
        for i in range(2):
            self.create_button(self.w // 2 - self.start_image.get_rect().w // 2 + 90, 100 + 100 * i, self.btn_names[i],
                               screen)
            if self.btns[i].check_position(x, y):
                cnt += 1
        if cnt > 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        screen.blit(self.start_image, (self.w // 2 - self.start_image.get_rect().w // 2, 0))


class Game_Over:
    def __init__(self, w, h, cntrl, mn):
        pygame.init()
        self.start_image = load_image("Game_Over.png")
        self.w = w
        self.h = h
        self.btns = []
        self.btn_names = ["Начать с последней точки", "Вернуться в главное меню", "     Выйти из игры     "]
        self.controller = cntrl
        self.game = Game(cntrl, mn, self)
        self.menu = mn
        self.menu.game = self.game

    def create_button(self, x, y, text, screen):
        btn = Button(x, y, 500, 100)
        background = btn.check_position(*pygame.mouse.get_pos())
        btn.draw_btn_and_txt(text, screen, background)
        self.btns.append(btn)

    def check_event(self, event, keys=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.btns:
                if btn.check_position(*pygame.mouse.get_pos()):
                    if btn.get_text().strip() == "Выйти из игры":
                        return True
                    if btn.get_text().strip() == "Вернуться в главное меню":
                        self.controller.set_current_window(self.menu)
                    if btn.get_text().strip() == "Начать с последней точки":
                        self.game = Game(self.controller, self.menu, self)
                        self.controller.set_current_window(self.game)

    def start(self, screen):
        screen.fill((0, 0, 0))
        self.btns = []
        x, y = pygame.mouse.get_pos()
        cnt = 0
        for i in range(3):
            self.create_button(self.w // 2 - self.start_image.get_rect().w // 2 - 70, 100 + 120 * i, self.btn_names[i],
                               screen)
            if self.btns[i].check_position(x, y):
                cnt += 1
        if cnt > 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        screen.blit(self.start_image, (self.w // 2 - self.start_image.get_rect().w // 2, 0))


class Settings:
    def __init__(self, cntrl, come_back, menu):
        self.controller = cntrl
        self.come_back = come_back
        self.menu = menu
        self.draw_scroll_btns = None
        self.btns = []
        self.btn_names = ["Вернуться назад", "Главное меню"]
        self.graphs = ["Низкие", "Обычные", "Высокие", "СУПЕР-УЛЬТРА-МЕГА-ГРАФОН"]
        self.scroll_graph = Scroll_btns(self.graphs)

    def check_event(self, event, keys=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.btns:
                if btn.check_position(*pygame.mouse.get_pos()):
                    if btn.get_text().strip() == "Вернуться назад":
                        self.controller.set_current_window(self.come_back)
                    if btn.get_text().strip() == "Главное меню":
                        self.controller.set_current_window(self.menu)
                    if btn.get_text().strip() == self.graphs[0]:
                        self.draw_scroll_btns = (260 + len("Настройки графики") * 15, 70, len("СУПЕР-УЛЬТРА-МЕГА-ГРАФОН") * 15, 40)
            if not self.scroll_graph.check_position(*pygame.mouse.get_pos()):
                self.draw_scroll_btns = None
            else:
                self.draw_scroll_btns = (260 + len("Настройки графики") * 15, 70, len("СУПЕР-УЛЬТРА-МЕГА-ГРАФОН") * 15, 40)

    def create_button(self, x, y, w, h, text, screen, size=0, add_to_lst=True):
        btn = Button(x, y, w, h)
        background = btn.check_position(*pygame.mouse.get_pos())
        btn.draw_btn_and_txt(text, screen, background, size=size)
        if add_to_lst:
            self.btns.append(btn)

    def start(self, screen):
        screen.fill((0, 0, 0))
        self.btns = []
        x, y = pygame.mouse.get_pos()
        cnt = 0
        font = pygame.font.Font(None, 30)
        text = font.render("Настройки графики", 1, (255, 255, 255))
        screen.blit(text, (260, 70))

        if self.draw_scroll_btns:
            self.scroll_graph.draw_btn_choice(screen, *self.draw_scroll_btns, 30)
        else:
            self.create_button(260 + len("Настройки графики") * 15, 70, len("СУПЕР-УЛЬТРА-МЕГА-ГРАФОН") * 15, 40,
                               self.graphs[0], screen, size=30)
            pygame.draw.rect(screen, (255, 255, 255),
                             (260 + len("Настройки графики") * 15, 70, len("СУПЕР-УЛЬТРА-МЕГА-ГРАФОН") * 15, 40),
                             width=3)
        for i in range(len(self.btn_names)):
            self.create_button(25, 20 + 110 * i, 200, 100, self.btn_names[i], screen)
            if self.btns[i].check_position(x, y):
                cnt += 1
        if self.btns[0].check_position(x, y):
            cnt += 1
        if cnt > 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class Menu:
    def __init__(self, w, h, cntrl):
        pygame.init()
        self.start_image = load_image("screen.jpg")
        self.w = w
        self.h = h
        self.btns = []
        self.btn_names = [" Начать игру ", "  Настройки  ", "Выйти из игры"]
        self.controller = cntrl
        self.go = Game_Over(w, h, cntrl, self)
        self.game = Game(cntrl, self, self.go)
        self.dialog = Dialog_window(self.w, self.h, cntrl, self)
        self.settings = Settings(self.controller, self, self)

    def create_button(self, x, y, text, screen):
        btn = Button(x, y, 500, 100)
        background = btn.check_position(*pygame.mouse.get_pos())
        btn.draw_btn_and_txt(text, screen, background)
        self.btns.append(btn)

    def check_event(self, event, keys=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.btns:
                if btn.check_position(*pygame.mouse.get_pos()):
                    if btn.get_text().strip() == "Выйти из игры":
                        self.controller.set_current_window(self.dialog)
                    if btn.get_text().strip() == "Настройки":
                        self.controller.set_current_window(self.settings)
                    if btn.get_text().strip() == "Начать игру":
                        self.go = Game_Over(self.w, self.h, self.controller, self)
                        self.game = Game(self.controller, self, self.go)
                        self.controller.set_current_window(self.game)

    def start(self, screen):
        screen.fill((0, 0, 0))
        self.btns = []
        x, y = pygame.mouse.get_pos()
        cnt = 0

        for i in range(3):
            self.create_button(25, 50 + 150 * i, self.btn_names[i], screen)
            if self.btns[i].check_position(x, y):
                cnt += 1

        if cnt > 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        screen.blit(self.start_image, (self.w // 1.8, 0))
