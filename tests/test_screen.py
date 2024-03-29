import pygame
import unittest
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

    def test_init(self):
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
        assert pygame.display.get_caption() == (
            "Algorithm Visualizer",
            "Algorithm Visualizer",
        )
        assert self.screen.background == (248, 244, 234)
        assert self.screen.pos_list == [75, 150, 225, 300, 375, 450, 525, 600, 675]
        assert self.screen.colors == [
            (0, 0, 0),
            (127, 127, 127),
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255),
            (165, 42, 42),
            (102, 0, 204),
        ]

        assert isinstance(self.screen.block_sprites, pygame.sprite.Group)
        assert isinstance(self.screen.complete_sprite, pygame.sprite.GroupSingle)
        assert isinstance(self.screen.arrow_sprite, pygame.sprite.GroupSingle)
        assert isinstance(self.screen.index_sprite, pygame.sprite.GroupSingle)
        assert isinstance(self.screen.algorithm_info, pygame.sprite.Group)

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
            "Bubble Sort": BubbleSort,
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
        self.screen.create_sorting_buttons()

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
        self.screen.create_sorting_buttons()
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

    def test_update_index_display_index_limit(self):
        self.screen.create_board()
        self.screen.create_index_display()
        self.screen.index = 8
        self.screen.update_index_display()
        assert len(self.screen.index_sprite) == 1
        assert self.screen.index == 8

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
            "Bubble Sort": BubbleSort,
        }
        for name, sorting_class in sorting_dict.items():
            self.screen.set_sorting_method(name)
            assert isinstance(self.screen.sort_method, sorting_class)
            if name == "Insertion Sort":
                assert self.screen.extra_loop is True
            else:
                assert self.screen.extra_loop is False
            self.screen.extra_loop = False

    def test_event_handler(self):
        self.screen.event_handler()

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
        self.screen.draw_sprites()

        for block in self.screen.blocks:
            r, g, b, _ = self.screen.window.get_at((block.x, block.y))
            assert (r, g, b) in self.screen.colors

        for index_sprite in self.screen.index_sprite:
            r, g, b, _ = self.screen.window.get_at(
                (index_sprite.x + 3, index_sprite.y + 12)
            )
            assert (r, g, b) == index_sprite.color

        for arrow_sprite in self.screen.arrow_sprite:
            r, g, b, _ = self.screen.window.get_at(
                (arrow_sprite.x + 5, arrow_sprite.y + 39)
            )
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
        assert self.screen.pause_game is False
        assert self.screen.extra_loop is False

    def test_event_handler_with_escape(self):
        with patch(
            "pygame.event.get",
            return_value=[pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})],
        ):
            assert self.screen.game_running is True
            self.screen.event_handler()
            assert self.screen.game_running is False

    def test_event_handler_pygame_quit(self):
        with patch("pygame.event.get", return_value=[pygame.event.Event(pygame.QUIT)]):
            assert self.screen.game_running is True
            self.screen.event_handler()
            assert self.screen.game_running is False

    def test_event_handler_with_mouse_button_down_insertion_sort(self):
        self.screen.create_sorting_buttons()
        button_mock = [True, False, False]

        with patch(
            "pygame.event.get",
            return_value=[
                pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)}
                )
            ],
        ), patch.object(Button, "check_button_clicked", side_effect=button_mock):
            assert self.screen.game_running is True

            self.screen.event_handler()
            assert self.screen.game_running is True
            assert self.screen.board is not None
            assert len(self.screen.blocks) == 9
            assert self.screen.index_sprite is not None
            assert self.screen.arrow_sprite is not None
            assert self.screen.sort_method.__class__.__name__ == "InsertionSort"
            assert self.screen.algorithm_info is not None
            assert self.screen.next_button is not None
            assert self.screen.alg_button_pressed is True
            assert self.screen.blocks_created is True

    def test_event_handler_with_mouse_button_down_selection_sort(self):
        self.screen.create_sorting_buttons()
        button_mock = [False, True, False]

        with patch(
            "pygame.event.get",
            return_value=[
                pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)}
                )
            ],
        ), patch.object(Button, "check_button_clicked", side_effect=button_mock):
            assert self.screen.game_running is True
            self.screen.event_handler()
            assert self.screen.game_running is True
            assert self.screen.board is not None
            assert len(self.screen.blocks) == 9
            assert self.screen.index_sprite is not None
            assert self.screen.arrow_sprite is not None
            assert self.screen.sort_method.__class__.__name__ == "SelectionSort"
            assert self.screen.algorithm_info is not None
            assert self.screen.next_button is not None
            assert self.screen.alg_button_pressed is True
            assert self.screen.blocks_created is True

    def test_event_handler_with_mouse_button_down_bubble_sort(self):
        self.screen.create_sorting_buttons()
        button_mock = [False, False, True]

        with patch(
            "pygame.event.get",
            return_value=[
                pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)}
                )
            ],
        ), patch.object(Button, "check_button_clicked", side_effect=button_mock):
            assert self.screen.game_running is True
            self.screen.event_handler()
            assert self.screen.game_running is True
            assert self.screen.board is not None
            assert len(self.screen.blocks) == 9
            assert self.screen.index_sprite is not None
            assert self.screen.arrow_sprite is not None
            assert self.screen.sort_method.__class__.__name__ == "BubbleSort"
            assert self.screen.algorithm_info is not None
            assert self.screen.next_button is not None
            assert self.screen.alg_button_pressed is True
            assert self.screen.blocks_created is True

    def test_event_handler_next_button_shown_alg_info(self):
        self.screen.create_next_button()

        button_mock = [True]

        with patch(
            "pygame.event.get",
            return_value=[
                pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)}
                )
            ],
        ), patch.object(Button, "check_button_clicked", side_effect=button_mock):
            # Write a test for self.screen.pause_game
            assert self.screen.game_running is True
            assert self.screen.shown_alg_info is False
            self.screen.event_handler()
            assert self.screen.shown_alg_info is True
            assert self.screen.pause_game is False

    def test_event_handler_next_button_alg_button_pressed_check_counter_complete(self):
        # Testing if screen.sort_method.counter >= len(self.blocks) self.complete == True
        self.screen.create_next_button()
        self.screen.alg_button_pressed = True
        self.screen.shown_alg_info = True
        self.screen.create_board()
        self.screen.create_blocks()  # Len of blocks == 9
        self.screen.set_sorting_method("Insertion Sort")
        button_mock = [True]

        with patch(
            "pygame.event.get",
            return_value=[
                pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)}
                )
            ],
        ), patch.object(Button, "check_button_clicked", side_effect=button_mock):
            self.screen.sort_method.counter = 9
            assert self.screen.complete is False
            self.screen.event_handler()
            assert self.screen.complete is True

    def test_event_handler_next_button_and_alg_button_pressed_check_counter_not_completed(
        self,
    ):
        # Testing the "else" with counter at 0
        self.screen.create_next_button()
        self.screen.alg_button_pressed = True
        self.screen.shown_alg_info = True

        self.screen.create_board()
        self.screen.create_blocks()
        self.screen.create_index_arrow()
        self.screen.set_sorting_method("Insertion Sort")
        button_mock = [True]

        with patch(
            "pygame.event.get",
            return_value=[
                pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)}
                )
            ],
        ), patch.object(Button, "check_button_clicked", side_effect=button_mock):
            assert self.screen.game_running is True
            assert self.screen.shown_alg_info is True
            assert self.screen.complete is False
            assert self.screen.sort_method.counter == 0
            assert self.screen.index == 0
            for arrow in self.screen.arrow_sprite:
                assert arrow.x == 100
            for index, block in enumerate(self.screen.blocks):
                assert block.x == self.screen.pos_list[index]

            self.screen.event_handler()

            assert self.screen.sort_method.counter == 1
            assert self.screen.index == 1

            assert self.screen.complete is False
            assert self.screen.shown_alg_info is True
            assert self.screen.pause_game is False
            for arrow in self.screen.arrow_sprite:
                assert arrow.x == 175
            for index, block in enumerate(self.screen.blocks):
                assert block.x == self.screen.pos_list[index]

    def test_event_handler_selection_sort_equal_after_sorting(self):
        # Testing self.screen.sort_method.counter == len(self.blocks) after the line
        # "self.blocks = self.sort_method.sort()" and update methods ran.
        self.screen.create_next_button()
        self.screen.alg_button_pressed = True
        self.screen.shown_alg_info = True

        self.screen.create_board()
        self.screen.create_blocks()
        self.screen.create_index_arrow()
        self.screen.set_sorting_method(
            "Selection Sort"
        )  # Insertion Sort would flag "screen.extra_loop" to True.
        self.screen.sort_method.counter = (
            8  # Setting counter to be larger than the length of self.blocks
        )
        button_mock = [True]

        with patch(
            "pygame.event.get",
            return_value=[
                pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)}
                )
            ],
        ), patch.object(Button, "check_button_clicked", side_effect=button_mock):
            assert self.screen.extra_loop is False
            assert self.screen.complete is False
            self.screen.event_handler()
            assert self.screen.complete is True

    def test_event_handler_insertion_sort_equal_after_update(self):
        # Testing self.complete == False
        # Insertion Sort flags screen.extra_loop
        self.screen.create_next_button()
        self.screen.alg_button_pressed = True
        self.screen.shown_alg_info = True

        self.screen.create_board()
        self.screen.create_blocks()
        self.screen.create_index_arrow()
        self.screen.set_sorting_method(
            "Insertion Sort"
        )  # Insertion Sort would flag "screen.extra_loop" to True.
        self.screen.sort_method.counter = (
            8  # Setting counter to be larger than the length of self.blocks
        )
        button_mock = [True]

        with patch(
            "pygame.event.get",
            return_value=[
                pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)}
                )
            ],
        ), patch.object(Button, "check_button_clicked", side_effect=button_mock):
            assert self.screen.extra_loop is True
            assert self.screen.complete is False
            self.screen.event_handler()
            assert self.screen.complete is False

    def test_event_handler_next_button_pause_game(self):
        ...

    def test_start(self):
        ...


if __name__ == "__main__":
    unittest.main()
