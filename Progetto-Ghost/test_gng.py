import unittest
from unittest.mock import Mock
from game import (
    Arthur, Zombie, Plant, Eyeball, Torch, Flame,
    Platform, Ladder, Gravestone, GngGame,
    ARTHUR_SPEED, ARTHUR_JUMP, ARTHUR_GRAVITY
)

class GngTests(unittest.TestCase):

    # -------------------------------------------------------------------------
    # TEST ARTHUR: MOVIMENTO E FISICA
    # -------------------------------------------------------------------------

    def test_01_arthur_move_right(self):
        # Controlla che Arthur si muova a destra e cambi stato in Running
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["ArrowRight"]
        
        # Piattaforma REALE sotto i piedi (y=100 + 31 = 131)
        platform = Platform((0, 131, 1000, 30))
        arena.actors.return_value = [platform]
        
        arthur = Arthur((100, 100))
        arthur._on_ground = True 
        
        arthur.move(arena)
        
        # FIX: Quando Arthur corre, lo sprite cambia dimensione (height 28px).
        # Poiché i piedi restano a 131, la testa scende: 131 - 28 = 103.
        self.assertEqual(arthur.pos(), (100 + ARTHUR_SPEED, 103))
        self.assertEqual(arthur.getstate(), "Running")

    def test_02_arthur_move_left(self):
        # Controlla che Arthur si muova a sinistra e cambi facing
        # Simuliamo movimento in aria (cade per gravità)
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["ArrowLeft"]
        arena.actors.return_value = []
        
        arthur = Arthur((100, 100))
        arthur.move(arena)
        
        self.assertEqual(arthur.pos(), (100 - ARTHUR_SPEED, 100.85))
        self.assertEqual(arthur._facing, "left")

    def test_03_arthur_jump(self):
        # Controlla l'inizio del salto (velocità verticale negativa)
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["ArrowUp"]
        arena.actors.return_value = []
        
        arthur = Arthur((100, 193))
        arthur._on_ground = True
        
        arthur.move(arena)
        
        expected_dy = ARTHUR_JUMP + ARTHUR_GRAVITY
        self.assertEqual(arthur._dy, expected_dy)
        self.assertEqual(arthur.getstate(), "Jumping")

    def test_04_arthur_gravity(self):
        # Controlla che la gravità venga applicata quando Arthur è in aria
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = []
        arena.actors.return_value = []
        
        arthur = Arthur((100, 100))
        arthur._dy = 0
        
        arthur.move(arena)
        
        self.assertEqual(arthur._dy, ARTHUR_GRAVITY)
        self.assertTrue(arthur.pos()[1] > 100)

    def test_05_arthur_collision_landing(self):
        # Controlla l'atterraggio su una piattaforma
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = []
        
        platform = Platform((100, 200, 100, 30))
        arena.actors.return_value = [platform]
        
        arthur = Arthur((120, 190)) 
        arthur._dy = 15 
        arthur._bottom_y = 190 
        
        arthur.move(arena)
        
        self.assertTrue(arthur._on_ground)
        self.assertEqual(arthur._dy, 0)
        self.assertEqual(arthur.pos()[1], 200 - 31) 

    def test_06_arthur_fall_off_platform(self):
        # Controlla che Arthur cada se cammina fuori dalla piattaforma
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["ArrowRight"]
        
        platform = Platform((0, 200, 100, 30)) # Finisce a x=100
        arena.actors.return_value = [platform]
        
        arthur = Arthur((101, 169)) 
        arthur._on_ground = True
        arthur._dy = 0
        
        arthur.move(arena)
        
        self.assertFalse(arthur._on_ground)
        self.assertTrue(arthur._dy > 0)

    def test_07_arthur_horizontal_collision(self):
        # Controlla che Arthur si fermi contro un ostacolo
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["ArrowRight"]
        
        grave = Gravestone((122, 193)) 
        arena.actors.return_value = [grave]
        
        arthur = Arthur((100, 193)) 
        
        arthur.move(arena)
        
        self.assertEqual(arthur.pos()[0], 102) 

    def test_08_arthur_crouch(self):
        # Controlla lo stato di accovacciamento
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["ArrowDown"]
        arena.actors.return_value = []
        
        arthur = Arthur((100, 193))
        arthur._on_ground = True
        
        arthur.move(arena)
        
        self.assertEqual(arthur.getstate(), "Crouch")

    # -------------------------------------------------------------------------
    # TEST ARTHUR: AZIONI E SCALE
    # -------------------------------------------------------------------------

    def test_09_arthur_throw_torch(self):
        # Controlla lo spawn della torcia
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["f"]
        arena.actors.return_value = []
        
        arthur = Arthur((100, 193))
        arthur._on_ground = True
        
        arthur.move(arena)
        
        self.assertEqual(arthur.getstate(), "Throw")
        args, _ = arena.spawn.call_args
        self.assertIsInstance(args[0], Torch)

    def test_10_arthur_throw_cooldown(self):
        # Controlla cooldown torcia
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["f"]
        arena.actors.return_value = []
        
        arthur = Arthur((100, 193))
        arthur._on_ground = True
        arthur._throw_cd = 10 
        
        arthur.move(arena)
        
        arena.spawn.assert_not_called()

    def test_11_arthur_climb_ladder_bottom(self):
        # Controlla l'inizio della scalata dal basso
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["ArrowUp"]
        
        ladder = Ladder((100, 100)) 
        arena.actors.return_value = [ladder]
        
        arthur = Arthur((100, 140))
        arthur._on_ground = True
        
        arthur.move(arena)
        
        self.assertTrue(arthur._climbing)
        self.assertEqual(arthur.getstate(), "Climbing")

    def test_12_arthur_climb_ladder_top(self):
        # Controlla l'ingresso nella scala dall'alto
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["ArrowDown"]
        
        ladder = Ladder((100, 200)) 
        arena.actors.return_value = [ladder]
        
        arthur = Arthur((98, 169))
        arthur._on_ground = True
        
        arthur.move(arena)
        
        self.assertTrue(arthur._climbing)

    def test_13_arthur_climb_movement(self):
        # Controlla il movimento verticale sulla scala
        arena = Mock()
        arena.size.return_value = (1000, 600)
        arena.current_keys.return_value = ["ArrowUp"]
        
        ladder = Ladder((100, 100))
        
        arthur = Arthur((100, 130))
        arthur._climbing = True
        arthur._ladder_obj = ladder
        
        initial_y = arthur.pos()[1]
        arthur.move(arena)
        
        self.assertTrue(arthur.pos()[1] < initial_y)

    # -------------------------------------------------------------------------
    # TEST DANNO E MORTE
    # -------------------------------------------------------------------------

    def test_14_arthur_take_damage(self):
        # Controlla la riduzione delle vite
        arena = Mock()
        arthur = Arthur((100, 100))
        initial_lives = arthur.lives()
        
        arthur.hit(arena)
        
        self.assertEqual(arthur.lives(), initial_lives - 1)
        self.assertTrue(arthur._blinking > 0)

    def test_15_arthur_invulnerability(self):
        # Controlla invulnerabilità
        arena = Mock()
        arthur = Arthur((100, 100))
        arthur._blinking = 10
        initial_lives = arthur.lives()
        
        arthur.hit(arena)
        
        self.assertEqual(arthur.lives(), initial_lives)

    
    # -------------------------------------------------------------------------
    # TEST NEMICI E ARMI
    # -------------------------------------------------------------------------

    def test_16_zombie_movement(self):
        # Controlla movimento zombie
        arena = Mock()
        arena.size.return_value = (1000, 600)
        
        floor = Platform((0, 200, 1000, 50)) 
        arena.actors.return_value = [floor]
        
        zombie = Zombie((100, 200 - 31), "right")
        zombie._state = "walk"
        initial_x = zombie.pos()[0]
        
        zombie.move(arena)
        
        self.assertTrue(zombie.pos()[0] > initial_x)

    def test_17_zombie_sink(self):
        # Controlla zombie sink
        arena = Mock()
        arena.size.return_value = (1000, 600)
        
        floor = Platform((0, 200, 1000, 50)) 
        arena.actors.return_value = [floor]
        
        zombie = Zombie((100, 200 - 31), "right")
        zombie._state = "walk"
        zombie._walked = zombie._max_walk + 1 
        
        zombie.move(arena) 
        self.assertEqual(zombie._state, "sink")
        
        zombie._frame = 16 
        zombie.move(arena) 
        
        arena.kill.assert_called_with(zombie)

    def test_18_zombie_hits_arthur(self):
        # Controlla danno zombie
        arena = Mock()
        arena.size.return_value = (1000, 600)
        
        arthur = Mock(spec=Arthur)
        arthur.pos.return_value = (100, 200)
        arthur.size.return_value = (20, 31)
        
        arena.actors.return_value = [arthur]
        
        zombie = Zombie((100, 200), "right")
        zombie._state = "walk"
        
        zombie.move(arena)
        
        arthur.hit.assert_called_once()

    def test_19_plant_shoots_eyeball(self):
        # Controlla sparo pianta
        arena = Mock()
        arena.size.return_value = (1000, 600)
        
        arthur = Mock(spec=Arthur)
        arthur.pos.return_value = (200, 200)
        arthur.size.return_value = (20, 30)
        arena.actors.return_value = [arthur]
        
        plant = Plant((100, 200))
        plant._shoot_timer = 0
        
        plant.move(arena)
        
        args, _ = arena.spawn.call_args
        self.assertIsInstance(args[0], Eyeball)

    def test_20_eyeball(self):
        # Controlla homing eyeball
        arthur = Mock(spec=Arthur)
        arthur.pos.return_value = (200, 100) 
        arthur.size.return_value = (20, 30)
        
        eyeball = Eyeball((100, 50), arthur)
        
        self.assertTrue(eyeball._dx > 0)
        self.assertTrue(eyeball._dy > 0)

    def test_21_torch_kills_zombie(self):
        # Controlla torcia uccide zombie
        arena = Mock()
        arena.size.return_value = (1000, 600)
        
        zombie = Mock(spec=Zombie)
        zombie.pos.return_value = (150, 150)
        zombie.size.return_value = (20, 30)
        arena.actors.return_value = [zombie]
        
        torch = Torch((150, 150), "right")
        
        torch.move(arena)
        
        arena.kill.assert_called_with(zombie)
        self.assertFalse(torch._alive)

    def test_22_torch_hits_gravestone_no_flame(self):
        # Controlla che la torcia colpendo una tomba sparisca SENZA creare fuoco
        arena = Mock()
        arena.size.return_value = (1000, 600)
        
        grave = Gravestone((150, 150))
        arena.actors.return_value = [grave]
        
        torch = Torch((150, 150), "right")
        
        torch.move(arena)
        
        self.assertFalse(torch._alive)
        arena.spawn.assert_not_called()

if __name__ == "__main__":
    unittest.main()