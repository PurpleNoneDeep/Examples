import random

import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Игрок движется за курсором")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
player_image = "alienYellow_walk2.png"
food_image = "alienYellow_walk2.png"
wrong_food_image = "alienYellow_walk2.png"

button_width = 200
button_height = 50
button_padding = 20

image = pygame.Surface((button_width, button_height))
image.fill(BLUE)
button1_rect = image.get_rect()
button1_rect.center = (screen_width / 2, screen_height / 2 - button_height - button_padding)

image2 = pygame.Surface((button_width, button_height))
image2.fill(BLUE)
button2_rect = image.get_rect()
button2_rect.center = (screen_width / 2, screen_height / 2 + button_height + button_padding)

selected_button = None

score = 0
font = pygame.font.Font(None, 34)
text = font.render(f"Score: {score}", True, (BLACK))
score_rect = text.get_rect(center=(50, 50))

btn_text1 = font.render("Кнопка 1", True, WHITE)
btn_text2 = font.render("Кнопка 2", True, WHITE)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(player_image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, target_pos, width, height):
        self.rect.x = target_pos[0] - width // 2
        self.rect.y = target_pos[1] - height // 2


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(food_image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(0, screen_height)


class WrongFood(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(wrong_food_image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(0, screen_height)


player = Player(0, 0, 50, 50)
player_sprites = pygame.sprite.Group()
player_sprites.add(player)

food = Food(50, 50, 25, 25)
food_sprites = pygame.sprite.Group()
food_sprites.add(food)
food2 = WrongFood(50, 50, 25, 25)
food2_sprites = pygame.sprite.Group()
food2_sprites.add(food2)
# Основной цикл
running = True
menu = True
while running:
    if menu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if selected_button == 1:
                    menu = False
                elif selected_button == 2:
                    pygame.quit()
        mouse_position = pygame.mouse.get_pos()
        if button1_rect.collidepoint(mouse_position):
            selected_button = 1
        elif button2_rect.collidepoint(mouse_position):
            selected_button = 2
        else:
            selected_button = 0

        if selected_button == 1:
            image.fill(WHITE)
        else:
            image.fill(BLUE)
        if selected_button == 2:
            image2.fill(WHITE)
        else:
            image2.fill(BLUE)

        screen.blit(image, button1_rect)
        screen.blit(btn_text1,
                    (button1_rect.centerx - text.get_width() // 2, button1_rect.centery - text.get_height() // 2))

        screen.blit(image2, button2_rect)
        screen.blit(btn_text2,
                    (button2_rect.centerx - text.get_width() // 2, button2_rect.centery - text.get_height() // 2))

        pygame.display.flip()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()
        player_sprites.update(mouse_pos, 50, 50)

        if pygame.sprite.collide_rect(player, food):
            food_sprites.update()
            score += 1
            text = font.render(f"Score: {score}", True, (BLACK))

        screen.fill(WHITE)

        player_sprites.draw(screen)
        food_sprites.draw(screen)
        food2_sprites.draw(screen)
        if pygame.sprite.collide_rect(player, food2):
            player.kill()

        screen.blit(text, score_rect)
        pygame.display.flip()

pygame.quit()
sys.exit()

