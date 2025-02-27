import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (10,255,10)

BLOCK_SIZE = 20
SPEED = 20
PENALTY = 2
SCORE = 1

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w//2, self.h//2)  # center of the screen
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self.poison = None
        self._place_food()
        self._place_poison()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _place_poison(self):
        size_multiple = 1 # block size bigger than 1
        b_size = BLOCK_SIZE * size_multiple 
        x = random.randint(0, (self.w-b_size )//b_size )*b_size
        y = random.randint(0, (self.h-b_size )//b_size )*b_size
        self.poison = Point(x, y)
        if self.poison in self.snake:
            self._place_poison()
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        

        # 4. place new food or just move
        if self.head == self.food:
            self.score += SCORE
            self._place_food()
        elif self.head == self.poison:
            self.score -= PENALTY
            self._place_poison()
            self.snake.pop()
            self.snake.pop()# shorten the body of the snake instead
        else:
            self.snake.pop() # removing the last in the snake list
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # snake too short
        if len(self.snake) == 0:
            game_over = True
        # score 0 game over
        if self.score < 0:
            game_over = True
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        # if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
        #     return True
        # crossing boudary
        # x
        if self.head.x > self.w - BLOCK_SIZE:
            self.head = Point(0 - BLOCK_SIZE, self.head.y)
        elif self.head.x < 0:
            self.head = Point(self.w, self.head.y)
        # y
        if self.head.y > self.h - BLOCK_SIZE:
            self.head = Point(self.head.x, 0 - BLOCK_SIZE)
        elif self.head.y < 0:
            self.head = Point(self.head.x, self.h)

        # hits itself
        if self.head in self.snake[1:]: # check except the first in the list because head always in the list
            return True
        
        return False


    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.poison.x, self.poison.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()