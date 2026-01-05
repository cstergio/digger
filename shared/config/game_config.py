from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    """
    Κλάση ρυθμίσεων (configuration) του παιχνιδιού.

    Περιέχει βασικές παραμέτρους που αφορούν:
    - το παράθυρο (ανάλυση)
    - το ρυθμό ανανέωσης (FPS)
    - τον τίτλο του παιχνιδιού

    Χρησιμοποιείται κυρίως κατά την αρχικοποίηση της εφαρμογής (GameApp).
    """

    # Πλάτος παραθύρου σε pixels
    screen_width: int = 1280

    # Ύψος παραθύρου σε pixels
    screen_height: int = 720

    # Frames Per Second (FPS)
    # Καθορίζει πόσες φορές το παιχνίδι ενημερώνεται και σχεδιάζεται ανά δευτερόλεπτο
    fps: int = 60

    # Τίτλος παραθύρου εφαρμογής
    title: str = "Digger (Beta Version)"

    @staticmethod
    def default() -> "GameConfig":
        """
        Στατική μέθοδος που επιστρέφει ένα αντικείμενο GameConfig
        με τις προεπιλεγμένες (default) ρυθμίσεις.

        Χρησιμοποιείται για:
        - καθαρή αρχικοποίηση
        - αποφυγή hard-coded τιμών μέσα στον κώδικα
        """
        return GameConfig()
