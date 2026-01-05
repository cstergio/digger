from shared.model.types import TileType, Direction
# Εισάγουμε:
# - TileType: τα είδη πλακιδίων του επιπέδου (DIRT, TUNNEL, GOLD_BAG κ.λπ.)
# - Direction: τις κατευθύνσεις κίνησης (UP, DOWN, LEFT, RIGHT)

from shared.services.audio_manager import AudioManager
# Διαχειρίζεται την αναπαραγωγή ήχων (π.χ. έκρηξη)


# Λεξικό που αντιστοιχίζει κάθε κατεύθυνση σε μετατόπιση στο grid
# Χρησιμοποιείται για τη μετακίνηση της σφαίρας ανά frame
DIR_VECTORS = {
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
}


class BulletSystem:
    """
    Το BulletSystem είναι υπεύθυνο για την ενημέρωση όλων των σφαιρών.

    Αρμοδιότητές του:
    - Μετακινεί τις σφαίρες στο grid
    - Ελέγχει αν έληξε ο χρόνος ζωής τους
    - Ελέγχει συγκρούσεις με το επίπεδο
    - Ελέγχει συγκρούσεις με εχθρούς
    - Επιστρέφει ποιοι εχθροί σκοτώθηκαν και από ποιον παίκτη

    Σημαντικό:
    Το BulletSystem ΔΕΝ αποδίδει πόντους.
    Αυτό γίνεται σε ανώτερο επίπεδο (GameScene).
    """

    def update(self, bullets, level, enemies, dt):
        """
        Ενημερώνει όλες τις σφαίρες για ένα frame.

        bullets : λίστα αντικειμένων Bullet
        level   : το επίπεδο του παιχνιδιού
        enemies : λίστα εχθρών
        dt      : χρόνος που πέρασε από το προηγούμενο frame

        Επιστρέφει:
        - λίστα από tuples (enemy, owner_id)
          ώστε το GameScene να αποδώσει σωστά το σκορ
        """

        # Λίστα με σφαίρες που πρέπει να αφαιρεθούν
        to_remove = []

        # Λίστα με σκοτωμούς (enemy, owner_id)
        kills = []

        # Διατρέχουμε όλες τις ενεργές σφαίρες
        for bullet in bullets:

            # Ενημερώνουμε την εσωτερική κατάσταση της σφαίρας
            # (π.χ. διάρκεια ζωής)
            bullet.update(dt)

            # Αν η σφαίρα έχει λήξει χρονικά
            if bullet.expired:
                to_remove.append(bullet)
                continue

            # Υπολογίζουμε την επόμενη θέση με βάση την κατεύθυνση
            dx, dy = DIR_VECTORS[bullet.direction]
            nx = bullet.tile_x + dx
            ny = bullet.tile_y + dy

            # Αν η σφαίρα βγει εκτός ορίων του επιπέδου
            if not level.in_bounds(nx, ny):
                to_remove.append(bullet)
                continue

            # Ελέγχουμε το πλακίδιο στο οποίο κατευθύνεται
            tile = level.get_tile(nx, ny)

            # Αν το πλακίδιο είναι συμπαγές (χώμα ή σακί χρυσού),
            # η σφαίρα σταματά και καταστρέφεται
            if tile in (TileType.DIRT, TileType.GOLD_BAG):
                to_remove.append(bullet)
                continue

            # Μετακινούμε τη σφαίρα στη νέα θέση
            bullet.tile_x = nx
            bullet.tile_y = ny

            # Έλεγχος σύγκρουσης με εχθρούς
            # Δεν αποδίδουμε σκορ εδώ, μόνο δηλώνουμε το kill
            for enemy in enemies:
                if enemy.alive and enemy.tile_x == nx and enemy.tile_y == ny:

                    # Ο εχθρός πεθαίνει
                    enemy.alive = False

                    # Αναπαραγωγή ήχου έκρηξης
                    AudioManager.play_sound("explosion")

                    # Αναγνωρίζουμε ποιος παίκτης έριξε τη σφαίρα
                    # Αν δεν υπάρχει owner_id, θεωρούμε τον Player 1
                    owner = getattr(bullet, "owner_id", "p1")

                    # Καταγράφουμε τον σκοτωμό
                    kills.append((enemy, owner))

                    # Η σφαίρα καταστρέφεται μετά τη σύγκρουση
                    to_remove.append(bullet)
                    break

        # Αφαιρούμε όλες τις σφαίρες που σημειώθηκαν για διαγραφή
        for b in to_remove:
            if b in bullets:
                bullets.remove(b)

        # Επιστρέφουμε τη λίστα σκοτωμών
        return kills
