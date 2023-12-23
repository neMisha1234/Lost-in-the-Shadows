class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def camera_configure(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

        l = min(0, l)
        l = max(-(camera.width - WIN_WIDTH), l)
        t = max(-(camera.height - WIN_HEIGHT), t)
        t = min(0, t)

        return Rect(l, t, w, h)


    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)
    camera.update(hero)
