# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 17:41:30 2022

@author: jill1
"""

import os 
import pygame 
import sys 
import random 
import pygame.font 
import time 
 
pygame.init() 
 
clos = 10       
rows = 20       
cell_size = 30      
block_size = cell_size - 1   
block_edge = int(block_size /10)  
fps = 40       
 
win_width = clos * 2 * cell_size + 6 * cell_size 
win_hight = (rows + 1) * cell_size  
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400,40) 
screen = pygame.display.set_mode((win_width, win_hight)) 
pygame.display.set_caption("The Crystal") 
 
BLACK=(255,255,0) 
 
blocks = { 
    #I型 
 1: [[(0,1),(1,1),(2,1),(3,1)], 
  [(2,0),(2,1),(2,2),(2,3)]],  
    #O型  
 2: [[(1,1),(2,1),(1,2),(2,2)]], 
    #T型   
 3: [[(0,1),(1,1),(2,1),(1,2)], 
  [(1,0),(0,1),(1,1),(1,2)], 
  [(1,1),(0,2),(1,2),(2,2)], 
  [(1,0),(1,1),(2,1),(1,2)]],  
    #L型  
 4: [[(0,1),(1,1),(2,1),(0,2)], 
  [(0,0),(1,0),(1,1),(1,2)], 
  [(2,1),(0,2),(1,2),(2,2)], 
  [(1,0),(1,1),(1,2),(2,2)]],  
     
 5: [[(0,1),(1,1),(2,1),(2,2)], 
  [(1,0),(1,1),(0,2),(1,2)], 
  [(0,1),(0,2),(1,2),(2,2)], 
  [(1,0),(2,0),(1,1),(1,2)]],  
    #Z型  
 6: [[(1,1),(2,1),(0,2),(1,2)], 
  [(0,0),(0,1),(1,1),(1,2)]], 
     
 7: [[(0,1),(1,1),(1,2),(2,2)], 
  [(2,0),(1,1),(2,1),(1,2)]],}  
   
 
block_color = [(199,238,206),(200,50,50),(50,200,200),(50,50,200),(200,200,50),(200,50,200),(50,200,50),(125,50,125),(180,180,180)] 
 
font_name=pygame.font.match_font('arial')    
def draw_text(self,text,size,x,y): 
    
    font=pygame.font.Font(font_name, size) 
    text_surface=font.render(text,True,BLACK) 
    text_rect=text_surface.get_rect() 
    text_rect.centerx=x 
    text_rect.top=y 
    self.blit(text_surface,text_rect) 
         
 
def draw_init(): 
    screen.fill((166,124,64)) 
    draw_text(screen, 'CRYSTALS', 64, win_width/2, win_hight/4) 
    draw_text(screen, '← →TO MOVE THE CRYSTALS', 22, win_width/2, win_hight/2) 
    draw_text(screen, 'PRESS ANY KEY TO START', 18, win_width/2, win_hight*3/4) 
    pygame.display.update() 
    waiting = True 
    while waiting: 
        time.tick(fps) 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                return True 
            elif event.type == pygame.KEYUP: 
                waiting = False 
                return False        
 
class Game_machine(): 
 def __init__(self,x0,y0): 
  self.x0, self.y0 = x0, y0     
  self.rect = pygame.Rect(0,0,block_size, block_size)   
  self.display_array = [[0 for i in range(clos)] for j in range(rows)]  
  self.color_array = [[0 for i in range(clos)] for j in range(rows)]   
  self.x, self.y = 0, 0      
  self.key = 0        
  self.index_ = 0        
  self.next_key = self.rand_key()    
  self.speed = fps       
  self.fall_buffer = self.speed    
  self.fall_speed_up = False     
  self.score = 0 
  self.lines = 0 
  self.level = 0 
  self.creat_new_block() 
       
 def creat_new_block(self): 
  self.key = self.next_key 
  self.next_key = self.rand_key() 
  self.index = 0 
  self.x = 4      
  self.y = -1      
 
 def rand_key(self): 
  keys = [1,1,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,7,7]   
  return keys[random.randint(0,len(keys)-1)] 
   
 def move(self, dx, dy): 
  if self.can_move(self.index, dx, dy): 
     self.x += dx 
     self.y += dy 
  elif dy: 
   if self.y <= 0: 
    self.game_over() 
   else: 
    self.stop_move() 
    
 def rotate(self): 
  next_index = (self.index + 1) % len(blocks[self.key]) 
  if self.can_move(next_index, 0, 0): 
   self.index = next_index 
  
 def can_move(self, index, dx, dy):  
  for (x,y) in blocks[self.key][index]: 
   clo, row = self.x + x + dx , self.y + y + dy 
   if clo >= clos  or clo < 0 or row >= rows or row < 0:  
    return False 
   if self.display_array[row][clo]:    
    return False 
  return True 
 
 def stop_move(self): 
  self.score += 4  
  for (x,y) in  blocks[self.key][self.index]: 
   self.display_array[y+self.y][x+self.x] = 1 
   self.color_array[y+self.y][x+self.x] = self.key 
  self.del_full_row()  
  self.creat_new_block()  
  
 def del_full_row(self): 
   
  lines = 0   
  for row in range(rows): 
   if sum(self.display_array[row]) == clos:    
    lines += 1     
    self.lines += 1 
    if self.lines % 5 == 0:     
     self.level = self.lines / 5 
     self.speed = int(self.speed * 0.9)    
    self.score += (self.level + clos * lines) * 5 
     
    del self.display_array[row] 
    self.display_array.insert(0,[0 for i in range(clos)]) 
     
 def display(self): 
  self.display_stop_blocks() 
  self.display_next_blocks() 
  self.display_move_blocks() 
  self.display_score() 
   
   
  self.fall_buffer -= 1 
  if self.fall_buffer == 0 or self.fall_speed_up: 
   self.fall_buffer = self.speed 
   self.move(0,1) 
     
 def display_stop_blocks(self): 
   
  for y in range(rows): 
   for x in range(clos): 
    self.rect.topleft = x * cell_size, y * cell_size 
    if  self.display_array[y][x]: 
     self.draw_block(self.color_array[y][x], 1) 
    else: 
     self.draw_block(0, 0) 
      
 def display_next_blocks(self): 
   
  for (x,y) in  blocks[self.next_key][0]: 
   self.rect.topleft = x * cell_size , (y - 1) * cell_size 
   self.draw_block(8, 1)   
 
 def display_move_blocks(self): 
  for (x,y) in  blocks[self.key][self.index]: 
   self.rect.topleft = (self.x + x) * cell_size, (self.y + y) * cell_size 
   self.draw_block(self.key, 1)  
 
 def display_score(self): 
  text = "score:%d  lines:%d  level:%d" %(self.score,self.lines,self.level) 
  self.img = pygame.font.SysFont("kaiti",25).render(text, True, (0,0,255))  
  self.img_rect = self.img.get_rect() 
  self.img_rect.topleft = (self.x0, rows * cell_size) 
  screen.blit(self.img, self.img_rect)   
        
     
 def game_over(self): 
  self.__init__(self.x0, self.y0) 
       
 def draw_block(self, color_index, draw_edge): 
   
  (r,g,b) = block_color[color_index] 
  self.rect.centerx = self.rect.left + self.x0 + int(cell_size / 2) 
  self.rect.centery = self.rect.top + self.y0 + int(cell_size / 2) 
  if draw_edge: 
   pygame.draw.rect(screen, (r,g,b), self.rect.inflate(-block_edge, -block_edge), 0) 
            
  else: 
   pygame.draw.rect(screen, (r,g,b), self.rect, 0) 
             
 
time = pygame.time.Clock()  
player1 = Game_machine(0, 0) 
player2 = Game_machine((clos + 6) * cell_size, 0) 
start_init=True 
 
while True: 
    if start_init:             
        close=draw_init() 
        if close: 
            break 
    start_init=False 
    time.tick(fps) 
    screen.fill((166,124,64)) 
    player1.display() 
    player2.display() 
    pygame.display.update()  
   
  
    for event in pygame.event.get():             
        if event.type == pygame.KEYDOWN:         
            if event.key == pygame.K_g:    
                player1.move(1,0) 
            elif event.key == pygame.K_d:   
                player1.move(-1,0) 
            elif event.key == pygame.K_r:   
                player1.rotate() 
            elif event.key == pygame.K_f:   
                player1.fall_speed_up = True 
     
            if event.key == pygame.K_RIGHT:   
                player2.move(1,0) 
            elif event.key == pygame.K_LEFT:  
                player2.move(-1,0) 
            elif event.key == pygame.K_UP:   
                player2.rotate() 
            elif event.key == pygame.K_DOWN:  
                player2.fall_speed_up = True 
     
            elif event.key == pygame.K_q: 
                sys.exit() 
     
        elif event.type == pygame.KEYUP:         
            if event.key == pygame.K_f: 
                player1.fall_speed_up = False 
            if event.key == pygame.K_DOWN: 
                player2.fall_speed_up = False  
                 
        elif event.type == pygame.QUIT:          
            pygame.quit()