import random
import pygame


class ExplosionSystem:
    """
    Σύστημα διαχείρισης εκρήξεων τύπου particle.

    Χαρακτηριστικά:
    - Δεν χρησιμοποιεί sprites ή εικόνες
    - Κάθε έκρηξη αποτελείται από πολλά μικρά particles
    - Τα particles έχουν φυσική συμπεριφορά (ταχύτητα, βαρύτητα, τριβή)
    - Το σύστημα είναι ανεξάρτητο από το gameplay

    Παρέχει τρεις βασικές λειτουργίες:
    - spawn / spawn_world : δημιουργία έκρηξης
    - update              : ενημέρωση φυσικής
    - draw                : σχεδίαση στην οθόνη
    """

    def __init__(self, tile_size: int = 32):
        # Μέγεθος πλακιδίου (tile) σε pixels
        # Χρησιμοποιείται για μετατροπή από tile coordinates σε world coordinates
        self.tile_size = tile_size

        # Λίστα particles
        # Κάθε particle αποθηκεύεται ως dictionary με φυσικές ιδιότητες
        self._particles = []

    def spawn(self, tile_x: int, tile_y: int, intensity: int = 18):
        """
        Δημιουργεί έκρηξη χρησιμοποιώντας συντεταγμένες πλακιδίων (tile coordinates).

        Χρησιμοποιείται κυρίως από το GameScene, το οποίο δουλεύει σε tile επίπεδο.
        Η μέθοδος αυτή μετατρέπει tiles → world pixels και καλεί τη spawn_world.
        """

        # Μετατροπή από tile coordinates σε world pixel coordinates
        world_x = tile_x * self.tile_size
        world_y = tile_y * self.tile_size

        # Δημιουργία έκρηξης σε world χώρο
        self.spawn_world(world_x, world_y, intensity)

    def spawn_world(self, world_x_px: float, world_y_px: float, intensity: int = 18):
        """
        Δημιουργεί έκρηξη με βάση συντεταγμένες world (σε pixels).

        world_x_px, world_y_px : επάνω αριστερή γωνία tile σε pixels
        intensity              : πόσα particles θα δημιουργηθούν
        """

        # Υπολογισμός κέντρου του tile
        # Η έκρηξη φαίνεται πιο φυσική όταν ξεκινά από το κέντρο
        cx = world_x_px + self.tile_size / 2
        cy = world_y_px + self.tile_size / 2

        # Δημιουργία πολλών particles
        for _ in range(intensity):

            # Τυχαία γωνία εκτόξευσης (0 έως 2π)
            angle = random.uniform(0.0, 6.28318)

            # Τυχαία αρχική ταχύτητα
            speed = random.uniform(90.0, 240.0)

            # Υπολογισμός διανύσματος ταχύτητας με περιστροφή
            vx = (
                speed
                * random.uniform(0.6, 1.0)
                * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            )
            vy = (
                speed
                * random.uniform(0.6, 1.0)
                * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            )

            # Δημιουργία particle ως dictionary
            self._particles.append({
                # Θέση (με μικρή τυχαιότητα)
                "x": cx + random.uniform(-3, 3),
                "y": cy + random.uniform(-3, 3),

                # Ταχύτητα
                "vx": vx,
                "vy": vy,

                # Συνολικός χρόνος ζωής
                "life": random.uniform(0.25, 0.55),

                # Χρόνος που έχει περάσει
                "ttl": 0.0,

                # Ακτίνα particle (pixels)
                "r": random.randint(2, 4),

                # Τύπος particle (οπτική διαφοροποίηση)
                "kind": random.choice(["spark", "dust"]),
            })

    def update(self, dt: float):
        """
        Ενημέρωση φυσικής των particles.

        dt : χρόνος που πέρασε από το προηγούμενο frame (σε δευτερόλεπτα)
        """

        # Συντελεστής "βαρύτητας"
        g = 420.0

        # Λίστα για τα ζωντανά particles
        alive = []

        for p in self._particles:
            # Αύξηση χρόνου ζωής
            p["ttl"] += dt

            # Αν το particle έχει ξεπεράσει τον χρόνο ζωής του, απορρίπτεται
            if p["ttl"] >= p["life"]:
                continue

            # Εφαρμογή βαρύτητας στην κατακόρυφη ταχύτητα
            p["vy"] += g * dt

            # Ενημέρωση θέσης
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt

            # Μικρή τριβή (drag) για πιο φυσική κίνηση
            p["vx"] *= (1.0 - 1.6 * dt)
            p["vy"] *= (1.0 - 1.2 * dt)

            # Το particle παραμένει ενεργό
            alive.append(p)

        # Αντικατάσταση λίστας με μόνο τα ζωντανά particles
        self._particles = alive

    def draw(self, surface, camera):
        """
        Σχεδιάζει όλα τα ενεργά particles στην οθόνη.

        surface : επιφάνεια pygame (συνήθως η οθόνη)
        camera  : Camera2D για μετατροπή world → screen
        """

        # Κάθε particle σχεδιάζεται σε μικρή προσωρινή επιφάνεια
        # Αυτό επιτρέπει alpha blending χωρίς να επηρεάζει την κύρια οθόνη
        for p in self._particles:

            # Υπολογισμός ποσοστού ζωής (0.0 → 1.0)
            t = p["ttl"] / max(0.0001, p["life"])

            # Fade-out όσο πλησιάζει στο τέλος ζωής
            alpha = int(255 * (1.0 - t))
            if alpha <= 0:
                continue

            # Μετατροπή από world σε screen coordinates
            sx, sy = camera.world_to_screen(p["x"], p["y"])

            # Επιλογή χρώματος ανάλογα με τον τύπο particle
            if p["kind"] == "spark":
                color = (255, 210, 90)
            else:
                color = (180, 140, 90)

            r = p["r"]

            # Δημιουργία προσωρινής επιφάνειας με διαφάνεια
            tmp = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)

            # Σχεδίαση κύκλου με alpha
            pygame.draw.circle(
                tmp,
                (*color, alpha),
                (r + 1, r + 1),
                r
            )

            # Σχεδίαση του particle στην κύρια επιφάνεια
            surface.blit(tmp, (sx - r, sy - r))
