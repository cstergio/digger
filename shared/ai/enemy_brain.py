from collections import deque
from shared.model.types import Direction, TileType, MonsterForm, GameMode


# Λεξικό που μετατρέπει μια κατεύθυνση σε μεταβολή συντεταγμένων (dx, dy)
# Χρησιμοποιείται τόσο για αναζήτηση όσο και για τελική κίνηση
DIRS = {
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
}


class EnemyBrain:
    """
    Σύστημα τεχνητής νοημοσύνης (AI) των εχθρών.

    Υλοποιεί λογική απόφασης κατεύθυνσης κίνησης
    χρησιμοποιώντας αναζήτηση διαδρομής (BFS) σε πλέγμα.

    Η συμπεριφορά εξαρτάται από:
    - τη μορφή του εχθρού (Nobbin / Hobbin)
    - την κατάσταση του παιχνιδιού (Normal / Bonus)
    """

    def decide(self, enemy, player, level, game_mode):
        """
        Αποφασίζει προς ποια κατεύθυνση θα κινηθεί ο εχθρός στο επόμενο βήμα.

        Επιστρέφει:
        - Direction (UP, DOWN, LEFT, RIGHT)
        - ή None αν δεν υπάρχει έγκυρη κίνηση
        """

        # Αρχική θέση εχθρού
        start = (enemy.tile_x, enemy.tile_y)

        # =========================
        # BONUS MODE — FLEE LOGIC
        # =========================
        # Αν το παιχνίδι βρίσκεται σε BONUS mode,
        # ο εχθρός προσπαθεί να απομακρυνθεί από τον παίκτη
        if game_mode == GameMode.BONUS:
            # Υπολογισμός διανύσματος από τον παίκτη προς τον εχθρό
            dx = enemy.tile_x - player.tile_x
            dy = enemy.tile_y - player.tile_y

            # Στόχος: ένα tile προς την αντίθετη κατεύθυνση
            goal = (enemy.tile_x + dx, enemy.tile_y + dy)
        else:
            # Κανονικό mode: στόχος είναι η θέση του παίκτη
            goal = (player.tile_x, player.tile_y)

        # =========================
        # BFS ΑΝΑΖΗΤΗΣΗ ΔΙΑΔΡΟΜΗΣ
        # =========================

        # Ουρά BFS (First In – First Out)
        queue = deque([start])

        # Λεξικό που κρατά από ποιο tile ήρθαμε σε κάθε tile
        # Χρησιμοποιείται για ανακατασκευή της διαδρομής
        came_from = {start: None}

        # Όσο υπάρχουν κόμβοι προς εξερεύνηση
        while queue:
            cx, cy = queue.popleft()

            # Αν φτάσαμε στο στόχο, σταματάμε
            if (cx, cy) == goal:
                break

            # Εξερεύνηση γειτονικών tiles
            for direction, (dx, dy) in DIRS.items():
                nx, ny = cx + dx, cy + dy

                # Έλεγχος ορίων πίστας
                if not level.in_bounds(nx, ny):
                    continue

                # Τύπος πλακιδίου
                tile = level.get_tile(nx, ny)

                # =========================
                # ΚΑΝΟΝΕΣ ΚΙΝΗΣΗΣ ΑΝΑ ΜΟΡΦΗ
                # =========================

                # Nobbin: κινείται ΜΟΝΟ σε tunnels
                if enemy.form == MonsterForm.NOBBIN:
                    if tile != TileType.TUNNEL:
                        continue

                # Hobbin: μπορεί να σκάβει
                elif enemy.form == MonsterForm.HOBBIN:
                    if tile not in (
                        TileType.TUNNEL,
                        TileType.DIRT,
                        TileType.EMERALD,
                    ):
                        continue

                # Αν το tile δεν έχει επισκεφθεί ακόμα
                if (nx, ny) not in came_from:
                    # Καταγράφουμε από πού ήρθαμε
                    came_from[(nx, ny)] = (cx, cy)
                    queue.append((nx, ny))

        # =========================
        # ΑΝ ΔΕΝ ΒΡΕΘΗΚΕ ΔΙΑΔΡΟΜΗ
        # =========================
        if goal not in came_from:
            return None

        # =========================
        # ΑΝΑΚΑΤΑΣΚΕΥΗ ΠΡΩΤΟΥ ΒΗΜΑΤΟΣ
        # =========================

        # Ξεκινάμε από τον στόχο
        cur = goal

        # Πηγαίνουμε πίσω μέχρι το tile που είναι ακριβώς δίπλα στον εχθρό
        while came_from[cur] != start:
            cur = came_from[cur]

            # Ασφαλιστική δικλείδα
            if cur is None:
                return None

        # Υπολογισμός διαφοράς θέσης
        dx = cur[0] - enemy.tile_x
        dy = cur[1] - enemy.tile_y

        # Μετατροπή διαφοράς σε Direction
        for direction, (vx, vy) in DIRS.items():
            if (vx, vy) == (dx, dy):
                return direction

        # Αν κάτι πήγε στραβά
        return None
