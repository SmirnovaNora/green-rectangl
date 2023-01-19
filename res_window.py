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
rectangls = pygame.sprite.Group()

rectangl_image = load_image('rect green.jpg').convert_alpha()
rectangl = pygame.sprite.Sprite(rectangls)
rectangl.image = rectangl_image
rectangl.rect = rectangl_image.get_rect()
rectangl.rect.x = 0
rectangl.rect.y = 0

rectangl_image = load_image('rect green.jpg').convert_alpha()
rectangl = pygame.sprite.Sprite(rectangls)
rectangl.image = rectangl_image
rectangl.rect = rectangl_image.get_rect()
rectangl.rect.x = 750
rectangl.rect.y = 400

file = open('resalt_score.txt', mode="r", encoding="utf-8")
text = file.readline()
file.close()

par = False

file2 = open('check_close.txt', mode="r", encoding="utf-8")
if file2.readline() == '2':
    par = True
file2.close()
file2 = open('check_close.txt', mode="w", encoding="utf-8")

vx = 50

rectangls_list = rectangls.sprites()

fon_image = load_image('фон 2.jpg')
fon = pygame.sprite.Sprite(all_sprites)
fon.image = fon_image
fon.rect = fon.image.get_rect()
fon.rect.topleft = (0, 0)

button_image = load_image('кнопка 2.jpg', -1)
button = pygame.sprite.Sprite(all_sprites)
button.image = button_image
button.rect = button.image.get_rect()
button.rect.topleft = (300, 350)

font = pygame.font.Font(None, 60)
text = font.render(f'Ваше счёт: {text}', True, (255, 255, 255))
place = text.get_rect(center=(350, 200))
screen.blit(text, place)

pos = 0

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            file2.write('1')
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 300 <= event.pos[0] <= 300 + 177 and 350 <= event.pos[1] <= 350 + 54:
                if par:
                    os.system('final_window.py')
                    file2.write('1')
                running = False

    all_sprites.draw(screen)
    rectangls.draw(screen)

    screen.blit(text, place)

    if pos == 0:
        rectangls_list[0].rect.x += vx
        if rectangls_list[0].rect.x == 750:
            pos = (pos + 1) % 4

        rectangls_list[1].rect.x -= vx

    if pos == 1:
        rectangls_list[0].rect.y += vx
        if rectangls_list[0].rect.y == 400:
            pos = (pos + 1) % 4

        rectangls_list[1].rect.y -= vx

    if pos == 2:
        rectangls_list[0].rect.x -= vx
        if rectangls_list[0].rect.x == 0:
            pos = (pos + 1) % 4

        rectangls_list[1].rect.x += vx

    if pos == 3:
        rectangls_list[0].rect.y -= vx
        if rectangls_list[0].rect.y == 0:
            pos = (pos + 1) % 4

        rectangls_list[1].rect.y += vx

    clock.tick(10)
    pygame.display.flip()

pygame.quit()
file2.close()

