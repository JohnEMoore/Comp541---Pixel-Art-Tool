import pygame as pg
import sys
import math
import pyperclip



from pygame.locals import *

clock = pg.time.Clock()

window_width = 1300
window_height = 832
pg.init()
window = pg.display.set_mode((window_width, window_height), 0, 32, display=0)
pg.display.set_caption('541 Pixel Art')
spriteMap = pg.Surface((832, 832))




#font
pg.font.init()
main_font = pg.font.SysFont('Bell MT', 24)


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
    
    


class Slider:
    def __init__(self, pos:tuple, size: tuple, min, max):
        #pos is the center of the slider
        self.pos = pos
        self.size = size
        self.slider_left = self.pos[0] - size[0]/2
        self.slider_right = self.pos[0] + size[0]/2
        self.slider_top = self.pos[1] + size[1]/2

        self.min = min
        self.max = max

        self.container_rect = pg.Rect(self.slider_left, self.slider_top, self.size[0], self.size[1])
        self.button_rect = pg.Rect(self.slider_left - 6, self.slider_top - 3, 12, self.size[1] + 6)

    def draw(self, screen):
        pg.draw.rect(screen, "black", self.container_rect)
        pg.draw.rect(screen, "white", self.button_rect, border_radius=6)

    def move(self, mouse_pos):
        x_loc  = ((mouse_pos[0] // 20) * 20)
        self.button_rect.centerx =  x_loc + 1 if x_loc <= (self.slider_left ) else x_loc      


    def get_val(self) -> int:
        length = self.slider_right - self.slider_left 
        button_loc = self.button_rect.centerx - self.slider_left 
        return math.ceil(button_loc / length * 15)
    
    def jump(self, val):
        self.button_rect.centerx = (val // 17) * self.size[0]//15   + self.slider_left

class Painter:

    def __init__(self):
        self.brush_color = pg.Color(0, 0, 0)
        self.brush_hexits = ["0", "0", "0"]
        self.brush_size = 1
        self.canvas_size = 16
        self.tool_type = "brush"

    def update_Color(self, color: pg.Color):
        self.brush_color = color
        self.brush_hexits
        self.brush_hexits = [f'{color.r//17:x}', f'{color.g//17:x}', f'{color.b//17:x}']

    def update_canvas_size(self, size):
        self.canvas_size = size
    
def blank_canvas(dimensions: int = 16):
    new_list = []
    offset = 0
    for i in range (0, dimensions**2):
        
        new_list.append( pg.Color(102, 102, 102) if (i + offset) % 2  == 0 else pg.Color(51, 51, 51))
        if i % dimensions == dimensions - 1:
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
        pg.draw.line(surf, (161, 161, 161), (0, spriteMap.get_width()//dimensions * x), (spriteMap.get_height(),spriteMap.get_width()//dimensions * x), 1)
        pg.draw.line(surf,  (161, 161, 161), (spriteMap.get_height()//dimensions * x, 0), (spriteMap.get_height()//dimensions * x, spriteMap.get_height()), 1)
    return surf

def blit_from_array(array: list, dimensions=16):
    surf = pg.Surface((832, 832))
    length = round(math.sqrt(len(array)))
    pixel_length = 832 // length # calculate size of each pixel given number of pixels and the magic number for canvas size
    for i in range(0, len(array)):
        #print(((i%length) * pixel_length,  (i // length) * pixel_length), (pixel_length, pixel_length))
        pg.draw.rect(surf, array[i], (((i%length) * pixel_length,  (i // length) * pixel_length), (pixel_length, pixel_length)), 0)
    return surf

def draw_canvas(canvas, x_loc, y_loc, color, size, dimensions = 16, mirrorV = False, mirrorH = False):
    pixel_length = 832 // dimensions
    for x in range (0, size):
        for y in range(0, size):
            pg.draw.rect(canvas, color, ((x_loc -468) // pixel_length *  pixel_length + x * pixel_length * (-1 if mirrorV else 1) ,  (y_loc //  pixel_length) * pixel_length  + y * pixel_length * (-1 if mirrorH else 1), pixel_length, pixel_length), 0)
    return canvas

def update_canvas_array(array: list, x_loc, y_loc, color, size, dimensions = 16, mirrorV = False, mirrorH = False):
    pixel_length = 832 // dimensions
    ret = array

    for x in range (0, size):
        for y in range(0, size):
            index = ((x_loc - 468) // pixel_length) + x * (-1 if mirrorV else 1) + (y_loc // pixel_length * dimensions) + dimensions * y * (-1 if mirrorH else 1) 
            if index < len(array):
                ret[index] = color
    return ret

    
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def slider_text(brush_hexits, window):
    draw_text('R', main_font, (255, 255, 255), window, 30, 725)
    draw_text('G', main_font, (255, 255, 255), window, 30, 765)
    draw_text('B', main_font, (255, 255, 255), window, 30, 805)
    draw_text(brush_hexits[0], main_font, (255, 255, 255), window, 385, 725)
    draw_text(brush_hexits[1], main_font, (255, 255, 255), window, 385, 765)
    draw_text(brush_hexits[2], main_font, (255, 255, 255), window, 385, 805)

def exportData(array):
    text = ""
    for i in range(0, len(array)):
        text += f'{array[i].r//17:x}' + f'{array[i].g//17:x}' + f'{array[i].b//17:x}'
        text += "\n"
    pyperclip.copy(text)

def selectColor(array,  x_loc, y_loc, dimensions = 16):
    pixel_length = 832 // dimensions
    return array[((x_loc - 468) // pixel_length) + (y_loc // pixel_length * dimensions)]

def fill(canvas, array, x_loc, y_loc, color, oldcolor, dimensions):
    if oldcolor == color:
        return array
    pixel_length = 832 // dimensions
    ret = array
    draw_canvas(canvas, x_loc, y_loc, color, 1, dimensions)
    index = ((x_loc - 468) // pixel_length) + (y_loc // pixel_length * dimensions)
    ret[index] = color
    if (index - dimensions >= 0 and ret[index - dimensions] == oldcolor):
        ret = fill(canvas, ret, x_loc , y_loc - pixel_length, color, oldcolor, dimensions)
    if (index + dimensions < len(array)  and ret[index + dimensions] == oldcolor):
        ret = fill(canvas, ret, x_loc, y_loc + pixel_length, color, oldcolor, dimensions)
    if (index - 1 >= 0 and ret[index - 1] == oldcolor and index // dimensions == (index - 1) // dimensions):
        ret = fill(canvas, ret, x_loc - pixel_length, y_loc, color, oldcolor, dimensions)
    if (index + 1 < len(array) and ret[index + 1] == oldcolor and index // dimensions == (index + 1) // dimensions):
        ret = fill(canvas, ret, x_loc + pixel_length, y_loc, color, oldcolor, dimensions)
    return ret

class Button:
    def __init__(self, x, y, width, height, val):
        self.rect = pg.Rect(x- width/2, y - height/2, width, height)
        self.val = val
    
    def draw(self, screen):
        pg.draw.rect(screen, "white", self.rect)


def main():
    user: Painter = Painter()
    

    overlay = grid()
    show_grid = True
    current_array = blank_canvas()
    spriteMap = blit_from_array(current_array)

    undo_tree: linkedList = linkedList()
    undo_tree.insert(current_array)
    temp = current_array

    R_slider: Slider = Slider((211, 720), (300, 6), 0, 15)
    G_slider: Slider = Slider((211, 760), (300, 6), 0, 15)
    B_slider: Slider = Slider((211, 800), (300, 6), 0, 15)
    sliders = [R_slider, G_slider, B_slider]

    button_8: Button = Button(110, 150, 90, 90, 8)
    button_16: Button = Button(230, 150, 90, 90, 16)
    button_32: Button = Button(350, 150, 90, 90, 32)

    buttons = [button_8 , button_16, button_32]

    mouse_down = False
    while(True):
        window.fill((80, 80, 80))

        mouse_pos = pg.mouse.get_pos()
        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                match(event.key):
                    case pg.K_o:
                        show_grid = not show_grid
                    case pg.K_z:
                        if(pg.key.get_mods() and pg.KMOD_CTRL):
                            undo_tree.goBack()
                            stuff = undo_tree.getData()
                            spriteMap = blit_from_array(stuff)
                            temp = stuff
                        

                    case pg.K_y:
                        if pg.key.get_mods() and pg.KMOD_CTRL:
                            undo_tree.goForward()
                            stuff = undo_tree.getData()
                            spriteMap = blit_from_array(stuff, user.canvas_size)
                            temp = stuff
                    case pg.K_s:
                        user.tool_type = "selector"
                    case pg.K_b:
                        user.tool_type = "brush"
                    case pg.K_c:
                        exportData(undo_tree.getData()) 
                    case pg.K_1:
                        user.brush_size = 1
                    case pg.K_2:
                        user.brush_size = 2
                    case pg.K_3:
                        user.brush_size = 3
                    case pg.K_4:
                        user.brush_size = 4
                    case pg.K_v:
                        user.tool_type = "vert_mirror"
                    case pg.K_h:
                        user.tool_type = "horz_mirror"
                    case pg.K_f:
                        user.tool_type = "fill"
                    
                
        mouse_X = pg.mouse.get_pos()[0]
        mouse_Y = pg.mouse.get_pos()[1]        
        if pg.mouse.get_pressed()[0]:
                match user.tool_type:
                    case "brush" | "horz_mirror" | "vert_mirror" | "fill":
                        mouse_down = True
                    case "selector":
                        if( mouse_X > 468 and abs(mouse_Y - 416) < 416):
                            user.update_Color(selectColor(current_array, mouse_X, mouse_Y, user.canvas_size))
                            R_slider.jump(user.brush_color.r)
                            G_slider.jump(user.brush_color.g)
                            B_slider.jump(user.brush_color.b)
                    
                            

        else: 
            if(mouse_down):
                undo_tree.insert(temp)
            current_array = temp.copy()
            mouse_down = False
                
        if(mouse_down):
            
            if( mouse_X > 468 and abs(mouse_Y - 416) < 416):
                if user.tool_type == "brush":
                    draw_canvas(spriteMap, mouse_X, mouse_Y, user.brush_color, user.brush_size,  user.canvas_size)
                    temp = update_canvas_array(temp, mouse_X, mouse_Y, user.brush_color, user.brush_size, user.canvas_size)
                if user.tool_type == "horz_mirror":
                    draw_canvas(spriteMap, mouse_X, mouse_Y, user.brush_color, user.brush_size,  user.canvas_size)
                    temp = update_canvas_array(temp, mouse_X, mouse_Y, user.brush_color, user.brush_size, user.canvas_size)
                    draw_canvas(spriteMap, mouse_X, abs(832 - mouse_Y), user.brush_color, user.brush_size,  user.canvas_size, mirrorH=True)
                    temp = update_canvas_array(temp, mouse_X, abs(832- mouse_Y), user.brush_color, user.brush_size, user.canvas_size, mirrorH=True)
                if user.tool_type == "vert_mirror":
                    draw_canvas(spriteMap, mouse_X, mouse_Y, user.brush_color, user.brush_size,  user.canvas_size)
                    temp = update_canvas_array(temp, mouse_X, mouse_Y, user.brush_color, user.brush_size, user.canvas_size)
                    draw_canvas(spriteMap,  abs(832 - mouse_X + 468) + 468, mouse_Y, user.brush_color, user.brush_size, user.canvas_size, mirrorV=True)
                    temp = update_canvas_array(temp, abs(832 - mouse_X + 468) + 468, mouse_Y, user.brush_color, user.brush_size, user.canvas_size, mirrorV=True)
                if user.tool_type == "fill":
                        if( mouse_X > 468 and abs(mouse_Y - 416) < 416):
                            temp = fill(spriteMap, temp.copy(), mouse_X, mouse_Y, user.brush_color, selectColor(current_array, mouse_X, mouse_Y, user.canvas_size), user.canvas_size)
                            
                       
        for slider in sliders:
            slider.draw(window)
            if slider.container_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
                slider.move(mouse_pos)
                user.update_Color(pg.Color((R_slider.get_val()<< 4) + R_slider.get_val(),(G_slider.get_val()<< 4) + G_slider.get_val(), (B_slider.get_val()<< 4) + B_slider.get_val() ))
        slider_text(user.brush_hexits, window)

        for button in buttons:
            button.draw(window)
            if button.rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
                new_size = button.val
                if new_size != user.canvas_size:
                    user.canvas_size = new_size
                    overlay = grid(new_size)
                    current_array = blank_canvas(new_size)
                    spriteMap = blit_from_array(current_array, new_size)

                    undo_tree: linkedList = linkedList()
                    undo_tree.insert(current_array)
                    temp = current_array
                    
                

       
        pg.draw.rect(window, user.brush_color, (60, 400, 300, 300))

        window.blit(spriteMap, (468,0))
        if (show_grid):
            window.blit(overlay, (468, 0))
        
      

        pg.display.update()
        clock.tick(120)



if __name__ == "__main__":
    main()