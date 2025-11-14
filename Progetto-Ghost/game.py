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
        self._gravity = 0.5
        self._jump_strength = -10
        self._run_tick = 0
        self._bottom_y = self._y + 31  # Posizione fondo
        self._state = "Idle"
        self._facing = "right"
        self._on_ground = False
    
    def move(self, arena: Arena):
        keys = arena.current_keys()
        aw, ah = arena.size()
        moving = False
        
        # Stato precedente
        old_bottom = self._bottom_y
        _, old_h = self.size()

        # Movimento orizzontale
        if "ArrowLeft" in keys:
            self._x -= self._dx
            self._facing = "left"
            moving = True
        if "ArrowRight" in keys:
            self._x += self._dx
            self._facing = "right"
            moving = True

        # Clamp orizzontale
        w, _ = self.size()
        self._x = max(0, min(self._x, aw - w))

        # Crouch
        if "ArrowDown" in keys and self._on_ground:
            self._state = "Crouch"
        elif "ArrowUp" in keys and self._on_ground:
            self._dy = self._jump_strength
            self._on_ground = False
            self._state = "Jumping"
        elif self._on_ground:
            moving = "ArrowLeft" in keys or "ArrowRight" in keys
            self._state = "Running" if moving else "Idle"

        #  Gravità
        self._dy += self._gravity
        self._bottom_y += self._dy

        # Animazione corsa
        self._run_tick = (self._run_tick + 1) % 12 if self._state == "Running" else 0
        
        # Posizione Y aggiornata in base allo sprite
        _, curr_h = self.size()
        self._y = self._bottom_y - curr_h

        #   Collisioni con Tombe e Piattafoorme
        self._on_ground = False
        
        for other in arena.actors():
            if isinstance(other, (Platform, Gravestone)) and check_collision(self, other):
                ox, oy = other.pos()
                ow, oh = other.size()
                
                # Calcolo dei centri per determinare la direzione della collisione
                player_center_x = self._x + w / 2
                player_center_y = self._bottom_y - curr_h / 2
                other_center_x = ox + ow / 2
                other_center_y = oy + oh / 2
                
                # Calcolo overlap su ogni asse
                overlap_x = (w + ow) / 2 - abs(player_center_x - other_center_x)
                overlap_y = (curr_h + oh) / 2 - abs(player_center_y - other_center_y)
                
                # Le piattaforme hanno solo collisione dall'alto
                if isinstance(other, Platform):
                    if old_bottom <= oy and self._dy > 0:
                        self._bottom_y = oy
                        self._y = self._bottom_y - curr_h
                        self._dy = 0
                        self._on_ground = True
                        if self._state == "Jumping":
                            self._state = "Idle"
                
                # Le tombe hanno collisione su tutti i lati
                elif isinstance(other, Gravestone):
                    # Risolvi la collisione sul lato con overlap minore
                    if overlap_x < overlap_y:
                        # Collisione laterale
                        if player_center_x < other_center_x:
                            # Collisione da sinistra
                            self._x = ox - w
                        else:
                            # Collisione da destra
                            self._x = ox + ow
                    else:
                        # Collisione verticale
                        if player_center_y < other_center_y:
                            # Collisione dall'alto (caduta sulla tomba)
                            self._bottom_y = oy
                            self._y = self._bottom_y - curr_h
                            self._dy = 0
                            self._on_ground = True
                            if self._state == "Jumping":
                                self._state = "Idle"
                        else:
                            # Collisione dal basso (saltando contro la tomba)
                            self._bottom_y = oy + oh + curr_h
                            self._y = self._bottom_y - curr_h
                            self._dy = 0


    def pos(self):
        return self._x, self._y

    def size(self):
        if self._state == "Idle":
            return (20, 31)
        if self._state == "Running":
            sizes = [(24, 28), (19, 32), (19, 31), (24, 29)]
            return sizes[(self._run_tick // 3) % 4]
        if self._state == "Jumping":
            return (32, 27) if self._dy < -1 else (27, 26)
        if self._state == "Crouch":
            return (22, 22)
        return (20, 31)

    def sprite(self):
        if self._state == "Idle":
            return (6, 43) if self._facing == "right" else (486, 43)
        
        if self._state == "Running":
            frame = (self._run_tick // 3) % 4
            right = [(40, 44), (66, 42), (88, 43), (109, 43)]
            left = [(449, 44), (427, 42), (405, 43), (379, 43)]
            return right[frame] if self._facing == "right" else left[frame]
        
        if self._state == "Jumping":
            if self._dy < -1:
                return (144, 29) if self._facing == "right" else (336, 29)
            return (180, 29) if self._facing == "right" else (305, 29)
        
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
        """Calcola posizione e direzione di spawn per un nuovo zombie.
        Restituisce (x, facing) oppure None se non può spawnare."""
        ax, _ = arthur_pos
        awidth, _ = arthur_size
        aw, _ = arena_size
        
        # lato di spawn
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
        
        # posizione spawn
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

        # Limiti orizzontali
        self._x = max(0, min(self._x, aw - w))

        # Gravità e collisione Tombe e Piattaforme
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
        # sink
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
        else:  # sink
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


def tick():
    aw, _ = arena.size()
    ax, _ = arthur.pos()


    view_x = int(ax - VIEW_W / 2)
    view_x = max(0, min(view_x, aw - VIEW_W))
    

    sfondo = "https://raw.githubusercontent.com/fondinfo/sprites/main/ghosts-goblins-bg.png"
    g2d.draw_image(sfondo, (-view_x - 2, -10), (ARENA_W, ARENA_H))

    # Spawn casuale zombie
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
            sprites = "https://raw.githubusercontent.com/fondinfo/sprites/refs/heads/main/ghosts-goblins.png"
            g2d.draw_image("ghosts-goblins.png", (x - view_x, y), sprite, actor.size())
        
    arena.tick(g2d.current_keys())


def main():
    global g2d, arena, arthur
    import g2d

    arena = Arena((ARENA_W, ARENA_H))
    
    # Piattaforme
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
        (59 - 9, 177),
        (251 - 9, 177),
        (539 - 9, 177),
        (763 - 9, 177),
        (971 - 9, 177),
        (1115 - 9, 177),
        (1531 - 9, 177),
        (875 - 9, 97),
        ]

    for g in gravestones:
        arena.spawn(Gravestone(g))

    # Spawn Arthur (posizione fissa sulla prima piattaforma)
    arthur = Arthur((400, 161))  # 193 - 31 = 161
    arthur._dy = 0.1
    arena.spawn(arthur)

    g2d.init_canvas((VIEW_W, VIEW_H))
    g2d.main_loop(tick)


if __name__ == "__main__":
    main()