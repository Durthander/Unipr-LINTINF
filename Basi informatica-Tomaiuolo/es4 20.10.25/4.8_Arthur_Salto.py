from actor import Arena, Actor, Point

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

    def pos(self) -> Point:
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



def tick():
    g2d.clear_canvas()
    for a in arena.actors():
        g2d.draw_image("ghosts-goblins.png", a.pos(), a.sprite(), a.size())
    arena.tick(g2d.current_keys())


def main():
    global g2d, arena
    import g2d
    arena = Arena((800, 300))
    arena.spawn(Arthur((400, 269)))
    g2d.init_canvas(arena.size())
    g2d.main_loop(tick)


if __name__ == "__main__":
    main()
