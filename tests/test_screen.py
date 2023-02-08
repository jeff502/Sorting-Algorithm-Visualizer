from gui.screen import Screen
import pygame
from unittest.mock import patch


def test_screen():
    screen = Screen()
    assert screen.pause_game is False
    assert screen.game_running is True
    assert screen.fps == 60
    assert screen.index == 0
    assert screen.board is None
    assert screen.board_length is None
    assert screen.blocks == []
    assert screen.blocks_created is False
    assert screen.alg_buttons == []
    assert screen.alg_button_pressed is False
    assert screen.next_button is None
    assert screen.shown_alg_info is False
    assert screen.sort_method is None
    assert screen.complete is False
    assert screen.extra_loop is False
    assert screen.window == pygame.display.set_mode((900, 500))
    assert pygame.display.get_caption() == ('Algorithm Visualizer', 'Algorithm Visualizer')
    assert screen.background == (248, 244, 234)
    assert screen.pos_list == [75, 150, 225, 300, 375, 450, 525, 600, 675]
    assert screen.colors == [(0, 0, 0), (127, 127, 127), (255, 0, 0), (0, 255, 0), (0, 0, 255),
                             (255, 255, 0), (0, 255, 255), (255, 0, 255), (165, 42, 42), (102, 0, 204)]

    # assert isinstance(screen.block_sprites, pygame.sprite.Group())
    # assert type(screen.block_sprites) is pygame.sprite.Group()
    # assert screen.complete_sprite == pygame.sprite.GroupSingle()
    # assert screen.arrow_sprite == pygame.sprite.GroupSingle()
    # assert screen.index_sprite == pygame.sprite.GroupSingle()
    # assert screen.index_text == pygame.sprite.GroupSingle()
    # assert screen.algorithm_info == pygame.sprite.Group()


def test_create_board():
    screen = Screen()
    screen.create_board()
    screen.board.sort()
    assert screen.board == [1, 51, 101, 151, 201, 251, 301, 351, 401]
    assert screen.board_length == len(screen.board)


def test_create_blocks():
    screen = Screen()
    screen.create_board()
    screen.create_blocks()
    assert len(screen.blocks) == 9
    assert len(screen.block_sprites) == 9
    # maybe find a different way to test sprites


def test_create_index_display():
    screen = Screen()
    pygame.init()
    screen.create_index_display()
    assert isinstance(screen.index_sprite, pygame.sprite.GroupSingle)
    for sprite in screen.index_sprite:
        assert sprite.color == (0, 0, 0)
        assert sprite.text == "Index: 0"
        assert sprite.font == pygame.font.SysFont("segoeui", 30)
        assert sprite.x == 0
        assert sprite.y == 450
