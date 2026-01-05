class InputSnapshot:
    """
    Η κλάση InputSnapshot αναπαριστά ένα στιγμιότυπο (snapshot)
    της εισόδου του παίκτη για ένα και μόνο frame του παιχνιδιού.

    Δημιουργείται από το σύστημα εισόδου (InputController)
    και περνά αυτούσια στις σκηνές (Scenes), ώστε:
    - οι σκηνές να μην διαβάζουν απευθείας το πληκτρολόγιο
    - να υπάρχει καθαρός διαχωρισμός input και game logic

    Το "Immutable-ish" σημαίνει ότι, παρότι τεχνικά τα πεδία
    μπορούν να αλλάξουν, στη φιλοσοφία του παιχνιδιού
    αντιμετωπίζεται ως αμετάβλητο αντικείμενο.
    """

    def __init__(
        self,
        up=False,
        down=False,
        left=False,
        right=False,
        fire=False,
        pause=False,
        backspace=False,
        text="",
    ):
        """
        Constructor της κλάσης InputSnapshot.

        Κάθε παράμετρος αντιστοιχεί σε μία συγκεκριμένη
        ενέργεια του παίκτη στο τρέχον frame.

        Όλες έχουν default τιμή, ώστε να μπορεί να δημιουργηθεί
        snapshot ακόμα και χωρίς καμία ενεργή είσοδο.
        """

        # True αν στο συγκεκριμένο frame πατήθηκε το πλήκτρο "πάνω"
        self.up = up

        # True αν στο συγκεκριμένο frame πατήθηκε το πλήκτρο "κάτω"
        self.down = down

        # True αν στο συγκεκριμένο frame πατήθηκε το πλήκτρο "αριστερά"
        self.left = left

        # True αν στο συγκεκριμένο frame πατήθηκε το πλήκτρο "δεξιά"
        self.right = right

        # True αν στο συγκεκριμένο frame πατήθηκε το πλήκτρο fire
        # (π.χ. SPACE για πυροβολισμό)
        self.fire = fire

        # True αν πατήθηκε το πλήκτρο pause
        # (π.χ. ESC για επιστροφή στο μενού)
        self.pause = pause

        # True αν πατήθηκε backspace
        # Χρησιμοποιείται κυρίως σε σκηνές εισαγωγής κειμένου
        self.backspace = backspace

        # Κείμενο που πληκτρολογήθηκε στο frame
        # Χρησιμοποιείται για:
        # - εισαγωγή ονόματος
        # - ρυθμίσεις
        # - high scores
        self.text = text
