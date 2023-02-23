import unittest
from random import shuffle

from algorithms.algorithms import InsertionSort, SelectionSort, BubbleSort
from spirtes.block_sprites import BlockSprite


class TestInsertionSort(unittest.TestCase):

    def setUp(self):
        block_values = [201, 101, 301, 51, 1, 151, 401, 351, 251]
        self.blocks = [BlockSprite(0, h, (0, 0, 0)) for h in block_values]
        self.sorter = InsertionSort(self.blocks)
        self.block_len = len(self.blocks)
        self.COMPLETED_SORT = [1, 51, 101, 151, 201, 251, 301, 351, 401]

    def tearDown(self) -> None:
        self.sorter = None
        self._blocks = None
        self.block_len = None
        self.COMPLETED_SORT = None

    def test_init(self):
        assert self.sorter.counter == 0
        assert self.sorter.blocks == self.blocks
        assert self.sorter.block_len == self.block_len

    def test_sort_once(self):
        # The first pass shouldn't change any vals
        self.sorter.sort()
        assert self.sorter.counter == 1
        assert self.sorter.blocks == self.blocks
        assert self.sorter.block_len == self.block_len

    def test_sort_several_times(self):
        for i in range(5):
            self.sorter.sort()

        insertion_sort_block_values = [block.height for block in self.sorter.blocks]
        assert self.sorter.counter == 5
        assert insertion_sort_block_values == [1, 51, 101, 201, 301, 151, 401, 351, 251]

    def test_sort_nine_times(self):
        # It should only take 9 calls to fully sort this list
        for i in range(9):
            self.sorter.sort()

        insertion_sort_block_values = [block.height for block in self.sorter.blocks]
        assert self.sorter.counter == 9
        assert insertion_sort_block_values == self.COMPLETED_SORT

    def test_sort_hundred_times(self):
        for i in range(100):
            self.sorter.sort()

        insertion_sort_block_values = [block.height for block in self.sorter.blocks]
        assert self.sorter.counter == 9
        assert insertion_sort_block_values == self.COMPLETED_SORT

    def test_algorithm_info(self):
        expected_output = [
            "Insertion sort is a simple sorting algorithm that builds the final sorted array one item at a time by "
            "comparisons.",
            "In this visualization, you'll see an array being updated one item at a time as the index increases.",
            "Time complexity: Best: Ω(n), Average: Θ(n^2), Worst: O(n^2)",
            "Space Complexity: O(1)"
            ]
        assert self.sorter.algorithm_info() == expected_output


class TestSelectionSort(unittest.TestCase):

    def setUp(self):
        block_values = [201, 101, 301, 51, 1, 151, 401, 351, 251]
        self.blocks = [BlockSprite(0, h, (0, 0, 0)) for h in block_values]
        self.sorter = SelectionSort(self.blocks)
        self.block_len = len(self.blocks)
        self.COMPLETED_SORT = [1, 51, 101, 151, 201, 251, 301, 351, 401]

    def tearDown(self) -> None:
        self.sorter = None
        self._blocks = None
        self.block_len = None
        self.COMPLETED_SORT = None

    def test_init(self):
        assert self.sorter.counter == 0
        assert self.sorter.blocks == self.blocks

    def test_sort_once(self):
        self.sorter.sort()
        assert [b.height for b in self.sorter.blocks] == [1, 101, 301, 51, 201, 151, 401, 351, 251]
        assert self.sorter.counter == 1

    def test_sort_several_times(self):
        for i in range(5):
            self.sorter.sort()
        assert [b.height for b in self.sorter.blocks] == [1, 51, 101, 151, 201, 301, 401, 351, 251]
        assert self.sorter.counter == 5

    def test_sort_nine_times(self):
        for i in range(9):
            self.sorter.sort()
        assert [b.height for b in self.sorter.blocks] == self.COMPLETED_SORT
        assert self.sorter.counter == 9

    def test_sort_hundred_times(self):
        for i in range(9):
            self.sorter.sort()
        assert [b.height for b in self.sorter.blocks] == self.COMPLETED_SORT
        assert self.sorter.counter == 9

    def test_sort_empty_list(self):
        self.sorter = SelectionSort([])
        assert self.sorter.sort() == []

    def test_sort_already_sorted(self):
        self.sorter = SelectionSort([BlockSprite(0, 1, (0, 0, 0)), BlockSprite(0, 2, (0, 0, 0)), BlockSprite(0, 3, (0, 0, 0))])
        assert[b.height for b in self.sorter.sort()] == [1, 2, 3]

    def test_sort_duplicate_vals(self):
        self.sorter = SelectionSort(
            [BlockSprite(0, 3, (0, 0, 0)), BlockSprite(0, 2, (0, 0, 0)), BlockSprite(0, 1, (0, 0, 0)),
             BlockSprite(0, 2, (0, 0, 0)), BlockSprite(0, 3, (0, 0, 0))])
        for i in range(0, len(self.sorter.blocks)):
            self.sorter.sort()
        assert [b.height for b in self.sorter.sort()] == [1, 2, 2, 3, 3]


class TestBubbleSort(unittest.TestCase):

    def setUp(self):
        block_values = [201, 101, 301, 51, 1, 151, 401, 351, 251]
        self.blocks = [BlockSprite(0, h, (0, 0, 0)) for h in block_values]
        self.sorter = SelectionSort(self.blocks)
        self.block_len = len(self.blocks)
        self.COMPLETED_SORT = [1, 51, 101, 151, 201, 251, 301, 351, 401]

    def tearDown(self) -> None:
        self.sorter = None
        self._blocks = None
        self.block_len = None
        self.COMPLETED_SORT = None

    def test_init(self):
        assert self.sorter.counter == 0
        assert self.sorter.blocks == self.blocks





if __name__ == '__main__':
    unittest.main()
