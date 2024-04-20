import pygame as pg
import sys
import math

from pygame.locals import *

clock = pg.time.Clock()

window_width = 1500
window_height = 832
pg.init()
window = pg.display.set_mode((window_width, window_height), 0, 32)
pg.display.set_caption('541 Pixel Art')
spriteMap = pg.Surface((832, 832))

class node:
    data: list[pg.Color]

    def __init__(self, data):
        self.data = data.copy()
        self.next = None


class linkedList:
    
    def __init__(self):
        self.head = None
        self.activeNode = 0
        self.size = 0

    def insert(self, data):   #places new node infront of current active node, dereferences items ahead of current active if changes
        new_node = node(data)
        if self.head == None:
            self.head = new_node
            self.size += 1
        elif(self.activeNode == 0):
            new_node.next = self.head
            self.head = new_node
            self.size += 1
        else:
            i = 0
            temp = self.head
            while (i < self.activeNode ):
                temp = temp.next
                i += 1 
            new_node.next = temp
            self.head = new_node
            
            self.size = (self.size + 1 - self.activeNode)
            self.activeNode = 0
        
    def goBack(self):
        if self.activeNode == self.size - 1: # already at last node
            return
        else:
            self.activeNode += 1

    def goForward(self):
        if self.activeNode == 0:
            return
        else:
            self.activeNode -= 1

    def getData(self):
        i = 0
        temp = self.head
        while (i < self.activeNode ):
            temp = temp.next
            i += 1
        return temp.data.copy()



    
def blank_canvas(dimensions: int = 16):
    new_list = []
    offset = 0
    for i in range (0, dimensions**2):
        
        new_list.append( pg.Color(102, 102, 102) if (i + offset) % 2  == 0 else pg.Color(51, 51, 51))
        if i % dimensions == 15:
            offset = not offset
    return new_list
    

def overlay_init():
    overlay = pg.Surface((832, 832))
    grid(overlay)
    return overlay
    

def grid(dimensions: int = 16):
    surf = pg.Surface((832, 832))
    surf.fill(pg.Color(0,255,0), None)
    surf.set_colorkey((0,255,0))
    for x in range(1, dimensions):
        pg.draw.line(surf, (153, 153, 153), (0, spriteMap.get_width()//dimensions * x), (spriteMap.get_height(),spriteMap.get_width()//dimensions * x), 2)
        pg.draw.line(surf, (153, 153, 153), (spriteMap.get_height()//dimensions * x, 0), (spriteMap.get_height()//dimensions * x, spriteMap.get_height()), 2)
    return surf

def blit_from_array(array: list):
    surf = pg.Surface((832, 832))
    length = round(math.sqrt(len(array)))
    pixel_length = 832 // length # calculate size of each pixel given number of pixels and the magic number for canvas size
    for i in range(0, len(array)):
        #print(((i%length) * pixel_length,  (i // length) * pixel_length), (pixel_length, pixel_length))
        pg.draw.rect(surf, array[i], (((i%length) * pixel_length,  (i // length) * pixel_length), (pixel_length, pixel_length)), 0)
    return surf

def draw_canvas(canvas, x_loc, y_loc, color, dimensions = 16):
    pixel_length = 832 // dimensions
    pg.draw.rect(canvas, color, ((x_loc -334) // pixel_length *  pixel_length ,  (y_loc //  pixel_length) * pixel_length, pixel_length, pixel_length), 0)
    return canvas

def update_canvas_array(array: list, x_loc, y_loc, color, dimensions = 16):
    pixel_length = 832 // dimensions
    ret = array.copy()
    ret[(x_loc - 334) // pixel_length + y_loc // pixel_length * dimensions] = color
    return ret
    

    


def run():
    overlay = grid()
    show_grid = True
    current_array = blank_canvas()
    spriteMap = blit_from_array(current_array)

    undo_tree: linkedList = linkedList()
    undo_tree.insert(current_array)
    temp = current_array.copy()

    j = 0
    mouse_down = False
    while(True):
        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                match(event.key):
                    case pg.K_o:
                        show_grid = not show_grid
                    case pg.K_z:
                        if pg.key.get_mods() and pg.KMOD_CTRL:
                            undo_tree.goBack()
                            stuff = undo_tree.getData()
                            spriteMap = blit_from_array(stuff)
                            temp = stuff
                    case pg.K_y:
                        if pg.key.get_mods() and pg.KMOD_CTRL:
                            undo_tree.goForward()
                            stuff = undo_tree.getData()
                            spriteMap = blit_from_array(stuff)
                            temp = stuff

        if pg.mouse.get_pressed()[0]:
                mouse_down = True
        else: 
            if(mouse_down):
                undo_tree.insert(temp)
            current_array = temp.copy()
            mouse_down = False
                
        if(mouse_down):
            mouse_X = pg.mouse.get_pos()[0]
            mouse_Y = pg.mouse.get_pos()[1]
            if( abs(mouse_X - 750) < 416 and abs(mouse_Y - 416) < 416):
                spriteMap = draw_canvas(spriteMap, mouse_X, mouse_Y, pg.Color(255, 0, 0), 16)
                temp = update_canvas_array(temp, mouse_X, mouse_Y, pg.Color(255, 0, 0))
                    
       
        window.blit(spriteMap, (334,0))
        if (show_grid):
            window.blit(overlay, (334, 0))
        pg.display.update()
        clock.tick(60)

def main():
    window.fill((80, 80, 80))
    run()
   


if __name__ == "__main__":
    main()