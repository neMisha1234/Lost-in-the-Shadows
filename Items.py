import os
import sqlite3
import pygame
from load_image import load_image

pygame.init()
pygame.font.SysFont('arial', 36)

items_descrip = {"Броня Титана": """Броня Титана – могучий&артефакт, некогда&принадлежащий одному&из владельцев&этого замка.&&На кирасе начерчено&предложение:&«Absolut defense»&&Способности:&&Absolute Defense:& увеличивает&сопротивление урону&на 75%, а также&уменьшает скорость&игрока в два раза.
                """, "Клеймор": "Клеймор-сильнейший из&существующих мечей, &повезло!, а нет&несовсем, меч ПРОКЛЯТ.&&Когда вы держите&меч в руках вы&слышыте шепот: &«Are you wanna&DEADLY power?»&&Способности:&&Deadly power:&увеличивает весь&урон игрока в два&раза, взамен&уменьшает&сопротивление&игрока на 100%.",
                 "Волшебный Посох": "РАЗРАБОТЧИК ПОД&&КОНЕЦ СРОКОВ&СДАЧИ СОВСЕМ&&ДОЛБАНУЛСЯ?&&Да. Предмет дает&20 урона и&увеличивает скорость&атаки в два раза&, взамен ничего не&забирает. Где баланс?&Явно не тут.&&Способности:&&Awama Kidawra:&увеливает урон на&20 и скорость атки&в два раза"}


class Item:
    def __init__(self, name, in_invent, image_name):
        self.name = name
        self.in_invent = in_invent
        self.image_name = image_name

    def add_to_db(self):
        con = sqlite3.connect(os.path.join("data/Items.sqlite"))
        cur = con.cursor()
        if (self.name, ) not in cur.execute("""SELECT name FROM all_items""").fetchall():
            cur.execute("""INSERT INTO all_items (name, in_invent, image) VALUES (?, ?, ?)""", (self.name, self.in_invent, self.image_name))
            con.commit()


class Item_description:
    def __init__(self, item, x, y):
        self.item = item[0]
        self.image = load_image(item[1], colorkey=(255, 255, 255))
        self.w, self.h = 255, 240
        self.x, self.y  = x, y
        descrip = items_descrip[self.item]
        descrip = descrip.split("&")
        self.text = []
        f = pygame.font.Font(None, 18)
        for el in descrip:
            self.text.append(f.render(el, True, (255, 255, 255)))

    def check_coords(self, coords):
        x, y = coords
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            return True

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            if self.x < x < self.x + 100 and self.y + self.h - 20 < y < self.y + self.h:
                return True

    def draw_on_screen(self, screen):
        temp_screen = pygame.surface.Surface((self.w, self.h))
        pygame.draw.rect(temp_screen, (255, 255, 255), (0, 0, self.w, self.h), width=5)
        pygame.draw.line(temp_screen, (255, 255, 255), (100, 0), (100, 500), width=2)
        pygame.draw.rect(temp_screen, (255, 255, 255), (0, 0, 100, 100), width=3)
        self.image = pygame.transform.scale(self.image, (95, 95))
        temp_screen.blit(self.image, (5, 5, 95, 95))
        for i in range(len(self.text)):
            temp_screen.blit(self.text[i], (103, 15 + i * 10))
        pygame.draw.rect(temp_screen, (255, 0, 0), (0, 220, 100, 20))
        f = pygame.font.Font(None, 18)
        close = f.render("Закрыть", True, (255, 255, 255))
        temp_screen.blit(close, (25, 223.5))
        screen.blit(temp_screen, (self.x, self.y))


class Current_inventory:
    def __init__(self, x, y, cell_size, hero):
        self.x, self.y, self.cell_size = x, y, cell_size
        self.hero = hero
        self.items = []
        self.load_from_db()

    def check_coords(self, coords):
        x, y = coords
        if self.x < x < self.x + 2 * self.cell_size and self.y < y < self.y + self.cell_size:
            return ((x - self.x) // self.cell_size, (y - self.y) // self.cell_size)

    def draw_on_screen(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.cell_size, self.cell_size), width=3)
        pygame.draw.rect(screen, (255, 255, 255), (self.x + self.cell_size, self.y, self.cell_size, self.cell_size), width=3)
        for i in range(len(self.items)):
            im = load_image(self.items[i][1], colorkey=(255, 255, 255))
            im = pygame.transform.scale(im, (self.cell_size - 10, self.cell_size - 10))
            screen.blit(im, (self.x + self.cell_size * i + 5, self.y + 5))

    def add_item(self, item, image):
        if len(self.items) < 2 and item not in map(lambda x: x[0], self.items):
            self.items.append((item, image))
            con = sqlite3.connect("data/Items.sqlite")
            cur = con.cursor()
            cur.execute("""UPDATE all_items SET in_cur_invent = 1 WHERE name = ?""", (item, ))
            con.commit()

    def delete_item(self, item):
        items_function["standart"](self.hero)
        index = list(map(lambda x: x[0], self.items)).index(item)
        self.items.pop(index)
        con = sqlite3.connect("data/Items.sqlite")
        cur = con.cursor()
        cur.execute("""UPDATE all_items SET in_cur_invent = 0 WHERE name = ?""", (item,))
        con.commit()


    def load_from_db(self):
        con = sqlite3.connect("data/Items.sqlite")
        cur = con.cursor()
        self.items = cur.execute("""SELECT name, image FROM all_items WHERE in_cur_invent > 0""").fetchall()


class Inventory:
    def __init__(self, x, y, cell_size, w, h):
        self.inventory = []
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cell_size = cell_size
        self.load_from_db()

    def load_from_db(self):
        con = sqlite3.connect("data/Items.sqlite")
        cur = con.cursor()
        self.inventory = cur.execute("""SELECT name, image FROM all_items WHERE in_invent > 0""").fetchall()

    def check_coords(self, coords):
        x, y = coords
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            t_x = (x - self.x) // self.cell_size
            t_y = (y - self.y) // self.cell_size
            return (t_x, t_y)

    def get_invent(self):
        return self.inventory

    def draw_on_screen(self, screen):
        invent = self.inventory.copy()
        for row in range(self.w // self.cell_size):
            for col in range(self.h // self.cell_size):
                pygame.draw.rect(screen, (255, 255, 255), (self.x + self.cell_size * row, self.y + self.cell_size * col, self.cell_size, self.cell_size), width=3)
                if invent:
                    im = load_image(invent[0][1], colorkey=(255, 255, 255))
                    invent.pop(0)
                    im = pygame.transform.scale(im, (self.cell_size - 10, self.cell_size - 10))
                    screen.blit(im, (self.x + self.cell_size * col + 5, self.y + self.cell_size * row + 5))


class Item_dialog:
    def __init__(self, x, y, cur_inv, t, txt1, txt2, type):
        self.w, self.h = 48, 27
        self.x, self.y = x, y
        self.dialog = pygame.surface.Surface((self.w, self.h))
        self.current_invent = cur_inv
        self.t = t
        self.txt1, self.txt2 = txt1, txt2
        self.type = type
        self.it_desc = None

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            if self.x < x < self.x + self.w and self.y < y < self.y + 12:
                if self.type:
                    self.current_invent.delete_item(self.t[0])
                else:
                    self.current_invent.add_item(*self.t)
                return True
            elif self.x < x < self.x + self.w and self.y + 12 < y < self.y + self.h:
                self.it_desc = Item_description(self.t, 625, 10)
            else:
                return True

    def create_btn(self, text, back=False):
        f1 = pygame.font.Font(None, 18)
        if back:
            text1 = f1.render(text, True, (0, 0, 0), (0, 140, 240))
        else:
            text1 = f1.render(text, True, (0, 0, 0))
        return text1

    def draw(self, screen):
        self.dialog.fill((255, 255, 255))
        x, y = pygame.mouse.get_pos()
        if self.x < x < self.x + self.w and self.y < y < self.y + 12:
            txt1 = self.create_btn(f" {self.txt1}", back=True)
        else:
            txt1 = self.create_btn(f" {self.txt1}")

        if self.x < x < self.x + self.w and self.y + 12 < y < self.y + self.h:
            txt2 = self.create_btn(f" {self.txt2}  ", back=True)
        else:
            txt2 = self.create_btn(f" {self.txt2}  ")

        self.dialog.blit(txt1, (0, 0))
        pygame.draw.rect(self.dialog, (0, 0, 0), (0, txt1.get_height(), self.w, 3))
        self.dialog.blit(txt2, (0, 15))
        screen.blit(self.dialog, (self.x, self.y))


titan_cuiras = Item("Броня Титана", 1, "titan_ciras.png")
titan_cuiras.add_to_db()
claimore = Item("Клеймор", 1, "claimore.png")
claimore.add_to_db()
magick_wand = Item("Волшебный Посох", 1, "magicwand.png")
magick_wand.add_to_db()

def absolute_defense(hero):
    hero.damage_resist += 75
    hero.vx /= 2

def set_to_standart(hero):
    hero.damage_resist = 0
    hero.vx, hero.vy = 150, 50
    hero.damage = 25
    hero.attack_speed = 100

def deadly_power(hero):
    hero.damage_resist -= 100
    hero.damage *= 2

def awama_kidavra(hero):
    hero.attack_speed *= 2.5
    hero.damage += 20


items_function = {titan_cuiras.name: absolute_defense,
                  "standart": set_to_standart,
                  claimore.name: deadly_power,
                  magick_wand.name: awama_kidavra}
