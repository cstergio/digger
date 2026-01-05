from shared.model.types import Direction, TileType
# Εισάγουμε:
# - Direction: τις κατευθύνσεις κίνησης (LEFT, RIGHT κ.λπ.)
# - TileType: τα είδη πλακιδίων του επιπέδου (TUNNEL, GOLD_BAG κ.ά.)


class GoldBagPushSystem:
    """
    Το GoldBagPushSystem είναι υπεύθυνο για το οριζόντιο σπρώξιμο
    των σακιών χρυσού από παίκτες ή εχθρούς.

    Υλοποιεί αυστηρά τους κανόνες του κλασικού Digger:
    - Το σπρώξιμο επιτρέπεται ΜΟΝΟ αριστερά ή δεξιά
    - Το σακί πρέπει να είναι σταθερό (STABLE)
    - Το πλακίδιο-στόχος πρέπει να είναι τούνελ (TUNNEL)
    - Η παλιά θέση του σακιού μετατρέπεται σε τούνελ
    """

    def try_push(self, bag, direction, level) -> bool:
        """
        Προσπαθεί να σπρώξει ένα σακί χρυσού οριζόντια.

        bag       : το αντικείμενο GoldBag που επιχειρούμε να μετακινήσουμε
        direction : κατεύθυνση ώθησης (LEFT ή RIGHT)
        level     : το επίπεδο του παιχνιδιού (grid πλακιδίων)

        Επιστρέφει:
        - True  αν το σπρώξιμο πραγματοποιήθηκε
        - False αν απορρίφθηκε λόγω κανόνων
        """

        # Αν το σακί δεν είναι σταθερό (π.χ. πέφτει ή έχει γίνει gold),
        # τότε απαγορεύεται το σπρώξιμο
        if bag.state != "STABLE":
            return False

        # Επιτρέπουμε σπρώξιμο μόνο προς τα αριστερά ή δεξιά
        if direction not in (Direction.LEFT, Direction.RIGHT):
            return False

        # Υπολογίζουμε τη μετατόπιση στον άξονα x
        # LEFT  -> -1
        # RIGHT -> +1
        dx = -1 if direction == Direction.LEFT else 1

        # Υπολογίζουμε τη θέση-στόχο
        target_x = bag.tile_x + dx
        target_y = bag.tile_y

        # Ελέγχουμε αν η νέα θέση βρίσκεται εντός των ορίων του επιπέδου
        if not level.in_bounds(target_x, target_y):
            return False

        # Το πλακίδιο-στόχος πρέπει να είναι τούνελ,
        # αλλιώς το σακί δεν μπορεί να μετακινηθεί
        if level.get_tile(target_x, target_y) != TileType.TUNNEL:
            return False

        # ==================================================
        # AUTHENTIC DIGGER RULE
        # ==================================================
        # Η παλιά θέση του σακιού γίνεται τούνελ
        old_x, old_y = bag.tile_x, bag.tile_y
        level.set_tile(old_x, old_y, TileType.TUNNEL)

        # Μετακινούμε το σακί στη νέα θέση
        bag.tile_x = target_x

        # Δηλώνουμε επιτυχία σπρωξίματος
        return True
