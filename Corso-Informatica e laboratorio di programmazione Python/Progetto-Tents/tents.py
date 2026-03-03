#!/usr/bin/env python3
"""
Gioco Tents - Progetto per Fondamenti di Informatica

@author Thiam El Hadji Fallou
"""

# TODO mettere apposto l'autosolving

from boardgame import BoardGame


# Simboli che uso per le cose nel gioco
# Li ho messi come costanti così se voglio cambiarli lo faccio una volta sola
TREE = "T"      # L'albero
TENT = "X"      # La tenda che devo piazzare
GRASS = "-"     # Quando sono sicuro che lì non ci va niente
EMPTY = ""      # Cella ancora da decidere


class Tents(BoardGame):
    """
    Classe principale del gioco:
    
    In pratica devo mettere le tende vicino agli alberi. Ogni albero ha
    una e una sola tenda associata, e le tende non possono toccarsi
    neanche in diagonale. Poi ci sono i numeri sui bordi che dicono
    quante tende ci devono essere in quella riga/colonna.
    """

    def __init__(self, filename: str | None = None) -> None:
        """
        Quando creo una nuova partita, imposto tutte le variabili che mi servono.
        Se passo un file lo carica, altrimenti usa uno schema di default per i test.
        """
        # Questi sono i numeri che stanno in cima e a sinistra
        self._col_constraints = []
        self._row_constraints = []
        
        # Qui tengo traccia di dove sono gli alberi
        self._trees = []
        
        # Qui salvo cosa ha messo il giocatore (o l'automatismo)
        # E' un dizionario tipo {(x, y): "X"} o {(x, y): "-"}
        self._annotations = {}
        
        # Quante righe e colonne ha il gioco (senza contare i vincoli)
        self._game_cols = 0
        self._game_rows = 0
        
        # Carico il puzzle
        if filename:
            self._load_from_file(filename)
        else:
            self._init_default()

    def _init_default(self) -> None:
        """
        Questo è un puzzle di default che uso per i test.
        L'ho preso dal file 5x5-example perché è il più semplice.
        """
        # I numeri in cima (vincoli colonne)
        self._col_constraints = [2, 0, 1, 0, 2]
        self._game_cols = 5
        
        # I numeri a sinistra (vincoli righe)
        self._row_constraints = [2, 0, 2, 0, 1]
        self._game_rows = 5
        
        # Posizioni degli alberi (coordinate x, y)
        self._trees = [
            (1, 0), (4, 1), (1, 2), (3, 2), (4, 3)
        ]

    def _load_from_file(self, filename: str) -> None:
        """
        Legge un puzzle da un file di testo.
        
        Il file è tipo:
        .20102      <- prima riga: punto + vincoli colonne
        2.T...      <- seconda riga: vincolo + celle (T = albero)
        0....T
        ... e così via
        """
        with open(filename, 'r') as f:
            lines = f.read().strip().split('\n')
        
        # La prima riga ha i vincoli delle colonne
        # Il primo carattere è un punto che ignoro
        first_line = lines[0]
        self._col_constraints = [int(c) for c in first_line[1:]]
        self._game_cols = len(self._col_constraints)
        
        # Le altre righe hanno il vincolo di riga + le celle
        self._row_constraints = []
        self._trees = []
        
        for y, line in enumerate(lines[1:]):
            # Primo carattere = vincolo di questa riga
            self._row_constraints.append(int(line[0]))
            
            # Gli altri caratteri sono le celle
            # Se c'è una T, è un albero
            for x, c in enumerate(line[1:]):
                if c == 'T':
                    self._trees.append((x, y))
        
        self._game_rows = len(self._row_constraints)

    # ========== Metodi getter da BoardGame ==========

    def cols(self) -> int:
        """Quante colonne ha la griglia (gioco + colonna vincoli)"""
        return self._game_cols + 1

    def rows(self) -> int:
        """Quante righe ha la griglia (gioco + riga vincoli)"""
        return self._game_rows + 1

    def read(self, x: int, y: int) -> str:
        """
        Cosa c'è nella cella (x, y)?
        
        La cella (0,0) è vuota (angolo in alto a sinistra).
        La riga 0 ha i vincoli delle colonne.
        La colonna 0 ha i vincoli delle righe.
        Il resto è il gioco vero e proprio.
        """
        # Angolo vuoto
        if x == 0 and y == 0:
            return ""
        
        # Vincoli colonne (prima riga)
        if y == 0 and x > 0:
            idx = x - 1
            if idx < len(self._col_constraints):
                return str(self._col_constraints[idx])
            return ""
        
        # Vincoli righe (prima colonna)
        if x == 0 and y > 0:
            idx = y - 1
            if idx < len(self._row_constraints):
                return str(self._row_constraints[idx])
            return ""
        
        # Celle di gioco - devo togliere 1 perché la riga/colonna 0 sono i vincoli
        gx = x - 1
        gy = y - 1
        
        # C'è un albero?
        if (gx, gy) in self._trees:
            return TREE
        
        # Il giocatore ha annotato qualcosa?
        if (gx, gy) in self._annotations:
            return self._annotations[(gx, gy)]
        
        # Altrimenti è vuota
        return EMPTY

    def play(self, x: int, y: int, action: str) -> None:
        """
        Quando il giocatore clicca su una cella, ruoto tra:
        vuoto -> prato -> tenda -> vuoto -> ...(loop)
        
        Ignoro i click sui vincoli e sugli alberi (non ha senso).
        """
        # Click sui vincoli? Ignoro
        if x == 0 or y == 0:
            return
        
        # Coordinate del gioco (tolgo l'offset dei vincoli)
        gx = x - 1
        gy = y - 1
        
        # Click su un albero? Ignoro
        if (gx, gy) in self._trees:
            return
        
        # Faccio la rotazione
        current = self._annotations.get((gx, gy), EMPTY)
        
        if current == EMPTY:
            # Vuoto -> Prato
            self._annotations[(gx, gy)] = GRASS
        elif current == GRASS:
            # Prato -> Tenda
            self._annotations[(gx, gy)] = TENT
        elif current == TENT:
            # Tenda -> Vuoto (rimuovo l'annotazione)
            del self._annotations[(gx, gy)]

    def finished(self) -> bool:
        """
        Ho vinto? Controllo che tutto sia a posto:
        - Ci sono tante tende quanti alberi
        - I vincoli di righe e colonne sono rispettati
        - Le tende non si toccano tra loro
        - Ogni tenda è vicina a un albero
        - C'è un'associazione 1-a-1 tra alberi e tende
        """
        tents = self._get_tents()
        
        # Prima cosa: devo avere una tenda per ogni albero
        if len(tents) != len(self._trees):
            return False
        
        # Controllo i vincoli delle colonne
        for col in range(self._game_cols):
            count = sum(1 for (x, y) in tents if x == col)
            if count != self._col_constraints[col]:
                return False
        
        # Controllo i vincoli delle righe
        for row in range(self._game_rows):
            count = sum(1 for (x, y) in tents if y == row)
            if count != self._row_constraints[row]:
                return False
        
        # Controllo che le tende non si tocchino (neanche in diagonale)
        for (x1, y1) in tents:
            for (x2, y2) in tents:
                if (x1, y1) != (x2, y2):
                    # Se sono troppo vicine, male!
                    if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                        return False
        
        # Ogni tenda deve essere vicina ad almeno un albero
        for (tx, ty) in tents:
            has_tree = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (tx + dx, ty + dy) in self._trees:
                    has_tree = True
                    break
            if not has_tree:
                return False
        
        # Infine controllo l'associazione univoca
        if not self._check_matching():
            return False
        
        return True

    def _get_tents(self) -> list[tuple[int, int]]:
        """Restituisce la lista di tutte le posizioni con una tenda."""
        return [(x, y) for (x, y), val in self._annotations.items() if val == TENT]

    def _check_matching(self) -> bool:
        """
        Devo verificare che ci sia un modo di associare 
        ogni albero a una tenda in modo univoco.
        
        Uso un trucco: tolgo le coppie "obbligate" (quando un albero
        ha solo una tenda vicina o viceversa) finché non rimane niente.
        Se alla fine non rimane niente, l'associazione esiste!
        """
        remaining_tents = set(self._get_tents())
        remaining_trees = set(self._trees)
        
        # Continuo finché riesco a togliere qualcosa
        changed = True
        while changed and remaining_trees and remaining_tents:
            changed = False
            
            # Per ogni albero, vedo quante tende ha vicino
            for tree in list(remaining_trees):
                tx, ty = tree
                nearby_tents = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    pos = (tx + dx, ty + dy)
                    if pos in remaining_tents:
                        nearby_tents.append(pos)
                
                # Se ha solo una tenda vicina, li associo per forza
                if len(nearby_tents) == 1:
                    tent = nearby_tents[0]
                    remaining_trees.remove(tree)
                    remaining_tents.remove(tent)
                    changed = True
            
            # Stessa cosa dal punto di vista delle tende
            for tent in list(remaining_tents):
                tx, ty = tent
                nearby_trees = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    pos = (tx + dx, ty + dy)
                    if pos in remaining_trees:
                        nearby_trees.append(pos)
                
                if len(nearby_trees) == 1:
                    tree = nearby_trees[0]
                    remaining_tents.remove(tent)
                    remaining_trees.remove(tree)
                    changed = True
        
        # Se è rimasto qualcosa, non sono riuscito a trovare l'associazione
        return len(remaining_trees) == 0 and len(remaining_tents) == 0

    def status(self) -> str:
        """Mostra lo stato attuale del gioco."""
        if self.finished():
            return "Hai vinto!"
        
        tents = len(self._get_tents())
        trees = len(self._trees)
        return f"Tende: {tents}/{trees}"

    # ========== Automatismi ==========

    def auto_grass(self) -> bool:
        """
        Tasto 'g': mette prato automaticamente dove sono sicuro che non ci va una tenda.
        
        Le regole sono:
        1. Se ho già messo tutte le tende di quella riga/colonna, il resto è prato
        2. Le celle vicine a una tenda (anche in diagonale) sono per forza prato
        3. Le celle che non sono vicine a nessun albero sono prato
        
        Ritorna True se ho messo almeno un prato, False se non ho fatto niente.
        """
        made_changes = False
        
        # Continuo finché riesco a mettere prati
        keep_going = True
        while keep_going:
            keep_going = False
            
            # Guardo tutte le celle
            for gx in range(self._game_cols):
                for gy in range(self._game_rows):
                    if self._is_free(gx, gy):
                        
                        # Regola 1: vincolo già raggiunto
                        if self._col_done(gx) or self._row_done(gy):
                            self._annotations[(gx, gy)] = GRASS
                            keep_going = True
                            made_changes = True
                            continue
                        
                        # Regola 2: vicina a una tenda
                        if self._near_tent(gx, gy):
                            self._annotations[(gx, gy)] = GRASS
                            keep_going = True
                            made_changes = True
                            continue
                        
                        # Regola 3: non vicina a nessun albero
                        if not self._near_tree(gx, gy):
                            self._annotations[(gx, gy)] = GRASS
                            keep_going = True
                            made_changes = True
                            continue
        
        return made_changes

    def _can_place_tent(self, gx: int, gy: int) -> bool:
        """
        Posso mettere una tenda in questa cella?
        
        Devo controllare un sacco di cose:
        - La cella è dentro la griglia
        - La cella è libera (non c'è già qualcosa)
        - Non è vicina ad altre tende
        - È vicina ad almeno un albero
        - Non sfora il vincolo di riga e colonna
        """
        # Controllo che sia dentro la griglia
        if not (0 <= gx < self._game_cols and 0 <= gy < self._game_rows):
            return False
        
        # La cella deve essere libera
        if not self._is_free(gx, gy):
            return False
        
        # Non deve essere vicina ad altre tende
        if self._near_tent(gx, gy):
            return False
        
        # Deve essere vicina ad almeno un albero
        if not self._near_tree(gx, gy):
            return False
        
        # Non devo superare il vincolo della colonna
        col_tents = self._count_tents_col(gx)
        if col_tents >= self._col_constraints[gx]:
            return False
        
        # Non devo superare il vincolo della riga
        row_tents = self._count_tents_row(gy)
        if row_tents >= self._row_constraints[gy]:
            return False
        
        return True

    def auto_tent(self) -> bool:
        """
        Tasto 't': mette tende automaticamente dove sono sicuro.
        
        Le regole:
        1. Se in una colonna/riga le celle valide = tende mancanti, riempio tutto
        2. Se un albero ha solo una cella valida vicino, ci metto la tenda
        3. Se le celle valide totali = tende mancanti totali, riempio tutto
        
        Ritorna True se ho fatto qualcosa, False altrimenti.
        """
        made_changes = False
        
        keep_going = True
        while keep_going:
            keep_going = False
            
            # Regola 1a: controllo colonne
            for col in range(self._game_cols):
                current = self._count_tents_col(col)
                target = self._col_constraints[col]
                missing = target - current
                
                if missing > 0:
                    # Trovo le celle dove posso mettere una tenda
                    valid_cells = []
                    for gy in range(self._game_rows):
                        if self._can_place_tent(col, gy):
                            valid_cells.append((col, gy))
                    
                    # Se ho esattamente il numero di celle che mi servono, le riempio
                    if len(valid_cells) == missing:
                        for pos in valid_cells:
                            if self._can_place_tent(pos[0], pos[1]):
                                self._annotations[pos] = TENT
                                keep_going = True
                                made_changes = True
            
            # Regola 1b: stessa cosa per le righe
            for row in range(self._game_rows):
                current = self._count_tents_row(row)
                target = self._row_constraints[row]
                missing = target - current
                
                if missing > 0:
                    valid_cells = []
                    for gx in range(self._game_cols):
                        if self._can_place_tent(gx, row):
                            valid_cells.append((gx, row))
                    
                    if len(valid_cells) == missing:
                        for pos in valid_cells:
                            if self._can_place_tent(pos[0], pos[1]):
                                self._annotations[pos] = TENT
                                keep_going = True
                                made_changes = True
            
            # Regola 2: albero con una sola scelta
            for (tx, ty) in self._trees:
                # L'albero ha già una tenda? Salto
                if self._tree_has_tent(tx, ty):
                    continue
                
                # Quali celle possono accogliere la sua tenda?
                cells = self._free_neighbors(tx, ty)
                valid = [p for p in cells if self._can_place_tent(p[0], p[1])]
                
                # Se c'è solo una scelta, la faccio
                if len(valid) == 1:
                    pos = valid[0]
                    if self._can_place_tent(pos[0], pos[1]):
                        self._annotations[pos] = TENT
                        keep_going = True
                        made_changes = True
            
            # Regola 3: conteggio globale
            placed = len(self._get_tents())
            total = len(self._trees)
            missing_total = total - placed
            
            if missing_total > 0:
                all_valid = []
                for gx in range(self._game_cols):
                    for gy in range(self._game_rows):
                        if self._can_place_tent(gx, gy):
                            all_valid.append((gx, gy))
                
                if len(all_valid) == missing_total:
                    for pos in all_valid:
                        if self._can_place_tent(pos[0], pos[1]):
                            self._annotations[pos] = TENT
                            keep_going = True
                            made_changes = True
        
        return made_changes

    # ========== Funzioni per controllare le cose ==========

    def _is_free(self, gx: int, gy: int) -> bool:
        """La cella è libera? (non c'è albero e non ho annotato niente)"""
        if (gx, gy) in self._trees:
            return False
        if (gx, gy) in self._annotations:
            return False
        return True

    def _col_done(self, col: int) -> bool:
        """Ho già messo tutte le tende che servono in questa colonna?"""
        count = self._count_tents_col(col)
        return count >= self._col_constraints[col]

    def _row_done(self, row: int) -> bool:
        """Ho già messo tutte le tende che servono in questa riga?"""
        count = self._count_tents_row(row)
        return count >= self._row_constraints[row]

    def _count_tents_col(self, col: int) -> int:
        """Quante tende ci sono in questa colonna?"""
        count = 0
        for (x, y), val in self._annotations.items():
            if x == col and val == TENT:
                count += 1
        return count

    def _count_tents_row(self, row: int) -> int:
        """Quante tende ci sono in questa riga?"""
        count = 0
        for (x, y), val in self._annotations.items():
            if y == row and val == TENT:
                count += 1
        return count

    def _count_free_col(self, col: int) -> int:
        """Quante celle libere ci sono in questa colonna?"""
        count = 0
        for gy in range(self._game_rows):
            if self._is_free(col, gy):
                count += 1
        return count

    def _count_free_row(self, row: int) -> int:
        """Quante celle libere ci sono in questa riga?"""
        count = 0
        for gx in range(self._game_cols):
            if self._is_free(gx, row):
                count += 1
        return count

    def _near_tent(self, gx: int, gy: int) -> bool:
        """
        C'è una tenda vicina (in tutte le 8 direzioni)?
        Le tende non possono toccarsi neanche in diagonale!
        """
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Non controllo la cella stessa
                pos = (gx + dx, gy + dy)
                if self._annotations.get(pos) == TENT:
                    return True
        return False

    def _near_tree(self, gx: int, gy: int) -> bool:
        """C'è un albero vicino? (solo 4 direzioni, non diagonale)"""
        for (tx, ty) in self._trees:
            # Distanza Manhattan = 1 significa che sono proprio vicini
            if abs(gx - tx) + abs(gy - ty) == 1:
                return True
        return False

    def _near_free_tree(self, gx: int, gy: int) -> bool:
        """C'è un albero vicino che non ha ancora una tenda?"""
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pos = (gx + dx, gy + dy)
            if pos in self._trees:
                if not self._tree_has_tent(pos[0], pos[1]):
                    return True
        return False

    def _tree_has_tent(self, tx: int, ty: int) -> bool:
        """Questo albero ha già una tenda vicina?"""
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pos = (tx + dx, ty + dy)
            if self._annotations.get(pos) == TENT:
                return True
        return False

    def _free_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Quali celle libere ci sono vicino a questa posizione?"""
        result = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pos = (x + dx, y + dy)
            # Controllo che sia dentro la griglia
            if 0 <= pos[0] < self._game_cols and 0 <= pos[1] < self._game_rows:
                if self._is_free(pos[0], pos[1]):
                    result.append(pos)
        return result

    # ========== Viecolo cieco ==========

    def wrong(self) -> bool:
        """
        La situazione è impossibile? Controllo varie cose che non devono succedere.
        
        Se ritorno True, significa che da qui non si può vincere. Magari ho fatto
        un errore prima e devo tornare indietro.
        """
        tents = [(x, y) for (x, y), v in self._annotations.items() if v == TENT]
        
        # Problema 1: due tende si toccano
        for (x1, y1) in tents:
            for (x2, y2) in tents:
                if (x1, y1) != (x2, y2):
                    if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                        return True  # Le tende si toccano
        
        # Problema 2: una tenda non è vicina a nessun albero
        for (tx, ty) in tents:
            has_tree = False
            for (ax, ay) in self._trees:
                if abs(tx - ax) + abs(ty - ay) == 1:
                    has_tree = True
                    break
            if not has_tree:
                return True  # La tenda è isolata
        
        # Problema 3: ho messo troppe tende in una colonna
        for col in range(self._game_cols):
            count = sum(1 for (x, y), v in self._annotations.items() if x == col and v == TENT)
            target = self._col_constraints[col]
            
            if count > target:
                return True  # Troppe tende!
            
            # Oppure: non ho abbastanza spazio per raggiungere il vincolo
            available = 0
            for row in range(self._game_rows):
                if self._can_be_tent(col, row):
                    available += 1
            
            if count + available < target:
                return True  # Non ce la farò mai
        
        # Problema 4: stessa cosa per le righe
        for row in range(self._game_rows):
            count = sum(1 for (x, y), v in self._annotations.items() if y == row and v == TENT)
            target = self._row_constraints[row]
            
            if count > target:
                return True
            
            available = 0
            for col in range(self._game_cols):
                if self._can_be_tent(col, row):
                    available += 1
            
            if count + available < target:
                return True
        
        # Problema 5: un albero non ha più celle dove mettere la sua tenda
        for (tx, ty) in self._trees:
            if self._tree_has_tent(tx, ty):
                continue  # Questo albero è a posto
            
            # Conta le celle dove potrei mettere la tenda
            spots = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = tx + dx, ty + dy
                if self._can_be_tent(nx, ny):
                    spots += 1
            
            if spots == 0:
                return True  # L'albero è bloccato!
        
        return False  # Nessun problema trovato

    def _can_be_tent(self, gx: int, gy: int) -> bool:
        """
        Questa cella potrebbe diventare una tenda in futuro?
        """
        # Fuori dalla griglia
        if not (0 <= gx < self._game_cols and 0 <= gy < self._game_rows):
            return False
        # C'è un albero
        if (gx, gy) in self._trees:
            return False
        # C'è già qualcosa
        if (gx, gy) in self._annotations:
            return False
        # È vicina a una tenda
        if self._near_tent(gx, gy):
            return False
        # Non è vicina a nessun albero
        if not self._near_tree(gx, gy):
            return False
        
        return True

    # ========== Suggerimenti ========== 

    def suggest(self) -> bool:
        """
        Tasto 'a': provo a trovare una mossa sicura.
        
        Come funziona: per ogni cella libera, provo a metterci una tenda
        e poi un prato. Se una delle due porte a un vicolo cieco (wrong),
        allora l'altra è la scelta giusta!
        
        Metto solo UNA mossa alla volta, così il giocatore può seguire il ragionamento.
        """
        for gx in range(self._game_cols):
            for gy in range(self._game_rows):
                if self._is_free(gx, gy):
                    
                    # Provo le due opzioni
                    try_tent = self._test_move(gx, gy, TENT)
                    try_grass = self._test_move(gx, gy, GRASS)
                    
                    # Se la tenda porta a vicolo cieco, metto prato
                    if try_tent == "wrong" and try_grass == "ok":
                        self._annotations[(gx, gy)] = GRASS
                        return True
                    
                    # Se il prato porta a vicolo cieco, metto tenda
                    if try_grass == "wrong" and try_tent == "ok":
                        self._annotations[(gx, gy)] = TENT
                        return True
                    
                    # Se entrambi portano a vicolo cieco, ho sbagliato prima
                    # Se entrambi sono ok, non posso decidere ancora
        
        # Se non ho trovato niente di sicuro, provo con il metodo avanzato
        return self.advanced_suggest()

    def _apply_auto(self) -> None:
        """Applica prato e tenda automatici finché cambiano cose."""
        changed = True
        while changed:
            before = len(self._annotations)
            self.auto_grass()
            self.auto_tent()
            changed = len(self._annotations) > before

    def _test_move(self, gx: int, gy: int, symbol: str) -> str:
        """
        Simulo una mossa per vedere se porta a vicolo cieco.
        
        Salvo lo stato, faccio la mossa + automatismi, controllo wrong(),
        poi rimetto tutto com'era.
        """
        # Salvo lo stato
        backup = dict(self._annotations)
        
        # Faccio la mossa
        self._annotations[(gx, gy)] = symbol
        
        # Applico gli automatismi
        changed = True
        while changed:
            before = len(self._annotations)
            self.auto_grass()
            self.auto_tent()
            changed = len(self._annotations) > before
        
        # Controllo se sono finito in un vicolo cieco
        result = "wrong" if self.wrong() else "ok"
        
        # Rimetto lo stato come prima
        self._annotations = backup
        
        return result

    # ========== Suggerimenti avanzati ========== 

    def advanced_suggest(self) -> bool:
        """
        Metodo più furbo: per ogni cella, simulo entrambe le ipotesi
        e vedo quali altre celle assumono lo stesso valore in entrambi i casi.
        
        Se una cella ha lo stesso valore sia ipotizzando tenda che prato,
        allora quel valore è sicuramente corretto!
        """
        found = False
        
        for gx in range(self._game_cols):
            for gy in range(self._game_rows):
                if self._is_free(gx, gy):
                    
                    # Simulo le due ipotesi
                    result_tent = self._simulate(gx, gy, TENT)
                    result_grass = self._simulate(gx, gy, GRASS)
                    
                    # Se una delle due porta a vicolo cieco, non posso confrontarle
                    if result_tent is None or result_grass is None:
                        continue
                    
                    # Cerco celle che hanno lo stesso valore in entrambe le simulazioni
                    for pos in result_tent:
                        if pos in result_grass:
                            if result_tent[pos] == result_grass[pos]:
                                # Questa cella ha lo stesso valore in entrambi i casi!
                                if pos not in self._annotations:
                                    self._annotations[pos] = result_tent[pos]
                                    found = True
        
        return found

    def _simulate(self, gx: int, gy: int, symbol: str) -> dict[tuple[int, int], str] | None:
        """
        Simulo una mossa e ritorno lo stato risultante.
        Se porta a wrong, ritorno None.
        """
        backup = dict(self._annotations)
        
        self._annotations[(gx, gy)] = symbol
        
        # Applico automatismi
        changed = True
        while changed:
            before = len(self._annotations)
            self.auto_grass()
            self.auto_tent()
            changed = len(self._annotations) > before
        
        # Se wrong, niente
        if self.wrong():
            self._annotations = backup
            return None
        
        # Copio il risultato
        result = dict(self._annotations)
        
        # Rimetto lo stato di prima
        self._annotations = backup
        
        return result

    # ========== Risoluzione automatica  ==========

    def solve(self) -> bool:
        """
        Provo a risolvere il puzzle da solo.
        
        Uso tutti i metodi che ho: automatismi, suggerimenti, suggerimenti avanzati.
        Se non faccio progressi per un po', mi arrendo.
        """
        max_tries = 1000  # Non voglio restare bloccato per sempre
        
        for _ in range(max_tries):
            # Ho vinto?
            if self.finished():
                return True
            
            # Sono in vicolo cieco?
            if self.wrong():
                return False
            
            before = len(self._annotations)
            
            # Provo gli automatismi
            self.auto_grass()
            self.auto_tent()
            
            # Ho fatto progressi? Continuo
            if len(self._annotations) > before:
                continue
            
            # Provo i suggerimenti
            if self.suggest():
                continue
            
            # Provo i suggerimenti avanzati
            if self.advanced_suggest():
                continue
            
            # Non riesco a fare progressi, mi arrendo
            break
        
        return self.finished()


# ==================== GUI ====================

def play_with_gui(filename: str | None = None) -> None:
    """Avvia il gioco con la finestra grafica."""
    from boardgamegui import BoardGameGui
    import g2d
    
    # Dimensioni delle celle
    W, H = 40, 40
    
    # Colori che uso
    GRASS_GREEN = (144, 238, 144)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    game = Tents(filename)
    
    # Configurazione tasti
    actions = {
        "LeftButton": "",       # Click: ruota vuoto/prato/tenda
        "g": "auto_grass",      # G: metti prati automatici
        "t": "auto_tent",       # T: metti tende automatiche
        "a": "suggest",         # A: dammi un suggerimento
        "r": "reset",           # R: resetta la partita
        "v": "solve"            # V: risolvi automaticamente
    }
    
    # Personalizzo la GUI per fare il prato verde e le tende rosse
    class TentsGui(BoardGameGui):
        def write(self, text: str, pos: tuple[int, int], cols: int = 1) -> None:
            x, y = pos
            # Colora alberi, tende e prati in verde, il resto bianco
            if text == TENT or text == GRASS or text == TREE:
                g2d.set_color(GRASS_GREEN)
            else:
                g2d.set_color(WHITE)
            g2d.draw_rect((x * W + 1, y * H + 1), (cols * W - 2, H - 2))
            # Scrivo il testo
            if text:
                chars = max(1, len(text))
                fsize = min(0.75 * H, 1.5 * cols * W / chars)
                center = (x * W + cols * W/2, y * H + H/2)
                g2d.set_color(BLACK)
                g2d.draw_text(text, center, fsize)
    
    # Gestisco i tasti speciali
    original_play = game.play
    
    def extended_play(x: int, y: int, action: str) -> None:
        if action == "auto_grass":
            if not game.auto_grass():
                print("[g] Nessun prato da mettere")
        elif action == "auto_tent":
            if not game.auto_tent():
                print("[t] Nessuna tenda da mettere")
        elif action == "suggest":
            if not game.suggest():
                print("[a] Nessun suggerimento trovato")
        elif action == "reset":
            game._annotations = {}
            print("[r] Reset completato")
        elif action == "solve":
            result = game.solve()
            if result:
                print("[v] Risolto!")
            else:
                print("[v] Impossibile risolvere")
        else:
            original_play(x, y, action)
    
    game.play = extended_play
    
    g2d.init_canvas((game.cols() * W, game.rows() * H + H))
    gui = TentsGui(game, actions, {})
    g2d.main_loop(gui.tick)


def select_level() -> str:
    """Menu per scegliere il livello."""
    
    levels = [
        "tents-2025-11-27-5x5-example.txt",
        "tents-2025-11-27-8x8-easy.txt",
        "tents-2025-11-27-8x8-medium.txt",
        "tents-2025-11-27-12x12-easy.txt",
        "tents-2025-11-27-12x12-medium.txt",
        "tents-2025-11-27-16x16-easy.txt",
        "tents-2025-11-27-16x16-medium.txt",
        "tents-2025-11-27-20x20-special.txt"
    ]
    
    print("\n=== GIOCO TENTS ===")
    print("\nSeleziona un livello:")
    
    for i, level in enumerate(levels, 1):
        name = level.split("/")[-1]
        print(f"{i}. {name}")
    
    print("\nInserisci il numero del livello: ", end="")
    
    try:
        choice = int(input())
        if 1 <= choice <= len(levels):
            return levels[choice - 1]
        else:
            print("Scelta non valida, uso il primo livello.")
            return levels[0]
    except ValueError:
        print("Input non valido, uso il primo livello.")
        return levels[0]


if __name__ == "__main__":
    filename = select_level()
    play_with_gui(filename)
