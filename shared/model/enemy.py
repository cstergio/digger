from shared.model.entity import Entity
# Εισαγωγή της βασικής κλάσης Entity,
# από την οποία κληρονομούν όλες οι οντότητες του παιχνιδιού
# που έχουν θέση στο grid και κατάσταση ζωής.

from shared.model.types import MonsterForm
# Εισαγωγή του Enum MonsterForm,
# το οποίο ορίζει τις μορφές του εχθρού (NOBBIN / HOBBIN)


class Enemy(Entity):
    """
    Κλάση που αναπαριστά έναν εχθρό του παιχνιδιού.

    Ο εχθρός έχει δύο μορφές:
    - NOBBIN: κινείται μόνο μέσα σε υπάρχοντα tunnels
    - HOBBIN: μπορεί να σκάβει το χώμα (DIRT -> TUNNEL)

    Η αλλαγή μορφής γίνεται δυναμικά κατά τη διάρκεια του παιχνιδιού
    μέσω ειδικού συστήματος (EnemyFormSystem).
    """

    def __init__(self, entity_id: str, tile_x: int, tile_y: int):
        # Κλήση του constructor της βασικής κλάσης Entity
        # Αρχικοποιεί:
        # - entity_id
        # - tile_x
        # - tile_y
        # - dir
        # - alive
        super().__init__(entity_id, tile_x, tile_y)

        # Κατάσταση ζωής του εχθρού
        # True  -> ο εχθρός είναι ενεργός
        # False -> ο εχθρός έχει σκοτωθεί
        self.alive = True

        # Τρέχουσα μορφή του εχθρού
        # Ξεκινά πάντα ως NOBBIN
        self.form = MonsterForm.NOBBIN

        # Χρονόμετρο που μετρά πόσο χρόνο
        # ο εχθρός βρίσκεται στην τρέχουσα μορφή
        # Χρησιμοποιείται για την εναλλαγή NOBBIN <-> HOBBIN
        self.form_timer = 0.0

        # Ανεξάρτητο χρονόμετρο κίνησης του εχθρού
        # Επιτρέπει στους εχθρούς να κινούνται
        # με διαφορετική ταχύτητα από τον παίκτη
        self.move_timer = 0.0
