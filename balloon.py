import pygame
import numpy as np
from random import random

class Balloon:
    def __init__(self, speed=100, size=(800, 600)) -> None:
        
        self.image = pygame.image.load('assets/balloon-red.png').convert_alpha()
        scale = random() * (0.7 - 1) + 0.7
        self.image = pygame.transform.scale(self.image, scale * np.array(self.image.get_size()))
        
        self.rect = self.image.get_rect()
        
        self.speed = speed
        self.y = size[1]
        self.x = np.random.randint(0, size[0] - self.rect.width)
        
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, window):
        window.blit(self.image, self.rect)
        
    def draw_rect(self, window):
        pygame.draw.rect(window, (255, 0, 0), self.rect, 2)
        
    def update(self, dtime):
        self.y -= self.speed * dtime
        self.rect.y = self.y
