import pygame
import os


class AudioManager:
    """
    Η κλάση AudioManager είναι υπεύθυνη για ΟΛΗ τη διαχείριση ήχου του παιχνιδιού.

    Συγκεκριμένα:
    - φορτώνει ηχητικά εφέ (sound effects)
    - αναπαράγει ήχους με βάση γεγονότα (menu, πυροβολισμοί, εκρήξεις)
    - διαχειρίζεται τη μουσική υποβάθρου
    - υποστηρίζει mute / unmute σε παγκόσμιο επίπεδο

    Η κλάση υλοποιείται ως utility class με classmethods,
    ώστε να χρησιμοποιείται από οπουδήποτε χωρίς instantiation.
    """

    # Κατάσταση σίγασης (mute) για ΟΛΟ το παιχνίδι
    _muted = False

    # Λεξικό που περιέχει όλα τα φορτωμένα ηχητικά εφέ
    _sounds = {}

    # Δείχνει αν η μουσική έχει ήδη φορτωθεί
    _music_loaded = False

    # Αποθηκεύει το path της τρέχουσας μουσικής
    # ώστε να επαναφορτωθεί σε περίπτωση unmute
    _current_music_path = None

    # Σταθερά έντασης μουσικής (χαμηλή ένταση)
    MUSIC_VOLUME = 0.12   # 12%

    @classmethod
    def init(cls):
        """
        Αρχικοποιεί το pygame mixer.

        Η μέθοδος ελέγχει πρώτα αν το mixer είναι ήδη ενεργό,
        ώστε να αποφευχθεί διπλή αρχικοποίηση που μπορεί να
        προκαλέσει σφάλματα ή παραμορφωμένο ήχο.
        """

        if not pygame.mixer.get_init():
            pygame.mixer.init()

    # ==================================================
    # Φόρτωση ήχων
    # ==================================================

    @classmethod
    def load_sounds(cls, base_path):
        """
        Φορτώνει όλα τα ηχητικά εφέ του παιχνιδιού.

        base_path:
        ο φάκελος όπου βρίσκονται τα αρχεία ήχου
        """

        # Ήχος πλοήγησης στο menu
        cls._sounds["menu_move"] = pygame.mixer.Sound(
            os.path.join(base_path, "menu_move.mp3")
        )

        # Ήχος επιλογής στο menu
        cls._sounds["menu_select"] = pygame.mixer.Sound(
            os.path.join(base_path, "menu_select.mp3")
        )

        # Ήχος πυροβολισμού
        cls._sounds["shot"] = pygame.mixer.Sound(
            os.path.join(base_path, "shot.ogg")
        )

        # Ήχος έκρηξης
        cls._sounds["explosion"] = pygame.mixer.Sound(
            os.path.join(base_path, "explosion.ogg")
        )

        # Σημείωση:
        # Εδώ μπορεί προαιρετικά να ρυθμιστεί ξεχωριστή ένταση
        # για κάθε ηχητικό εφέ, αν χρειαστεί.

    # ==================================================
    # Αναπαραγωγή ηχητικών εφέ
    # ==================================================

    @classmethod
    def play_sound(cls, name):
        """
        Αναπαράγει ένα ηχητικό εφέ.

        name:
        το όνομα του ήχου όπως είναι αποθηκευμένο στο λεξικό _sounds
        """

        # Αν το σύστημα είναι σε mute, δεν παίζεται κανένας ήχος
        if cls._muted:
            return

        # Ανακτούμε τον ήχο από το λεξικό
        sound = cls._sounds.get(name)

        # Αν ο ήχος υπάρχει, τον αναπαράγουμε
        if sound:
            sound.play()

    # ==================================================
    # Διαχείριση μουσικής
    # ==================================================

    @classmethod
    def play_music(cls, path, loop=True):
        """
        Φορτώνει και αναπαράγει μουσική υποβάθρου.

        path:
        το αρχείο μουσικής

        loop:
        αν True, η μουσική επαναλαμβάνεται συνεχώς
        """

        # Αποθηκεύουμε το path για πιθανό unmute
        cls._current_music_path = path

        # Αν είναι muted, δεν ξεκινάμε μουσική
        if cls._muted:
            return

        # Φορτώνουμε τη μουσική μόνο την πρώτη φορά
        if not cls._music_loaded:
            pygame.mixer.music.load(path)
            cls._music_loaded = True

        # Ορίζουμε ένταση μουσικής
        pygame.mixer.music.set_volume(cls.MUSIC_VOLUME)

        # Αναπαραγωγή με ή χωρίς loop
        pygame.mixer.music.play(-1 if loop else 0)

    @classmethod
    def stop_music(cls):
        """
        Σταματά άμεσα τη μουσική υποβάθρου.
        """

        pygame.mixer.music.stop()

    @classmethod
    def set_music_volume(cls, volume: float):
        """
        Ορίζει την ένταση της μουσικής.

        volume:
        τιμή από 0.0 έως 1.0
        """

        # Περιορίζουμε την τιμή στο αποδεκτό εύρος
        cls.MUSIC_VOLUME = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(cls.MUSIC_VOLUME)

    # ==================================================
    # Mute / Unmute
    # ==================================================

    @classmethod
    def mute_all(cls):
        """
        Θέτει το σύστημα σε κατάσταση mute.

        Σταματά αμέσως τη μουσική.
        """

        cls._muted = True
        pygame.mixer.music.stop()

    @classmethod
    def unmute_all(cls):
        """
        Επαναφέρει τον ήχο του παιχνιδιού.

        Αν υπήρχε μουσική πριν το mute,
        την επαναφορτώνει και την αναπαράγει ξανά.
        """

        cls._muted = False

        if cls._current_music_path:
            pygame.mixer.music.load(cls._current_music_path)
            pygame.mixer.music.set_volume(cls.MUSIC_VOLUME)
            pygame.mixer.music.play(-1)

    @classmethod
    def is_muted(cls) -> bool:
        """
        Επιστρέφει True αν το σύστημα ήχου είναι muted,
        αλλιώς False.
        """

        return cls._muted
