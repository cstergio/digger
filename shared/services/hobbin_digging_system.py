from shared.model.types import TileType, MonsterForm
# Εισάγουμε:
# - TileType: τα είδη πλακιδίων του επιπέδου (χώμα, τούνελ, διαμάντι, σακί χρυσού κ.λπ.)
# - MonsterForm: τη μορφή του τέρατος (π.χ. Nobbin, Hobbin),
#   η οποία επηρεάζει τη συμπεριφορά του εχθρού


class HobbinDiggingSystem:
    """
    Το HobbinDiggingSystem υλοποιεί τη λογική σκαψίματος
    που εφαρμόζεται αποκλειστικά στους εχθρούς τύπου Hobbin.

    Στο παιχνίδι Digger:
    - οι Nobbin ΔΕΝ μπορούν να σκάψουν
    - οι Hobbin ΜΠΟΡΟΥΝ να σκάβουν όπως ο παίκτης

    Αυτή η διαφορά υλοποιείται ξεκάθαρα και απομονωμένα
    σε αυτό το σύστημα.
    """

    def on_enter(self, enemy, level):
        """
        Καλείται όταν ένας εχθρός εισέρχεται σε νέο πλακίδιο.

        enemy : το αντικείμενο Enemy που κινείται
        level : το επίπεδο του παιχνιδιού (grid πλακιδίων)
        """

        # Αν ο εχθρός ΔΕΝ είναι Hobbin,
        # τότε δεν εφαρμόζεται καμία λογική σκαψίματος
        if enemy.form != MonsterForm.HOBBIN:
            return

        # Παίρνουμε το είδος του πλακιδίου
        # στο οποίο μόλις μπήκε ο Hobbin
        tile = level.get_tile(enemy.tile_x, enemy.tile_y)

        # Αν το πλακίδιο είναι:
        # - χώμα (DIRT)
        # - διαμάντι (EMERALD)
        # - σακί χρυσού (GOLD_BAG)
        # τότε ο Hobbin το "σκάβει"
        if tile in (TileType.DIRT, TileType.EMERALD, TileType.GOLD_BAG):

            # Μετατρέπουμε το πλακίδιο σε τούνελ,
            # όπως ακριβώς κάνει και ο παίκτης
            level.set_tile(
                enemy.tile_x,
                enemy.tile_y,
                TileType.TUNNEL
            )
