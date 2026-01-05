import pygame
import os
from shared.model.types import Direction


class PlayerSprite:
    """
    Κλάση υπεύθυνη για την ΟΠΤΙΚΗ αναπαράσταση του παίκτη.

    Δεν περιέχει καμία λογική κίνησης, σύγκρουσης ή gameplay.
    Ασχολείται αποκλειστικά με:
    - φόρτωση του sprite
    - περιστροφή / αναστροφή του sprite
    - σχεδίαση στην οθόνη
    """

    # Σταθερό μέγεθος sprite σε pixels (32x32)
    SIZE = 32

    def __init__(self):
        # Υπολογισμός διαδρομών φακέλων
        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(
            base_dir, "..", "..", "assets", "sprites"
        )

        # Πλήρης διαδρομή του αρχείου sprite του παίκτη
        sprite_path = os.path.join(assets_dir, "digger_player.png")

        # --------------------------------------------------
        # Φόρτωση βασικού sprite
        # Θεωρούμε ότι το αρχικό sprite "κοιτάει" προς τα ΔΕΞΙΑ
        # --------------------------------------------------
        self.base_image = pygame.image.load(sprite_path).convert_alpha()

        # --------------------------------------------------
        # Κλιμάκωση sprite για ασφάλεια
        # (εξασφαλίζει ότι είναι ακριβώς 32x32)
        # --------------------------------------------------
        self.base_image = pygame.transform.scale(
            self.base_image, (self.SIZE, self.SIZE)
        )

    def draw(self, surface, x, y, direction):
        """
        Σχεδιάζει το sprite του παίκτη στην οθόνη.

        surface   : pygame Surface (οθόνη ή υπο-οθόνη)
        x, y      : συντεταγμένες οθόνης (screen coordinates)
        direction : κατεύθυνση που κοιτάει ο παίκτης
        """

        # Από προεπιλογή χρησιμοποιούμε το βασικό sprite
        image = self.base_image

        # --------------------------------------------------
        # Μετασχηματισμός sprite ανάλογα με την κατεύθυνση
        # --------------------------------------------------

        # Αν ο παίκτης κοιτάει αριστερά, κάνουμε οριζόντια αναστροφή
        if direction == Direction.LEFT:
            image = pygame.transform.flip(self.base_image, True, False)

        # Αν κοιτάει προς τα πάνω, περιστρέφουμε 90 μοίρες
        elif direction == Direction.UP:
            image = pygame.transform.rotate(self.base_image, 90)

        # Αν κοιτάει προς τα κάτω, περιστρέφουμε -90 μοίρες
        elif direction == Direction.DOWN:
            image = pygame.transform.rotate(self.base_image, -90)

        # Direction.RIGHT:
        # Δεν χρειάζεται καμία αλλαγή, γιατί το sprite
        # έχει σχεδιαστεί αρχικά προς τα δεξιά

        # --------------------------------------------------
        # Τελική σχεδίαση του sprite στην οθόνη
        # --------------------------------------------------
        surface.blit(image, (x, y))
