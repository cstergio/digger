import pygame
import os

# --------------------------------------------------
# Τύποι πλακιδίων (χώμα, tunnel κ.λπ.)
# --------------------------------------------------
from shared.model.types import TileType


class TilemapView:
    """
    Υπεύθυνη κλάση για την ΟΠΤΙΚΗ απεικόνιση του tilemap.

    Δεν περιέχει καμία λογική gameplay.
    Απλώς:
    - διαβάζει τα tiles του Level
    - τα μετατρέπει σε εικόνες
    - τα σχεδιάζει στην οθόνη με βάση την κάμερα
    """

    def __init__(self, tile_size: int):
        # Μέγεθος πλακιδίου (π.χ. 32x32 pixels)
        self.tile_size = tile_size

        # Υπολογισμός διαδρομής assets
        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(base_dir, "..", "assets", "tiles")

        # --------------------------------------------------
        # Φόρτωση εικόνων πλακιδίων
        # --------------------------------------------------

        # Εικόνα grass (χρησιμοποιείται στην πάνω σειρά)
        self.grass_tile = pygame.image.load(
            os.path.join(assets_dir, "grass.png")
        ).convert()

        # Εικόνα dirt (χώμα)
        self.dirt_tile = pygame.image.load(
            os.path.join(assets_dir, "dirt.png")
        ).convert()

        # Εικόνα μπλε background (εκτός χάρτη)
        self.blue_bg = pygame.image.load(
            os.path.join(assets_dir, "blue.png")
        ).convert()

        # --------------------------------------------------
        # Tunnel tile = μαύρο πλακίδιο
        # Δημιουργείται δυναμικά, δεν φορτώνεται από αρχείο
        # --------------------------------------------------
        self.black_tile = pygame.Surface((tile_size, tile_size))
        self.black_tile.fill((0, 0, 0))

    def render(self, surface, level, camera):
        """
        Σχεδιάζει ΟΛΟ το tilemap στην οθόνη.

        surface : pygame Surface (η οθόνη ή υπο-οθόνη)
        level   : αντικείμενο Level (δεδομένα map)
        camera  : Camera2D (μετατροπή world → screen)
        """

        # Αριθμός γραμμών και στηλών του map
        rows = level.height
        cols = level.width

        # --------------------------------------------------
        # Γέμισμα background εκτός map με μπλε χρώμα
        # --------------------------------------------------
        surface.blit(
            pygame.transform.scale(self.blue_bg, surface.get_size()),
            (0, 0),
        )

        # --------------------------------------------------
        # Διπλός βρόχος: traversal όλων των tiles
        # --------------------------------------------------
        for y in range(rows):
            for x in range(cols):
                # Τύπος πλακιδίου από το Level
                tile = level.tiles[y][x]

                # Συντεταγμένες στον κόσμο (world coordinates)
                world_x = x * self.tile_size
                world_y = y * self.tile_size

                # Μετατροπή world → screen μέσω κάμερας
                sx, sy = camera.world_to_screen(world_x, world_y)

                # --------------------------------------------------
                # Απόρριψη πλακιδίων εκτός οθόνης
                # --------------------------------------------------
                if sx + self.tile_size < 0 or sy + self.tile_size < 0:
                    continue

                # --------------------------------------------------
                # TUNNEL → μαύρο πλακίδιο
                # --------------------------------------------------
                if tile == TileType.TUNNEL:
                    surface.blit(self.black_tile, (sx, sy))
                    continue

                # --------------------------------------------------
                # Πάνω σειρά του map → grass
                # --------------------------------------------------
                if y == 0:
                    surface.blit(self.grass_tile, (sx, sy))
                    continue

                # --------------------------------------------------
                # Όλα τα υπόλοιπα tiles → dirt
                # --------------------------------------------------
                surface.blit(self.dirt_tile, (sx, sy))
