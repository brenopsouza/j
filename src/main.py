import pygame
from pygame.locals import *
from sys import exit

from xml import sax

from Tilemap import TMXHandler
from Tilemap import Tileset

from Commands import *
from Command import *

from Caracter import *

def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True

    #Constantes
    DEFAULT_COLOR = (0,255,0)
    COMMAND_TIMEOUT = 750
    REPEAT_DELAY = 30 #milisseconds between each KEYDOWN event (when repeating)
    KEY_TIMEOUT = 185 #MAX milisseconds between key pressings
    SCREEN_WIDTH, SCREEN_HEIGHT = (640, 256)

    screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fat Good Samaritan")

    img_fatguy = pygame.image.load("gato.png")
    fatguy = Caracter("jonatas", img_fatguy, 5, 32, 32)

    parser = sax.make_parser()
    tmxhandler = TMXHandler()
    parser.setContentHandler(tmxhandler)
    parser.parse("fase1.tmx")

    command_timeout = -1
    color = DEFAULT_COLOR
    key_queue = []
    key_timeout = -1
    sprinting = False
    pending_sprints = 0

    pygame.key.set_repeat(REPEAT_DELAY*3, REPEAT_DELAY)
    while running:
        clock.tick(30)
#        pygame.draw.circle(screen_surface, color, (400,300) , 30)

#        screen_surface.fill((255,255,255))
        screen_surface.blit(tmxhandler.image, (0,0))

#        pygame.display.flip()

        screen_surface.blit(fatguy.image,  fatguy.get_pos())
        fatguy.update(pygame.time.get_ticks(), SCREEN_WIDTH, SCREEN_HEIGHT)

        if command_timeout >= 0:
            if (pygame.time.get_ticks() - command_timeout) > COMMAND_TIMEOUT:
                color = DEFAULT_COLOR
                command_timeout = -1

        if key_timeout >= 0:
            if (pygame.time.get_ticks() - key_timeout) > KEY_TIMEOUT:
                actual_state = 0
                key_timeout = -1

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                running = False
            elif e.type == KEYDOWN:
                key_timeout = pygame.time.get_ticks()
                refresh_state(e.key)

        pygame.display.update()
        pygame.time.delay(10)

if __name__ == "__main__": main()
