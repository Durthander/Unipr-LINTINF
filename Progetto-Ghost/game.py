from random import randint

from actor import Actor, Arena, check_collision

# Mondo e Vista
ARENA_W, ARENA_H = 3569, 224
VIEW_W, VIEW_H = 600, 224
view_x, view_y = 0, 0


class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx = 4
        self._dy = 0
        self._gravity = 0.75
        self._jump_strength = -7
        self._run_tick = 0
        self._throw_cd = 0
        self._throw_tick = 0
        self._throw_duration = 0
        self._crouched_throw = False
        self._bottom_y = self._y + 31
        self._state = "Idle"
        self._facing = "right"
        self._on_ground = False
        self._on_ladder = False
        self._ladder_obj = None
        self._climb_tick = 0
        self._climbing = False
        self._climb_facing = "right"
        self._exiting_top = False
        self._jump_running = False
        self._descending = False
        self._at_top = False  # Nuova variabile per tracciare se siamo in cima
    
    def move(self, arena: Arena):
        keys = arena.current_keys()
        
        # Blocca durante animazione lancio
        if self._state == "Throw":
            self._throw_duration -= 1
            if self._throw_duration <= 0:
                self._state = "Idle"
                self._throw_tick = 0
            return
        
        aw, ah = arena.size()
        
        # --- Controllo presenza scala (solo per rilevamento) ---
        self._on_ladder = False
        self._ladder_obj = None
        for other in arena.actors():
            if isinstance(other, Ladder):
                ox, oy = other.pos()
                ow, oh = other.size()
                px, py = self.pos()
                pw, ph = self.size()

                if (px + pw > ox and px < ox + ow and 
                    py + ph > oy and py < oy + oh):
                    self._on_ladder = True
                    self._ladder_obj = other
                    break
        
        # --- Gestione arrampicata attiva ---
        if self._climbing:
            # Se la scala è stata distrutta o rimossa
            if self._ladder_obj is None:
                self._climbing = False
                self._state = "Idle"
                return
            
            ladder_x, ladder_y = self._ladder_obj.pos()
            ladder_h = self._ladder_obj.size()[1]
            ladder_top = ladder_y
            ladder_bottom = ladder_y + ladder_h

            if self._exiting_top:
                # Continua l'animazione di uscita
                self._climb_tick += 1
                if self._climb_tick >= 12:
                    self._climbing = False
                    self._exiting_top = False
                    self._at_top = False
                    self._state = "Idle"
                    self._on_ground = True
                    self._climb_tick = 0
                    h = self.size()[1]
                    self._y = ladder_top - h
                    self._bottom_y = self._y + h
                self._dy = 0
                return

            # Movimento sulla scala
            moved = False
            if "ArrowUp" in keys:
                self._y -= 2
                self._climb_tick += 1
                moved = True
                self._descending = False

                # Raggiunto il top → inizia animazione uscita
                if self._y <= ladder_top + 5:
                    self._exiting_top = True
                    self._at_top = True
                    self._climb_tick = 0
                    self._y = ladder_top - 15
                    self._bottom_y = self._y + self.size()[1]

            if "ArrowDown" in keys:
                self._y += 2
                self._climb_tick += 1
                moved = True
                self._descending = True
                self._at_top = False

                # Raggiunto y = 193 - 30 (top corner di Arthur a y = 193)
                h = self.size()[1]
                if self._y >= 193 - h:
                    self._climbing = False
                    self._descending = False
                    self._state = "Idle"
                    self._on_ground = True
                    self._dy = 0
                    self._y = 193 - h
                    self._bottom_y = 193
                    self._climb_tick = 0
                    self._ladder_obj = None
                    self._at_top = False
                    return

            # Se non si preme niente, stai fermo
            if not moved:
                self._climb_tick = (self._climb_tick // 6) * 6

            self._dy = 0
            self._on_ground = False
            self._bottom_y = self._y + self.size()[1]
            return
        
        # === MOVIMENTO ORIZZONTALE ===
        moving = False
        if self._state != "Crouch":
            if "ArrowLeft" in keys:
                self._x -= self._dx
                self._facing = "left"
                moving = True
            if "ArrowRight" in keys:
                self._x += self._dx
                self._facing = "right"
                moving = True

        w, _ = self.size()
        self._x = max(0, min(self._x, aw - w))

        # === INGRESSO IN SCALATA ===
        # Ingresso normale dal basso con freccia SU
        if (not self._climbing and 
            self._on_ground and 
            self._on_ladder and 
            "ArrowUp" in keys):

            self._climbing = True
            self._state = "Climbing"
            self._dy = 0
            self._exiting_top = False
            self._at_top = False
            self._climb_tick = 0
            self._climb_facing = self._facing
            self._descending = False
            
            # Centra perfettamente sulla scala
            lx, _ = self._ladder_obj.pos()
            lw, _ = self._ladder_obj.size()
            self._x = lx + (lw - self.size()[0]) // 2
            return
        
        # Rientro dall'alto con freccia GIÙ
        # Controlla se Arthur è vicino a una scala dall'alto
        if not self._climbing and self._on_ground and "ArrowDown" in keys:
            for other in arena.actors():
                if isinstance(other, Ladder):
                    lx, ly = other.pos()
                    lw, lh = other.size()
                    px, py = self.pos()
                    pw, ph = self.size()
                    
                    # Verifica se Arthur è sopra la scala (entro un margine orizzontale)
                    if (px + pw > lx and px < lx + lw and 
                        py + ph >= ly - 5 and py + ph <= ly + 15):
                        
                        self._climbing = True
                        self._state = "Climbing"
                        self._dy = 0
                        self._exiting_top = False
                        self._at_top = False
                        self._climb_tick = 0
                        self._climb_facing = self._facing
                        self._descending = True
                        self._ladder_obj = other
                        
                        # Centra perfettamente sulla scala e posiziona appena sotto il top
                        self._x = lx + (lw - pw) // 2
                        self._y = ly + 2
                        self._bottom_y = self._y + ph
                        return

        # === CROUCH E JUMP ===
        if "ArrowDown" in keys and self._on_ground:
            self._state = "Crouch"
        elif "ArrowUp" in keys and self._on_ground:
            self._dy = self._jump_strength
            self._on_ground = False
            self._state = "Jumping"
            self._jump_running = moving
        elif self._on_ground:
            self._state = "Running" if moving else "Idle"
        
        # Cooldown lancio
        if self._throw_cd > 0:
            self._throw_cd -= 1

        # Lancio torcia
        if "f" in keys and self._throw_cd == 0:
            self._state = "Throw"
            self._throw_tick = 0
            self._throw_duration = 12
            w, h = self.size()
            start_x = self._x + w/2
            crouched_throw = ("ArrowDown" in keys)
            start_y = self._y + 5 if not crouched_throw else self._y + h - 10
            self._crouched_throw = crouched_throw
            arena.spawn(Torch((start_x, start_y), self._facing))
            self._throw_cd = 10

        # Gravità
        self._dy += self._gravity
        self._bottom_y += self._dy

        # Animazione corsa
        self._run_tick = (self._run_tick + 1) % 12 if self._state == "Running" else 0
        
        # Aggiorna Y
        _, curr_h = self.size()
        self._y = self._bottom_y - curr_h

        # Collisioni con piattaforme e lapidi
        self._on_ground = False
        old_bottom = self._bottom_y - self._dy

        for other in arena.actors():
            if isinstance(other, (Platform, Gravestone)) and check_collision(self, other):
                ox, oy = other.pos()
                ow, oh = other.size()
                
                player_center_x = self._x + w / 2
                player_center_y = self._bottom_y - curr_h / 2
                other_center_x = ox + ow / 2
                other_center_y = oy + oh / 2
                
                overlap_x = (w + ow) / 2 - abs(player_center_x - other_center_x)
                overlap_y = (curr_h + oh) / 2 - abs(player_center_y - other_center_y)
                
                if isinstance(other, Platform):
                    if old_bottom <= oy and self._dy > 0:
                        self._bottom_y = oy
                        self._y = oy - curr_h
                        self._dy = 0
                        self._on_ground = True
                        if self._state == "Jumping":
                            self._state = "Idle" if not moving else "Running"
                
                elif isinstance(other, Gravestone):
                    if overlap_x < overlap_y:
                        if player_center_x < other_center_x:
                            self._x = ox - w
                        else:
                            self._x = ox + ow
                    else:
                        if player_center_y < other_center_y:
                            self._bottom_y = oy
                            self._y = oy - curr_h
                            self._dy = 0
                            self._on_ground = True
                        else:
                            self._bottom_y = oy + oh + 1
                            self._y = self._bottom_y - curr_h
                            self._dy = 0

    def pos(self):
        return self._x, self._y

    def size(self):
        if self._state == "Climbing":
            if self._exiting_top:
                return (22, 25) if self._climb_tick < 6 else (22, 16)
            return (21, 30)
        if self._state == "Throw":
            if not self._crouched_throw:
                return (22,30) if self._throw_tick < 3 else (23,25)
            return (22,23) if self._throw_tick < 3 else (27,21)
        if self._state == "Idle":
            return (20, 31)
        if self._state == "Running":
            sizes = [(24, 28), (19, 32), (19, 31), (24, 29)]
            return sizes[(self._run_tick // 3) % 4]
        if self._state == "Jumping":
            return (32, 27) if self._jump_running else (27, 26)
        if self._state == "Crouch":
            return (22, 22)
        return (20, 31)

    def sprite(self):
        if self._state == "Climbing":
            if self._exiting_top:
                return (198, 132) if self._climb_facing == "right" else (292, 132) if self._climb_tick < 6 else (224, 133) if self._climb_facing == "right" else (266, 133)
            
            # Gestione animazione discesa
            frame = (self._climb_tick // 4) % 2
            if self._descending:
                if self._climb_facing == "right":
                    return (341, 133) if frame == 0 else (150, 133)
                else:
                    return (150, 133) if frame == 0 else (341, 133)
            else:
                if self._climb_facing == "right":
                    return (150, 133) if frame == 0 else (341, 133)
                else:
                    return (341, 133) if frame == 0 else (150, 133)
        
        if self._state == "Throw":
            self._throw_tick = min(self._throw_tick + 1, 6)
            frame = 0 if self._throw_tick < 3 else 1
            if self._crouched_throw:
                return [(75,140), (101,142), (415,140), (384,142)][frame + (2 if self._facing == "left" else 0)]
            else:
                return [(5,133), (30,138), (485,133), (459,138)][frame + (2 if self._facing == "left" else 0)]

        if self._state == "Idle":
            return (6, 43) if self._facing == "right" else (486, 43)
        if self._state == "Running":
            frames_right = [(40, 44), (66, 42), (88, 43), (109, 43)]
            frames_left = [(449, 44), (427, 42), (405, 43), (379, 43)]
            frame = (self._run_tick // 3) % 4
            return frames_right[frame] if self._facing == "right" else frames_left[frame]
        if self._state == "Jumping":
            if self._facing == "right":
                return (144,29) if self._jump_running else (180,29)
            else:
                return (336,29) if self._jump_running else (305,29)
        if self._state == "Crouch":
            return (223, 52) if self._facing == "right" else (267, 52)
        
        return (6, 43)

class Zombie(Actor):
    def __init__(self, pos, facing):
        self._x, top = pos
        self._ground_y = top + 31
        self._facing = facing
        self._state = "spawn"
        self._frame = 0
        self._walked = 0
        self._max_walk = randint(150, 300)
        self._dx = 2
    
    def calculate_spawn_position(arthur_pos, arthur_size, arena_size):
        ax, _ = arthur_pos
        awidth, _ = arthur_size
        aw, _ = arena_size
        
        can_spawn_left = ax - 50 > 0
        can_spawn_right = ax + awidth + 50 < aw
        
        if not can_spawn_left and not can_spawn_right:
            return None
        
        if can_spawn_left and can_spawn_right:
            spawn_side = "left" if randint(0, 1) == 0 else "right"
        elif can_spawn_left:
            spawn_side = "left"
        else:
            spawn_side = "right"
        
        if spawn_side == "left":
            offset = randint(50, min(200, int(ax)))
            x = ax - offset
            facing = "right"
        else:
            max_dist = aw - (ax + awidth)
            offset = randint(50, min(200, int(max_dist)))
            x = ax + offset
            facing = "left"
        
        return (x, facing)

    def move(self, arena):
        aw, ah = arena.size()
        old_ground = self._ground_y
        w, h = self.size()

        if self._state == "spawn":
            self._frame += 1
            if self._frame > 15:
                self._state = "walk"
                self._frame = 0

        elif self._state == "walk":
            self._x += self._dx if self._facing == "right" else -self._dx
            self._walked += self._dx
            self._frame = (self._frame + 1) % 30
            if self._walked >= self._max_walk:
                self._state = "sink"
                self._frame = 0

        elif self._state == "sink":
            self._frame += 1
            if self._frame > 15:
                arena.kill(self)
                return

        self._x = max(0, min(self._x, aw - w))

        self._ground_y = ah
        for other in arena.actors():
            if isinstance(other, (Platform, Gravestone)):
                ox, oy = other.pos()
                ow, _ = other.size()
                if self._x + w > ox and self._x < ox + ow and old_ground <= oy:
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
            frames = [((778, 88), (512, 88)), ((748, 85), (533, 85)), ((725, 73), (562, 73))]
            indice = 0 if self._frame <= 4 else (1 if self._frame <= 9 else 2)
        elif self._state == "walk":
            frames = [((699, 66), (585, 66)), ((677, 65), (610, 65)), ((654, 66), (631, 66))]
            indice = 0 if self._frame <= 9 else (1 if self._frame <= 19 else 2)
        else:
            frames = [((725, 73), (562, 73)), ((748, 85), (533, 85)), ((778, 88), (512, 88))]
            indice = 0 if self._frame <= 4 else (1 if self._frame <= 9 else 2)
        
        right, left = frames[indice]
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


class Ladder:
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 60
    
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
        self._w, self._h = 16, 16
    
    def move(self, arena: Arena): 
        pass
    def pos(self): 
        return (self._x, self._y)
    def size(self): 
        return (self._w, self._h)
    def sprite(self): 
        return None


class Torch(Actor):
    def __init__(self, pos, facing):
        self._x, self._y = pos
        self._facing = facing
        self._dx = 6 if facing == "right" else -6
        self._dy = -4
        self._gravity = 0.35
        self._frame = 0
        self._alive = True
        self._killed = False

    def move(self, arena):
        if not self._alive:
            arena.kill(self)
            return

        self._x += self._dx
        self._dy += self._gravity
        self._y += self._dy

        self._frame = (self._frame + 1) % 4

        px, py = self._x, self._y
        pw, ph = self.size()

        for other in arena.actors():
            ox, oy = other.pos()
            ow, oh = other.size()

            if isinstance(other, Zombie) and not self._killed:
                if px + pw > ox and px < ox + ow and py + ph > oy and py < oy + oh:
                    arena.kill(other)
                    self._killed = True
                    self._alive = False
                    return

            if isinstance(other, (Platform, Gravestone)):
                if px + pw > ox and px < ox + ow and py + ph > oy and py < oy + oh:

                    if isinstance(other, Platform):
                        flame_center_x = self._x + pw / 2
                        arena.spawn(Flame((flame_center_x, oy)))

                    self._alive = False
                    return

    def pos(self):
        return (self._x, self._y)

    def size(self):
        right_sizes = [(14, 13), (13, 15), (13, 15), (14, 13)]
        return right_sizes[self._frame]

    def sprite(self):
        right_frames = [(19, 401), (39, 399), (58, 399), (78, 399)]
        left_frames = [(479, 401), (460, 399), (441, 399), (420, 399)]
        return (right_frames if self._facing == "right" else left_frames)[self._frame]


class Flame(Actor):
    def __init__(self, pos):
        center_x, platform_y = pos
        self._center_x = center_x
        self._platform_y = platform_y
        self._tick = 0
        self._alive = True
        self._x_left = center_x
        self._y_top = platform_y - 31

    def move(self, arena):
        self._tick += 1
        if self._tick >= 60:
            arena.kill(self)
            return

        fw, fh = self.size()
        self._y_top = self._platform_y - fh
        self._x_left = self._center_x - fw / 2
        
        for other in arena.actors():
            if isinstance(other, Zombie):
                ox, oy = other.pos()
                ow, oh = other.size()
                if self._x_left + fw > ox and self._x_left < ox + ow and self._y_top + fh > oy and self._y_top < oy + oh:
                    arena.kill(other)

    def pos(self):
        return (self._x_left, self._y_top)

    def size(self):
        sizes = [(32,31),(24,24),(16,16),(10,9)]
        frame = self._tick % 12
        if frame < 4:
            return sizes[0]
        elif frame < 8:
            return sizes[1]
        elif frame < 10:
            return sizes[2]
        else:
            return sizes[3]

    def sprite(self):
        frames = [(117,428),(153,435),(210,443),(229,450)]
        frame = self._tick % 12
        if frame < 4:
            return frames[0]
        elif frame < 8:
            return frames[1]
        elif frame < 10:
            return frames[2]
        else:
            return frames[3]


def tick():
    global view_x
    aw, _ = arena.size()
    ax, _ = arthur.pos()

    view_x = int(ax - VIEW_W / 2)
    view_x = max(0, min(view_x, aw - VIEW_W))
    
    sfondo = "https://raw.githubusercontent.com/fondinfo/sprites/main/ghosts-goblins-bg.png"
    g2d.draw_image(sfondo, (-view_x - 2, -10), (ARENA_W, ARENA_H))

    if randint(1, 500) == randint(1,300):
        spawn_data = Zombie.calculate_spawn_position(arthur.pos(), arthur.size(), arena.size())
        if spawn_data:
            x, facing = spawn_data

            _, ah = arena.size()
            ground_y = ah
            for actor in arena.actors():
                if isinstance(actor, Platform):
                    px, py = actor.pos()
                    pw, _ = actor.size()
                    if px <= x <= px + pw:
                        ground_y = min(ground_y, py)
            
            arena.spawn(Zombie((x, ground_y - 31), facing))

    for actor in arena.actors():
        sprite = actor.sprite()
        if sprite != None:
            x, y = actor.pos()
            g2d.draw_image("ghosts-goblins.png", (x - view_x, y), sprite, actor.size())
        
    arena.tick(g2d.current_keys())


def main():
    global g2d, arena, arthur
    import g2d

    arena = Arena((ARENA_W, ARENA_H))
    
    platforms = [
        (1, 193, 1665, 48),
        (1794, 193, 160, 48),
        (1986, 193, 32, 48),
        (2050, 193, 400, 48),
        (2482, 193, 224, 48),
        (2738, 193, 848, 48),
        (595, 113, 125, 17),
        (738, 113, 176, 17),
        (930, 113, 143, 17),
        (1090, 113, 44, 17)
    ]                   

    for p in platforms:
        arena.spawn(Platform(p))
    
    gravestones = [
        (59 - 10, 177),
        (251 - 10, 177),
        (539 - 10, 177),
        (763 - 10, 177),
        (971 - 10, 177),
        (1115 - 10, 177),
        (1531 - 10, 177),
        (875 - 10, 97),
    ]

    for g in gravestones:
        arena.spawn(Gravestone(g))
    
    stairs = [
        (722, 113),
        (914, 113),
        (1074, 113)
    ]
    
    for s in stairs:
        arena.spawn(Ladder(s))

    arthur = Arthur((400, 161))
    arthur._dy = 0.1
    arena.spawn(arthur)

    g2d.init_canvas((VIEW_W, VIEW_H), 2)
    g2d.main_loop(tick)


if __name__ == "__main__":
    main()