from random import randint
import g2d
from actor import Actor, Arena, Point, check_collision

# =============================================================================
# CONFIGURAZIONE E COSTANTI
# =============================================================================

# Dimensioni logiche e viewport
ARENA_W, ARENA_H = 3569, 224
VIEW_W, VIEW_H = 600, 224

# File esterni
LEVEL_FILE = "Progetto-Ghost/Gng_map.csv" # ‼️IMPORTANTE‼️ RICORDARSI di rimuovere "Progetto-Ghost/" alla consegna
BACKGROUND_URL = "https://raw.githubusercontent.com/fondinfo/sprites/main/ghosts-goblins-bg.png"
SPRITE_SHEET = "ghosts-goblins.png"

# Fisica e Stato di Arthur
ARTHUR_SPEED = 4
ARTHUR_DY = 0.1         # Accelerazione verticale (gravità spicciola)
ARTHUR_GRAVITY = 0.75   # Gravità applicata in caduta
ARTHUR_JUMP = -7        # Impulso salto
ARTHUR_BLINK = 60       # Durata invulnerabilità post-danno
GROUND_Y = 193          # Livello del suolo base (se non ci sono piattaforme)

# Scale
LADDER_WIDTH = 16
LADDER_HEIGHT = 60

# Oggetti
GRAVESTONE_SIZE = 16
TORCH_SPEED = 7
TORCH_DY = -3
TORCH_GRAVITY = 0.35
TORCH_THROW_DURATION = 12 # Durata animazione lancio (blocca input)
TORCH_THROW_COUNTDOWN = 10 #Blocco del lancio in modo da non spammarlo

# Nemici
FLAME_ANIM_SPEED = 4
FLAME_COUNTDOWN = 12
ZOMBIE_SPEED = 2
ZOMBIE_MIN_WALK = 150
ZOMBIE_MAX_WALK = 300
EYEBALL_SPEED = 4
PLANT_MIN_SHOOT = 80
PLANT_MAX_SHOOT = 180
PLANT_PREPARE_FRAMES = (40, 30, 20, 10) # Soglie per cambiare frame pre-sparo

# Configurazione Partita
GAME_SECONDS = 180
TICKS_PER_SECOND = 30
ZOMBIE_SPAWN_CHANCE = 150 # Probabilità 1/150 per tick

# Coordinate HUD
HUD_Y = 10
HUD_TIME_X = 10
HUD_TIME_DIGITS_X = 45
HUD_LIVES_Y = 210
HUD_LIVES_X_START = 10


# =============================================================================
# CLASSI DI GIOCO
# =============================================================================

class Arthur(Actor):
    """
    Gestisce il protagonista. Gestione di movimento, salti, intereazione con scale, attacco e  morte.
    """

    def __init__(self, pos):
        self._x, self._y = pos
        
        # Fisica
        self._dx = ARTHUR_SPEED
        self._dy = ARTHUR_DY
        self._g = ARTHUR_GRAVITY
        self._jump_strength = ARTHUR_JUMP
        self._bottom_y = self._y + 31 # Traccia la base del personaggio per le collisioni
        
        # Stati
        self._state = "Idle"  # Stati: Idle, Running, Jumping, Crouch, Throw, Climbing, Dying, Dead
        self._facing = "right"
        self._on_ground = False
        self._lives = 5
        self._blinking = 0    # Counter invulnerabilità
        
        # Attacco
        self._throw_cd = 0
        self._throw_tick = 0
        self._throw_duration = 0
        self._crouched_throw = False

        # Gestione Scale
        self._on_ladder = False     # True se sovrapposto a una scala
        self._ladder_obj = None     # Riferimento all'oggetto scala
        self._climbing = False      # True se sta effettivamente scalando
        self._climb_tick = 0
        self._climb_facing = "right"
        self._exiting_top = False   # Per animazione uscita scala in alto
        self._descending = False
        self._at_top = False
        self._jump_running = False  #Controlla con un bool se stiamo correndo e saltando, per animazione Running Jumping
        self._run_tick = 0

        # Animazione Morte
        self._dying_tick = 0
        self._death_anim_speed = 5
    
    # -------------------------------------------------------------------------
    # FUNZIONI GETTER
    # -------------------------------------------------------------------------

    def pos(self) -> Point:
        return self._x, self._y

    def lives(self) -> int:
        return self._lives
    
    def getstate(self) -> str:
        return self._state

    # -------------------------------------------------------------------------
    # LOGICA PRINCIPALE (MOVE)
    # -------------------------------------------------------------------------

    def move(self, arena: Arena):
        """Gestione complessiva di tutte le funzionalità di Arthur."""
        
        # 1. Gestione Morte 
        if self._state == "Dying":
            self._handle_death_animation(arena)
            return

        # 2. Gestione Invulnerabilità
        self._update_blinking()

        keys = arena.current_keys() #lista di tasti premuti

        # 3. Gestione Lancio se in corso blocca movimento
        if self._throw_animation():
            return

        arena_width, _ = arena.size()

        # 4. Rilevamento scale
        self._detect_ladder(arena)

        # 5. Logica Scalata
        if self._climbing:
            self._climb(keys)
            return

        # 6. Movimento Orizzontale
        moving = self._horizontal_movement(keys, arena_width)

        # 7. Tentativo ingresso scale da sotto o da sopra
        if self._enter_ladder_from_bottom(keys) or self._enter_ladder_from_top(arena, keys):
            return

        # 8. Cambi di Stato (Jump e Crouch)
        self._crouch_and_jump(keys, moving)

        # 9. Gestione lancio Torce
        if self._throw_cd > 0:
            self._throw_cd -= 1
        self._torch_throw(keys, arena)

        # 10. Gravità
        self._gravity()

        # 11. Collisioni con Piattaforme e Tombe
        self._ground_collisions(arena, moving)

        # 12. Avanzamento animazione corsa
        if self._state == "Running":
            self._run_tick = (self._run_tick + 1) % 12
        else:
            self._run_tick = 0

    def _update_blinking(self):
        if self._blinking > 0:
            self._blinking -= 1
    
    # -------------------------------------------------------------------------
    # GESTIONE MORTE E DANNO
    # -------------------------------------------------------------------------

    def _handle_death_animation(self, arena: Arena):
        """Gestisce l'animazione della morte: Freeze -> Caduta Ossa -> Stop."""
        self._dying_tick += 1
        
        # Calcola fase animazione:
        # 0-2: Arthur perde l'armatura
        # 3-14: Loop Arthur che diventa scheletro
        # 15+: Ossa che cadono al suolo con la gravità.
        frame_idx = self._dying_tick // self._death_anim_speed
        
        if frame_idx < 15:
            # FASE 1: Freeze in aria 
            self._dy = 0
        else:
            # FASE 2: Caduta delle ossa, per via della gravità
            self._dy += self._g
            self._bottom_y += self._dy
            
            # # Collisione ossa col suolo
            if self._bottom_y >= GROUND_Y:
                self._bottom_y = GROUND_Y
                self._dy = 0
            
            # Collisione ossa con piattaforme
            for other in arena.actors():
                if isinstance(other, Platform):
                    ox, oy = other.pos()
                    ow, _ = other.size()
                    width, _ = self.size()
                    center_x = self._x + width / 2
                    
                    if ox <= center_x <= ox + ow:
                        # Se tocchiamo la piattaforma cadendo
                        if self._bottom_y >= oy and self._bottom_y <= oy + 10 and self._dy > 0:
                            self._bottom_y = oy
                            self._dy = 0

        # Ricalcola Y sprite basandosi sul fondo (perché lo sprite cambia altezza)
        _, curr_h = self.size()
        self._y = self._bottom_y - curr_h

        if frame_idx >= 20: # <--- Quando l'animazione è finita...
            # Se siamo a terra, passa allo stato Dead
            if self._dy == 0 and self._bottom_y >= GROUND_Y:
                self._state = "Dead"
            # Se non ha ancora toccato terra, continua l'animazione di caduta
            elif self._dy != 0: 
                pass
            # Se è su una piattaforma e ha smesso di muoversi, passa allo stato Dead
            else: 
                self._state = "Dead" 
            return

    def hit(self, arena):
        """Arthur viene colpito da un nemico."""
        if self._state == "Dying": return
        if self._blinking == 0:
            self._lives -= 1
            if self._lives <= 0:
                self._state = "Dying"
                self._dying_tick = 0
                self._blinking = 0
            else:
                self._blinking = ARTHUR_BLINK # Start invulnerabilità

    # -------------------------------------------------------------------------
    # LOGICA interazione con SCALE 
    # -------------------------------------------------------------------------

    def _detect_ladder(self, arena: Arena):
        """Controlla solo SE siamo sopra una scala."""
        if self._climbing:
            return

        self._on_ladder = False
        self._ladder_obj = None

        for other in arena.actors():
            if isinstance(other, Ladder) and check_collision(self, other):
                self._on_ladder = True
                self._ladder_obj = other
                return
    def _climb(self, keys):
        """Gestisce il movimento verticale quando lo stato è già 'Climbing'."""
        if self._ladder_obj is None:
            self._climbing = False
            self._state = "Idle"
            return

        ladder_x, ladder_y = self._ladder_obj.pos()
        ladder_top = ladder_y

        # Animazione automatica di uscita in cima alla scala
        if self._exiting_top:
            self._climb_tick += 1
            self._y -= 2
            self._bottom_y = self._y + self.size()[1]

            if self._climb_tick >= 12:
                # Fine scalata
                self._climbing = False
                self._exiting_top = False
                self._at_top = False
                self._state = "Idle"
                self._on_ground = True
                self._climb_tick = 0
                height = self.size()[1]
                self._y = ladder_top - height
                self._bottom_y = ladder_top
            self._dy = 0
            return

        # Movimento manuale Su/Giù
        moved = False
        if "ArrowUp" in keys:
            self._y -= 2
            self._climb_tick += 1
            moved = True
            self._descending = False
            # Controllo fine scala (in alto)
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
            
            # Logica uscita scale:
            current_height = self.size()[1]
            current_bottom = self._y + current_height
            
            # 1. Trova l'oggetto scala (per conoscere la base)
            ladder_x, ladder_y = self._ladder_obj.pos()
            ladder_w, ladder_h = self._ladder_obj.size()
            ladder_bottom = ladder_y + ladder_h
            
            # Se Arthur ha superato la fine della scala, uscirà dalla scala
            if current_bottom >= ladder_bottom:
                self._climbing = False
                self._descending = False
                self._state = "Idle"
                self._on_ground = False # Deve cadere o atterrare sulla piattaforma
                self._dy = 0
                self._climb_tick = 0
                self._ladder_obj = None
                self._at_top = False
                
                return

        if not moved:
            # Se siamo fermi mostra ultima animazione
            self._climb_tick = (self._climb_tick // 6) * 6

        self._dy = 0
        self._on_ground = False
        self._bottom_y = self._y + self.size()[1]

    def _enter_ladder_from_bottom(self, keys):
        """Entrata sulla scala partendo dal basso."""
        if (not self._climbing and self._on_ground and self._on_ladder and 
            "ArrowUp" in keys and self._ladder_obj is not None):
            
            # Verifica di non essere già sopra la metà della scala
            _, ladder_y = self._ladder_obj.pos()
            _, ladder_height = self._ladder_obj.size()
            ladder_center_y = ladder_y + (ladder_height / 2)
            
            if self._bottom_y > ladder_center_y:
                self._climbing = True
                self._state = "Climbing"
                self._dy = 0
                self._exiting_top = False
                self._climb_tick = 0
                self._climb_facing = self._facing
                # Centra Arthur orizzontalmente sulla scala
                lx, _ = self._ladder_obj.pos()
                lw, _ = self._ladder_obj.size()
                self._x = lx + (lw - self.size()[0]) // 2
                return True
        return False
    
    def _enter_ladder_from_top(self, arena: Arena, keys):
        """Entrata sulla scala partendo dall'alto."""
        if self._climbing or not self._on_ground or "ArrowDown" not in keys:
            return False
            
        px, py = self.pos()
        pw, ph = self.size()

        for ladder in arena.actors():
            if not isinstance(ladder, Ladder):
                continue

            lx, ly = ladder.pos()
            lw, _ = ladder.size()

            # check_collision
            if (px + pw > lx and px < lx + lw and abs((py + ph) - ly) < 10):
                self._climbing = True
                self._state = "Climbing"
                self._dy = 0
                self._ladder_obj = ladder
                self._x = lx + (lw - pw) // 2
                self._y = ly + 2
                self._bottom_y = self._y + ph
                return True

        return False

    # -------------------------------------------------------------------------
    # MOVIMENTO E STATI (RUN, JUMP, THROW)
    # -------------------------------------------------------------------------

    def _horizontal_movement(self, keys, arena_width) -> bool:
        """Controllo movimento a destra e a sinistra e restiruisce un bool"""
        moving = False
        
        # Sinistra
        if "ArrowLeft" in keys:
            self._facing = "left"            # Cambia SEMPRE il facing
            if self._state != "Crouch":      # Si muove SOLO se non è accovacciato
                self._x -= self._dx
                moving = True

        # Destra
        if "ArrowRight" in keys:
            self._facing = "right"           # Cambia SEMPRE il facing
            if self._state != "Crouch":      # Si muove SOLO se non è accovacciato
                self._x += self._dx
                moving = True
        
        # Clump mondo
        width, _ = self.size()
        self._x = max(0, min(self._x, arena_width - width))
        
        return moving

    def _crouch_and_jump(self, keys, moving):
        """Cambio stato in Salto e Accovacciamento"""
        if self._on_ground:
            if "ArrowDown" in keys:
                self._state = "Crouch"
            elif "ArrowUp" in keys:
                self._dy = self._jump_strength
                self._on_ground = False
                self._state = "Jumping"
                self._jump_running = moving
            else:
                self._state = "Running" if moving else "Idle"

    def _torch_throw(self, keys, arena: Arena):
        """Gestione lancio torcia"""
        if "f" in keys and self._throw_cd == 0 and self._on_ground:
            self._state = "Throw"
            self._throw_tick = 0
            self._throw_duration = TORCH_THROW_DURATION
            
            width, height = self.size()
            start_x = self._x + width / 2
            crouched_throw = ("ArrowDown" in keys)
            
            # Punto di spawn della torcia cambia se Arthur è accovacciato
            start_y = self._bottom_y - (20 if crouched_throw else (height - 5))
            self._crouched_throw = crouched_throw
            
            arena.spawn(Torch((start_x, start_y), self._facing))
            self._throw_cd = TORCH_THROW_COUNTDOWN
    
    def _throw_animation(self) -> bool:
        """Animazione torcia"""
        if self._state != "Throw": return False
        self._throw_duration -= 1
        if self._throw_duration <= 0:
            self._state = "Idle"
            self._throw_tick = 0
        return True # Ritorna True per bloccare altri movimenti

    def _gravity(self): #applica gravità
        self._dy += self._g
        self._bottom_y += self._dy
        _, curr_h = self.size()
        self._y = self._bottom_y - curr_h

    def _ground_collisions(self, arena: Arena, moving: bool):
        """Collisioni: prima verticali, poi orizzontali."""

        self._on_ground = False
        px, py = self.pos()
        pw, ph = self.size()

        old_bottom = self._bottom_y - self._dy

        for other in arena.actors():
            if not isinstance(other, (Platform, Gravestone)):
                continue
            if not check_collision(self, other):
                continue

            ox, oy = other.pos()
            ow, oh = other.size()

            # 1. COLLISIONE VERTICALE --> (per atterrare)
            # Atterra solo se viene dall’alto
            if old_bottom <= oy and self._dy > 0:
                self._bottom_y = oy
                self._y = oy - ph
                self._dy = 0
                self._on_ground = True
                if self._state == "Jumping":
                    self._state = "Running" if moving else "Idle"
                continue

            # 2. COLLISIONE ORIZZONTALE  --> (per tomba)
            if px + pw // 2 < ox + ow // 2:
                # Arthur a sinistra -> spingi da sinistra
                self._x = ox - pw
            else:
                # Arthur a destra -> spingi da destra
                self._x = ox + ow
    
    # -------------------------------------------------------------------------
    #  SIZE & SPRITE
    # -------------------------------------------------------------------------

    def size(self):
        if self._state == "Dying": # Morte
            frame_idx = self._dying_tick // self._death_anim_speed
            # 1. Arthur che perde l'armatura
            if frame_idx == 0: return (29, 29)
            if frame_idx == 1: return (34, 34)
            if frame_idx == 2: return (49, 49)
            # 2. Arthur che diventa scheletro 
            if frame_idx < 15: return (25, 28) 
            
            # Mucchio di ossa
            return (28, 12)
        
        if self._state == "Dead":
            return (28, 12) # Mucchio di ossa

        if self._state == "Climbing": #Arrampicata
            if self._exiting_top:
                return (22, 25) if self._climb_tick < 6 else (22, 16) #animazione uscita dalla scala
            return (21, 30) #animazione normale

        if self._state == "Throw": # Lancio 
            if not self._crouched_throw:
                return (22, 30) if self._throw_tick < 3 else (23, 25) #animazione lancio normale (da idle)
            return (22, 23) if self._throw_tick < 3 else (27, 21) #animazione lancio accovacciati (da Crouch)

        if self._state == "Idle": return (20, 31) #Idle (Arthur fermo)

        if self._state == "Running": # Corsa
            sizes = [(24, 28), (19, 32), (19, 31), (24, 29)]
            return sizes[(self._run_tick // 3) % 4] #animazione corsa

        if self._state == "Jumping": # Salto
            return (32, 27) if self._jump_running else (27, 26) # salto da fermo (Idle) se no animazione salto in corsa

        if self._state == "Crouch": return (22, 22) #Accovacciamento
        
        return (20, 31) #idle

    def sprite(self):
        # BLINKING: Arthur non viene disegnato in alcuni frame se ferito
        if self._blinking > 0 and self._blinking % 4 < 2:
            return None

        if self._state == "Dying": #animazione morte
            frame_idx = self._dying_tick // self._death_anim_speed
            is_right = self._facing == "right"

            # 1. Arthur che perde l'armatura
            if frame_idx == 0: return (129, 198) if is_right else (354, 198)
            if frame_idx == 1: return (161, 196) if is_right else (317, 196)
            if frame_idx == 2: return (201, 188) if is_right else (262, 188)
            
            # 2. Arthur che diventa scheletro (Loop)
            if frame_idx < 15:
                loop_frame = (frame_idx - 3) % 2
                if loop_frame == 0: return (8, 244) if is_right else (479, 244)
                else: return (37, 244) if is_right else (450, 244)

            # 3. Mucchio di ossa che cadono per terra
            collapse_idx = frame_idx - 15
            if collapse_idx == 0: return (80, 244) if is_right else (401, 244)
            if collapse_idx == 1: return (128, 247) if is_right else (354, 247)
            if collapse_idx == 2: return (176, 260) if is_right else (308, 260)
            else: return (224, 260) if is_right else (260, 260)
        
        if self._state == "Dead": # Morto = mucchio di ossa
            is_right = self._facing == "right"
            return (224, 260) if is_right else (260, 260)

        if self._state == "Climbing": # Arrampicata
            # Gestione sprite uscita dall'alto se no arrampicata normale
            if self._exiting_top:
                if self._climb_tick < 6:
                    return (198, 132) if self._climb_facing == "right" else (292, 132)
                else:
                    return (224, 133) if self._climb_facing == "right" else (266, 133)
            
            frame = (self._climb_tick // 4) % 2
            # Gli sprite sono invertiti se si sale o scende per creare movimento
            if self._descending:
                if self._climb_facing == "right": return (341, 133) if frame == 0 else (150, 133)
                else: return (150, 133) if frame == 0 else (341, 133)
            else:
                if self._climb_facing == "right": return (150, 133) if frame == 0 else (341, 133)
                else: return (341, 133) if frame == 0 else (150, 133)

        if self._state == "Throw": # Lancio
            self._throw_tick = min(self._throw_tick + 1, 6)
            frame = 0 if self._throw_tick < 3 else 1
            if self._crouched_throw:
                frames = [(75, 140), (101, 142), (415, 140), (384, 142)]
            else:
                frames = [(5, 133), (30, 138), (485, 133), (459, 138)]
            offset = 2 if self._facing == "left" else 0
            return frames[frame + offset]

        if self._state == "Idle":
            return (6, 43) if self._facing == "right" else (486, 43)

        if self._state == "Running": #Corsa
            frames_right = [(40, 44), (66, 42), (88, 43), (109, 43)]
            frames_left = [(449, 44), (427, 42), (405, 43), (379, 43)]
            frame = (self._run_tick // 3) % 4
            return frames_right[frame] if self._facing == "right" else frames_left[frame]

        if self._state == "Jumping": # Salto in Idle o in corsa
            if self._facing == "right": return (144, 29) if self._jump_running else (180, 29)
            else: return (336, 29) if self._jump_running else (305, 29)

        if self._state == "Crouch": # Accovacciamento
            return (223, 52) if self._facing == "right" else (267, 52)
        
        return (6, 43)


class Zombie(Actor):
    """Nemico semplice: Spawna casualmente dal terreno, cammina fino a un limite, poi riaffonda."""

    def __init__(self, pos, facing):
        self._x, top = pos
        self._ground_y = top + 31
        self._facing = facing 
        self._state = "spawn"  # Lifecycle: spawn -> walk -> sink
        self._frame = 0
        self._walked = 0
        self._max_walk = randint(ZOMBIE_MIN_WALK, ZOMBIE_MAX_WALK)
        self._dx = ZOMBIE_SPEED

    def calculate_spawn(arthur_pos, arthur_size, arena_size):
        """ Dertermina una posizione valida di spawn vicino ad Arthur."""
        ax, _ = arthur_pos
        awidth, _ = arthur_size
        aw, _ = arena_size

        # Verifica spazio disponibile a sx e dx
        can_spawn_left = ax - 50 > 0
        can_spawn_right = ax + awidth + 50 < aw

        if not can_spawn_left and not can_spawn_right: return None
        
        # Scelta direzione (facing) di spawn 
        if can_spawn_left and can_spawn_right:
            spawn_side = "left" if randint(0, 1) == 0 else "right"
        else:
            spawn_side = "left" if can_spawn_left else "right"
        
        # Scelta punto di spawn, unito al facing precendentemente scelto, in una tupla
        if spawn_side == "left":
            offset = randint(50, min(200, int(ax)))
            return ax - offset, "right"
        else:
            max_dist = aw - (ax + awidth)
            offset = randint(50, min(200, int(max_dist)))
            return ax + offset, "left"

    def move(self, arena: Arena):
        """ Movimento Zombie, insieme ad animazione uscita dal terreno, e collisioni con piattaforme e scale"""
        arena_width, arena_height = arena.size()
        width, _ = self.size()

        if self._state == "spawn":
            self._frame += 1
            if self._frame > 15:
                self._state = "walk"
                self._frame = 0

        elif self._state == "walk":
            dx = self._dx if self._facing == "right" else -self._dx
            next_x = self._x + dx
            
            # Controllo se finisce una piattaforma arriva al termine (e non ci sono altre piattaforme adiacenti a questa
            # che ne aumentino la superficie): lo zombie torna indietro se finisce il terreno
            has_ground = False
            if self._ground_y >= arena_height:
                has_ground = True # Livello base
            else:
                # Check presenza piattaforme sotto i piedi
                for other in arena.actors():
                    if not isinstance(other, (Platform, Ladder)): continue
                    ox, oy = other.pos()
                    ow, _ = other.size()
                    # Verifica se il prossimo passo è ancora sulla piattaforma
                    if next_x < ox + ow and next_x + width > ox:
                        if abs(oy - self._ground_y) < 5:
                            has_ground = True
                            break

            if not has_ground:
                self._facing = "left" if self._facing == "right" else "right"
            else:
                self._x = next_x
                self._walked += self._dx
                self._frame = (self._frame + 1) % 30
                # Tempo di vita finito -> affonda
                if self._walked >= self._max_walk:
                    self._state = "sink"
                    self._frame = 0

        elif self._state == "sink":
            self._frame += 1
            if self._frame > 15:
                arena.kill(self)
                return

        self._x = max(0, min(self._x, arena_width - width))

        # Danno ad Arthur
        for other in arena.actors():
            if isinstance(other, Arthur) and check_collision(self, other):
                other.hit(arena)

    def pos(self):
        _, height = self.size()
        return self._x, self._ground_y - height

    def size(self):
        # Dimensione varia in base all'animazione (emergere dal terreno)
        if self._state == "spawn" or self._state == "sink":
            # Frame specifici per altezza progressiva
            effective_frame = self._frame if self._state == "spawn" else (15 - self._frame) # Reverse per sink
            if effective_frame <= 4: return (16, 9)
            if effective_frame <= 9: return (25, 12)
            return (19, 24)

        # Walk standard
        if self._frame <= 9: return (22, 31)
        if self._frame <= 19: return (19, 32)
        return (21, 31)

    def sprite(self):
        # Seleziona sprite in base allo stato
        if self._state == "spawn":
            frames = [((778, 88), (512, 88)), ((748, 85), (533, 85)), ((725, 73), (562, 73))]
            idx = 0 if self._frame <= 4 else (1 if self._frame <= 9 else 2)
        elif self._state == "walk":
            frames = [((699, 66), (585, 66)), ((677, 65), (610, 65)), ((654, 66), (631, 66))]
            idx = 0 if self._frame <= 9 else (1 if self._frame <= 19 else 2)
        else: # sink (animazione inversa spawn)
            frames = [((725, 73), (562, 73)), ((748, 85), (533, 85)), ((778, 88), (512, 88))]
            idx = 0 if self._frame <= 4 else (1 if self._frame <= 9 else 2)

        right, left = frames[idx]
        return right if self._facing == "right" else left


class Eyeball(Actor):
    """Proiettile a ricerca di Arthur lanciato dalla pianta."""

    def __init__(self, pos, target: Actor):
        self._x, self._y = pos
        self._w, self._h = 8, 8
        
        # Calcolo vettore direzione verso il bersaglio (al momento del lancio)
        target_x, target_y = target.pos()
        target_w, target_h = target.size()
        target_center_x = target_x + target_w / 2
        target_center_y = target_y + target_h / 2

        dx = target_center_x - self._x
        dy = target_center_y - self._y
        steps = max(abs(dx), abs(dy))
        
        if steps > 0:
            self._dx = (dx / steps) * EYEBALL_SPEED
            self._dy = (dy / steps) * EYEBALL_SPEED
        else:
            self._dx, self._dy = 0, 0

        self._facing = "right" if self._dx >= 0 else "left"

    def move(self, arena: Arena):
        self._x += self._dx
        self._y += self._dy
        
        # Despawn fuori schermo
        w, h = arena.size()
        if not (0 <= self._x <= w and 0 <= self._y <= h):
            arena.kill(self)
            return

        # Collisione Arthur
        for other in arena.actors():
            if isinstance(other, Arthur) and check_collision(self, other):
                other.hit(arena)
                arena.kill(self)
                return
    
    def pos(self): return self._x, self._y
    def size(self): return self._w, self._h
    def sprite(self): return (552, 219) if self._facing == "right" else (746, 219)


class Plant(Actor):
    """Nemico stazionario che spara proiettili."""

    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 25
        self._shoot_timer = randint(60, 150)
        self._facing = "left"
        self._current_frame = 0

        # Lista coordinate sprite
        self._frames_right = [
            ((564, 214), (16, 25)), ((582, 214), (16, 25)), 
            ((600, 207), (16, 32)), ((618, 207), (16, 32)), ((636, 207), (16, 32))
        ]
        self._frames_left = [
            ((726, 214), (16, 25)), ((708, 214), (16, 25)),
            ((690, 207), (16, 32)), ((672, 207), (16, 32)), ((654, 207), (16, 32))
        ]

    def move(self, arena: Arena):
        # Cerca Arthur per orientarsi e sparare
        arthurs_list = [a for a in arena.actors() if isinstance(a, Arthur)]

        if arthurs_list:
            arthur = arthurs_list[0]
        else:
            arthur = None

        if arthur:
            ax, _ = arthur.pos()
            self._facing = "right" if ax > self._x else "left"
            
            # Non fa nulla se Arthur è troppo lontano
            if abs(self._x - ax) > VIEW_W / 2: return

        self._shoot_timer -= 1
        t = self._shoot_timer
        
        # Animazione di "caricamento" sparo basata sul timer
        if t > PLANT_PREPARE_FRAMES[0]: self._current_frame = 0
        elif t > PLANT_PREPARE_FRAMES[1]: self._current_frame = 1
        elif t > PLANT_PREPARE_FRAMES[2]: self._current_frame = 2
        elif t > PLANT_PREPARE_FRAMES[3]: self._current_frame = 3
        else: self._current_frame = 4 # Frame sparo

        if self._shoot_timer <= 0:
            if arthur: self._shoot(arena, arthur)
            self._shoot_timer = randint(PLANT_MIN_SHOOT, PLANT_MAX_SHOOT)

    def _shoot(self, arena: Arena, target_actor: Actor):
        w, _ = self.size()
        spawn_y = self.pos()[1] + 10
        spawn_x = self._x + w / 2
        arena.spawn(Eyeball((spawn_x, spawn_y), target_actor))

    def pos(self):
        # Allinea sprite in basso (perchè l'altezza cambia durante animazione)
        max_h = 32
        current_h = self.size()[1]
        return self._x, self._y + (max_h - current_h)

    def size(self):
        frames = self._frames_right if self._facing == "right" else self._frames_left
        return frames[self._current_frame][1]

    def sprite(self):
        frames = self._frames_right if self._facing == "right" else self._frames_left
        return frames[self._current_frame][0]


# --- Elementi Mappa ---

class Platform:
    def __init__(self, rect): self._x, self._y, self._w, self._h = rect
    def move(self, arena: Arena): pass
    def pos(self): return self._x, self._y
    def size(self): return self._w, self._h
    def sprite(self): return None # Invisibile, disegnato dal background

class Ladder:
    def __init__(self, pos): self._x, self._y = pos; self._w, self._h = LADDER_WIDTH, LADDER_HEIGHT
    def move(self, arena: Arena): pass
    def pos(self): return self._x, self._y
    def size(self): return self._w, self._h
    def sprite(self): return None

class Gravestone:
    def __init__(self, pos): self._x, self._y = pos; self._w, self._h = GRAVESTONE_SIZE, GRAVESTONE_SIZE
    def move(self, arena: Arena): pass
    def pos(self): return self._x, self._y
    def size(self): return self._w, self._h
    def sprite(self): return None

# --- Weapons/Armi ---

class Torch(Actor):
    """Arma di Arthur: traiettoria parabolica, genera fuoco all'impatto."""

    def __init__(self, pos, facing):
        self._x, self._y = pos
        self._facing = facing
        self._dx = TORCH_SPEED if facing == "right" else -TORCH_SPEED
        self._dy = TORCH_DY
        self._gravity = TORCH_GRAVITY
        self._frame = 0
        self._alive = True
        self._killed = False

    def move(self, arena: Arena):
        if not self._alive:
            arena.kill(self)
            return

        # Fisica a parabola
        self._x += self._dx
        self._dy += self._gravity
        self._y += self._dy
        self._frame = (self._frame + 1) % 4

        px, py = self._x, self._y
        pw, ph = self.size()

        for other in arena.actors():
            ox, oy = other.pos()
            ow, oh = other.size()
            
            # Collisione diretta con Nemici
            if isinstance(other, (Zombie)) and not self._killed:
                if (px + pw > ox and px < ox + ow and py + ph > oy and py < oy + oh):
                    arena.kill(other)
                    self._killed = True # Una torcia uccide un solo nemico per frame
                    self._alive = False
                    return

            # Collisione con Terreno -> Genera Fiamma / Con Tomba sparisce
            if isinstance(other, (Platform, Gravestone, Plant)):
                if (px + pw > ox and px < ox + ow and py + ph > oy and py < oy + oh):
                    if isinstance(other, Platform):
                        flame_center_x = self._x + pw / 2
                        arena.spawn(Flame((flame_center_x, oy)))
                    self._alive = False
                    return
    
    def pos(self): return self._x, self._y
    def size(self): return [(14, 13), (13, 15), (13, 15), (14, 13)][self._frame]
    def sprite(self):
        right_frames = [(19, 401), (39, 399), (58, 399), (78, 399)]
        left_frames = [(479, 401), (460, 399), (441, 399), (420, 399)]
        return (right_frames if self._facing == "right" else left_frames)[self._frame]


class Flame(Actor):
    """Effetto area che danneggia nemici dopo che la torcia tocca terra."""

    def __init__(self, pos):
        center_x, platform_y = pos
        self._center_x = center_x
        self._platform_y = platform_y
        self._tick = 0
        
        # Dati sprite: (pos, size)
        self._frames_data = [
            ((117, 428), (32, 31)), ((153, 435), (24, 24)), 
            ((210, 443), (16, 16)), ((229, 450), (10, 9))
        ]
        self._anim_speed = FLAME_ANIM_SPEED
        self._max_duration = FLAME_COUNTDOWN * self._anim_speed

        # Posizione iniziale
        fw, fh = self._frames_data[0][1]
        self._x_left = center_x - fw / 2
        self._y_top = platform_y - fh

    def move(self, arena: Arena):
        self._tick += 1
        if self._tick >= self._max_duration:
            arena.kill(self)
            return

        # Aggiorna posizione (la fiamma cambia dimensione) per farla rimanere centrata a terra
        fw, fh = self.size()
        self._y_top = self._platform_y - fh
        self._x_left = self._center_x - fw / 2

        # Brucia i nemici
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
        return 2 + (step % 2) # Fase di spegnimento

    def pos(self): return self._x_left, self._y_top
    def size(self): return self._frames_data[self._get_current_frame_index()][1]
    def sprite(self): return self._frames_data[self._get_current_frame_index()][0]


# =============================================================================
# LOGICA GIOCO E ARENA
# =============================================================================

class GngGame(Arena):
    """Estensione di Arena per gestire la logica specifica di G'n'G (livelli, camera, spawn)."""

    def __init__(self, time=GAME_SECONDS * TICKS_PER_SECOND):
        super().__init__((ARENA_W, ARENA_H))
        self._time = time
        self._arthur = None
        self._view_x = 0
        self._load_level(LEVEL_FILE)

    def _load_level(self, config_file: str):
        """Sottoclasse di Arena specializzata nella gestione del gioco."""
        
        with open(config_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line: continue
                    parts = [p.strip() for p in line.split(",")] #divido ogni riga del csv in parti, che metto in una lista
                    entity = parts[0].lower() #primo elemento caratterizza il tipo di entità
                    
                    # Creo una lista con gli elementi nella lista parts dal seconda in poi, in quanto rappresentano, rispettivamente...
                    # ..., pos(x,y) e size(w,h).
                    vals = [float(x) for x in parts[1:]]

                    if entity == "arthur":
                        self._arthur = Arthur((vals[0], vals[1]))
                        self.spawn(self._arthur)
                    elif entity == "platform":
                        self.spawn(Platform((vals[0], vals[1], vals[2], vals[3])))
                    elif entity == "gravestone":
                        self.spawn(Gravestone((vals[0], vals[1])))
                    elif entity == "ladder":
                        self.spawn(Ladder((vals[0], vals[1])))
                    elif entity == "plant":
                        self.spawn(Plant((vals[0], vals[1])))

    def get_arthur(self) -> Arthur: return self._arthur
    def get_view_x(self) -> int: return self._view_x

    def update_view(self):
        """Calcola lo zoom della camera su Arthur (con limiti)."""
        if self._arthur:
            ax, _ = self._arthur.pos()
            arena_width, _ = self.size()
            self._view_x = int(ax - VIEW_W / 2)
            self._view_x = max(0, min(self._view_x, arena_width - VIEW_W))

    def spawn_random_zombie(self):
        """Spawna zombie randomicamente nella stessa piattaforma in cui è Arthur"""
        if not self._arthur: return
        
        spawn_data = Zombie.calculate_spawn(self._arthur.pos(), self._arthur.size(), self.size())
        if not spawn_data: return

        x, facing = spawn_data
        _, arena_h = self.size()
        

        #Logica per capire la y della piattaforma in cui è Arthur
        # 1. Trova il centro orizzontale di Arthur
        arthur_x, arthur_y = self._arthur.pos()
        arthur_w, arthur_h = self._arthur.size()
        arthur_center_x = arthur_x + arthur_w / 2
        
        # Inizializza ground_y 
        ground_y = arena_h 
        
        # Cerco la piattaforma di Arthur
        for actor in self.actors():
            if isinstance(actor, (Platform, Gravestone)): 
                px, py = actor.pos()
                pw, ph = actor.size()
                
                
                if px <= arthur_center_x <= px + pw:
                    if py > arthur_y: 
                        ground_y = min(ground_y, py) 

        # Se Arthur sta saltando o non è su una piattaforma, ground_y sarà arena_h
        if ground_y == arena_h:
            # Se Arthur è sul terreno base, usa il GROUND_Y definito
            if self._arthur.getstate() in ("Idle", "Running", "Crouch"):
                ground_y = GROUND_Y
        
        self.spawn(Zombie((x, ground_y - 31), facing))

    # Stati partita
    def lives(self) -> int: return self._arthur.lives() if self._arthur else 0
    def time(self) -> int: return self._time - self.count()
    
    def game_over(self) -> bool:
        # Gioco perso solo quando l'animazione morte di Arthur finisce (stato Dead)
        return self.lives() <= 0 and (self._arthur.getstate() == "Dead")
    
    def game_won(self) -> bool:
        return self.time() <= 0 and self.lives() > 0


# =============================================================================
# INTERFACCIA GRAFICA (GUI)
# =============================================================================

class GngGui:
    def __init__(self):
        self._game = GngGame()
        g2d.init_canvas((VIEW_W, VIEW_H), 2) # Scale 2x

        # Mappa sprite numeri per HUD: "cifra": ((pos_x, pos_y), (w, h))
        self._digit_sprites = {
            "0": ((658, 685), (7, 8)), "1": ((668, 685), (4, 8)),
            "2": ((676, 685), (7, 8)), "3": ((685, 685), (7, 8)),
            "4": ((694, 685), (7, 8)), "5": ((703, 685), (6, 8)),
            "6": ((712, 685), (6, 8)), "7": ((721, 685), (7, 8)),
            "8": ((730, 685), (7, 8)), "9": ((740, 685), (6, 8)),
        }
        g2d.main_loop(self.tick)

    def _start_new_game(self):
        self._game = GngGame()

    def _draw_number(self, number: int, x: int, y: int):
        for digit in str(number):
            if digit in self._digit_sprites:
                spos, ssize = self._digit_sprites[digit]
                g2d.draw_image(SPRITE_SHEET, (x, y), spos, ssize)
                x += ssize[0] + 1

    def _draw_hud(self):
        # Label "TIME"
        g2d.draw_image(SPRITE_SHEET, (HUD_TIME_X, HUD_Y), (624, 676), (32, 8))
        
        # Timer
        time_remaining = max(0, self._game.time() // TICKS_PER_SECOND)
        self._draw_number(time_remaining, HUD_TIME_DIGITS_X, HUD_Y)

        # Vite (icone elmi)
        for i in range(self._game.lives()):
            x = HUD_LIVES_X_START + (i * 16)
            g2d.draw_image(SPRITE_SHEET, (x, HUD_LIVES_Y), (696, 696), (13, 13))

    def tick(self):
        view_x = self._game.get_view_x()
        is_game_over = self._game.game_over()

        # 1. Sfondo (scrollato)
        g2d.draw_image("ghosts-goblins-bg.png", (-view_x - 2, -10), (ARENA_W, ARENA_H))

        # 2. Logica Spawn (solo se il gioco è in corso)
        if not is_game_over and randint(1, ZOMBIE_SPAWN_CHANCE) == 1:
            self._game.spawn_random_zombie()

        # 3. Rendering Attori
        for actor in self._game.actors():
            sprite = actor.sprite()
            if sprite:
                x, y = actor.pos()
                g2d.draw_image(SPRITE_SHEET, (x - view_x, y), sprite, actor.size())

        # 4. HUD
        self._draw_hud()

        # 5. Controllo flusso gioco
        if is_game_over:
            # Una volta raggiunto lo stato Dead, lancia il prompt.
            ans = g2d.prompt("GAME OVER 💀\nPremere Y/y per rigiocare")
            if ans and ans.lower() == "y":
                self._start_new_game()
            else:
                g2d.close_canvas()
        elif self._game.game_won():
            g2d.alert("You Won!")
            g2d.close_canvas()
        else:
            # Continua la logica del gioco solo se non è game over
            self._game.tick(g2d.current_keys())
            self._game.update_view()

if __name__ == "__main__":
    GngGui()