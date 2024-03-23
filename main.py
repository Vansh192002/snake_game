import pygame
from pygame.locals import *
import time
import random

size = 40

class Apple:
    def __init__(self,parent_screen):
        self.image = pygame.image.load("resources/apple.jpg")
        self.parent_screen = parent_screen
        self.x = size * 3
        self.y = size * 3
    
    def draw(self):
        self.parent_screen.blit(self.image,(self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,23) * 40
        self.y = random.randint(1,18) * 40
class Snake:
    def __init__(self,parent_screen,length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [size]*length
        self.y = [size]*length
        self.direction = 'down'

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i], self.y[i]))
        pygame.display.flip()
    
    

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'
    
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Classic Snake Game")
        pygame.mixer.init()
        self.background_music()
        self.surface = pygame.display.set_mode((1000,800))
        self.render_background()
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        
        line1 = font.render(f"Your Score:{self.snake.length}", True ,(200,200,200))
        self.surface.blit(line1,(200,300))
        line2 = font.render("GAME OVER, press ENTER to play again. press ESCAPE to exit", True , (200, 200, 200))
        self.surface.blit(line2,(100,600))
        pygame.display.flip()

        pygame.mixer.music.pause()
        
    def background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score:{self.snake.length}", True ,(200,200,200))
        self.surface.blit(score, (800, 10))

    def is_collison(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 <= x2 + size:
            if y1 >= y2 and y1 <= y2 + size:
                return True
       
        return False

    def out_bounds(self,x1,y1):
        if x1 >= 1000 or x1 < 0 or y1 >= 800 or y1 < 0:
            return True
        return False
    
    def play(self):
         self.render_background()
         self.snake.walk()
         self.apple.draw()
         self.display_score()
         pygame.display.flip()

         #snake colliding with apple
         if self.is_collison(self.snake.x[0],self.snake.y[0], self.apple.x, self.apple.y):
             sound = pygame.mixer.Sound("resources/ding.mp3")
             pygame.mixer.Sound.play(sound)
             self.snake.increase_length()
             self.apple.move()

        #snake colliding with self
         for i in range(3, self.snake.length):
             if self.is_collison(self.snake.x[0], self.snake.y[0],self.snake.x[i], self.snake.y[i]):
                 sound = pygame.mixer.Sound("resources/crash.mp3")
                 pygame.mixer.Sound.play(sound)
                 raise "Game over"
         if self.out_bounds(self.snake.x[0],self.snake.y[0]):
                 sound = pygame.mixer.Sound("resources/crash.mp3")
                 pygame.mixer.Sound.play(sound)
                 raise "Game over"  

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        self.snake.length = 1
                        self.snake.x = [size]
                        self.snake.y = [size]
                        self.snake.direction = 'down'
                        pause = False

                    if event.key == K_UP:    
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()


                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                    
            
            time.sleep(0.15)
   

if __name__ == "__main__":
    game = Game()
    game.run()


