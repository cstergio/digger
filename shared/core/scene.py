from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Dict

from shared.services.input import InputSnapshot


class Scene(ABC):
    """
    Αφηρημένη βασική κλάση (Abstract Base Class) για όλες τις σκηνές του παιχνιδιού.

    Ορίζει το «συμβόλαιο» (contract) που ΠΡΕΠΕΙ να ακολουθεί κάθε σκηνή
    (π.χ. MainMenuScene, GameScene, GameOverScene).

    Με αυτόν τον τρόπο:
    - εξασφαλίζεται κοινή διεπαφή
    - το SceneManager μπορεί να διαχειρίζεται όλες τις σκηνές με τον ίδιο τρόπο
    """

    @abstractmethod
    def enter(self, payload: Optional[dict] = None) -> None:
        """
        Καλείται όταν η σκηνή γίνεται ενεργή.

        payload:
        - λεξικό με δεδομένα που μεταφέρονται από προηγούμενη σκηνή
        - π.χ. αριθμός παικτών, scores, ρυθμίσεις

        Κάθε σκηνή χρησιμοποιεί το payload όπως χρειάζεται.
        """
        ...

    @abstractmethod
    def exit(self) -> None:
        """
        Καλείται όταν η σκηνή απενεργοποιείται.

        Χρησιμοποιείται για:
        - καθαρισμό πόρων
        - reset timers
        - αποθήκευση κατάστασης αν χρειάζεται
        """
        ...

    @abstractmethod
    def handle_input(self, input_snapshot: InputSnapshot) -> None:
        """
        Παραλαμβάνει το στιγμιότυπο εισόδου (InputSnapshot) του τρέχοντος frame.

        Η σκηνή ΔΕΝ διαβάζει απευθείας πληκτρολόγιο input,
        αλλά βασίζεται σε αυτό το αντικείμενο.
        """
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Λογική ενημέρωσης της σκηνής.

        dt (delta time):
        - χρόνος σε δευτερόλεπτα από το προηγούμενο frame
        - χρησιμοποιείται για timers, κινήσεις, animations
        """
        ...

    @abstractmethod
    def render(self, surface) -> None:
        """
        Σχεδίαση (rendering) της σκηνής στην οθόνη.

        surface:
        - το pygame Surface της κύριας οθόνης
        """
        ...


class SceneManager:
    """
    Διαχειριστής σκηνών (Scene Manager).

    Είναι υπεύθυνος για:
    - καταχώριση σκηνών
    - εναλλαγή μεταξύ σκηνών
    - προώθηση input, update και render στην ενεργή σκηνή

    Αποτελεί κεντρικό κομμάτι της αρχιτεκτονικής του παιχνιδιού.
    """

    def __init__(self) -> None:
        # Λεξικό σκηνών: scene_id -> Scene instance
        self._scenes: Dict[str, Scene] = {}

        # Αναγνωριστικό τρέχουσας σκηνής (π.χ. "menu", "game")
        self._current_id: Optional[str] = None

        # Αντικείμενο της τρέχουσας σκηνής
        self._current_scene: Optional[Scene] = None

    def register_scene(self, scene_id: str, scene: Scene) -> None:
        """
        Καταχωρεί μία σκηνή στο σύστημα.

        scene_id:
        - μοναδικό string (π.χ. "menu", "gameover")

        scene:
        - αντικείμενο που υλοποιεί το Scene interface
        """
        if scene_id in self._scenes:
            # Απαγορεύεται διπλή καταχώριση με ίδιο id
            raise ValueError(f"Scene id already registered: {scene_id}")

        self._scenes[scene_id] = scene

    def set_scene(self, scene_id: str, payload: Optional[dict] = None) -> None:
        """
        Αλλάζει την ενεργή σκηνή.

        Βήματα:
        1. Καλεί exit() στην προηγούμενη σκηνή (αν υπάρχει)
        2. Ορίζει τη νέα σκηνή ως ενεργή
        3. Καλεί enter() στη νέα σκηνή με payload
        """
        if scene_id not in self._scenes:
            raise KeyError(f"Unknown scene id: {scene_id}")

        # Αν υπάρχει ενεργή σκηνή, την απενεργοποιούμε
        if self._current_scene is not None:
            self._current_scene.exit()

        # Ορισμός νέας σκηνής
        self._current_id = scene_id
        self._current_scene = self._scenes[scene_id]

        # Ενεργοποίηση νέας σκηνής
        self._current_scene.enter(payload or {})

    def handle_input(self, input_snapshot: InputSnapshot) -> None:
        """
        Προωθεί το input snapshot στην ενεργή σκηνή.
        """
        if self._current_scene is not None:
            self._current_scene.handle_input(input_snapshot)

    def update(self, dt: float) -> None:
        """
        Προωθεί το update (λογική) στην ενεργή σκηνή.
        """
        if self._current_scene is not None:
            self._current_scene.update(dt)

    def render(self, surface) -> None:
        """
        Προωθεί το render στην ενεργή σκηνή.
        """
        if self._current_scene is not None:
            self._current_scene.render(surface)

    @property
    def current_scene_id(self) -> Optional[str]:
        """
        Επιστρέφει το id της τρέχουσας σκηνής.

        Χρήσιμο για:
        - debugging
        - conditional λογική
        - overlays ή diagnostics
        """
        return self._current_id
