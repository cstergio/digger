import pygame
import os

from shared.core.scene import Scene, SceneManager
from shared.services.input import InputSnapshot
from shared.services.audio_manager import AudioManager


class SettingsScene(Scene):
    """
    Σκηνή ρυθμίσεων (Settings).

    Η σκηνή αυτή επιτρέπει στον χρήστη να:
    - απενεργοποιήσει όλους τους ήχους
    - ενεργοποιήσει ξανά όλους τους ήχους
    - επιστρέψει στο κεντρικό μενού με ESC

    Δεν περιλαμβάνει gameplay λογική.
    Ανήκει καθαρά στο UI / Menu layer του παιχνιδιού.
    """

    def __init__(self, scene_manager: SceneManager) -> None:
        # Αποθήκευση του SceneManager για αλλαγή σκηνών
        self.sm = scene_manager

        # -------------------------
        # Λίστα επιλογών μενού
        # -------------------------
        # Κάθε στοιχείο είναι (κείμενο, action_id)
        self.items = [
            ("MUTE ALL SOUNDS", "mute"),
            ("UNMUTE ALL SOUNDS", "unmute"),
            # ("BACK", "back"),  # δεν χρειάζεται, χρησιμοποιούμε ESC
        ]

        # Δείκτης επιλεγμένου στοιχείου
        self.selected = 0

        # -------------------------
        # Πόροι γραφικών
        # -------------------------
        self._font_item = None
        self._font_hint = None
        self._bg = None

        # -------------------------
        # Cooldowns για input
        # -------------------------
        # Αποτρέπουν την υπερβολικά γρήγορη επανάληψη ενεργειών
        self._nav_cooldown = 0.0
        self._confirm_cooldown = 0.0
        self._back_cooldown = 0.0

    # ==================================================
    # Scene lifecycle
    # ==================================================

    def enter(self, payload: dict | None = None) -> None:
        """
        Καλείται όταν η σκηνή γίνεται ενεργή.

        Φορτώνει:
        - γραμματοσειρές
        - background
        - αρχικοποιεί επιλογές και timers
        """

        # Εντοπισμός φακέλου assets
        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(base_dir, "..", "..", "assets")

        # -------------------------
        # Fonts (ίδιες με main menu)
        # -------------------------
        fonts_dir = os.path.join(assets_dir, "fonts")

        self._font_item = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 30
        )

        self._font_hint = pygame.font.Font(
            os.path.join(fonts_dir, "Orbitron-Bold.ttf"), 18
        )

        # -------------------------
        # Background εικόνα
        # -------------------------
        screen = pygame.display.get_surface()
        w, h = screen.get_size()

        bg_path = os.path.join(assets_dir, "menu", "menu_bg.png")
        self._bg = pygame.image.load(bg_path).convert()
        self._bg = pygame.transform.scale(self._bg, (w, h))

        # -------------------------
        # Reset κατάστασης
        # -------------------------
        self.selected = 0
        self._nav_cooldown = 0.0
        self._confirm_cooldown = 0.0
        self._back_cooldown = 0.25

    def exit(self) -> None:
        """
        Καλείται όταν φεύγουμε από τη σκηνή.
        Δεν απαιτείται κάποια ειδική ενέργεια εδώ.
        """
        pass

    # ==================================================
    # Input
    # ==================================================

    def handle_input(self, input_snapshot: InputSnapshot) -> None:
        """
        Αποθηκεύει το InputSnapshot του τρέχοντος frame.
        Η επεξεργασία γίνεται στο update().
        """
        self._last_input = input_snapshot

    # ==================================================
    # Update
    # ==================================================

    def update(self, dt: float) -> None:
        """
        Επεξεργασία λογικής της σκηνής:
        - πλοήγηση στο μενού
        - επιλογή ενέργειας
        - επιστροφή στο main menu
        """

        # Μείωση των cooldown timers
        self._nav_cooldown = max(0.0, self._nav_cooldown - dt)
        self._confirm_cooldown = max(0.0, self._confirm_cooldown - dt)
        self._back_cooldown = max(0.0, self._back_cooldown - dt)

        # Αν δεν υπάρχει input snapshot, σταματάμε
        inp: InputSnapshot = getattr(self, "_last_input", None)
        if inp is None:
            return

        # -------------------------
        # Πλοήγηση (UP / DOWN)
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
        # Επιβεβαίωση (SPACE)
        # -------------------------
        if self._confirm_cooldown <= 0.0 and inp.fire:
            AudioManager.play_sound("menu_select")
            _, action = self.items[self.selected]
            self._confirm_cooldown = 0.25

            if action == "mute":
                AudioManager.mute_all()

            elif action == "unmute":
                AudioManager.unmute_all()

        # -------------------------
        # ESC → επιστροφή στο menu
        # -------------------------
        if inp.pause and self._back_cooldown <= 0.0:
            self.sm.set_scene("menu", {})
            self._back_cooldown = 0.25

    # ==================================================
    # Render
    # ==================================================

    def render(self, surface) -> None:
        """
        Σχεδίαση της σκηνής:
        - background
        - επιλογές
        - hint στο κάτω μέρος
        """

        w, h = surface.get_width(), surface.get_height()

        # -------------------------
        # Background
        # -------------------------
        surface.blit(self._bg, (0, 0))

        # -------------------------
        # Μενού επιλογών
        # -------------------------
        start_y = h // 2 - 60
        line_h = 52
        cx = w // 2

        for i, (text, _) in enumerate(self.items):
            y = start_y + i * line_h

            if i == self.selected:
                self._draw_glow_text(surface, text, self._font_item, cx, y)
            else:
                item = self._font_item.render(text, True, (220, 220, 220))
                rect = item.get_rect(center=(cx, y))
                surface.blit(item, rect)

        # -------------------------
        # Hint
        # -------------------------
        hint = "UP / DOWN to navigate • SPACE to select • ESC to return"
        hint_surf = self._font_hint.render(hint, True, (160, 160, 160))
        surface.blit(
            hint_surf,
            (w // 2 - hint_surf.get_width() // 2, h - 60),
        )

    # ==================================================
    # Glow effect
    # ==================================================

    def _draw_glow_text(self, surface, text, font, cx, cy):
        """
        Βοηθητική μέθοδος για glow effect στο επιλεγμένο item.
        """

        glow_color = (255, 180, 80)
        main_color = (255, 255, 255)

        # Πολλαπλά layers glow με διαφορετική διαφάνεια
        for alpha in (50, 35, 20):
            glow = font.render(text, True, glow_color)
            glow.set_alpha(alpha)
            rect = glow.get_rect(center=(cx, cy))
            surface.blit(glow, rect)

        # Κεντρικό κείμενο
        main = font.render(text, True, main_color)
        rect = main.get_rect(center=(cx, cy))
        surface.blit(main, rect)
