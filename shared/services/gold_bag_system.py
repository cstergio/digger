from shared.model.types import TileType
# Εισάγουμε το TileType enum, το οποίο ορίζει
# τα είδη πλακιδίων του επιπέδου (TUNNEL, GOLD_BAG κ.λπ.)


class GoldBagSystem:
    """
    Το GoldBagSystem είναι υπεύθυνο για τη συμπεριφορά των σακιών χρυσού.

    Συγκεκριμένα:
    - ελέγχει πότε ένα σακί πρέπει να αρχίσει να πέφτει
    - διαχειρίζεται την κίνηση κατά την πτώση
    - αποφασίζει πότε η πτώση σταματά
    - μετατρέπει το σακί σε χρυσό (gold pile) όταν ολοκληρωθεί η πτώση

    Το σύστημα αυτό υλοποιεί πιστά τη λογική του κλασικού παιχνιδιού Digger.
    """

    # Καθυστέρηση μεταξύ δύο διαδοχικών κινήσεων πτώσης
    # Έχει οριστεί ίδια με το tempo της grid-based κίνησης του παίκτη
    FALL_DELAY = 0.12

    def __init__(self):
        """
        Constructor της κλάσης.

        Δημιουργεί ένα λεξικό timers, ένα για κάθε σακί χρυσού,
        ώστε κάθε σακί να μπορεί να πέφτει ανεξάρτητα από τα υπόλοιπα.
        """

        # Λεξικό: bag_id -> χρονόμετρο πτώσης
        self._fall_timers = {}

    def update(self, gold_bags, level, dt):
        """
        Ενημερώνει την κατάσταση όλων των σακιών χρυσού.

        gold_bags : λίστα με αντικείμενα GoldBag
        level     : το επίπεδο του παιχνιδιού
        dt        : χρόνος που πέρασε από το προηγούμενο frame
        """

        # Εξετάζουμε κάθε σακί χρυσού ξεχωριστά
        for bag in gold_bags:

            # Αν το σακί έχει ήδη συλλεχθεί,
            # δεν το επεξεργαζόμαστε άλλο
            if bag.collected:
                continue

            bag_id = bag.id

            # Αν δεν υπάρχει timer για αυτό το σακί,
            # δημιουργούμε έναν νέο
            if bag_id not in self._fall_timers:
                self._fall_timers[bag_id] = 0.0

            # ==================================================
            # ΠΕΡΙΠΤΩΣΗ 1: ΤΟ ΣΑΚΙ ΠΕΦΤΕΙ
            # ==================================================
            if bag.falling:

                # Αυξάνουμε το χρονόμετρο πτώσης
                self._fall_timers[bag_id] += dt

                # Ελέγχουμε αν πέρασε ο απαιτούμενος χρόνος
                if self._fall_timers[bag_id] >= self.FALL_DELAY:

                    # Επαναφέρουμε το timer
                    self._fall_timers[bag_id] = 0.0

                    # Παίρνουμε το πλακίδιο ακριβώς από κάτω
                    below_tile = level.get_tile(
                        bag.tile_x,
                        bag.tile_y + 1
                    )

                    # ---------- Συνεχίζει να πέφτει ----------
                    if below_tile == TileType.TUNNEL:

                        # Καθαρίζουμε το τρέχον πλακίδιο
                        level.set_tile(
                            bag.tile_x,
                            bag.tile_y,
                            TileType.TUNNEL
                        )

                        # Αποθηκεύουμε την προηγούμενη y θέση
                        # (χρησιμοποιείται για συγκρούσεις με εχθρούς)
                        bag.prev_tile_y = bag.tile_y

                        # Μετακινούμε το σακί ένα πλακίδιο κάτω
                        bag.tile_y += 1

                        # Τοποθετούμε το σακί στη νέα θέση
                        level.set_tile(
                            bag.tile_x,
                            bag.tile_y,
                            TileType.GOLD_BAG
                        )

                    # ---------- Η πτώση σταματά ----------
                    else:
                        # Το σακί σταματά να πέφτει
                        bag.falling = False

                        # Μετατρέπεται σε gold pile
                        bag.is_gold = True

                        # Καθαρίζουμε το πλακίδιο
                        level.set_tile(
                            bag.tile_x,
                            bag.tile_y,
                            TileType.TUNNEL
                        )

                # Αφού επεξεργαστήκαμε την πτώση,
                # συνεχίζουμε στο επόμενο σακί
                continue

            # ==================================================
            # ΠΕΡΙΠΤΩΣΗ 2: ΕΝΑΡΞΗ ΠΤΩΣΗΣ
            # ==================================================
            below = level.get_tile(bag.tile_x, bag.tile_y + 1)

            # Αν κάτω υπάρχει τούνελ και το σακί
            # δεν έχει ήδη μετατραπεί σε χρυσό
            if below == TileType.TUNNEL and not bag.is_gold:

                # Ξεκινά η πτώση
                bag.falling = True

                # Αποθηκεύουμε την αρχική y θέση
                # (ΑΠΑΡΑΙΤΗΤΟ για έλεγχο συντριβής εχθρών)
                bag.prev_tile_y = bag.tile_y

                # Μηδενίζουμε το timer πτώσης
                self._fall_timers[bag_id] = 0.0
