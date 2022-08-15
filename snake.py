# contains n blocks
# on each iteration remove last block add 1 front
class snake:
    def __init__(self, size, c_width, c_height):
        self.body = [(c_width/2, c_height/2)]
        self.size = size
        self.cw = c_width
        self.ch = c_height
        self.alive = True
    
    def update(self, dx, dy):
        fx, fy = self.body[0]
        new_loc = (fx + dx, fy + dy)
        self.body.insert(0, new_loc)
        del self.body[-1]
    
    def collision(self):
        x, y = self.body[0]
        if (x, y) in self.body[1:]:
            return True
        
        if x < 0 or y < 0 or x > self.cw - self.size or y > self.ch - self.size:
            return True
        
        return False
    
    def eat(self, dx, dy):
        fx, fy = self.body[0]
        new_loc = (fx + dx, fy + dy)
        self.body.insert(0, new_loc)
    
    def draw(self, display, color):
        for x, y in self.body:
            pygame.draw.rect(display, color, [x, y, self.size, self.size])
    
    def get_head(self):
        return self.body[0]
    
class Game:
    def __init__(self, size):
        self.size = size
        self.x = -1
        self.y = -1
        
    def get_loc(self, snake_locs, all_locs):
        self.x, self.y = random.choice(list(all_locs - snake_locs))
        
    def draw(self, display, color):
        pygame.draw.rect(display, color, [self.x, self.y, self.size, self.size])
    
    def get_food_loc(self):
        return self.x, self.y
    


# # Helper functions
def update_movement(e, size):
    if e == pygame.K_LEFT:
        if dx <= 0:
            return (-size, 0)
    elif event.key == pygame.K_RIGHT:
        if dx >= 0:
            return (size, 0)
    elif event.key == pygame.K_UP:
        if dy <= 0:
            return (0, -size)
    elif event.key == pygame.K_DOWN:
        if dy >= 0:
            return (0, size)
    return (dx, dy)

def message(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width/2, height/2])


# # init canvas

import pygame
import time
import random

pygame.init()

width = 800
height = 600

dis=pygame.display.set_mode((width, height))
pygame.display.update()
pygame.display.set_caption('Snake')
font_style = pygame.font.SysFont(None, 50)

clock = pygame.time.Clock()

blue = (0,255,0)
red = (255,0,0)
black = (13, 2, 8)
green = (0, 59, 0)

#object size
obs = 20
dx = 0
dy = 0

speed = 10
all_locs = set([(w, h) for w in range(0, width-obs+1, obs) for h in range(0, height-obs+1, obs)])


snk = snake(obs, width, height)
game = Game(snk.size)


# # Game

game_over = False
cnt = 0
game.get_loc(set(snk.body), all_locs)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            dx, dy = update_movement(event.key, snk.size)
            
    snk.update(dx, dy)
    game_over |= snk.collision()
    

    if game.get_food_loc() == snk.get_head():
        game.get_loc(set(snk.body), all_locs)
        snk.eat(dx, dy)
        
    dis.fill(black)
    snk.draw(dis, green)
    game.draw(dis, red)
    pygame.display.update()
    
    clock.tick(speed)
    
message("You lost", red)
pygame.display.update()
time.sleep(2)

pygame.quit()
quit()



