import pygame
import os

class PlayerSprite:
    FRAME_SIZE = 32
    ANIM_SPEED = 0.12  # seconds per frame

    def __init__(self):
        base_dir = os.path.dirname(__file__)
        sprite_path = os.path.join(
            base_dir, "..", "..", "assets", "sprites", "digger_player.png"
        )

        sheet = pygame.image.load(sprite_path).convert_alpha()

        self.frames = []
        for i in range(4):
            frame = sheet.subsurface(
                pygame.Rect(i * 32, 0, 32, 32)
            )
            self.frames.append(frame)

        self.frame_index = 0
        self.timer = 0.0

    def update(self, dt, moving: bool):
        if not moving:
            self.frame_index = 0
            self.timer = 0.0
            return

        self.timer += dt
        if self.timer >= self.ANIM_SPEED:
            self.timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, surface, x, y):
        surface.blit(self.frames[self.frame_index], (x, y))
