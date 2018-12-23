#THIS IS SMALL CODE FOR THE WIZARD THAT I BARELY UNDERSTAND
import pygame

class wizard(pygame.sprite.Sprite):

    def __init__(self):
        super(wizard, self).__init__()
        self.image = pygame.image.load("images/wizard3..png").convert_alpha()
        self.rect = self.image.get_rect(center=(0, 600))
        self.lives = 3

    def update(self, direction):
        if direction == 1:
            self.rect.x -= 5
        elif direction == 0:
            self.rect.x += 5
        elif direction == 2:
            self.rect.y -= 5
        elif direction == 3:
            self.rect.y += 5
        elif direction == 4:
            self.rect.y += 3

    def subtract_lives(self):
        if self.lives > 0:
            self.lives -= 1

    def get_lives(self):
        return self.lives

    def set_lives(self, lives_count):
        self.lives = lives_count
