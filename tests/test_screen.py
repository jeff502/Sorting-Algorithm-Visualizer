import pygame
import unittest
import asyncio
from unittest.mock import patch

from gui.screen import Screen
from gui.button import Button
from algorithms.algorithms import BubbleSort, SelectionSort, InsertionSort


class TestScreen(unittest.TestCase):

    def setUp(self):
        self.screen = Screen()
        pygame.init()

    def tearDown(self) -> None:
        self.screen = None

    def test_screen(self):
        assert self.screen.pause_game is False
        assert self.screen.game_running is True
        assert self.screen.fps == 60
        assert self.screen.index == 0
        assert self.screen.board is None
        assert self.screen.board_length is None
        assert self.screen.blocks == []
        assert self.screen.blocks_created is False
        assert self.screen.alg_buttons == []
        assert self.screen.alg_button_pressed is False
        assert self.screen.next_button is None
        assert self.screen.shown_alg_info is False
        assert self.screen.sort_method is None
        assert self.screen.complete is False
        assert self.screen.extra_loop is False
        assert self.screen.window == pygame.display.set_mode((900, 500))
        assert pygame.display.get_caption() == ('Algorithm Visualizer', 'Algorithm Visualizer')
        assert self.screen.background == (248, 244, 234)
        assert self.screen.pos_list == [75, 150, 225, 300, 375, 450, 525, 600, 675]
        assert self.screen.colors == [(0, 0, 0), (127, 127, 127), (255, 0, 0), (0, 255, 0), (0, 0, 255),
                                 (255, 255, 0), (0, 255, 255), (255, 0, 255), (165, 42, 42), (102, 0, 204)]

        # assert isinstance(self.screen.block_sprites, pygame.sprite)
        # assert type(self.screen.block_sprites) is pygame.sprite.Group()
        # assert self.screen.complete_sprite == pygame.sprite.GroupSingle()
        # assert self.screen.arrow_sprite == pygame.sprite.GroupSingle()
        # assert self.screen.index_sprite == pygame.sprite.GroupSingle()
        # assert self.screen.index_text == pygame.sprite.GroupSingle()
        # assert self.screen.algorithm_info == pygame.sprite.Group()

    def test_create_board(self):
        self.screen.create_board()
        self.screen.board.sort()
        assert self.screen.board == [1, 51, 101, 151, 201, 251, 301, 351, 401]
        assert self.screen.board_length == len(self.screen.board)

    def test_create_blocks(self):
        self.screen.create_board()
        self.screen.create_blocks()
        assert len(self.screen.blocks) == 9
        assert len(self.screen.block_sprites) == 9

        # maybe find a different way to test sprites

    def test_create_index_display(self):
        self.screen.create_index_display()
        assert isinstance(self.screen.index_sprite, pygame.sprite.GroupSingle)
        for text_sprite in self.screen.index_sprite:
            assert text_sprite.color == (0, 0, 0)
            assert text_sprite.text == "Index: 0"
            assert text_sprite.x == 0
            assert text_sprite.y == 450

            # Need to test font size and style

    def test_create_index_arrow(self):
        self.screen.create_index_arrow()
        assert isinstance(self.screen.arrow_sprite, pygame.sprite.GroupSingle)
        for text_sprite in self.screen.arrow_sprite:
            assert text_sprite.text == "↓"
            assert text_sprite.color == (0, 0, 0)
            assert text_sprite.x == 100
            assert text_sprite.y == 0

    def test_create_algorithm_info_display(self):
        sorting_algorithms = {
            "Insertion Sort": InsertionSort,
            "Selection Sort": SelectionSort,
            "Bubble Sort": BubbleSort
            }
        for name, sort_class in sorting_algorithms.items():
            self.screen.set_sorting_method(name)
            self.screen.create_algorithm_info_display()
            assert self.screen.sort_method is not None
            assert isinstance(self.screen.sort_method, sort_class)
            if sort_class == InsertionSort:
                assert self.screen.extra_loop is True

            algorithm_info = ""
            sort_class_info = "".join([text for text in sort_class.algorithm_info()])
            for line in self.screen.algorithm_info:
                algorithm_info += line.text

            assert algorithm_info is not None
            assert algorithm_info == sort_class_info
            self.screen.algorithm_info.empty()

    def test_create_buttons(self):
        self.screen.create_buttons()

        assert len(self.screen.alg_buttons) == 3
        assert "Insertion Sort" in self.screen.alg_buttons[0].text
        assert self.screen.alg_buttons[0].pos == (100, 100)
        assert "Selection Sort" in self.screen.alg_buttons[1].text
        assert self.screen.alg_buttons[1].pos == (225, 100)
        assert "Bubble Sort" in self.screen.alg_buttons[2].text
        assert self.screen.alg_buttons[2].pos == (350, 100)

    def test_create_next_button(self):
        self.screen.create_next_button()

        assert isinstance(self.screen.next_button, Button)
        assert self.screen.next_button.text == "Next"
        assert self.screen.next_button.pos == (750, 350)
        assert self.screen.next_button.width == 100
        assert self.screen.next_button.height == 100

    def test_create_complete_banner(self):
        self.screen.create_complete_banner()

        assert isinstance(self.screen.complete_sprite, pygame.sprite.GroupSingle)
        for complete_sprite in self.screen.complete_sprite:
            assert complete_sprite.text == "Complete!"
            assert complete_sprite.color == (0, 0, 0)
            assert complete_sprite.x == 200
            assert complete_sprite.y == 0
            assert complete_sprite.font.get_height() == 134

    def test_update_blocks(self):
        self.screen.create_board()
        self.screen.create_blocks()
        board_length = self.screen.board_length
        self.screen.update_blocks()
        test_updated_x_pos = [block.x for block in self.screen.blocks]
        assert self.screen.board_length == board_length
        assert self.screen.pos_list == test_updated_x_pos

    def test_update_buttons(self):
        self.screen.create_buttons()
        self.screen.update_buttons()
        button_pos = [button.pos for button in self.screen.alg_buttons]
        for b_pos in button_pos:
            x, y = b_pos
            r, g, b, _ = pygame.Surface.get_at(self.screen.window, (x + 5, y + 5))
            assert (r, g, b) == (87, 155, 177)

    def test_update_index_display(self):
        self.screen.create_board()
        self.screen.create_index_display()
        index_before_updating = self.screen.index
        self.screen.update_index_display()
        assert len(self.screen.index_sprite) == 1
        assert index_before_updating != self.screen.index

    def test_update_arrow_display(self):
        self.screen.create_board()
        self.screen.index = 1
        self.screen.board_length = 10
        self.screen.update_arrow_display()
        for sprite in self.screen.arrow_sprite:
            assert sprite.x == 175

        self.screen.index = 2
        self.screen.update_arrow_display()
        for sprite in self.screen.arrow_sprite:
            assert sprite.x == 250

        self.screen.index = 200
        for sprite in self.screen.arrow_sprite:
            assert sprite.x == 250

    def test_set_sorting_method(self):
        sorting_dict = {
            "Insertion Sort": InsertionSort,
            "Selection Sort": SelectionSort,
            "Bubble Sort": BubbleSort
        }
        for name, sorting_class in sorting_dict.items():
            self.screen.set_sorting_method(name)
            assert isinstance(self.screen.sort_method, sorting_class)
            if name == "Insertion Sort":
                assert self.screen.extra_loop is True
            else:
                assert self.screen.extra_loop is False
            self.screen.extra_loop = False

    def test_start(self):
        ...

    def test_event_handler(self):
        ...

    def test_start_up_creation(self):
        self.screen.start_up_creation("Insertion Sort")
        assert self.screen.board is not None
        assert len(self.screen.blocks) == 9
        assert len(self.screen.index_sprite) == 1
        assert self.screen.sort_method is not None
        assert self.screen.next_button is not None
        assert self.screen.alg_button_pressed is True
        assert self.screen.blocks_created is True

    def test_draw_sprites(self):
        self.screen.create_board()
        self.screen.create_blocks()
        self.screen.create_index_arrow()
        self.screen.create_index_display()
        self.screen.window.fill(self.screen.background)
        self.screen.draw_sprites()

        for block in self.screen.blocks:
            r, g, b, _ = self.screen.window.get_at((block.x, block.y))
            assert (r, g, b) in self.screen.colors

        for index_sprite in self.screen.index_sprite:
            r, g, b, _ = self.screen.window.get_at((index_sprite.x+3, index_sprite.y+12))
            assert (r, g, b) == index_sprite.color

        for arrow_sprite in self.screen.arrow_sprite:
            r, g, b, _ = self.screen.window.get_at((arrow_sprite.x+5, arrow_sprite.y+39))
            assert (r, g, b) == arrow_sprite.color

    def test_cleanup(self):
        self.screen.start_up_creation("Insertion Sort")
        self.screen.cleanup()
        r, g, b, _ = self.screen.window.get_at((0, 0))
        assert (r, g, b) == self.screen.background
        assert len(self.screen.block_sprites) == 0
        assert len(self.screen.index_sprite) == 0
        assert len(self.screen.arrow_sprite) == 0
        assert len(self.screen.blocks) == 0
        assert self.screen.index == 0
        assert self.screen.shown_alg_info is False
        assert self.screen.complete is False
        assert self.screen.blocks_created is False
        assert self.screen.alg_button_pressed is False
        assert self.screen.pause_game is True
        assert self.screen.extra_loop is False





if __name__ == "__main__":
    unittest.main()
