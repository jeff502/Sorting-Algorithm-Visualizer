from algorithms.algorithms import InsertionSort, SelectionSort, BubbleSort


def test_insertion_sort_class():
    insertion_sort = InsertionSort(blocks=[])
    assert insertion_sort.counter == 0
    assert insertion_sort.blocks == []
    assert insertion_sort.block_len == 0

def test_insertion_sort_sort():
    insertion_sort = InsertionSort(blocks=[])
    ...
