class EnemyAISystem:
    """
    Το EnemyAISystem είναι το σύστημα τεχνητής νοημοσύνης των εχθρών.

    Ρόλος του:
    - Συντονίζει την απόφαση κίνησης των εχθρών
    - Χρησιμοποιεί ένα εξωτερικό αντικείμενο 'brain' για τη λήψη αποφάσεων
    - Εφαρμόζει την απόφαση μέσω του συστήματος κίνησης

    Σημαντικό:
    Το EnemyAISystem ΔΕΝ περιέχει τη λογική απόφασης.
    Αυτή βρίσκεται στο EnemyBrain (separation of concerns).
    """

    def __init__(self, brain):
        """
        Constructor του συστήματος AI.

        brain:
        Αντικείμενο τύπου EnemyBrain που γνωρίζει
        πώς να αποφασίζει κατεύθυνση κίνησης για έναν εχθρό.
        """

        # Αποθηκεύουμε το brain ώστε να το χρησιμοποιούμε σε κάθε update
        self.brain = brain

    def update(self, enemies, player, level, movement_system, game_mode):
        """
        Ενημερώνει την τεχνητή νοημοσύνη όλων των εχθρών.

        enemies          : λίστα από αντικείμενα Enemy
        player           : ο παίκτης-στόχος (ή ο κοντινότερος παίκτης)
        level            : το επίπεδο του παιχνιδιού
        movement_system  : σύστημα κίνησης (GridMovementSystem)
        game_mode        : τρέχουσα κατάσταση παιχνιδιού (π.χ. NORMAL, BONUS)
        """

        # Διατρέχουμε όλους τους εχθρούς
        for enemy in enemies:

            # Αν ο εχθρός δεν είναι ζωντανός,
            # τον αγνοούμε και περνάμε στον επόμενο
            if not enemy.alive:
                continue

            # Ζητάμε από το brain να αποφασίσει
            # προς ποια κατεύθυνση πρέπει να κινηθεί ο εχθρός
            direction = self.brain.decide(enemy, player, level, game_mode)

            # Αν το brain επέστρεψε έγκυρη κατεύθυνση
            if direction:
                # Προσπαθούμε να μετακινήσουμε τον εχθρό
                # σύμφωνα με τους κανόνες του grid και του επιπέδου
                movement_system.try_move(enemy, direction, level)
