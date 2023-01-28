import pygame
import random
import os
from pygame.math import Vector2

# Initialize the game
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Snake")
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 25)


# Game Assets
APPLE = pygame.image.load(os.path.join("assets", "apple.png"))
HEAD_UP = pygame.image.load(os.path.join("assets", "head_up.png"))
HEAD_DOWN = pygame.image.load(os.path.join("assets", "head_down.png"))
HEAD_RIGHT = pygame.image.load(os.path.join("assets", "head_right.png"))
HEAD_LEFT = pygame.image.load(os.path.join("assets", "head_left.png"))

TAIL_UP = pygame.image.load(os.path.join("assets", "tail_up.png"))
TAIL_DOWN = pygame.image.load(os.path.join("assets", "tail_down.png"))
TAIL_RIGHT = pygame.image.load(os.path.join("assets", "tail_right.png"))
TAIL_LEFT = pygame.image.load(os.path.join("assets", "tail_left.png"))

BODY_VERTICAL = pygame.image.load(os.path.join("assets", "body_vertical.png"))
BODY_HORIZONTAL = pygame.image.load(os.path.join("assets", "body_horizontal.png"))

BODY_TR = pygame.image.load(os.path.join("assets", "body_tr.png"))
BODY_TL = pygame.image.load(os.path.join("assets", "body_tl.png"))
BODY_BR = pygame.image.load(os.path.join("assets", "body_br.png"))
BODY_BL = pygame.image.load(os.path.join("assets", "body_bl.png"))
crunch_sound = pygame.mixer.Sound('assets/crunch.wav')
crunch_sound.set_volume(0.1)


# Objects
class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)
        self.head = HEAD_RIGHT
        self.tail = TAIL_LEFT

    def draw(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                self.head_direction()
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                self.tail_direction()
                screen.blit(self.tail, block_rect)
            else:
                # Draw the correct snake body party based on X/Y Vector
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(BODY_VERTICAL, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(BODY_HORIZONTAL, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(BODY_TL, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(BODY_BL, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(BODY_TR, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(BODY_BR, block_rect)

    def move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def add_body(self):
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    # Draw the correct orientation of Head / Tail based on vector
    def head_direction(self):
        relation_vector = self.body[1] - self.body[0]
        if relation_vector == Vector2(1, 0):
            self.head = HEAD_LEFT
        elif relation_vector == Vector2(-1, 0):
            self.head = HEAD_RIGHT
        elif relation_vector == Vector2(0, 1):
            self.head = HEAD_UP
        elif relation_vector == Vector2(0, -1):
            self.head = HEAD_DOWN

    def tail_direction(self):
        relation_vector = self.body[-1] - self.body[-2]
        if relation_vector == Vector2(1, 0):
            self.tail = TAIL_RIGHT
        elif relation_vector == Vector2(-1, 0):
            self.tail = TAIL_LEFT
        elif relation_vector == Vector2(0, 1):
            self.tail = TAIL_DOWN
        elif relation_vector == Vector2(0, -1):
            self.tail = TAIL_UP

    def play_sound(self):
        crunch_sound.play()

    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)


class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.randomize()

    def draw(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(APPLE, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_gameover()

    def draw(self):
        self.checkered_grass()
        self.snake.draw()
        self.fruit.draw()
        self.score()

    def check_collision(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit.randomize()
            self.snake.add_body()
            self.snake.play_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_gameover(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    # Draw the checkered grass game board.
    def checkered_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(f"{score_text}", 1, (56, 74, 12))
        score_rect = score_surface.get_rect(center=(cell_number * cell_size - 60, cell_number * cell_size - 40))
        apple_rect = APPLE.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, score_rect.width + apple_rect.width + 10, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        screen.blit(score_surface, score_rect)
        screen.blit(APPLE, apple_rect)


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

        # Take user input and make sure user can't move in opposite direction
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and main_game.snake.direction != Vector2(1, 0):
            main_game.snake.direction = Vector2(-1, 0)
        if key[pygame.K_d] and main_game.snake.direction != Vector2(-1, 0):
            main_game.snake.direction = Vector2(1, 0)
        if key[pygame.K_w] and main_game.snake.direction != Vector2(0, 1):
            main_game.snake.direction = Vector2(0, -1)
        if key[pygame.K_s] and main_game.snake.direction != Vector2(0, -1):
            main_game.snake.direction = Vector2(0, 1)

    screen.fill((175,215,70))
    main_game.draw()
    pygame.display.update()
    clock.tick(60)

