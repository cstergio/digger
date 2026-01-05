from shared.model.types import Direction
# Εισαγωγή του Enum Direction,
# το οποίο ορίζει προς ποια κατεύθυνση κινείται η σφαίρα
# (UP, DOWN, LEFT, RIGHT)


class Bullet:
    """
    Κλάση που αναπαριστά μία σφαίρα (projectile).

    Η σφαίρα:
    - ξεκινά από τη θέση του παίκτη
    - κινείται σε μία σταθερή κατεύθυνση
    - έχει περιορισμένη διάρκεια ζωής
    - εξαφανίζεται είτε με τον χρόνο είτε αν συγκρουστεί
    """

    def __init__(self, tile_x: int, tile_y: int, direction: Direction):
        # Αρχική θέση της σφαίρας στο grid (σε tiles)
        self.tile_x = tile_x
        self.tile_y = tile_y

        # Κατεύθυνση κίνησης της σφαίρας
        # Η κατεύθυνση ορίζεται τη στιγμή που πυροβολεί ο παίκτης
        self.direction = direction

        # Μέγιστη διάρκεια ζωής της σφαίρας (σε δευτερόλεπτα)
        # Μετά από αυτό το χρονικό διάστημα η σφαίρα "λήγει"
        self.life_time = 0.8

        # Χρόνος που έχει περάσει από τη δημιουργία της σφαίρας
        self._age = 0.0

        # Χρονόμετρο για το απλό animation (flicker)
        # Χρησιμοποιείται για να αναβοσβήνει η σφαίρα
        self._anim_timer = 0.0

        # Ορίζει αν η σφαίρα είναι ορατή στο συγκεκριμένο frame
        # Αλλάζει τιμή ώστε να δημιουργείται arcade αίσθηση
        self.visible = True

    def update(self, dt: float):
        """
        Ενημέρωση της κατάστασης της σφαίρας ανά frame.

        Το dt είναι ο χρόνος που πέρασε από το προηγούμενο frame.
        """

        # Αύξηση της "ηλικίας" της σφαίρας
        self._age += dt

        # Αύξηση του timer για το animation
        self._anim_timer += dt

        # Απλό εφέ αναβοσβησίματος (flicker)
        # Κάθε 0.05 δευτερόλεπτα αλλάζει η ορατότητα
        if self._anim_timer >= 0.05:
            self.visible = not self.visible
            self._anim_timer = 0.0

    @property
    def expired(self) -> bool:
        """
        Επιστρέφει True αν η σφαίρα έχει ξεπεράσει
        τον επιτρεπτό χρόνο ζωής της.

        Χρησιμοποιείται από το BulletSystem
        για να αφαιρεί παλιές σφαίρες.
        """
        return self._age >= self.life_time
