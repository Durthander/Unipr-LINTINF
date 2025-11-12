from random import randint

from actor import Actor, Arena

# --- Parametri del mondo e della vista ---
ARENA_W, ARENA_H = 3569, 224
VIEW_W, VIEW_H = 600, 224
view_x, view_y = 0, 0


class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx = 4
        self._dy = 0
        self._state = "Idle"
        self.on_ground = True
        self.gravity = 0.5
        self.jump_strength = -7
        self.facing = "right"
        self.run_tick = 0
        self._w, self._h = 20, 31

    def move(self, arena: Arena):
        keys = arena.current_keys()
        aw, ah = arena.size()
        moving = False
        old_y = self._y
        _, prev_h = self.size()

        if "ArrowLeft" in keys:
            self._x -= self._dx
            self.facing = "left"
            moving = True
        if "ArrowRight" in keys:
            self._x += self._dx
            self.facing = "right"
            moving = True

        if "ArrowDown" in keys and self.on_ground:
            if self._state != "Crouch":
                self._y += (self._h - 22)
                self._h = 22
            self._state = "Crouch"
        else:
            if self._state == "Crouch":
                self._y -= (31 - self._h)
                self._h = 31

            if "ArrowUp" in keys and self.on_ground:
                self._dy = self.jump_strength
                self.on_ground = False
                self._state = "Jumping"
            elif moving and self.on_ground:
                self._state = "Running"
            elif self.on_ground:
                self._state = "Idle"

        if not self.on_ground:
            self._dy += self.gravity
            self._y += self._dy
            if self._y >= ah - self._h:
                self._y = ah - self._h
                self._dy = 0
                self.on_ground = True
                self._state = "Idle"

        self._x = max(0, min(self._x, aw - self._w))

        if self._state == "Running":
            self.run_tick = (self.run_tick + 1) % 16
        else:
            self.run_tick = 0

        _, curr_h = self.size()
        supported = False
        for other in arena.collisions():
            if isinstance(other, (Platform, Gravestone)):
                prev_bottom = old_y + prev_h
                curr_bottom = self._y + curr_h
                platform_top = other.pos()[1]

                if self._dy >= 0 and prev_bottom <= platform_top <= curr_bottom:
                    self._y = platform_top - curr_h
                    self._dy = 0
                    supported = True
                    self.on_ground = True
                    if self._state == "Jumping":
                        self._state = "Idle"

        if not supported and self._y < ah - self._h:
            self.on_ground = False

    def pos(self):
        return self._x, self._y

    def size(self):
        if self._state == "Idle":
            return (20, 31)

        if self._state == "Running":
            frame = (self.run_tick // 4) % 4
            if frame == 0: return (24, 28)
            if frame == 1: return (19, 32)
            if frame == 2: return (19, 31)
            return (24, 29)

        if self._state == "Jumping":
            if self._dy < -1: return (32, 27)
            return (27, 26)

        if self._state == "Crouch":
            return (22, 22)

        return (20, 31)

    def sprite(self):
        if self._state == "Idle":
            return (6, 43) if self.facing == "right" else (486, 43)

        if self._state == "Running":
            frame = (self.run_tick // 4) % 4
            if self.facing == "right":
                return [(40, 44), (66, 42), (88, 43), (109, 43)][frame]
            else:
                return [(449, 44), (427, 42), (405, 43), (379, 43)][frame]

        if self._state == "Jumping":
            if self._dy < -1:
                return (144, 29) if self.facing == "right" else (336, 29)
            else:
                return (180, 29) if self.facing == "right" else (305, 29)

        if self._state == "Crouch":
            return (223, 52) if self.facing == "right" else (267, 52)

        return (20, 31)


class Zombie(Actor):
    def __init__(self, pos, facing):
        self._x, top = pos
        self._ground_y = top + 31
        self._facing = facing
        self._state = "spawn"
        self._frame = 0
        self._walked = 0
        self._max_walk = randint(150, 300)
        self._speed = 2

    def move(self, arena):
        aw, ah = arena.size()
        old_ground = self._ground_y

        if self._state == "spawn":
            self._frame += 1
            if self._frame > 15:
                self._state = "walk"
                self._frame = 0

        elif self._state == "walk":
            self._x += self._speed if self._facing == "right" else -self._speed
            self._walked += self._speed
            self._frame = (self._frame + 1) % 30

            if self._walked >= self._max_walk:
                self._state = "sink"
                self._frame = 0

        elif self._state == "sink":
            self._frame += 1
            if self._frame > 15:
                arena.kill(self)
                return

        w, h = self.size()
        self._x = max(0, min(self._x, aw - w))
        self._ground_y = min(max(h, self._ground_y), ah)

        supported = False
        curr_bottom = self._ground_y
        for other in arena.collisions():
            if isinstance(other, (Platform, Gravestone)):
                platform_top = other.pos()[1]
                if old_ground <= platform_top <= curr_bottom:
                    self._ground_y = min(self._ground_y, platform_top)
                    supported = True

        if not supported:
            self._ground_y = ah

    def pos(self):
        _, h = self.size()
        return self._x, self._ground_y - h

    def size(self):
        if self._state == "spawn":
            if self._frame <= 4: return (16, 9)
            if self._frame <= 9: return (25, 12)
            return (19, 24)

        if self._state == "walk":
            if self._frame <= 9: return (22, 31)
            if self._frame <= 19: return (19, 32)
            return (21, 31)

        if self._frame <= 4: return (19, 24)
        if self._frame <= 9: return (25, 12)
        return (16, 9)

    def sprite(self):
        if self._state == "spawn":
            if self._frame <= 4:
                right, left = (778, 88), (512, 88)
            elif self._frame <= 9:
                right, left = (748, 85), (533, 85)
            else:
                right, left = (725, 73), (562, 73)

        elif self._state == "walk":
            if self._frame <= 9:
                right, left = (699, 66), (585, 66)
            elif self._frame <= 19:
                right, left = (677, 65), (610, 65)
            else:
                right, left = (654, 66), (631, 66)

        else:
            if self._frame <= 4:
                right, left = (725, 73), (562, 73)
            elif self._frame <= 9:
                right, left = (748, 85), (533, 85)
            else:
                right, left = (778, 88), (512, 88)

        return right if self._facing == "right" else left


class Platform:
    def __init__(self, rect):
        self._x, self._y, self._w, self._h = rect
    
    def move(self, arena: Arena): 
        pass
    def pos(self): 
        return (self._x, self._y)
    def size(self): 
        return (self._w, self._h)
    def sprite(self): 
        return None


class Gravestone:
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 24, 29
    
    def move(self, arena: Arena): pass
    def pos(self): return (self._x, self._y)
    def size(self): return (self._w, self._h)
    def sprite(self): return None


def maybe_spawn_zombie():
    if randint(1, 500) != 1: return

    ax, _ = arthur.pos()
    aw, ah = arena.size()
    awidth, _ = arthur.size()

    if ax - 50 > 0 and ax + awidth + 50 < aw:
        spawn_side = "left" if randint(0, 1) == 0 else "right"
    elif ax - 50 > 0:
        spawn_side = "left"
    elif ax + awidth + 50 < aw:
        spawn_side = "right"
    else:
        return

    if spawn_side == "left":
        offset = randint(50, min(200, int(ax)))
        zx = ax - offset
        facing = "right"
    else:
        max_dist = aw - (ax + awidth)
        offset = randint(50, min(200, int(max_dist)))
        zx = ax + offset
        facing = "left"

    zy = ah - 31
    arena.spawn(Zombie((zx, zy), facing))


def tick():
    global view_x, view_y

    aw, ah = arena.size()
    ax, _ = arthur.pos()

    view_x = int(ax - VIEW_W / 2)
    view_x = max(0, min(view_x, aw - VIEW_W))
    view_y = 0

    g2d.draw_image("ghosts-goblins-bg.png", (-view_x - 2, -10), (ARENA_W, ARENA_H))

    maybe_spawn_zombie()

    for actor in arena.actors():
        sprite = actor.sprite()
        x, y = actor.pos()
        screen_pos = (x - view_x, y - view_y)
        if sprite is not None:
            x, y = actor.pos()
            g2d.draw_image("ghosts-goblins.png",screen_pos, sprite, actor.size())
        else:
            g2d.draw_rect(screen_pos, actor.size())

    arena.tick(g2d.current_keys())


def main():
    global g2d, arena, arthur
    import g2d

    arena = Arena((ARENA_W, ARENA_H))
    arthur = Arthur((400, ARENA_H - 31))
    arena.spawn(arthur)

    # --- NUOVE PIATTAFORME ---
    arena.spawn(Platform((1, 192, 1665, 48)))
    arena.spawn(Platform((1794, 192, 160, 48)))
    arena.spawn(Platform((1986, 192, 32, 48)))
    arena.spawn(Platform((2050, 192, 400, 48)))
    arena.spawn(Platform((2482, 192, 224, 48)))
    arena.spawn(Platform((2738, 192, 848, 48)))

    ground_grave_y = ARENA_H - 29
    arena.spawn(Gravestone((200, ground_grave_y)))
    arena.spawn(Gravestone((500, ground_grave_y)))
    arena.spawn(Gravestone((750, ground_grave_y)))

    g2d.init_canvas((VIEW_W, VIEW_H))
    g2d.main_loop(tick)


if __name__ == "__main__":
    main()