from shared.model.types import TileType
# Εισαγωγή του Enum TileType που περιγράφει
# όλους τους δυνατούς τύπους πλακιδίων (χώμα, σήραγγα, διαμάντια κ.λπ.)


class Level:
    """
    Κλάση που αναπαριστά μία πίστα (level) του παιχνιδιού.
    Το επίπεδο υλοποιείται ως δισδιάστατος πίνακας tiles.
    Κάθε tile περιγράφει τι υπάρχει σε εκείνη τη θέση.
    """

    def __init__(self, width: int, height: int):
        # Πλάτος του επιπέδου (αριθμός στηλών)
        self.width = width

        # Ύψος του επιπέδου (αριθμός γραμμών)
        self.height = height

        # Δημιουργία δισδιάστατου πίνακα tiles
        # Αρχικά ΟΛΟ το επίπεδο γεμίζει με χώμα (DIRT)
        # self.tiles[y][x]
        self.tiles = [
            [TileType.DIRT for _ in range(width)]
            for _ in range(height)
        ]

        # ==================================================
        # Spawn παίκτη και αρχικό τούνελ
        # ==================================================

        # Σημείο εμφάνισης του Player 1
        self.tiles[5][5] = TileType.SPAWN_P1

        # Δημιουργία αρχικού οριζόντιου τούνελ
        # ώστε ο παίκτης να έχει ελεύθερο χώρο στην αρχή
        for x in range(5, 12):
            self.tiles[5][x] = TileType.TUNNEL

        # ==================================================
        # Placeholder θέσεις για gold bags (προς δοκιμή)
        # ==================================================
        # Οι γραμμές αυτές είναι σχολιασμένες
        # και μπορούν να χρησιμοποιηθούν για fixed τοποθέτηση
        # self.tiles[6][8] = TileType.GOLD_BAG
        # self.tiles[10][20] = TileType.GOLD_BAG

        # ==================================================
        # Ομάδες διαμαντιών (emerald clusters)
        # ==================================================

        # Πρώτο cluster διαμαντιών (2x2)
        self.tiles[6][6] = TileType.EMERALD
        self.tiles[6][7] = TileType.EMERALD
        self.tiles[7][6] = TileType.EMERALD
        self.tiles[7][7] = TileType.EMERALD

        # Δεύτερο cluster διαμαντιών (2x2)
        self.tiles[12][18] = TileType.EMERALD
        self.tiles[12][19] = TileType.EMERALD
        self.tiles[13][18] = TileType.EMERALD
        self.tiles[13][19] = TileType.EMERALD

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Ελέγχει αν οι συντεταγμένες (x, y) βρίσκονται
        εντός των ορίων του επιπέδου.
        Χρησιμοποιείται από movement, bullets, enemies κ.λπ.
        """

        return 0 <= x < self.width and 0 <= y < self.height

    def get_tile(self, x: int, y: int) -> TileType:
        """
        Επιστρέφει τον τύπο του tile στη θέση (x, y).
        Δεν κάνει έλεγχο ορίων, οπότε καλείται αφού
        προηγηθεί έλεγχος με in_bounds().
        """

        return self.tiles[y][x]

    def set_tile(self, x: int, y: int, tile: TileType):
        """
        Θέτει (αλλάζει) τον τύπο του tile στη θέση (x, y).
        Χρησιμοποιείται όταν:
        - σκάβεται χώμα
        - συλλέγεται διαμάντι
        - πέφτει gold bag
        """

        self.tiles[y][x] = tile
