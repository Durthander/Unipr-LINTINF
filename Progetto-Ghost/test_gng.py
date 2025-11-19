import unittest
from unittest.mock import Mock

from actor import Arena
from game import (
    Arthur, Ladder, Platform, Gravestone,
    Plant, Eyeball, Flame, Zombie, Torch,
    GngGame, ARENA_W, ARENA_H, VIEW_W
)


# ----------------------------------------------------------------------
#  FIXTURE PRINCIPALE: Arena semplice + Arthur su un pavimento
# ----------------------------------------------------------------------
class ArthurTest(unittest.TestCase):

    def setUp(self):
        self.arena = Arena((600, 224))
        # pavimento a y = 193 come nel gioco
        floor = Platform((0, 193, 600, 31))
        self.arthur = Arthur((100, 160))
        self.arena.spawn(floor)
        self.arena.spawn(self.arthur)

        # faccio qualche tick per farlo assestare a terra
        for _ in range(5):
            self.arena.tick([])

    # ---------------------- movimento base -----------------------------

    def test_move_right(self):
        self.arena.tick(["ArrowRight"])
        x, y = self.arthur.pos()
        self.assertEqual(x, 100 + 4)

    def test_move_left(self):
        self.arena.tick(["ArrowLeft"])
        x, y = self.arthur.pos()
        self.assertEqual(x, 100 - 4)

    def test_horizontal_movement_parametric(self):
        params = [
            (["ArrowRight"], 104),
            (["ArrowLeft"], 96),
            ([], 100)
        ]

        for keys, expected_x in params:
            with self.subTest(keys=keys):
                # reset posizione
                self.arthur._x = 100
                self.arena.tick(keys)
                x, _ = self.arthur.pos()
                self.assertEqual(x, expected_x)

    # ---------------------- salto e gravità ----------------------------

    def test_jump_and_gravity(self):
        # Tick 1: salto → deve salire
        self.arena.tick(["ArrowUp"])
        x, y1 = self.arthur.pos()

        # Tick 2: ancora salita (dy è ancora negativo)
        self.arena.tick([])
        x, y2 = self.arthur.pos()

        self.assertTrue(y2 < y1)

        # Ora facciamo molti tick → deve iniziare a scendere
        previous_y = y2
        descending_detected = False

        for _ in range(40):
            self.arena.tick([])
            x, y = self.arthur.pos()
            if y > previous_y:
                descending_detected = True
                break
            previous_y = y

        self.assertTrue(descending_detected)

    # ---------------------- sprite di base -----------------------------

    def test_idle_sprite_right(self):
        self.arthur._state = "Idle"
        self.arthur._facing = "right"
        self.assertEqual(self.arthur.sprite(), (6, 43))

    def test_idle_sprite_left(self):
        self.arthur._state = "Idle"
        self.arthur._facing = "left"
        self.assertEqual(self.arthur.sprite(), (486, 43))

    # ------------------ sequenze comandi → sprite ----------------------

    def test_sequence_running_sprite(self):
        # prima mi assicuro che sia a terra
        for _ in range(5):
            self.arena.tick([])

        # tengo premuto Right per qualche frame
        for _ in range(4):
            self.arena.tick(["ArrowRight"])

        self.assertEqual(self.arthur._state, "Running")
        sprite = self.arthur.sprite()
        # deve essere uno dei frame di corsa a destra
        frames_right = [(40, 44), (66, 42), (88, 43), (109, 43)]
        self.assertIn(sprite, frames_right)

    def test_sequence_jump_running_sprite(self):
        # cammina a destra un attimo
        self.arena.tick(["ArrowRight"])
        # poi salta mentre corre
        self.arena.tick(["ArrowRight", "ArrowUp"])

        self.assertEqual(self.arthur._state, "Jumping")
        sprite = self.arthur.sprite()
        # jump running a destra
        self.assertEqual(sprite, (144, 29))


    # -------------------- test con oggetto fantoccio -------------------

    def test_hit_reduces_lives_and_kills(self):
        fake_arena = Mock()
        self.assertEqual(self.arthur.lives(), 3)

        # 3 colpi, azzerando il blinking ogni volta
        for _ in range(3):
            self.arthur._blinking = 0
            self.arthur.hit(fake_arena)

        self.assertEqual(self.arthur.lives(), 0)
        fake_arena.kill.assert_called_once_with(self.arthur)


# ----------------------------------------------------------------------
#  TEST COLLISIONI CON GRAVESTONE
# ----------------------------------------------------------------------
class GravestoneTest(unittest.TestCase):

    def setUp(self):
        self.arena = Arena((600, 224))
        floor = Platform((0, 193, 600, 31))
        self.arthur = Arthur((80, 160))
        self.grave = Gravestone((120, 177))   # piccola lapide

        self.arena.spawn(floor)
        self.arena.spawn(self.grave)
        self.arena.spawn(self.arthur)

        for _ in range(5):
            self.arena.tick([])

    def test_collision_side(self):
        """Arthur non deve attraversare lateralmente la lapide."""
        # si muove verso destra finché tocca la lapide
        for _ in range(20):
            self.arena.tick(["ArrowRight"])

        ax, ay = self.arthur.pos()
        aw, ah = self.arthur.size()
        gx, gy = self.grave.pos()
        gw, gh = self.grave.size()

        # nessuna sovrapposizione orizzontale evidente
        overlap = (ax + aw > gx) and (ax < gx + gw) and (ay + ah > gy) and (ay < gy + gh)
        self.assertFalse(overlap)


# ----------------------------------------------------------------------
#  TEST PLANT
# ----------------------------------------------------------------------
class PlantTest(unittest.TestCase):

    def setUp(self):
        self.arena = Arena((600, 224))
        floor = Platform((0, 193, 600, 31))
        self.arthur = Arthur((100, 160))
        self.plant = Plant((200, 160))

        self.arena.spawn(floor)
        self.arena.spawn(self.arthur)
        self.arena.spawn(self.plant)

        for _ in range(5):
            self.arena.tick([])

    def test_plant_faces_arthur_right(self):
        # Arthur a destra della pianta
        self.arthur._x = 300
        self.plant.move(self.arena)
        self.assertEqual(self.plant._facing, "right")

    def test_plant_faces_arthur_left(self):
        self.arthur._x = 100
        self.plant.move(self.arena)
        self.assertEqual(self.plant._facing, "left")

    def test_plant_does_not_shoot_when_far(self):
        # Arthur troppo lontano (oltre VIEW_W / 2)
        self.arthur._x = self.plant._x + VIEW_W
        self.plant._shoot_timer = 1  # quasi pronto a sparare

        # Nessun proiettile deve essere creato
        actors_before = len(self.arena.actors())
        self.plant.move(self.arena)
        actors_after = len(self.arena.actors())

        self.assertEqual(actors_before, actors_after)

    def test_plant_shoots_eyeball_when_close(self):
        # Arthur vicino
        self.arthur._x = self.plant._x + 50
        self.plant._shoot_timer = 1  # tra poco spara

        self.plant.move(self.arena)

        has_eyeball = any(isinstance(a, Eyeball) for a in self.arena.actors())
        self.assertTrue(has_eyeball)


# ----------------------------------------------------------------------
#  TEST EYEBALL
# ----------------------------------------------------------------------
class EyeballTest(unittest.TestCase):

    def setUp(self):
        self.arena = Arena((600, 224))
        floor = Platform((0, 193, 600, 31))
        self.arthur = Arthur((300, 160))
        self.arena.spawn(floor)
        self.arena.spawn(self.arthur)

    def test_eyeball_moves_towards_target(self):
        eye = Eyeball((100, 100), self.arthur)
        self.arena.spawn(eye)

        x0, y0 = eye.pos()
        self.arena.tick([])  # un passo
        x1, y1 = eye.pos()

        # deve essersi avvicinato ad Arthur (che sta più a destra)
        self.assertTrue(x1 > x0)

    def test_eyeball_hits_arthur_and_is_removed(self):
        # Eyeball quasi sopra Arthur
        eye = Eyeball((self.arthur.pos()[0], self.arthur.pos()[1]), self.arthur)
        self.arena.spawn(eye)

        lives_before = self.arthur.lives()
        self.arena.tick([])

        lives_after = self.arthur.lives()
        self.assertTrue(lives_after < lives_before)

        # eyeball deve essere stato rimosso
        self.assertFalse(any(isinstance(a, Eyeball) for a in self.arena.actors()))


# ----------------------------------------------------------------------
#  TEST FLAME
# ----------------------------------------------------------------------
class FlameTest(unittest.TestCase):

    def setUp(self):
        self.arena = Arena((600, 224))
        floor = Platform((0, 193, 600, 31))
        self.arena.spawn(floor)

    def test_flame_kills_zombie_on_overlap(self):
        # piattaforma a y = 193, zombie sopra
        zom = Zombie((150, 193 - 31), "left")
        flame = Flame((150, 193))   # fiamma centrata sullo stesso x

        self.arena.spawn(zom)
        self.arena.spawn(flame)

        # alcuni tick per permettere la collisione
        for _ in range(10):
            self.arena.tick([])

        self.assertFalse(any(isinstance(a, Zombie) for a in self.arena.actors()))

    def test_flame_expires_after_some_time(self):
        flame = Flame((200, 193))
        self.arena.spawn(flame)

        # più tick della durata massima (≈ 48)
        for _ in range(60):
            self.arena.tick([])

        self.assertFalse(any(isinstance(a, Flame) for a in self.arena.actors()))


# ----------------------------------------------------------------------
#  TEST VIEW / CAMERA di GngGame
# ----------------------------------------------------------------------
class CameraTest(unittest.TestCase):

    def setUp(self):
        # monkeypatch di _load_level per evitare accesso al file CSV
        def fake_load_level(self, config_file):
            self._arthur = Arthur((0, 160))
            self.spawn(self._arthur)

        GngGame._load_level = fake_load_level   # patch della classe

        self.game = GngGame()
        # sicurezza: partenza con Arthur all'origine
        self.game.get_arthur()._x = 0
        self.game.update_view()

    def test_view_starts_at_zero(self):
        self.assertEqual(self.game.get_view_x(), 0)

    def test_view_follows_arthur_center(self):
        arthur = self.game.get_arthur()
        arthur._x = 300  # in mezzo circa
        self.game.update_view()

        expected = int(arthur.pos()[0] - VIEW_W / 2)
        self.assertEqual(self.game.get_view_x(), expected)

    def test_view_clamped_left(self):
        arthur = self.game.get_arthur()
        arthur._x = 10   # vicino al bordo sinistro
        self.game.update_view()

        self.assertEqual(self.game.get_view_x(), 0)

    def test_view_clamped_right(self):
        arthur = self.game.get_arthur()
        # molto vicino al bordo destro dell'arena
        arthur._x = ARENA_W - 10
        self.game.update_view()

        max_view = ARENA_W - VIEW_W
        self.assertEqual(self.game.get_view_x(), max_view)


# ----------------------------------------------------------------------
#  MAIN
# ----------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()