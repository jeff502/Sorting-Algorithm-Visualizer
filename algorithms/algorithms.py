from spirtes.block_sprites import BlockSprite


class InsertionSort:
    def __init__(self, blocks):
        self.counter = 0
        self.blocks = blocks
        self.block_len = len(self.blocks)

    def sort(self) -> list[BlockSprite]:
        if self.counter >= self.block_len:
            return self.blocks
        for index in range(1, self.block_len):
            current_value = self.blocks[self.counter]
            position = self.counter
            while position > 0 and self.blocks[position - 1].height > current_value.height:
                self.blocks[position] = self.blocks[position - 1]
                position -= 1
            self.blocks[position] = current_value
            self.counter += 1
            return self.blocks

    @staticmethod
    def algorithm_info():
        return [
            "Insertion sort is a simple sorting algorithm that builds the final sorted array one item at a time by "
            "comparisons.",
            "In this visualization, you'll see an array being updated one item at a time as the index increases.",
            "Time complexity: Best: Ω(n), Average: Θ(n^2), Worst: O(n^2)",
            "Space Complexity: O(1)"
            ]


class SelectionSort:
    def __init__(self, blocks):
        self.counter = 0
        self.blocks = blocks
        self.block_len = len(self.blocks)

    def sort(self) -> list[BlockSprite]:
        if self.counter >= self.block_len:
            return self.blocks
        min_index = self.counter
        for i in range(self.counter+1, self.block_len):
            if self.blocks[i].height < self.blocks[min_index].height:
                min_index = i
        self.blocks[self.counter], self.blocks[min_index] = self.blocks[min_index], self.blocks[self.counter]
        self.counter += 1
        return self.blocks

    @staticmethod
    def algorithm_info():
        return [
            "Selection sort divides the input list into two parts: a sorted sublist of items which is built up from "
            "left to right",
            "at the front (left) of the list and a sublist of the remaining unsorted items that occupy the rest of "
            "the list.",
            "Initially, the sorted sublist is empty and the unsorted sublist is the entire input list.",
            "The algorithm proceeds by finding the smallest element in the unsorted sublist, exchanging it with the "
            "leftmost",
            "unsorted element (putting it in sorted order), and moving the sublist boundaries one element to the "
            "right. ",
            "Time complexity: Best: O(n^2), Average: O(n^2), Worst: O(n^2)",
            "Space Complexity: O(1)"
        ]


class BubbleSort:
    def __init__(self, blocks):
        self.counter = 0
        self.blocks = blocks
        self.block_len = len(self.blocks)

    def sort(self) -> list[BlockSprite]:
        if self.counter >= self.block_len:
            return self.blocks
        for j in range(self.block_len - self.counter - 1):
            if self.blocks[j].height > self.blocks[j + 1].height:
                self.blocks[j], self.blocks[j + 1] = self.blocks[j + 1], self.blocks[j]
        self.counter += 1
        return self.blocks

    @staticmethod
    def algorithm_info():
        return [
            "Bubble sort is a simple sorting algorithm that repeatedly steps through the input list element by element,",
            "comparing the current element with the one after it, exchanging their values if needed.",
            "Time complexity: Best: O(n), Average: O(n^2), Worst: O(n^2)",
            "Space Complexity: O(1)"
        ]
