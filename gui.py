""" 
Main File containing all the windows for the GUI using helpers
from gui_helpers.py. Handling Events.

Partial Credit to @VegaSeat for his program to display image on GUI
https://www.daniweb.com/programming/software-development/code/493004/display-an-image-from-the-web-pygame
"""

import pygame as pg
import io
from urllib.request import urlopen

from gui_helpers import *
from scraper import *

def run_visualisation() -> None:
    """ Display an interactive graphical display of the Scraper """
    pg.init()
    pg.display.set_caption('My Anime List Scraper')
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    
    title_screen(screen)
    
    txt_screen(screen)
    

def txt_screen(screen) -> None:
    """ Display a textbox for the user's input """ 

    clear_screen(screen)
    border(screen)
    draw_header(screen, "Enter an Anime name")
    
    clock = pg.time.Clock()
    ip_box = InputBox(48, 270, 544, 50)

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()
            ip_box.handle_event(e)
        
        # If something has been entered
        if ip_box.last_inp != "":
            render_anime_stat(screen, ip_box.last_inp)
            
        clear_screen(screen)
        border(screen)
        draw_header(screen, "Enter an Anime Name")
        
        ip_box.update()
        ip_box.draw(screen)
    
        pg.display.flip()
        clock.tick(30)
 
 
def render_anime_stat(screen: pg.Surface, anime_name: str) -> None:
    """ Renders the screen with the overall stats of the anime """

    anime = search(anime_name)

    clear_screen(screen)
    border(screen)
    draw_header(screen, anime.title)

    # Loading the image 
    image_str = urlopen(anime.imageUrl).read()
    image_file = io.BytesIO(image_str)
    image = pg.image.load(image_file)
    screen.blit(image, (360,  100))

    # Displaying the Statistics
    write_text(screen, anime.rank, get_font(), TEXT, (48, 140))
    write_text(screen, "Score " + anime.score, get_font(), TEXT, (48, 240))
    write_text(screen, anime.popular, get_font(), TEXT, (48, 340))
    write_text(screen, "Link " + anime.link, get_font(24), TEXT, (48, 460))
    
    # Buttons for Next and Back
    next_b = PButton(screen, (442, 500, 150, 70))
    next_b.add_text("Next->")
    back_b = PButton(screen, (48, 500, 150, 70))
    back_b.add_text("<-Back")
    
    while True:
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()
            
            if e.type == pg.MOUSEBUTTONUP:
                if next_b.is_cursor_on(e.pos, True):
                    render_anime_desc(screen, anime)
                    
                if back_b.is_cursor_on(e.pos, True):
                    txt_screen(screen)
        
        # Drawing buttons depending on if they're clicked
        # or being hovered over
        if next_b.is_cursor_on(pg.mouse.get_pos()):
            next_b.hover()
        else:
            next_b.draw()
            
        if back_b.is_cursor_on(pg.mouse.get_pos()):
            back_b.hover()
        else:
            back_b.draw()
        
        pg.display.flip()


def render_anime_desc(screen: pg.Surface, anime: MAL) -> None:
    """ Render the description of said anime """

    clear_screen(screen)
    border(screen)
    draw_header(screen, anime.title)

    # Writing the description
    if len(anime.desc) >= 68:
        char_limit = 68
        for i in range(len(anime.desc) // char_limit):
            write_text(screen, anime.desc[char_limit * i: char_limit * (i + 1)],
                    get_font(22), TEXT, (48, 100 + (18 * i)))
        
        write_text(screen, anime.desc[char_limit * (i + 1):],
                    get_font(23), TEXT, (48, 100 + (18 * (i + 1))))
    else:
        write_text(screen, anime.desc, get_font(23), TEXT, (48, 100))
    
    # Buttons for Next and Back
    next_b = PButton(screen, (442, 500, 150, 70))
    next_b.add_text("Next->")
    
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()
            
            if e.type == pg.MOUSEBUTTONUP:
                if next_b.is_cursor_on(e.pos, True):
                    txt_screen(screen)
     
        if next_b.is_cursor_on(pg.mouse.get_pos()):
            next_b.hover()
        else:
            next_b.draw()
        
        pg.display.flip()


if __name__ == '__main__':
    run_visualisation()
    
    