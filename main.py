import pygame
import os
import random

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


class Play:
    def __init__(self, size):
        self.height = 9
        self.wight = 16
        self.size = size

        self.lvls = ['lvl1.txt', 'lvl2.txt']
        self.lvl = 0

        self.killings = 0
        self.score = 0
        self.open_door = 0

        self.rectangl_image = load_image('rect green.jpg').convert_alpha()
        self.rectangl = pygame.sprite.Sprite(all_sprites)
        self.rectangl.image = self.rectangl_image
        self.rectangl.rect = self.rectangl_image.get_rect()
        self.rectangl.rect.x = 1 * 50
        self.rectangl.rect.y = self.size[1] - 6 * 50

        self.motion_forward_x = True
        self.motion_back_x = True
        self.motion_back_y = True
        self.motion_forward_y = True

        self.v = 50
        self.jump = False
        self.timer = 0

        self.board_coords = []
        self.kill_coords = []
        self.exit_coords = []

        self.running = True

        self.draw()

    def load_lvl(self):
        file = open(self.lvls[self.lvl], mode="r", encoding="utf-8")
        file = file.readlines()

        self.board_coords = []
        self.kill_coords = []
        self.exit_coords = []

        kill.empty()
        bloks.empty()
        exit.empty()

        for j in range(self.height):
            for i in range(self.wight):
                if file[j][i] == '#':
                    self.board_coords.append((i, j))
                if file[j][i] == '/':
                    self.kill_coords.append((i, j))
                if file[j][i] == '0':
                    self.exit_coords.append((i, j))

        self.board_coords = self.update_coords(self.board_coords)
        self.kill_coords = self.update_coords(self.kill_coords)
        self.exit_coords = self.update_coords(self.exit_coords)

        self.kill_coords = [(i[0], i[1] + 25) for i in self.kill_coords]

        win_door = random.randint(0, len(self.exit_coords) - 1)
        self.win_door = self.exit_coords[win_door]

        self.draw()

    def update_coords(self, coords):
        return [(i[0] * 50, i[1] * 50) for i in coords]

    def draw(self):
        for i in range(len(self.board_coords)):
            block_image = load_image('блок.jpg', -1)
            block = pygame.sprite.Sprite(bloks)
            block.image = block_image
            block.rect = block.image.get_rect()
            block.rect.topleft = self.board_coords[i]

        for i in range(len(self.kill_coords)):
            block_image = load_image('колья.png', -1)
            block = pygame.sprite.Sprite(kill)
            block.image = block_image
            block.rect = block.image.get_rect()
            block.rect.topleft = self.kill_coords[i]

        for i in range(len(self.exit_coords)):
            block_image = load_image('выход.png', -1)
            block = pygame.sprite.Sprite(exit)
            block.image = block_image
            block.rect = block.image.get_rect()
            block.rect.topleft = self.exit_coords[i]

    def update_rect(self, motion):
        self.motion_forward_x = True
        self.motion_back_x = True
        self.motion_forward_y = True

        self.check()

        if motion == 2:
            if self.rectangl.rect.x + 50 != size[0] and self.motion_forward_x:
                self.rectangl.rect.x += self.v

        if motion == 3:
            if self.rectangl.rect.x != 0 and self.motion_back_x:
                self.rectangl.rect.x -= self.v

        if motion == 1:
            if not self.jump:
                self.jump = True
                if self.rectangl.rect.y != 0 and self.motion_forward_y:
                    self.rectangl.rect.y -= self.v

                    if self.motion_back_y:
                        self.timer = 15  # изменить если поменяю значение тика

    def check_kill(self):
        if pygame.sprite.spritecollideany(all_sprites.sprites()[0], kill):
            self.killings += 1

            self.rectangl.rect.x = 1 * 50
            self.rectangl.rect.y = self.size[1] - 6 * 50

    def check_win(self):
        if pygame.sprite.spritecollideany(all_sprites.sprites()[0], exit):
            if self.rectangl.rect.x == self.win_door[0] and self.rectangl.rect.y == self.win_door[1]:
                self.lvl += 1

                self.file = open('resalt_score.txt', mode="w", encoding="utf-8")
                self.file.write(self.get_score())
                self.file.close()

                if not self.lvl > len(self.lvls) - 1:
                    self.rectangl.rect.x = 1 * 50
                    self.rectangl.rect.y = self.size[1] - 6 * 50

                    self.killings = 0
                    self.open_door = 0
                    self.score = 0

                    self.load_lvl()

                else:
                    file2 = open('check_close.txt', mode="w", encoding="utf-8")
                    file2.write('2')
                    file2.close()

                    self.running = False

                os.system('res_window.py')


            else:
                exit.sprites()[self.exit_coords.index((self.rectangl.rect.x, self.rectangl.rect.y))].kill()
                self.exit_coords.pop(self.exit_coords.index((self.rectangl.rect.x, self.rectangl.rect.y)))

                self.rectangl.rect.x = 1 * 50
                self.rectangl.rect.y = self.size[1] - 6 * 50

                self.open_door += 1

    def get_score(self):
        return str(self.score - 50 * self.killings + 200 * self.open_door + 100)

    def get_running(self):
        self.file2 = open('check_close.txt', mode="r", encoding="utf-8")
        if self.file2.readline() == '1':
            self.running = False
        self.file2.close()

        return self.running

    def down(self):
        for i in self.board_coords:
            if self.rectangl.rect.y == i[1] - 50 and self.rectangl.rect.x == i[0]:
                self.motion_back_y = False

        if self.rectangl.rect.y != 8 * 50 and not self.jump and self.motion_back_y and self.timer == 0:
            self.rectangl.rect.y += self.v

        if not self.motion_back_y:
            self.timer = 0

        self.motion_back_y = True

        if self.timer != 0:
            self.timer -= 1
        else:
            self.jump = False

        self.check_kill()
        self.check_win()

    def check(self):
        for i in self.board_coords:
            if self.rectangl.rect.x == i[0] - 50 and self.rectangl.rect.y == i[1]:
                self.motion_forward_x = False
            if self.rectangl.rect.x == i[0] + 50 and self.rectangl.rect.y == i[1]:
                self.motion_back_x = False
            if self.rectangl.rect.y - 50 == i[1] and self.rectangl.rect.x == i[0]:
                self.motion_forward_y = False


bloks = pygame.sprite.Group()
kill = pygame.sprite.Group()
exit = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

size = (16 * 50, 9 * 50)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('GREEN RECTANGL')

new_game = Play(size)
new_game.load_lvl()

clock = pygame.time.Clock()

bloks.draw(screen)
kill.draw(screen)
exit.draw(screen)

font = pygame.font.Font(None, 60)
text = font.render(
    new_game.get_score(), True, (255, 255, 255))
place = text.get_rect(
    center=(700, 25))
screen.blit(text, place)

file2 = open('check_close.txt', mode="w", encoding="utf-8")
file2.write('0')
file2.close()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                new_game.update_rect(2)
            if event.key == pygame.K_LEFT:
                new_game.update_rect(3)
            if event.key == pygame.K_SPACE:
                new_game.update_rect(1)

    screen.fill((0, 0, 0))

    bloks.draw(screen)
    kill.draw(screen)
    exit.draw(screen)
    all_sprites.draw(screen)

    text = font.render(
        new_game.get_score(), True, (255, 255, 255))
    screen.blit(text, place)

    new_game.down()

    if running:
        running = new_game.get_running()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
file2 = open('check_close.txt', mode="w", encoding="utf-8")
file2.write('2')
file2.close()
