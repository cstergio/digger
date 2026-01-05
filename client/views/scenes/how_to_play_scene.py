import pygame
import os
from shared.core.scene import Scene


class HowToPlayScene(Scene):
    """
    Σκηνή οδηγιών παιχνιδιού (How To Play).

    Παρουσιάζει στον παίκτη:
    - σύντομη περιγραφή gameplay
    - στόχους παιχνιδιού
    - χειρισμό για Player 1 και Player 2
    - στοιχεία δημιουργών

    Η σκηνή είναι παθητική (μόνο ανάγνωση) και
    επιστρέφει στο main menu με ESC.
    """

    def __init__(self, scene_manager):
        # Αναφορά στον SceneManager για αλλαγή σκηνής
        self.sm = scene_manager

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
        # Χρησιμοποιείται ξεχωριστό background από το main menu
        self.bg = pygame.image.load(
            os.path.join(menu_dir, "menu_bg2.png")
        ).convert()

        # -------------------------
        # Fonts
        # -------------------------
        # Τίτλος (μεγαλύτερο μέγεθος)
        self.font_title = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 44
        )

        # Κείμενο οδηγιών (μικρό μέγεθος για να χωράει)
        self.font = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 18
        )

        # -------------------------
        # Input handling
        # -------------------------
        # Cooldown ώστε να μη γίνεται άμεση επιστροφή με ESC
        self._cooldown = 0.3

        # Τελευταίο InputSnapshot
        self._input = None

    # ===============================
    # Scene interface
    # ===============================

    def enter(self, payload=None):
        """
        Καλείται όταν η σκηνή ενεργοποιείται.

        Επαναφέρει το cooldown για ασφαλή είσοδο.
        """
        self._cooldown = 0.3

    def exit(self):
        """
        Καλείται όταν η σκηνή απενεργοποιείται.
        Δεν απαιτείται καθαρισμός πόρων.
        """
        pass

    def handle_input(self, input_snapshot):
        """
        Αποθηκεύει το input του τρέχοντος frame.
        """
        self._input = input_snapshot

    # ===============================
    # Update
    # ===============================

    def update(self, dt):
        """
        Ελέγχει αν ο παίκτης πάτησε ESC για επιστροφή
        στο main menu, αφού περάσει το cooldown.
        """

        # Μείωση cooldown με βάση τον χρόνο frame
        self._cooldown = max(0.0, self._cooldown - dt)

        # Αν το cooldown δεν έχει λήξει, δεν κάνουμε τίποτα
        if self._cooldown > 0:
            return

        # ESC → επιστροφή στο main menu
        if self._input and self._input.pause:
            self.sm.set_scene("menu", {})

    # ===============================
    # Render
    # ===============================

    def render(self, surface):
        """
        Σχεδίαση της σκηνής οδηγιών.
        """

        # Background
        surface.blit(self.bg, (0, 0))

        w, h = surface.get_width(), surface.get_height()

        # -------------------------
        # Τίτλος
        # -------------------------
        title = "HOW TO PLAY"
        title_surf = self.font_title.render(title, True, (255, 255, 255))
        surface.blit(
            title_surf,
            (w // 2 - title_surf.get_width() // 2, 60)
        )

        # -------------------------
        # Κείμενο οδηγιών
        # -------------------------
        # Αρχική θέση κειμένου κάτω από τον τίτλο
        y = 60 + title_surf.get_height() + 16

        # Μικρό line spacing ώστε να χωράει όλο το κείμενο
        line_spacing = 4

        # Κείμενο χωρισμένο σε γραμμές
        text_lines = [
            "You control the Digger, exploring an underground maze",
            "of tunnels while collecting emeralds and avoiding enemies.",
            "",
            "Dig through dirt, drop gold bags to crush enemies,",
            "and use your weapon wisely to survive.",
            "",
            "Clear all emeralds to advance to the next level.",
            "If you lose all your lives, the game is over.",
            "",
            "CONTROLS",
            "Arrow Keys  : Move",
            "SPACE       : Fire weapon",
            "ESC         : Back to Menu",
            "",
            "Player 2 (Co-op)",
            "W A S D     : Move",
            "LEFT SHIFT : Fire",
            "",
            "CREATED BY",
            "Konstantinos Gaitanis",
            "Charalampos Stergiopoulos Roubas",
        ]

        # Σχεδίαση κάθε γραμμής
        for line in text_lines:
            surf = self.font.render(line, True, (230, 230, 230))
            surface.blit(
                surf,
                (w // 2 - surf.get_width() // 2, y)
            )

            # Αν η γραμμή είναι κενή, μικρότερο κενό (παράγραφος)
            if line.strip() == "":
                y += surf.get_height() // 3
            else:
                y += surf.get_height() + line_spacing
