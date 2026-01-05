import pygame
import os
from shared.core.scene import Scene
from shared.persistence.score_repository import ScoreRepository


class HighScoresScene(Scene):
    """
    Σκηνή εμφάνισης High Scores.

    Εμφανίζει τις 10 καλύτερες βαθμολογίες που είναι
    αποθηκευμένες στη βάση δεδομένων (SQLite).

    Η σκηνή:
    - δεν έχει επιλογές / μενού
    - λειτουργεί μόνο ως προβολή δεδομένων
    - επιστρέφει στο main menu με το πλήκτρο ESC
    """

    def __init__(self, scene_manager):
        # Αναφορά στον SceneManager για αλλαγή σκηνών
        self.sm = scene_manager

        # Repository για πρόσβαση στη βάση δεδομένων scores
        self.repo = ScoreRepository()

        # Αποθήκευση του τελευταίου InputSnapshot
        self._input = None

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
        # Χρησιμοποιείται το ίδιο background με το main menu
        self.bg = pygame.image.load(
            os.path.join(menu_dir, "menu_bg.png")
        ).convert()

        # -------------------------
        # Fonts
        # -------------------------
        # Τίτλος High Scores
        self.font_title = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 48
        )

        # Κείμενο βαθμολογιών
        self.font = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 22
        )

    # ==================================================
    # REQUIRED by abstract Scene
    # ==================================================

    def enter(self, payload=None):
        """
        Καλείται όταν η σκηνή ενεργοποιείται.
        Δεν απαιτείται αρχικοποίηση κατά την είσοδο.
        """
        pass

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

    def update(self, dt):
        """
        Ελέγχει αν ο παίκτης πάτησε ESC
        ώστε να επιστρέψει στο main menu.
        """

        if self._input and self._input.pause:
            self.sm.set_scene("menu", {})

    def render(self, surface):
        """
        Σχεδίαση της σκηνής High Scores.
        """

        # -------------------------
        # Background
        # -------------------------
        surface.blit(self.bg, (0, 0))

        w = surface.get_width()

        # -------------------------
        # Τίτλος
        # -------------------------
        title = self.font_title.render("HIGH SCORES", True, (255, 255, 255))

        # Το +160 χρησιμοποιείται για να ευθυγραμμιστεί
        # οπτικά με το layout του main menu
        surface.blit(
            title,
            (w // 2 - title.get_width() // 2 + 160, 100)
        )

        # -------------------------
        # Ανάκτηση scores από τη βάση
        # -------------------------
        scores = self.repo.top_10()

        # -------------------------
        # Εμφάνιση λίστας
        # -------------------------
        y = 200  # αρχικό ύψος πρώτης γραμμής

        for i, (name, date, time, score) in enumerate(scores, start=1):
            # Μορφοποίηση γραμμής:
            # θέση, όνομα παιχνιδιού, ημερομηνία, ώρα, σκορ
            line = f"{i:>2}. {name:<6} {date} {time}   {score:>6}"

            txt = self.font.render(line, True, (230, 230, 230))

            surface.blit(
                txt,
                (w // 2 - txt.get_width() // 2 + 160, y)
            )

            # Μετακίνηση στην επόμενη γραμμή
            y += 32
