import pygame
import os
pygame.font.init()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Can not load image", name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


size = (16 * 50, 9 * 50)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('GREEN RECTANGL')

all_sprites = pygame.sprite.Group()

fon_image = load_image('фон.png')
fon = pygame.sprite.Sprite(all_sprites)
fon.image = fon_image
fon.rect = fon.image.get_rect()
fon.rect.topleft = (0, 0)

button_image = load_image('кнопка.jpg', -1)
button = pygame.sprite.Sprite(all_sprites)
button.image = button_image
button.rect = button.image.get_rect()
button.rect.topleft = (300, 350)

font = pygame.font.Font('comic.ttf', 50)
text = font.render(
    'GREEN RECTANGL', True, (60, 179, 113))
place = text.get_rect(
    center=(400, 200))
screen.blit(text, place)

par = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 300 <= event.pos[0] <= 300 + 177 and 350 <= event.pos[1] <= 350 + 54:
                par = True
                running = False

    all_sprites.draw(screen)
    screen.blit(text, place)

    pygame.display.flip()

pygame.quit()

if par:
    os.system('main.py')
