#THIS IS SMALL CODE FOR THE KNIGHT THAT I BARELY UNDERSTAND
import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("images/knight2.png").convert_alpha()
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
        if self.lives > 2:
            self.lives -= 1
            print("Ouch!  You now have " + str(self.lives) + " lives.")
        elif self.lives == 2:
            self.lives -= 1
            print("You only have one life left!")
        elif self.lives == 1:
            self.lives -= 1

    def get_lives(self):
        return self.lives

    def set_lives(self, lives_count):
        self.lives = lives_count
