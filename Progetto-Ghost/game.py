from random import randint
from actor import Actor, Arena, check_collision


# Mondo e Vista
ARENA_W, ARENA_H = 3569, 224
VIEW_W, VIEW_H = 600, 224


class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx = 4
        self._dy = 0.1
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
        self._at_top = False
        self._lives = 3
        self._blinking = 0
    
    def move(self, arena: Arena):
        if self._blinking > 0:
            self._blinking -= 1
            
        keys = arena.current_keys()
        
        # Blocca durante animazione lancio
        if self._state == "Throw":
            self._throw_duration -= 1
            if self._throw_duration <= 0:
                self._state = "Idle"
                self._throw_tick = 0
            return
        
        aw, ah = arena.size()
        
        # --- Controllo presenza scala (Detection) ---
        self._on_ladder = False
        self._ladder_obj = None
        for other in arena.actors():
            if isinstance(other, Ladder):
                ox, oy = other.pos()
                ow, oh = other.size()
                px, py = self.pos()
                pw, ph = self.size()

                # Rileva sovrapposizione con la scala
                if (px + pw > ox and px < ox + ow and 
                    py + ph > oy and py < oy + oh):
                    self._on_ladder = True
                    self._ladder_obj = other
                    break
        
        # --- Gestione arrampicata attiva ---
        if self._climbing:
            if self._ladder_obj is None:
                self._climbing = False
                self._state = "Idle"
                return
            
            ladder_x, ladder_y = self._ladder_obj.pos()
            ladder_h = self._ladder_obj.size()[1]
            ladder_top = ladder_y

            # Animazione automatica di uscita (Top Ladder) - RESA FLUIDA
            if self._exiting_top:
                self._climb_tick += 1
                self._y -= 2  
                self._bottom_y = self._y + self.size()[1]

                if self._climb_tick >= 12:
                    self._climbing = False
                    self._exiting_top = False
                    self._at_top = False
                    self._state = "Idle"
                    self._on_ground = True
                    self._climb_tick = 0
                    
                    # Allineamento finale preciso
                    h = self.size()[1]
                    self._y = ladder_top - h
                    self._bottom_y = ladder_top
                
                self._dy = 0
                return

            # Movimento manuale sulla scala
            moved = False
            if "ArrowUp" in keys:
                self._y -= 2
                self._climb_tick += 1
                moved = True
                self._descending = False

                # Inizia uscita solo quando la testa spunta bene sopra
                if self._y <= ladder_top - 8:
                    self._exiting_top = True
                    self._at_top = True
                    self._climb_tick = 0

            if "ArrowDown" in keys:
                self._y += 2
                self._climb_tick += 1
                moved = True
                self._descending = True
                self._at_top = False

                # Scendi dalla scala se tocchi il pavimento (193 è il suolo standard)
                h = self.size()[1]
                if self._y + h >= 193:
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

        # Memorizza posizione Y prima del movimento verticale
        old_y = self._y

        # === INGRESSO IN SCALATA (Dal Basso) ===
        if (not self._climbing and 
            self._on_ground and 
            self._on_ladder and 
            "ArrowUp" in keys):

            lx, ly = self._ladder_obj.pos()
            lw, lh = self._ladder_obj.size() # Variabili definite qui
            ladder_center_y = ly + (lh / 2)

            if self._bottom_y > ladder_center_y:
                self._climbing = True
                self._state = "Climbing"
                self._dy = 0
                self._exiting_top = False
                self._at_top = False
                self._climb_tick = 0
                self._climb_facing = self._facing
                self._descending = False
                self._x = lx + (lw - self.size()[0]) // 2
                return
        
        # === INGRESSO IN SCALATA (Dall'Alto) ===
        if not self._climbing and self._on_ground and "ArrowDown" in keys:
            for other in arena.actors():
                if isinstance(other, Ladder):
                    lx, ly = other.pos()
                    lw, lh = other.size()
                    px, py = self.pos()
                    pw, ph = self.size()
                    
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

        # Lancio torcia (Solo se a terra)
        if "f" in keys and self._throw_cd == 0 and self._on_ground:
            self._state = "Throw"
            self._throw_tick = 0
            self._throw_duration = 12
            w, h = self.size()
            start_x = self._x + w/2
            crouched_throw = ("ArrowDown" in keys)
            start_y = self._y + 5 if not crouched_throw else self._y + h - 20
            self._crouched_throw = crouched_throw
            arena.spawn(Torch((start_x, start_y), self._facing))
            self._throw_cd = 10

        # Gravità e Fisica
        self._dy += self._gravity
        self._bottom_y += self._dy
        self._run_tick = (self._run_tick + 1) % 12 if self._state == "Running" else 0
        
        # Calcola Y in base al nuovo bottom e all'altezza corrente dello sprite
        _, curr_h = self.size()
        self._y = self._bottom_y - curr_h

        # Collisioni Terreno
        self._on_ground = False
        # VECCHIO fondo prima del movimento verticale
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

    def hit(self, arena):
        """Gestione danni ricevuti da nemici"""
        if self._blinking == 0:
            self._blinking = 60
            self._lives -= 1
            if self._lives <= 0:
                arena.kill(self)

    def lives(self) -> int:
        return self._lives

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
        # Effetto blinking quando danneggiato
        if self._blinking > 0 and self._blinking % 4 < 2:
            return None
            
        if self._state == "Climbing":
            if self._exiting_top:
                return (198, 132) if self._climb_facing == "right" else (292, 132) if self._climb_tick < 6 else (224, 133) if self._climb_facing == "right" else (266, 133)
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
        if not can_spawn_left and not can_spawn_right: return None
        if can_spawn_left and can_spawn_right: spawn_side = "left" if randint(0, 1) == 0 else "right"
        elif can_spawn_left: spawn_side = "left"
        else: spawn_side = "right"
        
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
        w, h = self.size()

        if self._state == "spawn":
            self._frame += 1
            if self._frame > 15:
                self._state = "walk"
                self._frame = 0

        elif self._state == "walk":
            dx = self._dx if self._facing == "right" else -self._dx
            next_x = self._x + dx
            
            # Range di collisione orizzontale dopo il movimento
            next_x_start = next_x
            next_x_end = next_x + w
            
            # --- CONTROLLO BORDO/CONTINUITÀ PIATTAFORMA/SCALA ---
            has_ground = False
            
            if self._ground_y >= ah:
                has_ground = True
            else:
                # Ricerca di qualsiasi superficie sotto la nuova posizione orizzontale
                for other in arena.actors():
                    # Check contro Platform O Ladder
                    if isinstance(other, (Platform, Ladder)): 
                        ox, oy = other.pos()
                        ow, _ = other.size()
                        
                        # 1. Check Orizzontale (Overlap dopo il movimento):
                        if next_x_start < ox + ow and next_x_end > ox:
                            
                            # 2. Check Verticale (Altezza):
                            if abs(oy - self._ground_y) < 5:
                                has_ground = True
                                break
            
            if not has_ground:
                # Inverte la direzione se non c'è più terra
                self._facing = "left" if self._facing == "right" else "right"
            else:
                # Movimento normale
                self._x = next_x
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
        
        # Controllo collisione con Arthur
        for other in arena.actors():
            if isinstance(other, Arthur):
                if check_collision(self, other):
                    other.hit(arena)

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


class Eyeball(Actor):
    def __init__(self, pos, target: Actor):
        self._x, self._y = pos
        self._w, self._h = 8, 8
        tx, ty = target.pos()
        tw, th = target.size()
        target_center_x = tx + tw / 2
        target_center_y = ty + th / 2
        dx = target_center_x - self._x
        dy = target_center_y - self._y
        steps = max(abs(dx), abs(dy))
        speed = 4
        if steps > 0:
            self._dx = (dx / steps) * speed
            self._dy = (dy / steps) * speed
        else:
            self._dx, self._dy = 0, 0
        self._facing = "right" if self._dx >= 0 else "left"

    def move(self, arena: Arena):
        aw, ah = arena.size()
        self._x += self._dx
        self._y += self._dy
        if self._x < 0 or self._x > aw or self._y < 0 or self._y > ah:
            arena.kill(self)
            return
        for other in arena.actors():
            if isinstance(other, Arthur):
                if check_collision(self, other):
                    other.hit(arena)
                    arena.kill(self)
                    return

    def pos(self): return self._x, self._y
    def size(self): return self._w, self._h
    def sprite(self):
        if self._facing == "right": return (552, 219)
        else: return (746, 219)


class Plant(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 25
        self._shoot_timer = randint(60, 150)
        self._facing = "left"
        self._current_frame = 0
        # "Reverse" (X crescenti) -> Destra
        self._frames_right = [((564, 214), (16, 25)), ((582, 214), (16, 25)), ((600, 207), (16, 32)), ((618, 207), (16, 32)), ((636, 207), (16, 32))]
        # "Normal" (X decrescenti) -> Sinistra
        self._frames_left = [((726, 214), (16, 25)), ((708, 214), (16, 25)), ((690, 207), (16, 32)), ((672, 207), (16, 32)), ((654, 207), (16, 32))]

    def move(self, arena: Arena):
        arthur = None
        for a in arena.actors():
            if isinstance(a, Arthur):
                arthur = a
                break
        
        if arthur:
            ax, _ = arthur.pos()
            self._facing = "right" if ax > self._x else "left"
            
            # CONTROLLO RANGE: Spara solo se Arthur è entro 300px
            dist_x = abs(self._x - ax)
            if dist_x > VIEW_W / 2:
                return

        self._shoot_timer -= 1
        if self._shoot_timer > 40: self._current_frame = 0
        elif self._shoot_timer > 30: self._current_frame = 1
        elif self._shoot_timer > 20: self._current_frame = 2
        elif self._shoot_timer > 10: self._current_frame = 3
        else: self._current_frame = 4

        if self._shoot_timer <= 0:
            if arthur: self.shoot(arena, arthur)
            self._shoot_timer = randint(80, 180)

    def shoot(self, arena, target_actor):
        w, h = self.size()
        spawn_y = self.pos()[1] + 10
        spawn_x = self._x + w / 2
        arena.spawn(Eyeball((spawn_x, spawn_y), target_actor))

    def pos(self):
        # Allineamento al terreno (32px è l'altezza massima)
        max_h = 32
        current_h = self.size()[1]
        offset_y = max_h - current_h
        return self._x, self._y + offset_y

    def size(self):
        frames = self._frames_right if self._facing == "right" else self._frames_left
        return frames[self._current_frame][1]

    def sprite(self):
        frames = self._frames_right if self._facing == "right" else self._frames_left
        return frames[self._current_frame][0]


class Platform:
    def __init__(self, rect):
        self._x, self._y, self._w, self._h = rect
    def move(self, arena: Arena): pass
    def pos(self): return (self._x, self._y)
    def size(self): return (self._w, self._h)
    def sprite(self): return None


class Ladder:
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 60
    def move(self, arena: Arena): pass
    def pos(self): return (self._x, self._y)
    def size(self): return (self._w, self._h)
    def sprite(self): return None


class Gravestone:
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
    def move(self, arena: Arena): pass
    def pos(self): return (self._x, self._y)
    def size(self): return (self._w, self._h)
    def sprite(self): return None


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
        px, py, pw, ph = self._x, self._y, *self.size()

        for other in arena.actors():
            ox, oy = other.pos()
            ow, oh = other.size()
            # Aggiunto Plant per collisione torcia
            if isinstance(other, (Zombie, Plant)) and not self._killed:
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

    def pos(self): return (self._x, self._y)
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
        self._center_x, self._platform_y = center_x, platform_y
        self._tick = 0
        self._frames_data = [((117, 428), (32, 31)), ((153, 435), (24, 24)), ((210, 443), (16, 16)), ((229, 450), (10, 9))]
        self._anim_speed = 4
        self._max_duration = 12 * self._anim_speed
        fw, fh = self._frames_data[0][1]
        self._x_left, self._y_top = center_x - fw / 2, platform_y - fh

    def move(self, arena):
        self._tick += 1
        if self._tick >= self._max_duration:
            arena.kill(self)
            return
        fw, fh = self.size()
        self._y_top = self._platform_y - fh
        self._x_left = self._center_x - fw / 2
        for other in arena.actors():
            if isinstance(other, (Zombie, Plant)):
                ox, oy = other.pos()
                ow, oh = other.size()
                if (self._x_left + fw > ox and self._x_left < ox + ow and 
                    self._y_top + fh > oy and self._y_top < oy + oh):
                    arena.kill(other)

    def _get_current_frame_index(self):
        step = self._tick // self._anim_speed
        if step < 8: return step % 2
        else: return 2 + (step % 2)

    def pos(self): return (self._x_left, self._y_top)
    def size(self): return self._frames_data[self._get_current_frame_index()][1]
    def sprite(self): return self._frames_data[self._get_current_frame_index()][0]


# ========== GNGAME - Sottoclasse di Arena ==========
class GngGame(Arena):
    """Classe di gioco specializzata per Ghosts'n Goblins"""
    
    def __init__(self, time=180*30):  # 3 minuti = 180 secondi * 30 fps
        super().__init__((ARENA_W, ARENA_H))
        self._time = time  # Timer di gioco
        self._load_level("/Users/thiam/Unipr-LINTINF/Progetto-Ghost/Gng_map.csv")
        # View tracking
        self._view_x = 0
        
    def _load_level(self, config_file):
        """Carica il livello da file CSV"""
    
        with open(config_file, 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            
            parts = [p.strip() for p in line.split(',')]
            entity_type = parts[0].lower()
            
            if entity_type == 'arthur':
                # arthur, x, y
                x, y = float(parts[1]), float(parts[2])
                self._arthur = Arthur((x, y))
                self.spawn(self._arthur)
            
            elif entity_type == 'platform':
                # platform, x, y, width, height
                x = float(parts[1])
                y = float(parts[2])
                w = float(parts[3])
                h = float(parts[4])
                self.spawn(Platform((x, y, w, h)))
            
            elif entity_type == 'gravestone':
                # gravestone, x, y
                x, y = float(parts[1]), float(parts[2])
                self.spawn(Gravestone((x, y)))
            
            elif entity_type == 'ladder':
                # ladder, x, y
                x, y = float(parts[1]), float(parts[2])
                self.spawn(Ladder((x, y)))
            
            elif entity_type == 'plant':
                # plant, x, y
                x, y = float(parts[1]), float(parts[2])
                self.spawn(Plant((x, y)))

    def get_arthur(self):
        """Restituisce il riferimento ad Arthur"""
        return self._arthur
    
    def get_view_x(self):
        """Restituisce la posizione orizzontale della vista"""
        return self._view_x
    
    def update_view(self):
        """Aggiorna la posizione della camera seguendo Arthur"""
        aw, _ = self.size()
        ax, _ = self._arthur.pos()
        self._view_x = int(ax - VIEW_W / 2)
        self._view_x = max(0, min(self._view_x, aw - VIEW_W))
    
    def spawn_random_zombie(self):
        """Spawn casuale di zombie"""
        spawn_data = Zombie.calculate_spawn_position(
            self._arthur.pos(), 
            self._arthur.size(), 
            self.size()
        )
        if spawn_data:
            x, facing = spawn_data
            _, ah = self.size()
            ground_y = ah
            
            # Trova la piattaforma più vicina sotto lo spawn
            for actor in self.actors():
                if isinstance(actor, Platform):
                    px, py = actor.pos()
                    pw, _ = actor.size()
                    if px <= x <= px + pw:
                        ground_y = min(ground_y, py)
            
            self.spawn(Zombie((x, ground_y - 31), facing))
    
    def lives(self) -> int:
        """Restituisce le vite rimanenti di Arthur"""
        if self._arthur:
            return self._arthur.lives()
        return 0
    
    def time(self) -> int:
        """Restituisce il tempo rimanente in tick"""
        return self._time - self.count()
    
    def game_over(self) -> bool:
        """Verifica se il gioco è finito (sconfitta)"""
        return self.lives() <= 0
    
    def game_won(self) -> bool:
        """Verifica se il gioco è vinto (sopravvissuto 3 minuti)"""
        return self.time() <= 0 and self.lives() > 0


# ========== GNGGUI - Interfaccia grafica ==========
class GngGui:
    """Classe per la rappresentazione grafica del gioco"""
    
    def __init__(self):
        self._game = GngGame()
        g2d.init_canvas((VIEW_W, VIEW_H), 2)
        
        # Sprite per i numeri (0-9)
        self._digit_sprites = {
            '0': ((658, 685), (7, 8)),
            '1': ((668, 685), (4, 8)),
            '2': ((676, 685), (7, 8)),
            '3': ((685, 685), (7, 8)),
            '4': ((694, 685), (7, 8)),
            '5': ((703, 685), (6, 8)),
            '6': ((712, 685), (6, 8)),
            '7': ((721, 685), (7, 8)),
            '8': ((730, 685), (7, 8)),
            '9': ((740, 685), (6, 8))
        }
        
        g2d.main_loop(self.tick)
    
    def _draw_number(self, number, x, y):
        """Disegna un numero usando gli sprite"""
        num_str = str(number)
        current_x = x
        for digit in num_str:
            if digit in self._digit_sprites:
                sprite_pos, sprite_size = self._digit_sprites[digit]
                g2d.draw_image("ghosts-goblins.png", (current_x, y), sprite_pos, sprite_size)
                current_x += sprite_size[0] + 1  # Spaziatura tra cifre
    
    def _draw_hud(self):
        """Disegna l'HUD con sprite (vite e tempo)"""
        hud_y = 10
        
        # Disegna "TIME"
        g2d.draw_image("ghosts-goblins.png", (10, hud_y), (624, 676), (32, 8))
        
        # Disegna il tempo rimanente (in secondi)
        time_remaining = max(0, self._game.time() // 30)
        self._draw_number(time_remaining, 45, hud_y)
        
        # Disegna le vite rimanenti come icone di Arthur
        lives = self._game.lives()
        lives_x_start = 10  # Posizione a destra
        for i in range(lives):
            x = lives_x_start + (i * 16)  # Spaziatura tra le icone
            g2d.draw_image("ghosts-goblins.png", (x, 210), (696, 696), (13, 13))
    
    def tick(self):
        """Funzione chiamata ad ogni frame"""
        view_x = self._game.get_view_x()
        
        # Disegna sfondo
        sfondo = "https://raw.githubusercontent.com/fondinfo/sprites/main/ghosts-goblins-bg.png"
        g2d.draw_image(sfondo, (-view_x - 2, -10), (ARENA_W, ARENA_H))
        
        # Spawn casuale zombie
        if randint(1, 150) == 1:
            self._game.spawn_random_zombie()
        
        # Disegna tutti gli attori
        for actor in self._game.actors():
            sprite = actor.sprite()
            if sprite is not None:
                x, y = actor.pos()
                g2d.draw_image("ghosts-goblins.png", (x - view_x, y), sprite, actor.size())
            # else:
            #     # x, y = actor.pos()
            #     # g2d.set_color((111,111,111))
            #     # g2d.draw_rect((x - view_x, y), actor.size())
            #     return
        # Disegna HUD con sprite
        self._draw_hud()
        
        # Verifica condizioni di fine gioco
        if self._game.game_over():
            g2d.alert("Game Over!")
            g2d.close_canvas()
        elif self._game.game_won():
            g2d.alert("You Won!")
            g2d.close_canvas()
        else:
            # Aggiorna logica di gioco
            self._game.tick(g2d.current_keys())
            self._game.update_view()


# ========== MAIN ==========
if __name__ == "__main__":
    import g2d
    gui = GngGui()