# ------------------------------------------------------------
# Βασικές βιβλιοθήκες
# ------------------------------------------------------------

# pygame: βιβλιοθήκη για γραφικά, input, χρόνο (dt), surfaces,
# sprites και γενικά όλο το game loop
import pygame

# random: χρησιμοποιείται για τυχαίες επιλογές μέσα στο παιχνίδι,
# π.χ. spawn εχθρών ή τυχαία συμπεριφορά AI
import random


# ------------------------------------------------------------
# Core αρχιτεκτονική σκηνών
# ------------------------------------------------------------

# Η Scene είναι αφηρημένη κλάση (abstract base class)
# Όλες οι σκηνές του παιχνιδιού (menu, game, game over κ.λπ.)
# κληρονομούν από αυτή και είναι υποχρεωμένες να υλοποιούν
# τις μεθόδους enter, exit, handle_input, update και render
from shared.core.scene import Scene


# ------------------------------------------------------------
# MODEL layer – αντικείμενα παιχνιδιού (καθαρά δεδομένα)
# ------------------------------------------------------------

# Level:
# Αναπαριστά την πίστα του παιχνιδιού ως grid (tiles).
# Περιέχει πληροφορίες για:
# - πλάτος / ύψος
# - τύπο κάθε tile (DIRT, TUNNEL, EMERALD κ.λπ.)
# - έλεγχο ορίων (in_bounds)
from shared.model.level import Level

# Player:
# Αναπαριστά τον παίκτη.
# Κρατά:
# - tile_x, tile_y (θέση στο grid)
# - direction (προς τα πού κοιτάει)
# - alive (αν είναι ζωντανός)
from shared.model.player import Player

# Enemy:
# Αναπαριστά έναν εχθρό.
# Κληρονομεί από Entity και περιέχει:
# - μορφή (NOBBIN ή HOBBIN)
# - timers για αλλαγή μορφής και κίνηση
# - alive flag
from shared.model.enemy import Enemy

# GoldBag:
# Αναπαριστά έναν σάκο χρυσού.
# Μπορεί να:
# - πέσει (falling)
# - σπάσει και να γίνει gold pile
# - συλλεχθεί
from shared.model.gold_bag import GoldBag

# Score:
# Διαχειρίζεται το σκορ του παίκτη.
# Υποστηρίζει:
# - απλή προσθήκη πόντων
# - combo από emeralds
# - bonus από φαγωμένους εχθρούς
from shared.model.score import Score

# Lives:
# Διαχειρίζεται τις ζωές του παίκτη.
# Περιέχει:
# - αριθμό ζωών
# - λογική extra life κάθε X πόντους
from shared.model.lives import Lives

# Weapon:
# Διαχειρίζεται το όπλο του παίκτη.
# Περιέχει:
# - cooldown
# - timer για το πότε μπορεί να ξαναπυροβολήσει
from shared.model.weapon import Weapon

# Types / Enums:
# Direction  : κατεύθυνση κίνησης
# TileType   : τύπος πλακιδίου πίστας
# GameMode  : κατάσταση παιχνιδιού (NORMAL, BONUS, LEVEL_COMPLETE)
from shared.model.types import Direction, TileType, GameMode


# ------------------------------------------------------------
# SYSTEMS – λογική παιχνιδιού (gameplay rules)
# ------------------------------------------------------------

# GridMovementSystem:
# Υλοποιεί την κίνηση entity στο grid (πάνω/κάτω/αριστερά/δεξιά)
from shared.services.grid_movement import GridMovementSystem

# TileInteractionSystem:
# Χειρίζεται αλληλεπίδραση entity με tiles
# π.χ. σκάψιμο χώματος
from shared.services.tile_interaction import TileInteractionSystem

# EnemyAISystem:
# Συνδέει τον EnemyBrain με το movement system
# και αποφασίζει πώς κινούνται οι εχθροί
from shared.services.enemy_ai_system import EnemyAISystem

# EnemyFormSystem:
# Διαχειρίζεται την αλλαγή μορφής εχθρού
# (NOBBIN <-> HOBBIN)
from shared.services.enemy_form_system import EnemyFormSystem

# HobbinDiggingSystem:
# Επιτρέπει στους Hobbin να σκάβουν χώμα και emeralds
from shared.services.hobbin_digging_system import HobbinDiggingSystem

# GoldBagSystem:
# Διαχειρίζεται πτώση σακιών χρυσού και μετατροπή τους σε gold
from shared.services.gold_bag_system import GoldBagSystem

# GoldBagPushSystem:
# Διαχειρίζεται το σπρώξιμο σακιών χρυσού αριστερά / δεξιά
from shared.services.gold_bag_push_system import GoldBagPushSystem

# ScoreSystem:
# Συνδέει το score με το gameplay
# π.χ. συλλογή emeralds
from shared.services.score_system import ScoreSystem

# WeaponSystem:
# Διαχειρίζεται το firing του όπλου
# (δημιουργία bullets, cooldown)
from shared.services.weapon_system import WeaponSystem

# BulletSystem:
# Διαχειρίζεται την κίνηση bullets και συγκρούσεις με εχθρούς
from shared.services.bullet_system import BulletSystem

# EnemySpawner:
# Δημιουργεί νέους εχθρούς σε συγκεκριμένα spawn points
from shared.services.enemy_spawner import EnemySpawner

# DifficultyScaler:
# Ορίζει τη δυσκολία ανά πίστα
# (αριθμός enemies, emeralds, ταχύτητα κ.λπ.)
from shared.services.difficulty_scaler import DifficultyScaler


# ------------------------------------------------------------
# AI
# ------------------------------------------------------------

# EnemyBrain:
# Υλοποιεί την τεχνητή νοημοσύνη εχθρών
# (εύρεση διαδρομής προς τον παίκτη ή φυγή σε bonus mode)
from shared.ai.enemy_brain import EnemyBrain


# ------------------------------------------------------------
# VIEW layer – κάμερα και γραφικά
# ------------------------------------------------------------

# Camera2D:
# Μετατρέπει συντεταγμένες κόσμου (tiles) σε συντεταγμένες οθόνης
from client.views.camera import Camera2D

# TilemapView:
# Ζωγραφίζει την πίστα (χώμα, tunnels, background)
from client.views.tilemap_view import TilemapView


# ------------------------------------------------------------
# SPRITES – οπτική αναπαράσταση αντικειμένων
# ------------------------------------------------------------

# PlayerSprite:
# Ζωγραφίζει τον παίκτη με σωστή κατεύθυνση
from client.views.sprites.player_sprite import PlayerSprite

# EmeraldSprite:
# Ζωγραφίζει τα emeralds
from client.views.sprites.emerald_sprite import EmeraldSprite

# GoldBagSprite:
# Ζωγραφίζει σάκους χρυσού / πτώση / gold pile
from client.views.sprites.gold_bag_sprite import GoldBagSprite

# EnemySprite:
# Ζωγραφίζει Nobbin / Hobbin με σωστή κατεύθυνση
from client.views.sprites.enemy_sprite import EnemySprite


# ------------------------------------------------------------
# EFFECTS
# ------------------------------------------------------------

# ExplosionSystem:
# Υλοποιεί απλά particle effects εκρήξεων
from client.views.effects.explosion import ExplosionSystem


# ------------------------------------------------------------
# AUDIO
# ------------------------------------------------------------

# AudioManager:
# Διαχειρίζεται μουσική και ηχητικά εφέ
from shared.services.audio_manager import AudioManager



class GameScene(Scene):
    # ==================================================
    # ΣΤΑΘΕΡΕΣ (CONSTANTS) ΤΗΣ ΣΚΗΝΗΣ
    # ==================================================

    # Μέγεθος ενός tile σε pixels (32x32)
    TILE_SIZE = 32

    # Χρόνος (σε δευτερόλεπτα) που ο παίκτης είναι άτρωτος
    # μετά από respawn
    INVULN_SECONDS = 0.70

    # Αρχική θέση respawn του παίκτη στο grid
    RESPAWN_X = 5
    RESPAWN_Y = 5

    # Καθυστέρηση πριν περάσουμε στο επόμενο level
    # αφού καθαριστεί η πίστα
    LEVEL_COMPLETE_DELAY = 2.0


    # ==================================================
    # ΑΡΧΙΚΟΠΟΙΗΣΗ ΣΚΗΝΗΣ
    # ==================================================
    def __init__(self, scene_manager):
        # Αναφορά στο SceneManager
        # Χρησιμοποιείται για αλλαγή σκηνών (π.χ. game → game over)
        self.sm = scene_manager


        # ==================================================
        # LEVEL & PLAYER
        # ==================================================

        # Τρέχον επίπεδο παιχνιδιού (ξεκινάμε από το 1)
        self.level_index = 1

        # Δημιουργία του Level αντικειμένου
        # Κλάση: Level
        # Αναπαριστά την πίστα ως grid 60x40 tiles
        self.level = Level(60, 40)

        # Δημιουργία του Player 1
        # Κλάση: Player
        # Τοποθετείται στη θέση respawn
        self.player = Player("p1", self.RESPAWN_X, self.RESPAWN_Y)

        # Timer άτρωτου παίκτη (invulnerability)
        # Μηδενίζεται αρχικά
        self._invuln_timer = 0.0

        # Λίστα παικτών (προετοιμασία για multiplayer)
        # Προς το παρόν περιέχει μόνο τον Player 1
        self.players = [self.player]


        # ==================================================
        # GAME STATE
        # ==================================================

        # Κατάσταση παιχνιδιού
        # NORMAL / BONUS / LEVEL_COMPLETE
        self.game_mode = GameMode.NORMAL

        # Timer που μετράει πόσο έχουμε μείνει
        # στο LEVEL_COMPLETE state
        self.level_complete_timer = 0.0


        # ==================================================
        # DIFFICULTY SYSTEM
        # ==================================================

        # Δημιουργία DifficultyScaler
        # Κλάση: DifficultyScaler
        # Όλη η λογική δυσκολίας βρίσκεται εκεί
        self.scaler = DifficultyScaler()

        # Συνολικός αριθμός εχθρών για το level
        self.total_enemies = self.scaler.enemies_for_level(self.level_index)

        # Μέγιστοι ταυτόχρονοι εχθροί στην πίστα
        # (αρχικά περιορισμένοι για ομαλή δυσκολία)
        self.max_active = min(2, self.total_enemies)

        # Καθυστέρηση κίνησης εχθρών
        # Όσο μικρότερη, τόσο πιο γρήγοροι
        self.enemy_delay = self.scaler.enemy_move_delay(self.level_index)


        # ==================================================
        # ENEMY MANAGEMENT
        # ==================================================

        # Δημιουργία EnemySpawner
        # Κλάση: EnemySpawner
        # Καθορίζει από πού εμφανίζονται οι εχθροί
        self.enemy_spawner = EnemySpawner(
            spawn_x=self.level.width - 2,
            spawn_y=2
        )

        # Λίστα ενεργών εχθρών στην πίστα
        self.enemies: list[Enemy] = []

        # Πόσοι εχθροί έχουν γίνει spawn συνολικά
        self.spawned_total = 0

        # Timer για spawn νέων εχθρών
        self._spawn_timer = 0.0

        # Καθυστέρηση ανάμεσα σε spawns
        self.spawn_delay = 0.8


        # ==================================================
        # GOLD BAGS
        # ==================================================

        # Λίστα σακιών χρυσού
        # Δημιουργούνται δυναμικά αργότερα
        self.gold_bags = []


        # ==================================================
        # SYSTEMS (ΛΟΓΙΚΗ ΠΑΙΧΝΙΔΙΟΥ)
        # ==================================================

        # Σύστημα κίνησης σε grid
        self.movement = GridMovementSystem()

        # Σύστημα αλληλεπίδρασης με tiles (σκάψιμο κ.λπ.)
        self.tile_interaction = TileInteractionSystem()

        # Enemy AI
        # EnemyBrain: αποφασίζει κατεύθυνση
        # EnemyAISystem: εφαρμόζει την απόφαση
        self.enemy_brain = EnemyBrain()
        self.enemy_ai = EnemyAISystem(self.enemy_brain)

        # Σύστημα αλλαγής μορφής εχθρού (Nobbin ↔ Hobbin)
        self.enemy_form_system = EnemyFormSystem()

        # Σύστημα σκαψίματος Hobbin
        self.hobbin_digging = HobbinDiggingSystem()

        # Σύστημα πτώσης σακιών χρυσού
        self.gold_bag_system = GoldBagSystem()

        # Σύστημα σπρωξίματος σακιών χρυσού
        self.gold_bag_push = GoldBagPushSystem()


        # ==================================================
        # SCORE & LIVES
        # ==================================================

        # Score Player 1
        self.score = Score()

        # Σύστημα που συνδέει gameplay με score
        self.score_system = ScoreSystem(self.score)

        # Ζωές Player 1
        self.lives = Lives(start_lives=3)

        # Player 2 (έτοιμο αλλά ανενεργό)
        self.score_p2 = Score()
        self.lives_p2 = Lives(start_lives=3)


        # ==================================================
        # WEAPON & BULLETS
        # ==================================================

        # Όπλο παίκτη με cooldown
        self.weapon = Weapon(cooldown=2.0)

        # Σύστημα χρήσης όπλου
        self.weapon_system = WeaponSystem()

        # Σύστημα bullets (κίνηση, συγκρούσεις)
        self.bullet_system = BulletSystem()

        # Λίστα ενεργών bullets
        self.bullets = []


        # ==================================================
        # VIEW (ΚΑΜΕΡΑ & ΓΡΑΦΙΚΑ)
        # ==================================================

        # Legacy camera (κρατιέται για παλιό κώδικα)
        self.camera = None

        # Κάμερα Player 1
        self.camera_p1 = None

        # Κάμερα Player 2 (split screen)
        self.camera_p2 = None

        # View της πίστας
        self.tilemap_view = TilemapView(self.TILE_SIZE)

        # Font HUD (θα φορτωθεί στο enter)
        self._font = None


        # ==================================================
        # TIMING & INPUT
        # ==================================================

        # Cooldown κίνησης παίκτη (grid-based)
        self._move_cooldown = 0.0

        # Τελευταίο InputSnapshot
        self._last_input = None


        # ==================================================
        # SPRITES
        # ==================================================

        # Sprite παίκτη
        self.player_sprite = PlayerSprite()

        # Sprite emerald
        self.emerald_sprite = EmeraldSprite()

        # Sprite gold bag
        self.gold_bag_sprite = GoldBagSprite()

        # Sprite εχθρών
        self.enemy_sprite = EnemySprite()


        # ==================================================
        # EFFECTS
        # ==================================================

        # Σύστημα εκρήξεων (particles)
        self.explosions = ExplosionSystem(self.TILE_SIZE)

        # Αποθήκευση προηγούμενων ζωντανών εχθρών
        # Χρησιμοποιείται για detection θανάτων
        self._alive_enemy_ids_prev = set()


        # ==================================================
        # PLAYERS (MULTI-READY)
        # ==================================================

        # Player 1 (υπάρχων)
        self.player1 = self.player

        # Player 2 (θα δημιουργηθεί αν επιλεγεί multiplayer)
        self.player2 = None

        # Λίστα παικτών (ξεκινά με τον Player 1)
        self.players = [self.player1]


    # ==================================================
    # Scene interface
    # ==================================================

    def enter(self, payload=None):
        # --------------------------------------------------
        # Φόρτωση γραμματοσειράς HUD
        # --------------------------------------------------
        # Γίνεται μόνο την πρώτη φορά που μπαίνουμε στη σκηνή
        # ώστε να μη φορτώνεται ξανά άσκοπα
        if self._font is None:
            self._font = pygame.font.Font(
                "assets/fonts/Orbitron-Bold.ttf", 18
            )

        # --------------------------------------------------
        # Πλήθος παικτών
        # --------------------------------------------------
        # Αν το payload υπάρχει, διαβάζουμε πόσοι παίκτες επιλέχθηκαν
        # από το Main Menu
        # Αν όχι, default = 1 παίκτης
        self.player_count = payload.get("players", 1) if payload else 1

        # ==================================================
        # HARD RESET – ΚΑΘΕ ΝΕΟ GAME (SINGLE ή MULTI)
        # ==================================================
        # Ό,τι ακολουθεί επαναφέρει το παιχνίδι στην αρχική
        # κατάσταση, σαν να άνοιξε μόλις το παιχνίδι.

        # --------------------------------------------------
        # Reset Level
        # --------------------------------------------------
        # Επαναφορά στο πρώτο επίπεδο
        self.level_index = 1

        # Δημιουργία ΝΕΟΥ αντικειμένου Level
        # Κλάση: Level
        # Η παλιά πίστα πετιέται και ξεκινάμε από καθαρό grid
        self.level = Level(60, 40)

        # --------------------------------------------------
        # Reset Difficulty
        # --------------------------------------------------
        # Δημιουργία νέου DifficultyScaler
        self.scaler = DifficultyScaler()

        # Υπολογισμός συνολικών εχθρών για το level 1
        self.total_enemies = self.scaler.enemies_for_level(self.level_index)

        # Μέγιστοι ενεργοί εχθροί στην πίστα
        self.max_active = min(2, self.total_enemies)

        # Καθυστέρηση κίνησης εχθρών
        self.enemy_delay = self.scaler.enemy_move_delay(self.level_index)

        # ==================================================
        # Players
        # ==================================================

        # --------------------------------------------------
        # Player 1 (υπάρχει ΠΑΝΤΑ)
        # --------------------------------------------------
        # Επαναφορά κατάστασης
        self.player.alive = True

        # Τοποθέτηση στο σημείο respawn
        self.player.tile_x = self.RESPAWN_X
        self.player.tile_y = self.RESPAWN_Y

        # Μηδενισμός κατεύθυνσης (ώστε να μην πυροβολεί άμεσα)
        self.player.direction = None

        # --------------------------------------------------
        # Player 2 (μόνο αν επιλεγεί multiplayer)
        # --------------------------------------------------
        if self.player_count == 2:

            # Αν δεν υπάρχει ήδη Player 2, τον δημιουργούμε
            if self.player2 is None:
                self.player2 = Player(
                    "p2",
                    self.RESPAWN_X + 2,
                    self.RESPAWN_Y
                )

            # Reset κατάστασης Player 2
            self.player2.alive = True
            self.player2.tile_x = self.RESPAWN_X + 2
            self.player2.tile_y = self.RESPAWN_Y
            self.player2.direction = None

            # Λίστα ενεργών παικτών
            self.players = [self.player, self.player2]

        else:
            # Single Player
            # Ο Player 2 απενεργοποιείται πλήρως
            self.player2 = None
            self.players = [self.player]

        # ==================================================
        # Cameras
        # ==================================================

        # Παίρνουμε το μέγεθος της οθόνης
        screen = pygame.display.get_surface()
        w, h = screen.get_size()

        if self.player2:
            # Split screen:
            # Κάθε παίκτης έχει τη δική του κάμερα
            self.camera_p1 = Camera2D(w // 2, h, self.TILE_SIZE)
            self.camera_p2 = Camera2D(w // 2, h, self.TILE_SIZE)
        else:
            # Single player:
            # Μία κάμερα για όλη την οθόνη
            self.camera_p1 = Camera2D(w, h, self.TILE_SIZE)
            self.camera_p2 = None

        # Legacy camera
        # Χρησιμοποιείται από παλιό κώδικα για ασφάλεια
        self.camera = self.camera_p1

        # --------------------------------------------------
        # Reset προηγούμενων εχθρών (για explosion detection)
        # --------------------------------------------------
        self._alive_enemy_ids_prev = set()

        # ==================================================
        # Spawn περιεχομένου πίστας
        # ==================================================
        # ΠΡΟΣΟΧΗ:
        # Γίνεται ΠΑΝΩ ΣΕ ΝΕΟ, ΚΑΘΑΡΟ Level

        # Δημιουργία emeralds
        self._spawn_emeralds()

        # Δημιουργία gold bags
        self._spawn_gold_bags()

        # ==================================================
        # Stats & Runtime State
        # ==================================================

        # Reset score
        self.score.points = 0
        self.score_p2.points = 0

        # Reset ζωών
        self.lives.count = 3
        self.lives_p2.count = 3

        # Καθαρισμός λιστών gameplay
        self.enemies.clear()
        self.bullets.clear()

        # Reset spawn counters
        self.spawned_total = 0
        self._spawn_timer = 0.0

        # Ενεργοποίηση άτρωτου μετά το respawn
        self._invuln_timer = self.INVULN_SECONDS

        # Reset κατάστασης παιχνιδιού
        self.game_mode = GameMode.NORMAL
        self.level_complete_timer = 0.0

    def exit(self):
        # Η μέθοδος exit() καλείται όταν η σκηνή GameScene
        # εγκαταλείπεται (π.χ. πάμε σε Game Over ή Menu).
        # Εδώ δεν απαιτείται καθαρισμός πόρων,
        # γιατί το reset γίνεται στο enter().
        pass


    def handle_input(self, input_snapshot):
        # Αποθηκεύουμε το στιγμιότυπο εισόδου (InputSnapshot)
        # ώστε να χρησιμοποιηθεί στο update().
        # Το InputSnapshot παράγεται από το InputController
        # και περιέχει την κατάσταση πλήκτρων για ΑΥΤΟ το frame.
        self._last_input = input_snapshot


    # ==================================================
    # Helpers (βοηθητικές μέθοδοι gameplay)
    # ==================================================

    def _respawn_player2(self):
        # Επαναφορά Player 2 μετά από απώλεια ζωής

        # Αν δεν υπάρχει Player 2 (single player),
        # δεν κάνουμε τίποτα
        if not self.player2:
            return

        # Τοποθέτηση Player 2 στο προκαθορισμένο respawn
        self.player2.tile_x = self.RESPAWN_X + 2
        self.player2.tile_y = self.RESPAWN_Y

        # Μηδενισμός κατεύθυνσης
        # ώστε να μην πυροβολήσει αμέσως
        self.player2.direction = None


    def _spawn_emeralds(self):
        """
        Δημιουργία emeralds στην πίστα.

        Κανόνας παιχνιδιού:
        - Level 1: 40 emeralds
        - Κάθε επόμενο level: +10
        """

        # Υπολογισμός πλήθους emeralds
        count = 40 + (self.level_index - 1) * 10

        placed = 0          # πόσα emeralds έχουν τοποθετηθεί
        attempts = 0        # πόσες προσπάθειες έγιναν
        max_attempts = count * 10  # όριο για αποφυγή infinite loop

        # Προσπαθούμε μέχρι να τοποθετηθούν όλα
        # ή να ξεπεραστεί το όριο προσπαθειών
        while placed < count and attempts < max_attempts:
            attempts += 1

            # Τυχαία θέση ΜΕΣΑ στα όρια της πίστας
            x = random.randint(1, self.level.width - 2)
            y = random.randint(1, self.level.height - 2)

            # Emerald μπορεί να μπει ΜΟΝΟ πάνω σε DIRT
            if self.level.get_tile(x, y) == TileType.DIRT:
                self.level.set_tile(x, y, TileType.EMERALD)
                placed += 1


    def _spawn_gold_bags(self):
        """
        Δημιουργία gold bags (σάκοι χρυσού).

        Κανόνας παιχνιδιού:
        - Level 1: 5 σάκοι
        - Κάθε επόμενο level: +2
        """

        # Υπολογισμός πλήθους σάκων
        count = 5 + (self.level_index - 1) * 2

        # Καθαρισμός παλιάς λίστας
        self.gold_bags.clear()

        placed = 0
        attempts = 0
        max_attempts = count * 15

        while placed < count and attempts < max_attempts:
            attempts += 1

            # Επιλέγουμε θέση όχι κοντά στα άκρα
            x = random.randint(2, self.level.width - 3)
            y = random.randint(2, self.level.height - 3)

            # Κανόνας:
            # - το tile ΠΡΕΠΕΙ να είναι DIRT
            # - από κάτω ΠΡΕΠΕΙ επίσης να είναι DIRT
            #   (ώστε να μπορεί να πέσει αργότερα)
            if (
                self.level.get_tile(x, y) == TileType.DIRT
                and self.level.get_tile(x, y + 1) == TileType.DIRT
            ):
                # Δημιουργία αντικειμένου GoldBag
                # Κλάση: GoldBag
                bag_id = f"g{placed}_{self.level_index}"
                bag = GoldBag(bag_id, x, y)

                # Προσθήκη στη λίστα gold bags
                self.gold_bags.append(bag)

                # Ενημέρωση tile map
                self.level.set_tile(x, y, TileType.GOLD_BAG)

                placed += 1


    def _respawn_player(self):
        # Επαναφορά Player 1 μετά από απώλεια ζωής

        # Τοποθέτηση στο respawn
        self.player.tile_x = self.RESPAWN_X
        self.player.tile_y = self.RESPAWN_Y

        # Μηδενισμός κατεύθυνσης
        self.player.direction = None

        # Καθαρισμός bullets
        # (δεν συνεχίζουν να υπάρχουν μετά τον θάνατο)
        self.bullets.clear()

        # Ενεργοποίηση προσωρινής αθανασίας
        self._invuln_timer = self.INVULN_SECONDS


    def _handle_player_hit(self):
        # Διαχείριση σύγκρουσης Player 1 με enemy

        # Αν ο παίκτης είναι ακόμα άτρωτος,
        # αγνοούμε το χτύπημα
        if self._invuln_timer > 0.0:
            return

        # Χάνει μία ζωή
        if not self.lives.lose_life():
            # -----------------------------------------
            # Player 1 ΠΕΘΑΝΕ ΟΡΙΣΤΙΚΑ
            # -----------------------------------------
            self.player.alive = False

            # Αν υπάρχει Player 2 και έχει ζωές,
            # το παιχνίδι συνεχίζεται σε co-op
            if self.player2 and self.lives_p2.count > 0:
                return

            # Αλλιώς → Game Over
            self.sm.set_scene(
                "gameover",
                {
                    "score_p1": self.score.points,
                    "score_p2": self.score_p2.points
                }
            )
            return

        # -----------------------------------------
        # Player 1 έχει ακόμα ζωές → respawn
        # -----------------------------------------
        self._respawn_player()


    def _load_next_level(self):
        # --------------------------------------------------
        # ΦΟΡΤΩΣΗ ΕΠΟΜΕΝΟΥ LEVEL
        # --------------------------------------------------
        # Η μέθοδος καλείται όταν:
        # - έχουν συλλεχθεί ΟΛΑ τα emeralds
        # - έχει ολοκληρωθεί το delay ολοκλήρωσης level
        # --------------------------------------------------

        # Έλεγχος αν υπάρχει επόμενο level
        # Το DifficultyScaler γνωρίζει πόσα levels υποστηρίζονται
        if not self.scaler.has_next_level(self.level_index):
            # Δεν υπάρχει επόμενο level → ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ
            self.sm.set_scene(
                "gameover",
                {
                    "score_p1": self.score.points,
                    "score_p2": self.score_p2.points
                }
            )
            return

        # --------------------------------------------------
        # Αύξηση δείκτη level & δημιουργία ΝΕΟΥ Level
        # --------------------------------------------------
        self.level_index += 1

        # Δημιουργία νέου αντικειμένου Level
        # Κλάση: Level (model)
        self.level = Level(60, 40)

        # --------------------------------------------------
        # RESET Player 1
        # --------------------------------------------------
        # Ο Player είναι αντικείμενο της κλάσης Player
        self.player.tile_x = self.RESPAWN_X
        self.player.tile_y = self.RESPAWN_Y
        self.player.direction = None

        # ΣΗΜΑΝΤΙΚΟ:
        # Αν ο Player είχε πεθάνει στο τέλος του προηγούμενου level,
        # εδώ τον επαναφέρουμε ΖΩΝΤΑΝΟ
        self.player.alive = True

        # --------------------------------------------------
        # RESET Player 2 (αν υπάρχει)
        # --------------------------------------------------
        if self.player2:
            self.player2.tile_x = self.RESPAWN_X + 2
            self.player2.tile_y = self.RESPAWN_Y
            self.player2.direction = None

            # Αντίστοιχα επαναφέρουμε τον Player 2
            self.player2.alive = True

        # --------------------------------------------------
        # RESET runtime αντικειμένων
        # --------------------------------------------------

        # Καθαρισμός enemies (κλάση Enemy)
        self.enemies.clear()

        # Reset spawn counters
        self.spawned_total = 0
        self._spawn_timer = 0.0

        # Καθαρισμός bullets (κλάση Bullet)
        self.bullets.clear()

        # Επιστροφή σε κανονικό game mode
        self.game_mode = GameMode.NORMAL

        # Reset timer ολοκλήρωσης level
        self.level_complete_timer = 0.0

        # --------------------------------------------------
        # Difficulty scaling για νέο level
        # --------------------------------------------------
        self.total_enemies = self.scaler.enemies_for_level(self.level_index)

        # Όσο ανεβαίνει το level:
        # - αυξάνεται το max πλήθος ταυτόχρονων enemies
        self.max_active = min(
            2 + self.level_index // 2,
            self.total_enemies
        )

        # Enemy movement delay (πιο γρήγοροι enemies)
        self.enemy_delay = self.scaler.enemy_move_delay(self.level_index)

        # --------------------------------------------------
        # Spawn περιεχομένου πίστας
        # --------------------------------------------------
        self._spawn_emeralds()
        self._spawn_gold_bags()


    def _handle_player2_input(self, dt):
        # --------------------------------------------------
        # ΧΕΙΡΙΣΜΟΣ INPUT ΓΙΑ PLAYER 2 (CO-OP)
        # --------------------------------------------------

        # Αν δεν υπάρχει Player 2 ή είναι νεκρός → αγνοούμε
        if not self.player2 or not self.player2.alive or self.lives_p2.count <= 0:
            return

        # Άμεση ανάγνωση πληκτρολογίου (WASD)
        keys = pygame.key.get_pressed()

        direction = None

        # --------------------------------------------------
        # ΚΙΝΗΣΗ (WASD)
        # --------------------------------------------------
        if keys[pygame.K_w]:
            direction = Direction.UP
        elif keys[pygame.K_s]:
            direction = Direction.DOWN
        elif keys[pygame.K_a]:
            direction = Direction.LEFT
        elif keys[pygame.K_d]:
            direction = Direction.RIGHT

        # Αν έχει πατηθεί κατεύθυνση
        # και δεν υπάρχει cooldown κίνησης
        if direction and self._move_cooldown <= 0:
            self.player2.direction = direction

            # Προσπάθεια μετακίνησης στο grid
            # Κλάση: GridMovementSystem
            if self.movement.try_move(self.player2, direction, self.level):
                # Αν μπήκε σε νέο tile:
                # ελέγχουμε interactions (emerald, dirt κ.λπ.)
                self.tile_interaction.on_enter(self.player2, self.level)

                # Θέτουμε cooldown για επόμενη κίνηση
                self._move_cooldown = 0.12

        # --------------------------------------------------
        # FIRE (LEFT SHIFT)
        # --------------------------------------------------
        if keys[pygame.K_LSHIFT]:
            # Αποθηκεύουμε πόσες σφαίρες υπήρχαν πριν
            before = len(self.bullets)

            # Προσπάθεια πυροβολισμού
            # Κλάση: WeaponSystem
            self.weapon_system.try_fire(
                self.weapon,
                self.player2,
                self.bullets
            )

            # Όσες σφαίρες δημιουργήθηκαν τώρα
            # δηλώνονται ως bullets του Player 2
            for b in self.bullets[before:]:
                b.owner_id = "p2"

            # Αν όντως πυροβόλησε
            if len(self.bullets) > before:
                AudioManager.play_sound("shot")


    def _get_closest_player(self, enemy):
        # --------------------------------------------------
        # ΕΠΙΛΟΓΗ ΣΤΟΧΟΥ ΓΙΑ ENEMY
        # --------------------------------------------------
        # Επιστρέφει τον κοντινότερο ΖΩΝΤΑΝΟ παίκτη
        # Χρησιμοποιείται από το Enemy AI
        # --------------------------------------------------

        alive_players = []

        # Player 1
        if self.player and self.player.alive:
            alive_players.append(self.player)

        # Player 2
        if self.player2 and self.player2.alive:
            alive_players.append(self.player2)

        # Αν δεν υπάρχει ΚΑΝΕΝΑΣ ζωντανός παίκτης
        # → enemy δεν έχει στόχο
        if not alive_players:
            return None

        # Manhattan distance (grid-based απόσταση)
        def dist(p):
            return abs(p.tile_x - enemy.tile_x) + abs(p.tile_y - enemy.tile_y)

        # Επιστροφή παίκτη με τη μικρότερη απόσταση
        return min(alive_players, key=dist)

    def _render_view(self, surface, camera, focus_player):
        # --------------------------------------------------
        # Ζωγραφίζει μία "άποψη" του κόσμου (world view)
        # Χρησιμοποιείται:
        # - στο single player (μία φορά)
        # - στο split screen (μία φορά ανά παίκτη)
        #
        # surface       : pygame.Surface όπου ζωγραφίζουμε
        # camera        : Camera2D που μετατρέπει world → screen coords
        # focus_player  : παίκτης που ακολουθεί η camera (δεν χρησιμοποιείται εδώ άμεσα)
        # --------------------------------------------------

        # Καθαρίζουμε το surface με μαύρο φόντο
        surface.fill((0, 0, 0))

        # Ζωγραφίζουμε το tilemap (χώμα, tunnels, background)
        # Κλάση: TilemapView
        # ΔΕΝ γνωρίζει τίποτα για παίκτες, εχθρούς ή bullets
        self.tilemap_view.render(surface, self.level, camera)

        # --------------------------------------------------
        # ΠΑΙΚΤΕΣ (Player 1 & Player 2)
        # --------------------------------------------------
        # Ζωγραφίζουμε ΚΑΙ τους δύο παίκτες στο ίδιο world
        for p in (self.player, self.player2):

            # Αν ο παίκτης δεν υπάρχει (None) ή είναι νεκρός
            # ΔΕΝ τον ζωγραφίζουμε
            if p is None or not p.alive:
                continue

            # Flag που ελέγχει αν θα ζωγραφιστεί τελικά
            draw_it = True

            # Invulnerability blink ΜΟΝΟ για Player 1
            # Ο Player 2 δεν έχει invulnerability
            if p == self.player and self._invuln_timer > 0.0:
                # Δημιουργούμε blinking effect
                # Ανάλογα με τον χρόνο, κάποιες φορές δεν ζωγραφίζεται
                if int(self._invuln_timer * 18) % 2 == 0:
                    draw_it = False

            if draw_it:
                # Μετατροπή από tile coordinates σε world coordinates
                px = p.tile_x * self.TILE_SIZE
                py = p.tile_y * self.TILE_SIZE

                # Μετατροπή από world σε screen coordinates μέσω camera
                sx, sy = camera.world_to_screen(px, py)

                # Ζωγραφίζουμε το sprite του παίκτη
                # Κλάση: PlayerSprite
                # Χρησιμοποιεί direction για rotation / flip
                self.player_sprite.draw(surface, sx, sy, p.direction)

        # --------------------------------------------------
        # ENEMIES
        # --------------------------------------------------
        for enemy in self.enemies:
            # Tile → world
            ex = enemy.tile_x * self.TILE_SIZE
            ey = enemy.tile_y * self.TILE_SIZE

            # World → screen
            sx, sy = camera.world_to_screen(ex, ey)

            # Ζωγραφίζουμε τον enemy
            # Κλάση: EnemySprite
            # Εσωτερικά επιλέγει nobbin / hobbin sprite
            self.enemy_sprite.draw(surface, enemy, sx, sy)

        # --------------------------------------------------
        # EMERALDS (αντικείμενα που είναι αποθηκευμένα στο tilemap)
        # --------------------------------------------------
        # Διατρέχουμε ΟΛΟ το grid του level
        for y, row in enumerate(self.level.tiles):
            for x, tile in enumerate(row):

                # Αν το tile είναι emerald
                if tile == TileType.EMERALD:
                    # Tile → world
                    wx = x * self.TILE_SIZE
                    wy = y * self.TILE_SIZE

                    # World → screen
                    sx, sy = camera.world_to_screen(wx, wy)

                    # Ζωγραφίζουμε emerald sprite
                    # Κλάση: EmeraldSprite
                    self.emerald_sprite.draw(surface, sx, sy)

        # --------------------------------------------------
        # GOLD BAGS / GOLD PILES
        # --------------------------------------------------
        for bag in self.gold_bags:

            # Αν έχει συλλεχθεί, δεν ζωγραφίζεται
            if bag.collected:
                continue

            # Tile → world
            gx = bag.tile_x * self.TILE_SIZE
            gy = bag.tile_y * self.TILE_SIZE

            # World → screen
            sx, sy = camera.world_to_screen(gx, gy)

            # Ζωγραφίζουμε sack / falling sack / gold pile
            # Κλάση: GoldBagSprite
            self.gold_bag_sprite.draw(surface, bag, sx, sy)

        # --------------------------------------------------
        # BULLETS
        # --------------------------------------------------
        # Τα bullets είναι απλά τετράγωνα (όχι sprite)
        # Αυτό βοηθά debugging και arcade αίσθηση
        for b in self.bullets:
            # Tile → world
            bx = b.tile_x * self.TILE_SIZE
            by = b.tile_y * self.TILE_SIZE

            # World → screen
            sx, sy = camera.world_to_screen(bx, by)

            # Ζωγραφίζουμε μικρό λευκό τετράγωνο
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                pygame.Rect(sx + 12, sy + 12, 8, 8)
            )

        # --------------------------------------------------
        # EXPLOSIONS (particles)
        # --------------------------------------------------
        # Κλάση: ExplosionSystem
        # Χρησιμοποιεί camera για σωστή τοποθέτηση
        self.explosions.draw(surface, camera)

    # ==================================================
    # Update
    # ==================================================

    def update(self, dt):
        # ==================================================
        # ΓΕΝΙΚΟ UPDATE LOOP ΤΗΣ ΣΚΗΝΗΣ ΠΑΙΧΝΙΔΙΟΥ
        #
        # Η μέθοδος αυτή καλείται ΚΑΘΕ FRAME.
        # Το dt (delta time) είναι ο χρόνος σε δευτερόλεπτα
        # από το προηγούμενο frame.
        # ==================================================

        # Μείωση cooldown κίνησης παίκτη
        self._move_cooldown = max(0.0, self._move_cooldown - dt)

        # Ενημέρωση weapon cooldown
        # Κλάση: Weapon
        self.weapon.update(dt)

        # Ενημέρωση invulnerability timer του Player 1
        if self._invuln_timer > 0.0:
            self._invuln_timer = max(0.0, self._invuln_timer - dt)

        # ==================================================
        # BONUS MODE
        # ==================================================
        # Σε bonus mode οι εχθροί αλλάζουν συμπεριφορά
        if self.game_mode == GameMode.BONUS:
            self.bonus_timer -= dt
            if self.bonus_timer <= 0:
                self.game_mode = GameMode.NORMAL

        # ==================================================
        # LEVEL COMPLETE MODE
        # ==================================================
        # Όταν τελειώσουν όλα τα emeralds, μπαίνουμε εδώ
        if self.game_mode == GameMode.LEVEL_COMPLETE:
            self.level_complete_timer -= dt
            if self.level_complete_timer <= 0:
                self._load_next_level()
            return  # σταματάμε update όσο περιμένουμε

        # ==================================================
        # ΕΛΕΓΧΟΣ ΟΛΟΚΛΗΡΩΣΗΣ ΠΙΣΤΑΣ
        # ==================================================
        # Αν υπάρχει έστω ένα emerald στο grid, συνεχίζουμε
        emerald_exists = any(
            TileType.EMERALD in row for row in self.level.tiles
        )

        if not emerald_exists:
            self.game_mode = GameMode.LEVEL_COMPLETE
            self.level_complete_timer = self.LEVEL_COMPLETE_DELAY
            return

        # Snapshot input από InputController
        inp = self._last_input

        # ==================================================
        # PLAYER 1 MOVEMENT
        # ==================================================
        if self.player.alive and inp and self._move_cooldown <= 0:

            direction = None

            # Ανάγνωση input και αντιστοίχιση σε Direction enum
            if inp.up:
                direction = Direction.UP
            elif inp.down:
                direction = Direction.DOWN
            elif inp.left:
                direction = Direction.LEFT
            elif inp.right:
                direction = Direction.RIGHT

            if direction:
                # Αποθήκευση direction (χρησιμοποιείται στο sprite)
                self.player.direction = direction

                # Grid-based μετακίνηση
                # Κλάση: GridMovementSystem
                if self.movement.try_move(self.player, direction, self.level):
                    # Αλληλεπίδραση με tile (DIRT -> TUNNEL κ.λπ.)
                    # Κλάση: TileInteractionSystem
                    self.tile_interaction.on_enter(self.player, self.level)

                    # Έλεγχος για emerald pickup και scoring
                    # Κλάση: ScoreSystem
                    self.score_system.on_player_enter(self.player, self.level)

                    # Θέτουμε cooldown κίνησης
                    self._move_cooldown = 0.12

        # ==================================================
        # PLAYER 2 EMERALD PICKUP (ΧΩΡΙΣ TileInteraction)
        # ==================================================
        if self.player2:
            tx = self.player2.tile_x
            ty = self.player2.tile_y

            if self.level.get_tile(tx, ty) == TileType.EMERALD:
                self.level.set_tile(tx, ty, TileType.TUNNEL)
                self.score_p2.add_points(100)
                AudioManager.play_sound("menu_select")

        # ==================================================
        # PLAYER 1 FIRE WEAPON
        # ==================================================
        if self.player.alive and inp and inp.fire:

            before = len(self.bullets)

            # Δημιουργία bullet αν το weapon επιτρέπει fire
            # Κλάση: WeaponSystem
            self.weapon_system.try_fire(self.weapon, self.player, self.bullets)

            # Όλα τα νέα bullets ανήκουν στον Player 1
            for b in self.bullets[before:]:
                b.owner_id = "p1"

            if len(self.bullets) > before:
                AudioManager.play_sound("shot")

        # ==================================================
        # PLAYER 2 MOVEMENT & FIRE
        # ==================================================
        self._handle_player2_input(dt)

        # ==================================================
        # ENEMY SPAWN
        # ==================================================
        self._spawn_timer += dt

        if (
                len(self.enemies) < self.max_active
                and self._spawn_timer >= self.spawn_delay
        ):
            # Δημιουργία enemy μέσω EnemySpawner
            enemy = self.enemy_spawner.spawn()
            enemy.move_timer = 0.0

            self.enemies.append(enemy)
            self.spawned_total += 1
            self._spawn_timer = 0.0

        # ==================================================
        # ENEMY UPDATE
        # ==================================================
        for enemy in self.enemies:
            if not enemy.alive:
                continue

            # Εναλλαγή NOBBIN / HOBBIN
            # Κλάση: EnemyFormSystem
            self.enemy_form_system.update(enemy, dt)

            enemy.move_timer += dt

            if enemy.move_timer >= self.enemy_delay:
                # Επιλογή κοντινότερου ζωντανού παίκτη
                target_player = self._get_closest_player(enemy)

                if target_player:
                    # AI απόφαση κίνησης
                    # Κλάση: EnemyAISystem + EnemyBrain
                    self.enemy_ai.update(
                        enemies=[enemy],
                        player=target_player,
                        level=self.level,
                        movement_system=self.movement,
                        game_mode=self.game_mode,
                    )

                # Αν είναι Hobbin, σκάβει
                self.hobbin_digging.on_enter(enemy, self.level)

                enemy.move_timer = 0.0

        # ==================================================
        # BULLETS UPDATE
        # ==================================================
        kills = self.bullet_system.update(
            self.bullets,
            self.level,
            self.enemies,
            dt,
        )

        # ==================================================
        # BULLET KILLS -> SCORE
        # ==================================================
        for enemy, owner in kills:
            if owner == "p2":
                self.score_p2.add_points(250)
            else:
                self.score.add_points(250)

        # ==================================================
        # PLAYER 1 VS ENEMY
        # ==================================================
        if self.player.alive and self._invuln_timer <= 0.0:
            for enemy in self.enemies:
                if (
                        enemy.alive
                        and enemy.tile_x == self.player.tile_x
                        and enemy.tile_y == self.player.tile_y
                ):
                    self._handle_player_hit()
                    break

        # ==================================================
        # PLAYER 2 VS ENEMY
        # ==================================================
        if self.player2 and self.lives_p2.count > 0:
            for enemy in self.enemies:
                if (
                        enemy.alive
                        and enemy.tile_x == self.player2.tile_x
                        and enemy.tile_y == self.player2.tile_y
                ):
                    if not self.lives_p2.lose_life():
                        self.player2.alive = False
                    else:
                        self._respawn_player2()
                    break

        # ==================================================
        # GAME OVER CHECK
        # ==================================================
        if (
                not self.player.alive
                and (not self.player2 or not self.player2.alive)
                and self._invuln_timer <= 0.0
        ):
            self.sm.set_scene(
                "gameover",
                {
                    "score_p1": self.score.points,
                    "score_p2": self.score_p2.points
                }
            )
            return

        # ==================================================
        # ENEMY DEATH EXPLOSIONS
        # ==================================================
        alive_now = set(id(e) for e in self.enemies if e.alive)
        dead_ids = self._alive_enemy_ids_prev - alive_now

        if dead_ids:
            for e in self.enemies:
                if id(e) in dead_ids:
                    self.explosions.spawn(e.tile_x, e.tile_y)

        self._alive_enemy_ids_prev = alive_now

        # ==================================================
        # CLEANUP
        # ==================================================
        self.enemies = [e for e in self.enemies if e.alive]

        # Ενημέρωση gold sack physics
        # Κλάση: GoldBagSystem
        self.gold_bag_system.update(self.gold_bags, self.level, dt)

        # ==================================================
        # GOLD BAG INTERACTIONS
        # ==================================================
        for bag in self.gold_bags:
            if bag.collected:
                continue

            # Player 1 eats sack
            if not bag.is_gold and not bag.falling:
                if bag.tile_x == self.player.tile_x and bag.tile_y == self.player.tile_y:
                    bag.collected = True
                    self.level.set_tile(bag.tile_x, bag.tile_y, TileType.TUNNEL)
                    AudioManager.play_sound("menu_select")
                    continue

            # Player 2 eats sack
            if self.player2 and not bag.is_gold and not bag.falling:
                if bag.tile_x == self.player2.tile_x and bag.tile_y == self.player2.tile_y:
                    bag.collected = True
                    self.level.set_tile(bag.tile_x, bag.tile_y, TileType.TUNNEL)
                    AudioManager.play_sound("menu_select")
                    continue

            # Gold pile pickup
            if bag.is_gold:
                if bag.tile_x == self.player.tile_x and bag.tile_y == self.player.tile_y:
                    bag.collected = True
                    self.score_system.add_points(500)
                    AudioManager.play_sound("menu_select")
                    continue

            if self.player2 and bag.is_gold:
                if bag.tile_x == self.player2.tile_x and bag.tile_y == self.player2.tile_y:
                    bag.collected = True
                    self.score_p2.add_points(500)
                    AudioManager.play_sound("menu_select")
                    continue

            # Enemy interactions with gold
            for enemy in self.enemies:
                if not enemy.alive:
                    continue

                if bag.tile_x != enemy.tile_x:
                    continue

                if bag.falling:
                    y_min = min(bag.prev_tile_y, bag.tile_y)
                    y_max = max(bag.prev_tile_y, bag.tile_y)

                    if y_min <= enemy.tile_y <= y_max:
                        enemy.alive = False
                        self.explosions.spawn_world(
                            enemy.tile_x * self.TILE_SIZE,
                            enemy.tile_y * self.TILE_SIZE
                        )
                        self.score_system.add_points(250)
                        break

                elif bag.is_gold and bag.tile_y == enemy.tile_y:
                    bag.collected = True
                    break

        # ==================================================
        # CAMERA FOLLOW
        # ==================================================
        if self.camera_p1 and self.player.alive:
            self.camera_p1.follow(self.player)

        if self.player2 and self.player2.alive and self.camera_p2:
            self.camera_p2.follow(self.player2)

        # ==================================================
        # PARTICLES UPDATE
        # ==================================================
        self.explosions.update(dt)

    # ==================================================
    # Render
    # ==================================================

    def render(self, surface):
        # ==================================================
        # ΜΕΘΟΔΟΣ RENDER ΤΗΣ GameScene
        #
        # Καλείται σε κάθε frame μετά το update().
        # Αναλαμβάνει ΑΠΟΚΛΕΙΣΤΙΚΑ τη σχεδίαση (ΟΧΙ λογική).
        # ==================================================

        # Διαστάσεις παραθύρου
        w, h = surface.get_size()

        # ==================================================
        # SINGLE PLAYER MODE
        # Αν ΔΕΝ υπάρχει Player 2, ζωγραφίζουμε κανονικά
        # σε ολόκληρη την οθόνη.
        # ==================================================
        if not self.player2:

            # Καθαρίζουμε την οθόνη με μαύρο χρώμα
            surface.fill((0, 0, 0))

            # Σχεδίαση tilemap (χώμα, tunnels κ.λπ.)
            # Κλάση: TilemapView
            self.tilemap_view.render(surface, self.level, self.camera_p1)

            # ==================================================
            # PLAYER 1
            # ==================================================

            draw_player = True

            # Αν ο παίκτης είναι invulnerable,
            # εφαρμόζουμε blinking effect
            if self._invuln_timer > 0.0 and int(self._invuln_timer * 18) % 2 == 0:
                draw_player = False

            if draw_player:
                # Μετατροπή tile συντεταγμένων σε world pixels
                px = self.player.tile_x * self.TILE_SIZE
                py = self.player.tile_y * self.TILE_SIZE

                # Μετατροπή world -> screen μέσω camera
                sx, sy = self.camera_p1.world_to_screen(px, py)

                # Σχεδίαση sprite παίκτη
                # Κλάση: PlayerSprite
                self.player_sprite.draw(surface, sx, sy, self.player.direction)

            # ==================================================
            # ENEMIES
            # ==================================================
            for enemy in self.enemies:
                ex = enemy.tile_x * self.TILE_SIZE
                ey = enemy.tile_y * self.TILE_SIZE
                sx, sy = self.camera.world_to_screen(ex, ey)

                # Σχεδίαση enemy sprite
                # Κλάση: EnemySprite
                self.enemy_sprite.draw(surface, enemy, sx, sy)

            # ==================================================
            # EMERALDS
            # ==================================================
            # Διατρέχουμε ΟΛΟ το grid και ζωγραφίζουμε
            # όσα tiles είναι EMERALD
            for y, row in enumerate(self.level.tiles):
                for x, tile in enumerate(row):
                    if tile == TileType.EMERALD:
                        wx = x * self.TILE_SIZE
                        wy = y * self.TILE_SIZE
                        sx, sy = self.camera.world_to_screen(wx, wy)

                        # Κλάση: EmeraldSprite
                        self.emerald_sprite.draw(surface, sx, sy)

            # ==================================================
            # GOLD BAGS / GOLD PILES
            # ==================================================
            for bag in self.gold_bags:
                if bag.collected:
                    continue

                gx = bag.tile_x * self.TILE_SIZE
                gy = bag.tile_y * self.TILE_SIZE
                sx, sy = self.camera.world_to_screen(gx, gy)

                # Κλάση: GoldBagSprite
                self.gold_bag_sprite.draw(surface, bag, sx, sy)

            # ==================================================
            # BULLETS
            # ==================================================
            # Τα bullets σχεδιάζονται απλά ως λευκά τετράγωνα
            for b in self.bullets:
                bx = b.tile_x * self.TILE_SIZE
                by = b.tile_y * self.TILE_SIZE
                sx, sy = self.camera.world_to_screen(bx, by)

                pygame.draw.rect(
                    surface,
                    (255, 255, 255),
                    pygame.Rect(sx + 12, sy + 12, 8, 8)
                )

            # ==================================================
            # EXPLOSIONS (particles)
            # ==================================================
            # Κλάση: ExplosionSystem
            self.explosions.draw(surface, self.camera_p1)

            # ==================================================
            # HUD (Score, Lives, Level)
            # ==================================================

            hud = f"SCORE: {self.score.points}   LIVES: {self.lives.count}"
            hud_surf = self._font.render(hud, True, (255, 255, 255))
            surface.blit(hud_surf, (16, 12))

            level_surf = self._font.render(
                f"LEVEL: {self.level_index}", True, (255, 255, 255)
            )
            surface.blit(
                level_surf,
                (w // 2 - level_surf.get_width() // 2, 12)
            )

            # Τερματίζουμε εδώ, ΔΕΝ πάμε σε split screen
            return

        # ==================================================
        # SPLIT SCREEN MODE – 2 PLAYERS
        # ==================================================

        half_w = w // 2

        # ==================================================
        # LEFT VIEW – PLAYER 1
        # ==================================================
        left_surface = surface.subsurface((0, 0, half_w, h))
        self._render_view(left_surface, self.camera_p1, self.player)

        # ==================================================
        # RIGHT VIEW – PLAYER 2
        # ==================================================
        right_surface = surface.subsurface((half_w, 0, half_w, h))
        self._render_view(right_surface, self.camera_p2, self.player2)

        # ==================================================
        # DIVIDER LINE
        # ==================================================
        pygame.draw.line(
            surface,
            (70, 70, 70),
            (half_w, 0),
            (half_w, h),
            2
        )

        # ==================================================
        # HUD PLAYER 1
        # ==================================================
        hud_p1 = f"P1  SCORE: {self.score.points}   LIVES: {self.lives.count}"
        hud_p1_surf = self._font.render(hud_p1, True, (255, 255, 255))
        surface.blit(hud_p1_surf, (16, 12))

        # ==================================================
        # HUD PLAYER 2
        # ==================================================
        hud_p2 = f"P2  SCORE: {self.score_p2.points}   LIVES: {self.lives_p2.count}"
        hud_p2_surf = self._font.render(hud_p2, True, (255, 255, 255))
        surface.blit(
            hud_p2_surf,
            (w - hud_p2_surf.get_width() - 16, 12)
        )

        # ==================================================
        # LEVEL (κεντρικά)
        # ==================================================
        level_surf = self._font.render(
            f"LEVEL: {self.level_index}", True, (255, 255, 255)
        )
        surface.blit(
            level_surf,
            (w // 2 - level_surf.get_width() // 2, 12)
        )






