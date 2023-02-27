import unittest
from unittest.mock import patch

import pygame
from gui.button import Button


class TestScreen(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.test_surface = pygame.display.set_mode((900, 500))
        self.button = Button(
            (0, 0), 100, 100, "Testing", self.test_surface
        )

    def tearDown(self) -> None:
        self.button = None

    def test_init(self):
        assert self.button.pos == (0, 0)
        assert self.button.width == 100
        assert self.button.height == 100
        assert self.button.text == "Testing"
        assert isinstance(self.button.window, pygame.Surface)
        assert self.button.button_color == (87, 155, 177)
        assert self.button.hover_color == (225, 215, 198)
        assert self.button.click_color == (236, 232, 221)
        assert self.button.text_color == (0, 0, 0)
        assert isinstance(self.button.top_rect, pygame.Rect)
        assert self.button.top_color == self.button.button_color
        assert isinstance(self.button.bottom_rect, pygame.Rect)
        assert self.button.bottom_color == self.button.hover_color
        assert isinstance(self.button.text_surf, pygame.Surface)
        assert isinstance(self.button.text_rect, pygame.Rect)
        assert self.button.clicked is False

    def test_draw_button(self):
        self.button.draw_button()
        assert self.test_surface.get_at((5, 5)) == self.button.button_color

    @patch('pygame.mouse.get_pressed', return_value=[True, False, False])
    @patch('pygame.mouse.get_pos', return_value=(0, 0))
    def test_check_button_clicked(self, mock_get_pos, mock_get_pressed):

        # Create a mock rect that always returns True for collide point
        mock_rect = MockRect(0, 0, 100, 100)
        mock_rect._collidepoint_return_value = True

        # Set the top_rect attribute of my_obj to the mock rect
        self.button.top_rect = mock_rect

        # Call check_button_clicked and assert that it returns True
        assert self.button.check_button_clicked() is True
        assert self.button.top_color == self.button.hover_color

        # Set the mock rect to always return False for collide point
        mock_rect._collidepoint_return_value = False

        # Call check_button_clicked and assert that it returns False
        assert self.button.check_button_clicked() is False
        assert self.button.top_color == self.button.button_color


class MockRect(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._collidepoint_return_value = False

    def collidepoint(self, *args):
        return self._collidepoint_return_value