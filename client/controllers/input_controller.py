import pygame
from shared.services.input import InputSnapshot


class InputController:
    """
    Η κλάση InputController είναι υπεύθυνη για:
    - την ανάγνωση της τρέχουσας κατάστασης εισόδου από το pygame
    - τη δημιουργία και επιστροφή ενός InputSnapshot

    Σε αντίθεση με έναν event-based InputManager,
    εδώ χρησιμοποιούμε:
    - polling (pygame.key.get_pressed)
    - ελάχιστη χρήση events (TEXTINPUT, BACKSPACE, QUIT)

    Ο στόχος είναι κάθε frame να παράγεται
    ένα πλήρες και συνεπές snapshot εισόδου.
    """

    def capture(self) -> InputSnapshot:
        """
        Συλλέγει την είσοδο του χρήστη για το τρέχον frame
        και επιστρέφει ένα νέο InputSnapshot.

        Το snapshot αυτό:
        - χρησιμοποιείται από όλες τις σκηνές
        - είναι ανεξάρτητο από το pygame
        """

        # ---------------------------------------------
        # Μεταβλητές για εισαγωγή κειμένου (π.χ. ονόματα)
        # ---------------------------------------------
        text = ""          # χαρακτήρες που πληκτρολογήθηκαν στο frame
        backspace = False  # αν πατήθηκε backspace στο frame

        # ---------------------------------------------
        # Επεξεργασία pygame events
        # ---------------------------------------------
        # Εδώ ΔΕΝ χειριζόμαστε κίνηση.
        # Χρησιμοποιούμε events μόνο όπου χρειάζεται στιγμιακή πληροφορία.
        for event in pygame.event.get():

            # Αν ο χρήστης κλείσει το παράθυρο
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            # Εισαγωγή χαρακτήρων (unicode-safe)
            # Χρησιμοποιείται κυρίως σε input πεδία (π.χ. High Scores)
            if event.type == pygame.TEXTINPUT:
                text += event.text

            # Αν πατήθηκε backspace
            # Δεν χρησιμοποιούμε key.get_pressed εδώ,
            # γιατί μας ενδιαφέρει το στιγμιαίο πάτημα
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    backspace = True

        # ---------------------------------------------
        # Polling κατάστασης πληκτρολογίου
        # ---------------------------------------------
        # pygame.key.get_pressed επιστρέφει την τρέχουσα
        # κατάσταση όλων των πλήκτρων
        keys = pygame.key.get_pressed()

        # ---------------------------------------------
        # Δημιουργία και επιστροφή InputSnapshot
        # ---------------------------------------------
        return InputSnapshot(
            up=keys[pygame.K_UP],        # κίνηση προς τα πάνω
            down=keys[pygame.K_DOWN],    # κίνηση προς τα κάτω
            left=keys[pygame.K_LEFT],    # κίνηση αριστερά
            right=keys[pygame.K_RIGHT],  # κίνηση δεξιά
            fire=keys[pygame.K_SPACE],   # γενική χρήση: confirm / shoot
            pause=keys[pygame.K_ESCAPE], # pause ή επιστροφή
            backspace=backspace,         # διαγραφή χαρακτήρα
            text=text,                   # κείμενο που πληκτρολογήθηκε
        )
