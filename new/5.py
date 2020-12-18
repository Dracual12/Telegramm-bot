import pygame, os, sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


if __name__ == '__main__':
    image = load_image("arrow.png")
    pygame.init()
    pygame.display.set_caption('Свой курсор')
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)

    running = True
    v = 20
    fps = 60
    clock = pygame.time.Clock()
    pos = (0, 0)
    while running:
        screen.fill((0, 0, 0))
        if pygame.mouse.get_focused():
            screen.blit(image, pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()
