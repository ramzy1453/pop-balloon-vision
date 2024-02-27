import pygame
import numpy as np
import cv2 as cv
from time import time
from balloon import Balloon
from hand_detector import HandDetector

class Game:
    def __init__(self, size=(800, 600), title=None, fps=60) -> None:
        # Initialize
        pygame.init()
        
        self.size = size

        # Webcam
        self.camera = cv.VideoCapture(0)
        
        self.camera.set(3, int(size[0])) 
        self.camera.set(4, int(size[1])) 

        # Create Window/Display
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        
        # Load icon
        icon = pygame.image.load('assets/icon.png').convert()
        pygame.display.set_icon(icon)
        
        # Initialize Clock for FPS
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.dtime = 1000 / self.fps
        self.frame_count = 0
        
        self.score = 0
        self.startTime = time()
        self.totalTime = 120
        
        # Main loop
        self.run = True
        
        # Balloons
        self.balloons = []
        
        # Detector integration
        self.detector = HandDetector(max_hands=1)
        
        # Speed of balloons
        self.speed = 1
        self.acceleration = 0.01
        
        
        
        
    def quit(self):
        self.run = False
        pygame.quit()
        
    def mainloop(self):
        while self.run:
            self.game_logic()
            
            # Update Display
            pygame.display.update()
                
            # Set FPS
            self.frame_count += 1
            
            self.clock.tick(self.fps)
            
        
    def events_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
        
        
    def game_logic(self):
        # Get Events
        self.events_handler()
        
        self.do_each(0.6, self.pop_ballon)
        
        # Apply logic
        self.timeRemain = int(self.totalTime - (time() - self.startTime))
        
        
        success, frame = self.camera.read()
        hands, frame = self.detector.find_hands(frame, draw=True)
        
        # img_rgb = pygame.transform.flip(img_rgb, True, False)
        

        
        if len(hands) != 0:
            fingers = hands[0]['landmarks_list']
            x, y = fingers[8]
            cv.circle(frame, (x, y), 13, (0, 255, 0), cv.FILLED)
            cv.circle(frame, (x, y), 10, (255, 255, 255), cv.FILLED)
            
            x = self.size[0] - x
            y = self.size[1] - y
            
            self.check_collision(x, y)
           
        img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_rgb = np.rot90(img_rgb)
        img_rgb = pygame.surfarray.make_surface(img_rgb).convert()
        self.window.blit(img_rgb, (0, 0))


        self.update_and_draw_ballons()
        self.draw_score()
        
    def pop_ballon(self):
        ballon = Balloon(speed=self.speed, size=self.size)
        self.balloons.append(ballon)
        # Speed updating
        self.speed += self.acceleration

        
    def update_and_draw_ballons(self):
        for ballon in self.balloons:
            ballon.update(self.dtime)
            ballon.draw(self.window)
            
            if ballon.y < -2*ballon.rect.height:
                self.balloons.remove(ballon)
    
    def check_collision(self, x, y):
            for ballon in self.balloons:
                if ballon.rect.collidepoint(x, y):
                    self.score += 10
                    self.balloons.remove(ballon)
                    
                    
    def do_each(self, seconds, callback, *args, **kwargs):
        if self.frame_count % (self.fps * seconds) == 0:
            callback(*args, **kwargs)
            

    def draw_score(self):
        font = pygame.font.Font(None, 50)
        textScore = font.render(f'Score: {self.score}', True, (50, 50, 255))
        textTime = font.render(f'Time: {self.timeRemain}', True, (50, 50, 255))
        self.window.blit(textScore, (35, 35))
        self.window.blit(textTime, (1000, 35))
        if self.timeRemain <0:
            self.window.fill((255,255,255))
            textScore = font.render(f'Your Score: {self.score}', True, (50, 50, 255))
            textTime = font.render(f'Time UP', True, (50, 50, 255))
            self.window.blit(textScore, (450, 350))
            self.window.blit(textTime, (530, 275))
            

