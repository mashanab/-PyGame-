import os
import sys
from random import randint

import pygame
import pygame_menu

pygame.init()

size = w, h = 300, 500  # размер окна
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Поймай еду')  # заголовок
pygame.display.set_icon(pygame.image.load('data/korzina.png'))  # иконка

speed_food = 1  # скорость, с которой падает первый спрайт, затем она увеличивается на 0.08 в функции createFood()
speed_korzina = 7  # скорость, с которой передвигается корзина

life = 3  # начальное количество жизней
score = 0  # начальное количество очков


def start_the_game():
    screen.fill((135, 206, 250))  # фон основного игрового окна

    # включение фоновой музыки
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    # 3000 миллисекунд = 3 секунды - время создания нового падающего объекта
    pygame.time.set_timer(pygame.USEREVENT, 3000)
    running = True

    clock = pygame.time.Clock()
    FPS = 60

    #  загрузка скатерти
    fullname1 = os.path.join('data', 'skatert.jpg')
    if not os.path.isfile(fullname1):
        print(f"Файл с изображением '{fullname1}' не найден")
        sys.exit()
    skatert = pygame.image.load(fullname1)

    #  загрузка фона для подсчета жизней
    fullname2 = os.path.join('data', 'life_fon.png')
    if not os.path.isfile(fullname2):
        print(f"Файл с изображением '{fullname2}' не найден")
        sys.exit()
    image2 = pygame.image.load(fullname2)
    life_fon = pygame.transform.scale(image2, (50, 50))
    life_font = pygame.font.SysFont('arial', 25)

    #  загрузка фона для подсчета очков
    fullname3 = os.path.join('data', 'score_fon.png')
    if not os.path.isfile(fullname3):
        print(f"Файл с изображением '{fullname3}' не найден")
        sys.exit()
    image3 = pygame.image.load(fullname3)
    score_fon = pygame.transform.scale(image3, (90, 40))
    score_font = pygame.font.SysFont('arial', 25)

    #  загрузка корзины
    fullname4 = os.path.join('data', 'korzina.png')
    if not os.path.isfile(fullname4):
        print(f"Файл с изображением '{fullname4}' не найден")
        sys.exit()
    image4 = pygame.image.load(fullname4)
    korzina = pygame.transform.scale(image4, (100, 50))
    korzina_rect = korzina.get_rect(centerx=w // 2, bottom=h - 95)  # начальные координаты корзины

    #  создания спрайта
    class Food(pygame.sprite.Sprite):
        def __init__(self, x, speed, surf, life, score, group):
            pygame.sprite.Sprite.__init__(self)
            self.image = surf
            self.rect = self.image.get_rect(center=(x, 0))
            self.speed = speed
            self.life = life
            self.score = score
            self.add(group)  # добавление спрайта в группу

        # логика падения спрайта
        def update(self, *args):
            if self.rect.y < args[0] - 20:
                self.rect.y += self.speed
            else:
                self.kill()

    # изображения падающих объектов
    food_images = ['data/apple.png', 'data/avocado.png', 'data/burger.png', 'data/cookies.png', 'data/orange.png',
                   'data/pizza.png', 'data/sushi.png',
                   'data/boot.png', 'data/disk.png', 'data/phone.png', 'data/toy.png']

    # словарь со значением количества жизней
    food_life = {'data/apple.png': 0, 'data/avocado.png': 0, 'data/burger.png': 0,
                 'data/cookies.png': 0, 'data/orange.png': 0,
                 'data/pizza.png': 0, 'data/sushi.png': 0,
                 'data/boot.png': 1, 'data/disk.png': 1,
                 'data/phone.png': 1, 'data/toy.png': 1}

    # словрь со значением очков
    food_score = {'data/apple.png': 50, 'data/avocado.png': 50, 'data/burger.png': 50,
                  'data/cookies.png': 100, 'data/orange.png': 100,
                  'data/pizza.png': 200, 'data/sushi.png': 200,
                  'data/boot.png': 0, 'data/disk.png': 0,
                  'data/phone.png': 0, 'data/toy.png': 0}

    # загрузка изображений падающих  объектов
    food_surf1 = [pygame.image.load(i).convert_alpha() for i in food_images]

    # преобразование изображений
    food_surf = [pygame.transform.scale(image, (40, 40)) for image in food_surf1]

    # группа, содержащая все спрайты
    food = pygame.sprite.Group()

    # создание нового падающего объекта
    def createFood(group):
        global speed_food
        index = randint(0, len(food_surf) - 1)
        x = randint(20, w - 20)
        speed_food += 0.08
        return Food(x, speed_food, food_surf[index], food_life[food_images[index]],
                    food_score[food_images[index]], group)

    createFood(food)

    # проверка столкновения падающих объектов и корзины; проверка съедобный ли объект поймала корзина
    def catchFood():
        global life
        global score
        global speed_food
        for i in food:
            if korzina_rect.collidepoint(i.rect.center):
                life -= i.life  # жизнь
                score += i.score  # очки

                #  появление окна-меню, когда количество жизней равно нулю
                if life == 0:
                    size = 300, 500
                    new_screen = pygame.display.set_mode(size)
                    new_menu = pygame_menu.Menu(500, 300, 'YOU DIED', theme=pygame_menu.themes.THEME_DARK)
                    new_menu.add_label(f"Ваш счёт: {score}")
                    new_menu.add_button('Играть снова', start_the_game)
                    new_menu.add_button('Выход', pygame_menu.events.EXIT)

                    # добавление звука проигрыша
                    pygame.mixer.music.load('fail_music.mp3')
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(0.4)

                    life = 3
                    score = 0
                    speed_food = 1
                    new_menu.mainloop(new_screen)
                i.kill()

    #  главный цикл игры
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # событие, по которому каждые 3 секунды создается новый спрайт
            elif event.type == pygame.USEREVENT:
                createFood(food)

        # движение корзины с помощью клавиш-стрелок
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            korzina_rect.x -= speed_korzina
            if korzina_rect.x < 0:
                korzina_rect.x = 0
        elif keys[pygame.K_RIGHT]:
            korzina_rect.x += speed_korzina
            if korzina_rect.x > w - korzina_rect.width:
                korzina_rect.x = w - korzina_rect.width

    # отрисовка нового кадра
        catchFood()
        screen.fill((135, 206, 250))

        # отображение количества жизней
        screen.blit(life_fon, (0, 0))
        text1 = life_font.render(str(life), 1, (0, 0, 0))
        screen.blit(text1, (19, 11))

        # отображение количества очков
        screen.blit(score_fon, (210, 5))
        text2 = score_font.render(str(score), 1, (0, 0, 0))
        screen.blit(text2, (235, 11))

        screen.blit(skatert, (0, 400))
        food.draw(screen)

        # отображение корзины и ее расположение
        screen.blit(korzina, korzina_rect)

        pygame.display.flip()

        clock.tick(FPS)

        food.update(h)


# меню заставки игры
menu = pygame_menu.Menu(500, 300, 'Welcome', theme=pygame_menu.themes.THEME_GREEN)

menu.add_button('Играть', start_the_game)
menu.add_button('Выход', pygame_menu.events.EXIT)

menu.mainloop(screen)
