import pygame
import os

from shared.model.types import MonsterForm


class EnemySprite:
    """
    Κλάση υπεύθυνη για την οπτική αναπαράσταση των εχθρών (enemies).

    Η κλάση αυτή:
    - δεν περιέχει λογική AI
    - δεν περιέχει λογική κίνησης
    - δεν αλλάζει την κατάσταση του enemy

    Διαβάζει μόνο:
    - τη μορφή του enemy (NOBBIN / HOBBIN)
    - την κίνησή του στον άξονα x
    και επιλέγει το κατάλληλο sprite.
    """

    # Σταθερό μέγεθος πλακιδίου (32x32 pixels)
    TILE_SIZE = 32

    def __init__(self):
        # --------------------------------------------------
        # Εντοπισμός φακέλου sprites με ασφάλεια
        # --------------------------------------------------
        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(base_dir, "..", "..", "assets", "sprites")

        # ==================================================
        # Φόρτωση sprites
        # Θεωρούμε ότι τα βασικά sprites κοιτάνε ΑΡΙΣΤΕΡΑ
        # ==================================================

        # Sprite για NOBBIN που κοιτάει αριστερά
        self.nobbin_left = pygame.image.load(
            os.path.join(assets_dir, "nobbin.png")
        ).convert_alpha()

        # Sprite για NOBBIN που κοιτάει δεξιά (flip)
        self.nobbin_right = pygame.transform.flip(
            self.nobbin_left, True, False
        )

        # Sprite για HOBBIN που κοιτάει αριστερά
        self.hobbin_left = pygame.image.load(
            os.path.join(assets_dir, "hobbin.png")
        ).convert_alpha()

        # Sprite για HOBBIN που κοιτάει δεξιά (flip)
        self.hobbin_right = pygame.transform.flip(
            self.hobbin_left, True, False
        )

        # ==================================================
        # Κατάσταση sprite ΑΝΑ enemy
        # (δεν αποθηκεύεται στο μοντέλο Enemy)
        # ==================================================

        # Λεξικό που αποθηκεύει αν ο enemy κοιτάει αριστερά
        # key: id(enemy), value: True / False
        self._facing_left = {}

        # Λεξικό που αποθηκεύει την προηγούμενη θέση x
        # Χρησιμοποιείται για να καταλάβουμε την κατεύθυνση κίνησης
        self._last_x = {}

    # ==================================================
    # Σχεδίαση enemy
    # ==================================================
    def draw(self, surface, enemy, sx, sy):
        """
        Σχεδιάζει τον enemy στην οθόνη.

        surface : pygame Surface (οθόνη ή υπο-οθόνη)
        enemy   : αντικείμενο Enemy (μοντέλο παιχνιδιού)
        sx, sy  : συντεταγμένες οθόνης (screen coordinates)
        """

        # Χρησιμοποιούμε το id(enemy) ώστε να ξεχωρίζουμε
        # διαφορετικούς enemies χωρίς να αλλάζουμε το μοντέλο
        eid = id(enemy)

        # --------------------------------------------------
        # Αρχικοποίηση κατάστασης για νέο enemy
        # --------------------------------------------------
        if eid not in self._facing_left:
            # Από προεπιλογή θεωρούμε ότι κοιτάει αριστερά
            self._facing_left[eid] = True

            # Αποθηκεύουμε την αρχική θέση x
            self._last_x[eid] = enemy.tile_x

        # --------------------------------------------------
        # Ανίχνευση κατεύθυνσης κίνησης
        # --------------------------------------------------

        # Αν το x αυξήθηκε, ο enemy κινείται δεξιά
        if enemy.tile_x > self._last_x[eid]:
            self._facing_left[eid] = False

        # Αν το x μειώθηκε, ο enemy κινείται αριστερά
        elif enemy.tile_x < self._last_x[eid]:
            self._facing_left[eid] = True

        # Ενημέρωση της τελευταίας θέσης x
        self._last_x[eid] = enemy.tile_x

        # --------------------------------------------------
        # Επιλογή sprite με βάση:
        # 1) μορφή enemy (NOBBIN / HOBBIN)
        # 2) κατεύθυνση (αριστερά / δεξιά)
        # --------------------------------------------------
        if enemy.form == MonsterForm.HOBBIN:
            sprite = (
                self.hobbin_left
                if self._facing_left[eid]
                else self.hobbin_right
            )
        else:
            sprite = (
                self.nobbin_left
                if self._facing_left[eid]
                else self.nobbin_right
            )

        # --------------------------------------------------
        # Σχεδίαση sprite στην οθόνη
        # --------------------------------------------------
        surface.blit(sprite, (sx, sy))
