import pygame
import os

# --------------------------------------------------
# Ρυθμίσεις παιχνιδιού (ανάλυση, fps, τίτλος)
# --------------------------------------------------
from shared.config.game_config import GameConfig

# --------------------------------------------------
# Διαχείριση σκηνών (SceneManager)
# --------------------------------------------------
from shared.core.scene import SceneManager

# --------------------------------------------------
# Σύστημα εισόδου (πληκτρολόγιο)
# --------------------------------------------------
from client.controllers.input_controller import InputController

# --------------------------------------------------
# Σκηνές του παιχνιδιού
# --------------------------------------------------
from client.views.scenes.main_menu_scene import MainMenuScene
from client.views.scenes.game_scene import GameScene
from client.views.scenes.highscores_scene import HighScoresScene
from client.views.scenes.settings_scene import SettingsScene
from client.views.scenes.gameover_scene import GameOverScene
from client.views.scenes.how_to_play_scene import HowToPlayScene

# --------------------------------------------------
# Διαχείριση ήχου και μουσικής
# --------------------------------------------------
from shared.services.audio_manager import AudioManager


class GameApp:
    """
    Κεντρική κλάση της εφαρμογής.

    Είναι υπεύθυνη για:
    - αρχικοποίηση pygame
    - φόρτωση ήχου
    - δημιουργία παραθύρου
    - διαχείριση σκηνών
    - εκτέλεση του κύριου game loop
    """

    def __init__(self) -> None:
        # --------------------------------------------------
        # Φόρτωση default ρυθμίσεων παιχνιδιού
        # --------------------------------------------------
        self.config = GameConfig.default()

        # --------------------------------------------------
        # Προ-αρχικοποίηση audio mixer
        # Γίνεται ΠΡΙΝ το pygame.init για καθαρό ήχο
        # --------------------------------------------------
        pygame.mixer.pre_init(
            frequency=44100,   # ποιότητα CD
            size=-16,          # 16-bit signed
            channels=2,        # stereo
            buffer=512         # μικρό buffer για χαμηλό latency
        )

        # --------------------------------------------------
        # Αρχικοποίηση pygame
        # --------------------------------------------------
        pygame.init()
        # pygame.mixer.init()  # δεν χρειάζεται, γίνεται μέσω AudioManager

        # --------------------------------------------------
        # Δημιουργία παραθύρου παιχνιδιού
        # --------------------------------------------------
        pygame.display.set_caption(self.config.title)
        self.screen = pygame.display.set_mode(
            (self.config.screen_width, self.config.screen_height)
        )

        # Ρολόι για υπολογισμό delta time (dt)
        self.clock = pygame.time.Clock()

        # --------------------------------------------------
        # Αρχικοποίηση AudioManager
        # --------------------------------------------------
        AudioManager.init()

        # Φάκελος ήχων (κάτω από client/assets/audio)
        assets_dir = os.path.join(
            os.path.dirname(__file__), "assets", "audio"
        )

        # Φόρτωση ηχητικών εφέ
        AudioManager.load_sounds(assets_dir)

        # Φόρτωση και αναπαραγωγή μουσικής μενού
        menu_music = os.path.join(assets_dir, "menu_melody.ogg")
        AudioManager.play_music(menu_music, loop=True)
        AudioManager.set_music_volume(0.12)

        # --------------------------------------------------
        # CORE ΣΥΣΤΗΜΑΤΑ
        # --------------------------------------------------
        self.input_controller = InputController()
        self.scene_manager = SceneManager()
        self._running = True

        # --------------------------------------------------
        # Καταχώρηση όλων των σκηνών
        # --------------------------------------------------
        self.scene_manager.register_scene(
            "menu",
            MainMenuScene(self.scene_manager, quit_callback=self.stop)
        )

        self.scene_manager.register_scene(
            "game",
            GameScene(self.scene_manager)
        )

        self.scene_manager.register_scene(
            "howto",
            HowToPlayScene(self.scene_manager)
        )

        self.scene_manager.register_scene(
            "highscores",
            HighScoresScene(self.scene_manager)
        )

        self.scene_manager.register_scene(
            "settings",
            SettingsScene(self.scene_manager)
        )

        self.scene_manager.register_scene(
            "gameover",
            GameOverScene(self.scene_manager)
        )

        # --------------------------------------------------
        # Εκκίνηση από το κεντρικό μενού
        # --------------------------------------------------
        self.scene_manager.set_scene("menu", {})

    # ==================================================
    # Τερματισμός εφαρμογής
    # ==================================================
    def stop(self) -> None:
        """
        Σταματά τον κύριο βρόχο του παιχνιδιού.
        Καλείται όταν ο χρήστης επιλέξει Quit ή κλείσει το παράθυρο.
        """
        self._running = False

    # ==================================================
    # Κύριος βρόχος παιχνιδιού (Game Loop)
    # ==================================================
    def run(self) -> None:
        """
        Ο βασικός game loop.

        Εκτελείται συνεχώς μέχρι το _running να γίνει False.
        """
        while self._running:
            # Υπολογισμός delta time σε δευτερόλεπτα
            dt = self.clock.tick(self.config.fps) / 1000.0

            # --------------------------------------------------
            # Διαχείριση events (π.χ. κλείσιμο παραθύρου)
            # --------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

            # --------------------------------------------------
            # Ανάγνωση input και ενημέρωση σκηνής
            # --------------------------------------------------
            snapshot = self.input_controller.capture()
            self.scene_manager.handle_input(snapshot)
            self.scene_manager.update(dt)
            self.scene_manager.render(self.screen)

            # Ενημέρωση οθόνης
            pygame.display.flip()

        # --------------------------------------------------
        # Καθαρός τερματισμός pygame
        # --------------------------------------------------
        pygame.quit()
