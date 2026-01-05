import pygame
from shared.services.input import InputSnapshot


class InputManager:
    """
    Η κλάση InputManager είναι υπεύθυνη για:
    - τη συλλογή των γεγονότων (events) από το pygame
    - τη μετατροπή τους σε μία ενιαία κατάσταση εισόδου (InputSnapshot)

    Ουσιαστικά λειτουργεί ως "μεταφραστής" μεταξύ:
    pygame events → λογική εισόδου του παιχνιδιού
    """

    def __init__(self) -> None:
        # Δημιουργούμε ένα αντικείμενο InputSnapshot
        # Το snapshot αυτό θα ενημερώνεται συνεχώς
        # και θα επιστρέφεται σε κάθε frame
        self._snapshot = InputSnapshot()

    def process_events(self) -> InputSnapshot:
        """
        Επεξεργάζεται όλα τα pygame events του τρέχοντος frame
        και ενημερώνει το InputSnapshot.

        Επιστρέφει:
        - ένα InputSnapshot που περιγράφει
          ποια πλήκτρα είναι πατημένα αυτή τη στιγμή
        """

        # Διατρέχουμε όλα τα γεγονότα που έχει συλλέξει το pygame
        for event in pygame.event.get():

            # Αν ο χρήστης πατήσει το Χ του παραθύρου
            # τερματίζουμε άμεσα την εφαρμογή
            if event.type == pygame.QUIT:
                raise SystemExit

            # =========================
            # ΠΑΤΗΜΑ ΠΛΗΚΤΡΟΥ
            # =========================
            if event.type == pygame.KEYDOWN:

                # Πάνω βέλος → κίνηση προς τα πάνω
                if event.key == pygame.K_UP:
                    self._snapshot.up = True

                # Κάτω βέλος → κίνηση προς τα κάτω
                elif event.key == pygame.K_DOWN:
                    self._snapshot.down = True

                # Αριστερό βέλος → κίνηση αριστερά
                elif event.key == pygame.K_LEFT:
                    self._snapshot.left = True

                # Δεξί βέλος → κίνηση δεξιά
                elif event.key == pygame.K_RIGHT:
                    self._snapshot.right = True

                # Escape → pause / επιστροφή σε menu
                elif event.key == pygame.K_ESCAPE:
                    self._snapshot.pause = True

                # Space → πυροβολισμός (fire)
                elif event.key == pygame.K_SPACE:
                    self._snapshot.fire = True   # FIRE DOWN

            # =========================
            # ΑΦΗΝΩ ΠΛΗΚΤΡΟ
            # =========================
            elif event.type == pygame.KEYUP:

                # Αφήνουμε το πάνω βέλος
                if event.key == pygame.K_UP:
                    self._snapshot.up = False

                # Αφήνουμε το κάτω βέλος
                elif event.key == pygame.K_DOWN:
                    self._snapshot.down = False

                # Αφήνουμε το αριστερό βέλος
                elif event.key == pygame.K_LEFT:
                    self._snapshot.left = False

                # Αφήνουμε το δεξί βέλος
                elif event.key == pygame.K_RIGHT:
                    self._snapshot.right = False

                # Αφήνουμε το Escape
                elif event.key == pygame.K_ESCAPE:
                    self._snapshot.pause = False

                # Αφήνουμε το Space
                elif event.key == pygame.K_SPACE:
                    self._snapshot.fire = False  # FIRE UP

        # Επιστρέφουμε το ενημερωμένο snapshot
        # Το ίδιο αντικείμενο χρησιμοποιείται σε όλο το frame
        return self._snapshot
