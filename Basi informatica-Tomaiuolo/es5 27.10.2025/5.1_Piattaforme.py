from random import randint

from actor import Actor, Arena


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
        self._w, self._h = 20, 31  # dimensione iniziale

    def move(self, arena: Arena):
        keys = arena.current_keys()
        aw, ah = arena.size()
        moving = False
        old_x, old_y = self._x, self._y

        # movimento destra/sinistra
        if "ArrowLeft" in keys:
            self._x -= self._dx
            self.facing = "left"
            moving = True
        if "ArrowRight" in keys:
            self._x += self._dx
            self.facing = "right"
            moving = True

        # Crouch
        if "ArrowDown" in keys and self.on_ground:
            if self._state != "Crouch":  # entra nel crouch
                self._y += (self._h - 22)     # compensa altezza
                self._h = 22                 
            self._state = "Crouch"
        else:
            if self._state == "Crouch":  # uscita dal crouch
                self._y -= (31 - self._h)  # riporta in piedi
                self._h = 31
            # salto
            if "ArrowUp" in keys and self.on_ground:
                self._dy = self.jump_strength
                self.on_ground = False
                self._state = "Jumping"
            elif moving and self.on_ground:
                self._state = "Running"
            elif self.on_ground:
                self._state = "Idle"

        # gravità
        if not self.on_ground:
            self._dy += self.gravity
            self._y += self._dy
            # quando tocca terra
            if self._y >= ah - self._h:
                self._y = ah - self._h
                self._dy = 0
                self.on_ground = True
                # atterraggio fluido: torna a Idle solo dopo il contatto
                self._state = "Idle"

        # bordo
        self._x = max(0, min(self._x, aw - self._w))

        if self._state == "Running":
            self.run_tick = (self.run_tick + 1) % 16
        else:
            self.run_tick = 0

        # risoluzione collisioni con piattaforme e lapidi
        # usa posizione precedente per capire la direzione dell'impatto
        for other in arena.collisions():
            if isinstance(other, Platform) or isinstance(other, Gravestone):
                ox, oy = other.pos()
                ow, oh = other.size()
                ax, ay = self._x, self._y
                awi, ahi = self.size()

                prev_bottom = old_y + ahi
                platform_top = oy
                # atterraggio dall'alto
                if self._dy >= 0 and prev_bottom <= platform_top and ay + ahi >= platform_top:
                    self._y = platform_top - ahi
                    self._dy = 0
                    self.on_ground = True
                    if self._state == "Jumping":
                        self._state = "Idle"
                    continue

                # solidità laterale: solo per Gravestone
                if isinstance(other, Gravestone):
                    prev_right = old_x + awi
                    prev_left = old_x
                    right = ax + awi
                    left = ax
                    other_left = ox
                    other_right = ox + ow
                    # impatto da sinistra
                    if prev_right <= other_left and right > other_left:
                        self._x = other_left - awi
                    # impatto da destra
                    elif prev_left >= other_right and left < other_right:
                        self._x = other_right

    def pos(self):
        return self._x, self._y

    def size(self):
        if self._state == "Idle":
            return (20, 31)
        if self._state == "Running":
            frame = (self.run_tick // 4) % 4
            if frame == 0:
                return (24, 28)
            if frame == 1:
                return (19, 32)
            if frame == 2:
                return (19, 31)
            return (24, 29)
        if self._state == "Jumping":
            # due frame: salita e discesa
            if self._dy < -1:   # salita
                return (32, 27)
            else:               # discesa
                return (27, 26)
        if self._state == "Crouch":
            return (22, 22)
        return (20, 31)

    def sprite(self):
        if self._state == "Idle":
            if self.facing == "right":
                return (6, 43)
            return (486, 43)

        if self._state == "Running":
            frame = (self.run_tick // 4) % 4
            if self.facing == "right":
                if frame == 0:
                    return (40, 44)
                if frame == 1:
                    return (66, 42)
                if frame == 2:
                    return (88, 43)
                return (109, 43)
            else:
                if frame == 0:
                    return (449, 44)
                if frame == 1:
                    return (427, 42)
                if frame == 2:
                    return (405, 43)
                return (379, 43)

        if self._state == "Jumping":
            if self._dy < -1:  # salita
                if self.facing == "right":
                    return (144, 29)
                else:
                    return (336, 29)
            else:  # discesa
                if self.facing == "right":
                    return (180, 29)
                else:
                    return (305, 29)

        if self._state == "Crouch":
            if self.facing == "right":
                return (223, 52)
            return (267, 52)

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

        if self._state == "spawn":
            self._frame += 1
            if self._frame > 15:
                self._state = "walk"
                self._frame = 0
        elif self._state == "walk":
            if self._facing == "right":
                self._x += self._speed
            else:
                self._x -= self._speed
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

        # atterra sulle piattaforme; ignora le lapidi
        for other in arena.collisions():
            if isinstance(other, Platform):
                oy = other.pos()[1]
                self._ground_y = min(self._ground_y, oy)

    def pos(self):
        _, h = self.size()
        return self._x, self._ground_y - h

    def size(self):
        if self._state == "spawn":
            if self._frame <= 4:
                return (16, 9)
            if self._frame <= 9:
                return (25, 12)
            return (19, 24)
        if self._state == "walk":
            if self._frame <= 9:
                return (22, 31)
            if self._frame <= 19:
                return (19, 32)
            return (21, 31)
        if self._frame <= 4:
            return (19, 24)
        if self._frame <= 9:
            return (25, 12)
        return (16, 9)

    def sprite(self):
        if self._state == "spawn":
            if self._frame <= 4:
                right = (778, 88)
                left = (512, 88)
            elif self._frame <= 9:
                right = (748, 85)
                left = (533, 85)
            else:
                right = (725, 73)
                left = (562, 73)
        elif self._state == "walk":
            if self._frame <= 9:
                right = (699, 66)
                left = (585, 66)
            elif self._frame <= 19:
                right = (677, 65)
                left = (610, 65)
            else:
                right = (654, 66)
                left = (631, 66)
        else:
            if self._frame <= 4:
                right = (725, 73)
                left = (562, 73)
            elif self._frame <= 9:
                right = (748, 85)
                left = (533, 85)
            else:
                right = (778, 88)
                left = (512, 88)
        if self._facing == "right":
            return right
        return left


class Platform(Actor):
    def __init__(self, rect):
        self._x, self._y, self._w, self._h = rect

    def move(self, arena: Arena):
        # immobile, fa solo da ostacolo
        pass

    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        # parte dello sfondo; non viene disegnata
        return None


class Gravestone(Actor):
    def __init__(self, rect):
        self._x, self._y, self._w, self._h = rect

    def move(self, arena: Arena):
        # immobile, solida per Arthur ma attraversabile dagli zombie
        pass

    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        # parte dello sfondo; non viene disegnata
        return None


def maybe_spawn_zombie():
    if randint(1, 500) != 1:
        return

    ax, _ = arthur.pos()
    aw, ah = arena.size()
    awidth, _ = arthur.size()

    spawn_side = None
    if ax - 50 > 0 and ax + awidth + 50 < aw:
        if randint(0, 1) == 0:
            spawn_side = "left"
        else:
            spawn_side = "right"
    elif ax - 50 > 0:
        spawn_side = "left"
    elif ax + awidth + 50 < aw:
        spawn_side = "right"

    if spawn_side is None:
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
    g2d.clear_canvas()
    maybe_spawn_zombie()
    

    for actor in arena.actors():
        sprite = actor.sprite()
        if sprite is not None:
            g2d.draw_image("ghosts-goblins.png", actor.pos(), sprite, actor.size())
        else:
            g2d.set_color((20,20,20))
            g2d.draw_rect(actor.pos(), actor.size())

    arena.tick(g2d.current_keys())


def main():
    global g2d, arena, arthur
    import g2d

    arena = Arena((1000, 300))
    arthur = Arthur((400, 269))
    arena.spawn(arthur)
    # piattaforme di prova (rettangoli invisibili)
    arena.spawn(Platform((100, 220, 150, 10)))
    arena.spawn(Platform((350, 180, 120, 10)))
    # lapidi: solide per Arthur, attraversabili dagli zombie
    arena.spawn(Gravestone((270, 270, 30, 30)))
    arena.spawn(Gravestone((720, 269-31+9, 20, 31)))
    g2d.init_canvas(arena.size())
    g2d.main_loop(tick)


if __name__ == "__main__":
    main()
