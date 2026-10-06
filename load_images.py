import os

import pygame

BASE_IMG_PATH = 'assets/'

def load_image(path):
    # print(BASE_IMG_PATH + path)
    img = pygame.image.load(BASE_IMG_PATH + path)

    # Transfer colorkey to per-pixel alpha because colorkey with pygame.gfxdraw.textured_polygon is really slow
    s = pygame.Surface(img.get_size(), pygame.SRCALPHA)
    img.set_colorkey((0, 0, 0))
    s.blit(img, (0, 0))

    return s

def load_images(path):
    images = []

    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))

    return images