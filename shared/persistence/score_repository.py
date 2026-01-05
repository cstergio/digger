import sqlite3
import os
from datetime import datetime
# sqlite3: ενσωματωμένη βιβλιοθήκη της Python για βάσεις δεδομένων SQLite
# os: για ασφαλή χειρισμό διαδρομών αρχείων
# datetime: για καταγραφή ημερομηνίας και ώρας επίτευξης score


class ScoreRepository:
    """
    Η κλάση ScoreRepository είναι υπεύθυνη για την αποθήκευση
    και ανάκτηση των scores του παιχνιδιού.

    Αποτελεί το επίπεδο πρόσβασης δεδομένων (Data Access Layer)
    και απομονώνει πλήρως τη λογική της βάσης δεδομένων
    από το υπόλοιπο παιχνίδι.
    """

    def __init__(self):
        """
        Constructor της κλάσης.

        Δημιουργεί ή ανοίγει τη βάση δεδομένων scores.db
        και εξασφαλίζει ότι ο πίνακας scores υπάρχει.
        """

        # Εντοπίζουμε τον φάκελο στον οποίο βρίσκεται το αρχείο αυτό
        base_dir = os.path.dirname(__file__)

        # Δημιουργούμε τη διαδρομή προς το αρχείο της βάσης
        db_path = os.path.join(base_dir, "scores.db")

        # Δημιουργούμε σύνδεση με τη βάση δεδομένων SQLite
        self.conn = sqlite3.connect(db_path)

        # Δημιουργούμε τον πίνακα αν δεν υπάρχει
        self._create_table()

    def _create_table(self):
        """
        Δημιουργεί τον πίνακα scores στη βάση δεδομένων,
        αν αυτός δεν υπάρχει ήδη.
        """

        # Δημιουργούμε cursor για εκτέλεση SQL εντολών
        cur = self.conn.cursor()

        # SQL εντολή δημιουργίας πίνακα
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                score INTEGER,
                date TEXT,
                time TEXT
            )
        """)

        # Επιβεβαιώνουμε τις αλλαγές στη βάση
        self.conn.commit()

    def _next_game_name(self) -> str:
        """
        Δημιουργεί αυτόματα όνομα παιχνιδιού τύπου:
        GAME01, GAME02, GAME03, ...

        Το όνομα βασίζεται στο πλήθος των ήδη αποθηκευμένων scores.
        """

        cur = self.conn.cursor()

        # Μετράμε πόσες εγγραφές υπάρχουν ήδη
        cur.execute("SELECT COUNT(*) FROM scores")
        count = cur.fetchone()[0] + 1

        # Επιστρέφουμε το όνομα σε μορφή GAME##
        return f"GAME{count:02d}"

    def add_score(self, score: int):
        """
        Αποθηκεύει ένα νέο score στη βάση δεδομένων.

        score:
        το τελικό σκορ του παιχνιδιού
        """

        # Παίρνουμε την τρέχουσα ημερομηνία και ώρα
        now = datetime.now()

        # Δημιουργούμε αυτόματο όνομα παιχνιδιού
        name = self._next_game_name()

        cur = self.conn.cursor()

        # Εισάγουμε νέα εγγραφή στον πίνακα scores
        cur.execute(
            "INSERT INTO scores (name, score, date, time) VALUES (?, ?, ?, ?)",
            (
                name,
                score,
                now.strftime("%d/%m/%Y"),
                now.strftime("%H:%M"),
            )
        )

        # Επιβεβαιώνουμε την εισαγωγή
        self.conn.commit()

    def top_10(self):
        """
        Επιστρέφει τα 10 καλύτερα scores
        ταξινομημένα κατά φθίνουσα σειρά σκορ.
        """

        cur = self.conn.cursor()

        # SQL ερώτημα για τα κορυφαία 10 scores
        cur.execute("""
            SELECT name, date, time, score
            FROM scores
            ORDER BY score DESC
            LIMIT 10
        """)

        # Επιστρέφουμε όλα τα αποτελέσματα
        return cur.fetchall()
