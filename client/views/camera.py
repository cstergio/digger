class Camera2D:
    """
    Κλάση κάμερας 2D.

    Η Camera2D είναι υπεύθυνη για τη μετατροπή συντεταγμένων
    από τον «κόσμο του παιχνιδιού» (world coordinates)
    σε συντεταγμένες οθόνης (screen coordinates).

    Δεν σχεδιάζει τίποτα.
    Δεν γνωρίζει tiles, enemies ή gameplay.
    Απλώς κρατά τη θέση της κάμερας.
    """

    def __init__(self, screen_w, screen_h, tile_size):
        # Πλάτος οθόνης σε pixels
        self.screen_w = screen_w

        # Ύψος οθόνης σε pixels
        self.screen_h = screen_h

        # Μέγεθος πλακιδίου (π.χ. 32 pixels)
        self.tile_size = tile_size

        # Τρέχουσα θέση κάμερας στον κόσμο (πάνω αριστερή γωνία)
        # Εκφράζεται σε pixels
        self.x = 0
        self.y = 0

    def follow(self, entity):
        """
        Κεντράρει την κάμερα πάνω σε ένα entity (π.χ. player).

        Υπολογίζει τη θέση της κάμερας έτσι ώστε
        το entity να εμφανίζεται στο κέντρο της οθόνης.
        """

        # Μετατροπή tile συντεταγμένων του entity σε pixels
        world_x = entity.tile_x * self.tile_size
        world_y = entity.tile_y * self.tile_size

        # Η κάμερα μετακινείται έτσι ώστε το entity
        # να βρίσκεται στο κέντρο της οθόνης
        self.x = world_x - self.screen_w // 2
        self.y = world_y - self.screen_h // 2

    def world_to_screen(self, wx, wy):
        """
        Μετατρέπει συντεταγμένες κόσμου (world)
        σε συντεταγμένες οθόνης (screen).

        Αυτή η μέθοδος χρησιμοποιείται από ΟΛΑ τα render συστήματα.
        """

        # Αφαιρούμε τη θέση της κάμερας από τις world συντεταγμένες
        # ώστε να πάρουμε screen συντεταγμένες
        return wx - self.x, wy - self.y
