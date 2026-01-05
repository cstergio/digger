import pygame
import os
from shared.core.scene import Scene
from shared.persistence.score_repository import ScoreRepository


class GameOverScene(Scene):
    """
    Σκηνή Game Over.

    Εμφανίζεται όταν το παιχνίδι τελειώσει (loss condition).
    Παρουσιάζει:
    - Τον τίτλο GAME OVER
    - Το τελικό σκορ Player 1 και Player 2
    - Οδηγία επιστροφής στο Main Menu

    Δεν επιτρέπει άλλη ενέργεια εκτός από ESC → επιστροφή στο menu.
    """

    def __init__(self, scene_manager):
        # Αναφορά στον SceneManager για αλλαγή σκηνών
        self.sm = scene_manager

        # Repository για αποθήκευση / ανάγνωση scores
        # (μπορεί να χρησιμοποιηθεί για μελλοντική επέκταση)
        self.repo = ScoreRepository()

        # -------------------------
        # Paths για assets
        # -------------------------
        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(base_dir, "..", "..", "assets")
        fonts_dir = os.path.join(assets_dir, "fonts")
        menu_dir = os.path.join(assets_dir, "menu")

        # -------------------------
        # Background εικόνα
        # -------------------------
        # Χρησιμοποιείται το ίδιο background με το menu
        self.bg = pygame.image.load(
            os.path.join(menu_dir, "menu_bg.png")
        ).convert()

        # -------------------------
        # Fonts
        # -------------------------
        # Μεγάλη γραμματοσειρά για τον τίτλο GAME OVER
        self.font_title = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 64
        )

        # Μικρότερη γραμματοσειρά για σκορ και οδηγίες
        self.font = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 24
        )

        # -------------------------
        # Κατάσταση σκηνής
        # -------------------------
        self.score = 0          # (δεν χρησιμοποιείται άμεσα, κρατιέται για επεκτασιμότητα)
        self._cooldown = 0.0    # cooldown για αποφυγή άμεσης εξόδου
        self._input = None      # τελευταίο InputSnapshot

    # =========================================
    # Scene interface
    # =========================================

    def enter(self, payload=None):
        """
        Καλείται όταν η σκηνή Game Over ενεργοποιείται.

        Το payload περιέχει τα τελικά σκορ των παικτών.
        """
        payload = payload or {}

        # Ανάκτηση σκορ από το payload
        self.score_p1 = payload.get("score_p1", 0)
        self.score_p2 = payload.get("score_p2", 0)

        # Μικρή καθυστέρηση ώστε να μη φύγει άμεσα
        # αν ο παίκτης κρατά πατημένο ESC
        self._cooldown = 0.4

    def exit(self):
        """
        Καλείται όταν η σκηνή απενεργοποιείται.
        Δεν απαιτείται καθαρισμός.
        """
        pass

    def handle_input(self, input_snapshot):
        """
        Αποθηκεύει το input του τρέχοντος frame.
        """
        self._input = input_snapshot

    # =========================================
    # Update / Render
    # =========================================

    def update(self, dt):
        """
        Ελέγχει το input και επιτρέπει επιστροφή
        στο Main Menu μόνο μετά το cooldown.
        """

        # Μείωση cooldown
        self._cooldown = max(0, self._cooldown - dt)

        # Όσο υπάρχει cooldown, αγνοούμε input
        if self._cooldown > 0:
            return

        if not self._input:
            return

        # ΜΟΝΟ ESC (pause) → επιστροφή στο menu
        if self._input.pause:
            self.sm.set_scene("menu", {})

    def render(self, surface):
        """
        Σχεδίαση της σκηνής Game Over.
        """

        # -------------------------
        # Background
        # -------------------------
        surface.blit(self.bg, (0, 0))
        w = surface.get_width()

        # -------------------------
        # Τίτλος GAME OVER
        # -------------------------
        title = self.font_title.render(
            "GAME OVER", True, (255, 255, 255)
        )

        surface.blit(
            title,
            (w // 2 - title.get_width() // 2 + 160, 140)
        )

        # -------------------------
        # Εμφάνιση σκορ παικτών
        # -------------------------
        score_txt = self.font.render(
            f"P1: {self.score_p1}   P2: {self.score_p2}",
            True,
            (255, 255, 255)
        )

        surface.blit(
            score_txt,
            (w // 2 - score_txt.get_width() // 2 + 160, 240)
        )

        # -------------------------
        # Οδηγία επιστροφής
        # -------------------------
        info = self.font.render(
            "ESC: MAIN MENU",
            True,
            (200, 200, 200)
        )

        surface.blit(
            info,
            (w // 2 - info.get_width() // 2 + 160, 340)
        )
