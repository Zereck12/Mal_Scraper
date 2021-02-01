""" 
All the basic functions needed for pygame GUI for scraper.
Also contains Objects such as PButton, InputBox which acts 
as their name implies

Partial Credit to: @skrx for the InputBox class
https://stackoverflow.com/questions/46390231
/how-can-i-create-a-text-input-box-with-pygame
"""

import pygame as pg
from typing import List, Tuple, Optional

# Dimensions of Window
HEIGHT, WIDTH = 600, 640

# Colors
BACKGROUND = (105, 0, 191)
TEXT = (231, 177, 250)

# Font Styles and Size
FONT_FAMILY = "consolas"
FONT_HEIGHT = 40

# InputBox colors
COLOR_INACTIVE = BACKGROUND
COLOR_ACTIVE = (BACKGROUND[0] + 30, BACKGROUND[1] + 30, BACKGROUND[2] + 30)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        """ Initalizes an InputBox object """
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = get_font().render(text, True, BACKGROUND)
        self.active = False
        self.last_inp = ""


    def handle_event(self, event):
        """ Handles any input from the user in
        the pygame window """
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.last_inp = self.text
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = get_font().render(self.text, True, BACKGROUND)


    def update(self):
        """ Resizes the box if text is too long """
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width


    def draw(self, screen):
        """ Draws the box and Writes the text """
        pg.draw.rect(screen, TEXT, self.rect)
        pg.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        
        
class PButton():
    
    coord: Tuple[int]
    color: Tuple[int]
    text: Optional[str]
    
    def __init__(self, screen: pg.Surface, coord: Tuple[int], 
                 color = TEXT) -> None:
        """ Initalizes a PButton Object """
        self.coord = coord
        self.color = color
        self.screen = screen
        self.text = ""
        self.draw()
        
        
    def draw(self) -> None:
        """ Draws a Button with an Outline """
        # [WHITE] Outline
        out = (self.coord[0] - 3, self.coord[1] - 3, self.coord[2] + 6, 
               self.coord[3] + 6)
        light_bg = (BACKGROUND[0] + 30, BACKGROUND[1] + 30, BACKGROUND[2] + 30)
        pg.draw.rect(self.screen, light_bg, out)
        
        # Actual button
        pg.draw.rect(self.screen, self.color, self.coord)
        self.add_text(self.text)
        
    
    def is_cursor_on(self, pos: Tuple[int], clicked=False) -> bool:
        """Return whether <x> and <y> are within the PButton"""
        
        ans = self.coord[0] < pos[0] < self.coord[0] + self.coord[2] and \
            self.coord[1] < pos[1] < self.coord[1] + self.coord[3]
        
        if not clicked:
            self.hover()
        return ans
        
    
    def hover(self) -> None:
        """Render the drawing action of PButton"""
        
        new_color = (self.color[0] - 60, self.color[1] - 60, self.color[2] - 60)
        pg.draw.rect(self.screen, new_color, self.coord)
        self.add_text(self.text)
        
        
    def add_text(self, text: str) -> None:
        """Add text to current button"""
        
        self.text = text
        pos = (self.coord[0] + (self.coord[2] // 2) - len(text) * 9
               , self.coord[1] + (self.coord[3] // 2) - (FONT_HEIGHT// 2))
        write_text(self.screen, text, get_font(), BACKGROUND, pos)
        

def get_font(size=FONT_HEIGHT, bold=False) -> pg.font:
    """Return font of <size>"""
    
    font = pg.font.SysFont(FONT_FAMILY, size - 8)
    if bold:
        font.set_bold(True)
    return font


def border(screen: pg.Surface, color=TEXT, thick=3) -> None:
    """Draws a Border around the screen"""
    
    pg.draw.rect(screen, color, (5, 5, thick, HEIGHT - 10))
    pg.draw.rect(screen, color, (5, 5, WIDTH - 10, thick))
    pg.draw.rect(screen, color, (WIDTH - thick - 5, 5, thick, HEIGHT - 10))
    pg.draw.rect(screen, color, (5, HEIGHT - thick - 5, WIDTH - 10, thick))


def write_text(screen: pg.Surface, text: str, font: pg.font, color: Tuple,
               pos: Tuple) -> None:
    """Write the <text> on <screen> at <post> with <font> and <color>"""
    
    text_surface = font.render(text, 1, color)
    screen.blit(text_surface, pos)


def title_screen(screen: pg.Surface) -> None:
    """Draws the title screen of the program"""

    clear_screen(screen)
    border(screen)

    write_text(screen, "MAL Scraper", get_font(72), TEXT, (140, 210))
    pg.draw.rect(screen, TEXT, (50, 310, 540, 10))

    time_loop(screen, 3000)   
    
    
def clear_screen(screen: pg.Surface, color=BACKGROUND) -> None:
    """Clears screen i.e. draws a rectangle that
    covers the whole <screen> of color <BACKGROUND>"""
    
    pg.draw.rect(screen, color, (0, 0, WIDTH, HEIGHT))
    

def draw_header(screen: pg.Surface, text: str, offset=48, thick=5) -> None:
    """Draws the header at the top"""
    
    write_text(screen, text, get_font(), TEXT, 
               (offset, 23))
    pg.draw.rect(screen, TEXT, (offset, 70, WIDTH - (offset * 2), thick))
    
    
def time_loop(screen: pg.Surface, timer: int) -> None:
    """Makes the current display on screen stay for <timer> 
    (milliseconds) long""" 
    
    clock = pg.time.Clock()
    time_elapsed = 0
    while time_elapsed < timer:
        
        dt = clock.tick()
        time_elapsed += dt
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()
        pg.display.flip()