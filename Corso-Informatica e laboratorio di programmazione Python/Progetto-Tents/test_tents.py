#!/usr/bin/env python3
"""
Unit test per il gioco Tents
Esercizio 9.9
"""

import unittest
from tents import Tents, TENT, GRASS, TREE


class TestTents(unittest.TestCase):
    """Test per la classe Tents."""

    def test_creazione_default(self):
        """Test creazione gioco con griglia default."""
        game = Tents()
        
        # Verifica dimensioni (6x6 con vincoli)
        self.assertEqual(game.cols(), 6)
        self.assertEqual(game.rows(), 6)

    def test_read_vincoli(self):
        """Test lettura vincoli numerici."""
        game = Tents()
        
        # Vincoli colonne (riga 0)
        self.assertEqual(game.read(1, 0), "2")  # Prima colonna di gioco
        self.assertEqual(game.read(2, 0), "0")
        self.assertEqual(game.read(3, 0), "1")
        self.assertEqual(game.read(4, 0), "0")
        self.assertEqual(game.read(5, 0), "2")
        
        # Vincoli righe (colonna 0)
        self.assertEqual(game.read(0, 1), "2")
        self.assertEqual(game.read(0, 2), "0")
        self.assertEqual(game.read(0, 3), "2")
        self.assertEqual(game.read(0, 4), "0")
        self.assertEqual(game.read(0, 5), "1")

    def test_read_alberi(self):
        """Test lettura posizione alberi."""
        game = Tents()
        
        # Alberi nella griglia default (5x5 example)
        # Tree at game (1,0) -> GUI (2,1)
        self.assertEqual(game.read(2, 1), TREE)
        # Tree at game (4,1) -> GUI (5,2)
        self.assertEqual(game.read(5, 2), TREE)

    def test_play_rotazione(self):
        """Test rotazione al click: vuoto -> prato -> tenda -> vuoto."""
        game = Tents()
        
        # Cella vuota inizialmente (1,1 GUI = 0,0 gioco)
        # (0,0) è vuoto nel nuovo default
        self.assertEqual(game.read(1, 1), "")
        
        # Primo click: prato
        game.play(1, 1, "")
        self.assertEqual(game.read(1, 1), GRASS)
        
        # Secondo click: tenda
        game.play(1, 1, "")
        self.assertEqual(game.read(1, 1), TENT)
        
        # Terzo click: vuoto
        game.play(1, 1, "")
        self.assertEqual(game.read(1, 1), "")

    def test_play_su_albero(self):
        """Test che click su albero non faccia nulla."""
        game = Tents()
        
        # L'albero deve rimanere albero (GUI 2,1)
        game.play(2, 1, "")
        self.assertEqual(game.read(2, 1), TREE)

    def test_play_su_vincoli(self):
        """Test che click sui vincoli non faccia nulla."""
        game = Tents()
        
        # Click su vincolo colonna
        game.play(1, 0, "")
        self.assertEqual(game.read(1, 0), "2")
        
        # Click su vincolo riga
        game.play(0, 1, "")
        self.assertEqual(game.read(0, 1), "2")

    def test_finished_incompleto(self):
        """Test che gioco incompleto non sia finito."""
        game = Tents()
        self.assertFalse(game.finished())

    def test_wrong_tende_adiacenti(self):
        """Test wrong() con due tende adiacenti."""
        game = Tents()
        
        # Metti due tende adiacenti
        game._annotations[(1, 0)] = TENT  # (1,0) gioco
        game._annotations[(2, 0)] = TENT  # (2,0) gioco
        
        self.assertTrue(game.wrong())

    def test_wrong_troppo_tende_colonna(self):
        """Test wrong() con troppe tende in una colonna."""
        game = Tents()
        
        # Colonna 1 ha vincolo 0, mettiamo una tenda
        game._annotations[(1, 0)] = TENT
        
        self.assertTrue(game.wrong())

    def test_wrong_albero_isolato(self):
        """Test wrong() con albero senza celle libere."""
        game = Tents()
        
        # Circonda l'albero in (1,0) gioco -> (2,1) GUI
        # Celle adiacenti libere: (0,0), (2,0), (1,1) -> GUI (1,1), (3,1), (2,2)
        game._annotations[(0, 0)] = GRASS
        game._annotations[(2, 0)] = GRASS
        game._annotations[(1, 1)] = GRASS
        
        self.assertTrue(game.wrong())

    def test_auto_grass_vicina_tenda(self):
        """Test auto_grass marca celle vicine a tende."""
        game = Tents()
        
        # Metti una tenda
        game._annotations[(2, 2)] = TENT
        
        game.auto_grass()
        
        # Celle diagonali dovrebbero essere prato
        self.assertEqual(game._annotations.get((1, 1)), GRASS)
        self.assertEqual(game._annotations.get((3, 1)), GRASS)
        self.assertEqual(game._annotations.get((1, 3)), GRASS)
        self.assertEqual(game._annotations.get((3, 3)), GRASS)

    def test_carica_da_file(self):
        """Test caricamento da file."""
        game = Tents("Progetto-Tents/tents-games/tents-2025-11-27-8x8-easy.txt")
        
        # Verifica dimensioni (9x9 con vincoli per griglia 8x8)
        self.assertEqual(game.cols(), 9)
        self.assertEqual(game.rows(), 9)


class TestTentsSoluzione(unittest.TestCase):
    """Test per la risoluzione automatica."""

    def test_solve_easy(self):
        """Test che il solver faccia progressi."""
        game = Tents("Progetto-Tents/tents-games/tents-2025-11-27-8x8-easy.txt")
        
        # Verifica che il solver riesca a fare qualche progresso
        annotazioni_iniziali = len(game._annotations)
        game.solve()
        annotazioni_finali = len(game._annotations)
        
        # Deve aver fatto progressi
        self.assertGreater(annotazioni_finali, annotazioni_iniziali)


if __name__ == "__main__":
    unittest.main()
