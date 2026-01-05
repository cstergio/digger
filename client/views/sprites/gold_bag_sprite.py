import pygame
import os


class GoldBagSprite:
    """
    Κλάση υπεύθυνη για την ΟΠΤΙΚΗ αναπαράσταση των gold bags.

    Η κλάση αυτή:
    - δεν περιέχει λογική πτώσης
    - δεν περιέχει λογική συλλογής
    - δεν αλλάζει την κατάσταση του αντικειμένου

    Απλώς διαβάζει την ΚΑΤΑΣΤΑΣΗ του gold bag
    και επιλέγει ποια εικόνα θα σχεδιαστεί.
    """

    # Σταθερό μέγεθος sprite (32x32 pixels)
    SIZE = 32

    def __init__(self):
        # --------------------------------------------------
        # Εντοπισμός του φακέλου client/ με ασφάλεια
        # --------------------------------------------------
        base_dir = os.path.dirname(__file__)

        # Μετακίνηση δύο επίπεδα πάνω ώστε να φτάσουμε στο client/
        client_dir = os.path.abspath(
            os.path.join(base_dir, "..", "..")
        )

        # Φάκελος sprites
        assets_dir = os.path.join(client_dir, "assets", "sprites")

        # --------------------------------------------------
        # Φόρτωση εικόνων gold bag
        # --------------------------------------------------

        # Κανονικός σάκος χρυσού (σταθερός)
        self.bag_image = pygame.image.load(
            os.path.join(assets_dir, "gold_sack.png")
        ).convert_alpha()

        # Σάκος χρυσού σε κατάσταση πτώσης
        self.falling_image = pygame.image.load(
            os.path.join(assets_dir, "gold_sack_fall.png")
        ).convert_alpha()

        # Gold pile (όταν σπάσει ο σάκος)
        self.gold_image = pygame.image.load(
            os.path.join(assets_dir, "gold_pile.png")
        ).convert_alpha()

    def draw(self, surface, bag, sx, sy):
        """
        Σχεδιάζει το gold bag στην οθόνη.

        surface : pygame Surface (οθόνη ή υπο-οθόνη)
        bag     : αντικείμενο GoldBag (κατάσταση gameplay)
        sx, sy  : συντεταγμένες οθόνης (screen coordinates)
        """

        # --------------------------------------------------
        # Αν το gold bag έχει συλλεχθεί,
        # δεν σχεδιάζεται τίποτα
        # --------------------------------------------------
        if bag.collected:
            return

        # --------------------------------------------------
        # Αν έχει μετατραπεί σε gold pile,
        # σχεδιάζουμε την εικόνα του χρυσού
        # --------------------------------------------------
        if bag.is_gold:
            surface.blit(self.gold_image, (sx, sy))
            return

        # --------------------------------------------------
        # Αν βρίσκεται σε πτώση,
        # σχεδιάζουμε το falling sprite
        # --------------------------------------------------
        if bag.falling:
            surface.blit(self.falling_image, (sx, sy))
            return

        # --------------------------------------------------
        # Διαφορετικά, σχεδιάζουμε τον κανονικό σάκο
        # --------------------------------------------------
        surface.blit(self.bag_image, (sx, sy))
