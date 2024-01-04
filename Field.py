from BaseObject import BaseObject


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))



def generate_level(level, group, all_sprites):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                BaseObject(group, 'wall', x, y, all_sprites)
            elif level[y][x] == 'F':
                BaseObject(group, 'floor', x, y, all_sprites)
    # вернем игрока, а также размер поля в клетках
    return x, y
