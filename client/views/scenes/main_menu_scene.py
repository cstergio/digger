import pygame
import os

from shared.core.scene import Scene, SceneManager
from shared.services.input import InputSnapshot
from shared.services.audio_manager import AudioManager


class MainMenuScene(Scene):
    """
    Κεντρική σκηνή μενού (Main Menu).

    Από εδώ ο χρήστης μπορεί να:
    - ξεκινήσει νέο παιχνίδι (1 ή 2 παίκτες)
    - δει οδηγίες παιχνιδιού
    - δει high scores
    - αλλάξει ρυθμίσεις
    - τερματίσει την εφαρμογή

    Η σκηνή αυτή αποτελεί το βασικό entry point του UI.
    """

    def __init__(self, scene_manager: SceneManager, quit_callback) -> None:
        # Αναφορά στον SceneManager για εναλλαγή σκηνών
        self.sm = scene_manager

        # Callback για ομαλό κλείσιμο της εφαρμογής
        self.quit_callback = quit_callback

        # Τίτλος παιχνιδιού (μπορεί να τεθεί δυναμικά)
        self.title = ""

        # -------------------------
        # Λίστα επιλογών μενού
        # -------------------------
        # Κάθε στοιχείο είναι (κείμενο, action_id)
        self.items = [
            ("NEW GAME (Single Player)", "single"),
            ("NEW GAME (Two Players)", "multi"),
            ("HOW TO PLAY", "howto"),
            ("HIGH SCORES", "highscores"),
            ("SETTINGS", "settings"),
            ("QUIT", "quit"),
        ]

        # Δείκτης τρέχουσας επιλογής
        self.selected = 0

        # -------------------------
        # Fonts
        # -------------------------
        self._font_title = None
        self._font_item = None
        self._font_hint = None

        # Background εικόνα
        self._bg = None

        # -------------------------
        # Cooldowns input
        # -------------------------
        self._nav_cooldown = 0.0
        self._confirm_cooldown = 0.0

    # ==================================================
    # Scene lifecycle
    # ==================================================

    def enter(self, payload: dict | None = None) -> None:
        """
        Καλείται όταν η σκηνή ενεργοποιείται.

        Φορτώνει:
        - γραμματοσειρές
        - background
        - αρχικοποιεί δείκτες και timers
        """

        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(base_dir, "..", "..", "assets")

        # -------------------------
        # Fonts
        # -------------------------
        fonts_dir = os.path.join(assets_dir, "fonts")

        self._font_title = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 64
        )

        self._font_item = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 30
        )

        self._font_hint = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 18
        )

        # -------------------------
        # Background
        # -------------------------
        screen = pygame.display.get_surface()
        w, h = screen.get_size()

        bg_path = os.path.join(assets_dir, "menu", "menu_bg.png")
        self._bg = pygame.image.load(bg_path).convert()
        self._bg = pygame.transform.scale(self._bg, (w, h))

        # Reset κατάστασης
        self.selected = 0
        self._nav_cooldown = 0.0
        self._confirm_cooldown = 0.0

    def exit(self) -> None:
        """
        Καλείται όταν η σκηνή απενεργοποιείται.
        Δεν απαιτείται ειδική ενέργεια.
        """
        pass

    # ==================================================
    # Input
    # ==================================================

    def handle_input(self, input_snapshot: InputSnapshot) -> None:
        """
        Αποθήκευση input snapshot του τρέχοντος frame.
        """
        self._last_input = input_snapshot

    # ==================================================
    # Update
    # ==================================================

    def update(self, dt: float) -> None:
        """
        Επεξεργασία λογικής μενού:
        - πλοήγηση
        - επιλογή
        - αλλαγή σκηνών
        """

        # Ενημέρωση cooldown timers
        self._nav_cooldown = max(0.0, self._nav_cooldown - dt)
        self._confirm_cooldown = max(0.0, self._confirm_cooldown - dt)

        # Αν δεν υπάρχει input snapshot, σταματάμε
        inp: InputSnapshot = getattr(self, "_last_input", None)
        if inp is None:
            return

        # -------------------------
        # Πλοήγηση μενού
        # -------------------------
        if self._nav_cooldown <= 0.0:
            if inp.up:
                self.selected = (self.selected - 1) % len(self.items)
                AudioManager.play_sound("menu_move")
                self._nav_cooldown = 0.16

            elif inp.down:
                self.selected = (self.selected + 1) % len(self.items)
                AudioManager.play_sound("menu_move")
                self._nav_cooldown = 0.16

        # -------------------------
        # Επιβεβαίωση επιλογής
        # -------------------------
        if self._confirm_cooldown <= 0.0 and inp.fire:
            AudioManager.play_sound("menu_select")
            label, action = self.items[self.selected]
            self._confirm_cooldown = 0.20

            if action == "quit":
                self.quit_callback()
                return

            if action == "single":
                self.sm.set_scene("game", {"players": 1})
                return

            if action == "multi":
                self.sm.set_scene("game", {"players": 2})
                return

            if action == "howto":
                self.sm.set_scene("howto", {})
                return

            if action == "highscores":
                self.sm.set_scene("highscores", {})
                return

            if action == "settings":
                self.sm.set_scene("settings", {})
                return

    # ==================================================
    # Render
    # ==================================================

    def render(self, surface) -> None:
        """
        Σχεδίαση γραφικών του main menu.
        """

        w, h = surface.get_width(), surface.get_height()

        # -------------------------
        # Background
        # -------------------------
        surface.blit(self._bg, (0, 0))

        # -------------------------
        # Τίτλος παιχνιδιού
        # -------------------------
        self._draw_glow_text(
            surface,
            self.title,
            self._font_title,
            160,
            90,
        )

        # -------------------------
        # Μενού επιλογών
        # -------------------------
        start_y = 300
        line_h = 48
        menu_x = int(w * 0.28)

        for i, (text, _) in enumerate(self.items):
            y = start_y + i * line_h

            if i == self.selected:
                self._draw_glow_text(surface, text, self._font_item, menu_x, y)
            else:
                item = self._font_item.render(text, True, (220, 220, 220))
                rect = item.get_rect(center=(menu_x, y))
                surface.blit(item, rect)

        # -------------------------
        # Hint
        # -------------------------
        hint = "UP / DOWN to navigate • SPACE to select"
        hint_surf = self._font_hint.render(hint, True, (160, 160, 160))
        surface.blit(
            hint_surf,
            (w // 2 - hint_surf.get_width() // 2, h - 50),
        )

    # ==================================================
    # Glow effect
    # ==================================================

    def _draw_glow_text(self, surface, text, font, cx, cy):
        """
        Δημιουργεί glow effect για επιλεγμένο κείμενο.
        """

        glow_color = (255, 180, 80)
        main_color = (255, 255, 255)

        # Επικάλυψη glow layers
        for alpha in (50, 35, 20):
            glow = font.render(text, True, glow_color)
            glow.set_alpha(alpha)
            rect = glow.get_rect(center=(cx, cy))
            surface.blit(glow, rect)

        # Κεντρικό κείμενο
        main = font.render(text, True, main_color)
        rect = main.get_rect(center=(cx, cy))
        surface.blit(main, rect)
