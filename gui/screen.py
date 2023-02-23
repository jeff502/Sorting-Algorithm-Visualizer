import sys
from random import shuffle

import pygame

from algorithms.algorithms import InsertionSort, SelectionSort, BubbleSort
from spirtes.block_sprites import BlockSprite
from spirtes.text_sprites import TextSprite
from gui.button import Button


class Screen:
    def __init__(self):
        self.pause_game = False
        self.game_running = True
        self.fps = 60
        self.index = 0
        self.window = pygame.display.set_mode((900, 500))
        pygame.display.set_caption("Algorithm Visualizer")
        self.background = (248, 244, 234)
        self.pos_list = [75, 150, 225, 300, 375, 450, 525, 600, 675]
        self.colors = [(0, 0, 0), (127, 127, 127), (255, 0, 0), (0, 255, 0), (0, 0, 255),
                       (255, 255, 0), (0, 255, 255), (255, 0, 255), (165, 42, 42), (102, 0, 204)]
        self.board = None
        self.board_length = None
        self.blocks = []
        self.blocks_created = False
        self.alg_buttons = []
        self.alg_button_pressed = False
        self.next_button = None
        self.shown_alg_info = False
        self.sort_method = None
        self.complete = False
        self.extra_loop = False

        self.block_sprites = pygame.sprite.Group()
        self.complete_sprite = pygame.sprite.GroupSingle()
        self.arrow_sprite = pygame.sprite.GroupSingle()
        self.index_sprite = pygame.sprite.GroupSingle()
        self.algorithm_info = pygame.sprite.Group()

    def create_board(self):
        randomized_board = [i for i in range(1, 451, 50)]
        shuffle(randomized_board)
        self.board = randomized_board
        self.board_length = len(self.board)

    def create_blocks(self):
        x_pos = 75
        for i in range(self.board_length):
            num = abs(i % 10)
            color = self.colors[num]
            block = BlockSprite(x_pos, self.board[i], color)
            self.blocks.append(block)
            self.block_sprites.add(block)
            x_pos += 75

    def create_index_display(self):
        index_display = TextSprite(f"Index: {self.index}", 30, (0, 0, 0), 0, 450)
        self.index_sprite.add(index_display)

    def create_index_arrow(self, x=100):
        arrow_display = TextSprite(f"↓", 40, (0, 0, 0), x, 0)
        self.arrow_sprite.add(arrow_display)

    def create_algorithm_info_display(self):
        alg_text = self.sort_method.algorithm_info()
        y = 50
        for text in alg_text:
            algorithm_info_display = TextSprite(f"{text}", 18, (0, 0, 0), 50, y)
            self.algorithm_info.add(algorithm_info_display)
            y += 50

    def create_buttons(self):
        algorithms = ["Insertion Sort", "Selection Sort", "Bubble Sort"]
        x = 100
        for alg in algorithms:
            button = Button((x, 100), 100, 100, alg, self.window)
            self.alg_buttons.append(button)
            x += 125

    def create_next_button(self):
        button = Button((750, 350), 100, 100, "Next", self.window)
        self.next_button = button

    def create_complete_banner(self):
        complete_banner = TextSprite("Complete!", 100, (0, 0, 0), 200, 0)
        self.complete_sprite.add(complete_banner)

    def update_blocks(self):
        for i, block in enumerate(self.blocks):
            block.x = self.pos_list[i]
            block.rect.topleft = [block.x, block.y]

    def update_buttons(self):
        for b in self.alg_buttons:
            b.draw_button()

    def update_index_display(self):
        self.index += 1
        self.index_sprite.empty()
        self.create_index_display()
        self.index_sprite.draw(self.window)

    def update_arrow_display(self):
        if self.index >= self.board_length:
            return
        index_pos = {0: 100, 1: 175, 2: 250, 3: 325, 4: 400, 5: 475, 6: 550, 7: 625, 8: 700}
        self.arrow_sprite.empty()
        self.create_index_arrow(index_pos[self.index])
        self.arrow_sprite.draw(self.window)

    def set_sorting_method(self, name):
        sorting_dict = {"Insertion Sort": InsertionSort, "Selection Sort": SelectionSort, "Bubble Sort": BubbleSort}
        if sorting_dict[name] == InsertionSort:
            self.extra_loop = True
        self.sort_method = sorting_dict[name](self.blocks)

    def start(self):
        self.window.fill(self.background)
        self.create_buttons()
        clock = pygame.time.Clock()
        while self.game_running:
            self.event_handler()
            self.window.fill(self.background)
            if self.complete:
                self.cleanup()
                self.next_button.draw_button()
                self.create_complete_banner()
            if not self.pause_game:
                if not self.alg_button_pressed:
                    self.update_buttons()
                if self.alg_button_pressed:
                    if self.blocks_created and not self.shown_alg_info:
                        self.algorithm_info.draw(self.window)
                    elif self.blocks_created and self.shown_alg_info:
                        self.window.fill(self.background)
                        self.draw_sprites()
                    self.next_button.draw_button()
            else:
                self.next_button.draw_button()
                self.complete_sprite.draw(self.window)
            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_running = False
                    pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.next_button:
                    if self.next_button.check_button_clicked():
                        if self.pause_game:
                            self.pause_game = False

                        if not self.shown_alg_info:
                            self.shown_alg_info = True

                        elif not self.complete and self.alg_button_pressed:
                            if self.sort_method.counter >= len(self.blocks):
                                self.complete = True
                            else:
                                self.blocks = self.sort_method.sort()
                                self.update_blocks()
                                self.update_index_display()
                                self.update_arrow_display()
                                if self.sort_method.counter > len(self.blocks) and not self.extra_loop:
                                    self.complete = True
                for b in self.alg_buttons:
                    button_pressed = b.check_button_clicked()
                    if button_pressed:
                        self.start_up_creation(b.text)

    def start_up_creation(self, text):
        self.create_board()
        self.create_blocks()
        self.create_index_display()
        self.create_index_arrow()
        self.set_sorting_method(text)
        self.create_algorithm_info_display()
        self.create_next_button()
        self.alg_button_pressed = True
        self.blocks_created = True

    def draw_sprites(self):
        self.block_sprites.draw(self.window)
        self.index_sprite.draw(self.window)
        self.arrow_sprite.draw(self.window)

    def cleanup(self):
        self.window.fill(self.background)
        self.block_sprites.empty()
        self.index_sprite.empty()
        self.arrow_sprite.empty()
        self.blocks = []
        self.index = 0
        self.shown_alg_info = False
        self.complete = False
        self.blocks_created = False
        self.alg_button_pressed = False
        self.pause_game = True
        self.extra_loop = False
