from shared.model.types import Direction
# Εισαγωγή του Enum Direction, το οποίο χρησιμοποιείται
# για να δηλώνει προς ποια κατεύθυνση κοιτάζει ή κινείται ο παίκτης


class Player:
    """
    Κλάση που αναπαριστά έναν παίκτη στο παιχνίδι.
    Περιέχει μόνο την ΚΑΤΑΣΤΑΣΗ του παίκτη (position, direction, alive)
    και ΟΧΙ τη λογική κίνησης ή αλληλεπίδρασης.
    """

    def __init__(self, player_id: str, tile_x: int, tile_y: int):
        # Μοναδικό αναγνωριστικό παίκτη (π.χ. "p1", "p2")
        self.id = player_id

        # Συντεταγμένες του παίκτη στο grid του επιπέδου (σε tiles)
        self.tile_x = tile_x
        self.tile_y = tile_y

        # Κατεύθυνση προς την οποία "κοιτάζει" ο παίκτης
        # Χρησιμοποιείται κυρίως από το σύστημα όπλου
        # Είναι None όταν ο παίκτης δεν έχει κινηθεί ακόμα
        self.direction: Direction | None = None

        # Κατάσταση ζωής του παίκτη
        # True  -> ο παίκτης είναι ενεργός στο παιχνίδι
        # False -> ο παίκτης έχει πεθάνει (π.χ. στο game over ή co-op)
        self.alive = True
