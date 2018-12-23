#THIS IS SMALL CODE FOR THE ENEMY THAT I BARELY UNDERSTAND
import pygame
class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("images/zombie1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += 5
        if self.rect.y >= 600:
            self.rect.y = 0

    def collision(self):
        self.rect.y = 0